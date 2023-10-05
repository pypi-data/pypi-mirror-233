# Copyright (c) 2023 NEC Corporation. All Rights Reserved.
"""FireDucks: Dataframe with FIRE
"""
from __future__ import annotations

from firefw import tracing

import logging
import os
import warnings

import numpy as np

with tracing.scope(tracing.Level.DEFAULT, "import pandas"):
    import pandas
    from pandas.util._decorators import deprecate_nonkeyword_arguments
    from pandas.util._validators import validate_bool_kwarg
    import pandas._libs.lib as pandas_lib

import fireducks.core
from fireducks import ir, irutils
from fireducks.pandas.binop import (
    # get_binop_vector_scalar,
    # get_binop_vector_vector,
    get_binop_table_scalar,
    get_binop_table_vector,
    get_binop_table_table,
)

import fireducks.pandas.utils as utils
from fireducks.pandas.utils import (
    _unwrap,
    make_agg_args,
    is_supported_df_agg_funcs,
)

from fireducks.pandas.generic import (
    FireDucksPandasCompat,
    _Scalar,
    _install_binops,
    _install_fallback_may_inplace,
    _install_fallback_mutating_method,
    _install_unary_op_fallbacks,
    _wrap_pandas,
)

from fireducks.pandas.series import Series
from fireducks.pandas.expr import QueryParser
from fireducks.pandas.metadata import IRMetadataWrapper

logger = logging.getLogger(__name__)


def _setup_DataFrame(cls):
    utils.install_fallbacks(cls, ["__contains__"])
    _install_unary_op_fallbacks(cls, pandas.DataFrame)
    _install_binops(cls, pandas.DataFrame)

    # `pop` is used to call _fallback_mutating_method in
    # `test_anti_dep_fallback`. If you change it to non-fallback, please fix
    # the test. See GT #1069
    _install_fallback_mutating_method(cls, "pop")

    _install_fallback_mutating_method(cls, "_set_value")
    _install_fallback_mutating_method(cls, "__delitem__")

    methods_may_inplace = [["dropna", 4]]
    for name, pos, *default in methods_may_inplace:
        if not default:
            default = [False]
        _install_fallback_may_inplace(cls, name, pos, default[0])

    _wrap_pandas(cls, pandas.DataFrame)
    return cls


def create_metadata(df: pandas.DataFrame):
    """Create IR metadata to pass to from_pandas"""
    from fireducks.fireducks_ext import (
        Metadata,
        ColumnMetadata,
        Scalar,
        ColumnName,
    )

    index = df.columns
    logger.debug("create_metadata: df.columns.nlevels=%d", index.nlevels)
    logger.debug("create_metadata: df.columns.names=%s", index.names)
    logger.debug(
        "create_metadata: isMultiindex=%s",
        isinstance(index, pandas.MultiIndex),
    )

    def to_column_name(name, isMulti):
        if isinstance(name, (frozenset, tuple)):
            if isMulti:
                return ColumnName.Multi([Scalar(e) for e in name])
            else:
                return ColumnName.SingleFromScalars([Scalar(e) for e in name])
        else:
            # return [Scalar(name)]
            return ColumnName.Single(Scalar(name))

    isMulti = isinstance(index, pandas.MultiIndex)
    column_names = [to_column_name(name, isMulti) for name in index]
    columns = [ColumnMetadata(name) for name in column_names]
    column_index_names = [Scalar(name) for name in index.names]
    return Metadata(
        columns, column_index_names, isinstance(df.index, pandas.MultiIndex)
    )


def _from_pandas_frame(df: pandas.DataFrame):
    """
    Returns fire.Value
    """
    logger.debug("_from_pandas_frame")
    if fireducks.core.get_ir_prop().has_metadata:
        # rename to ensure no duplicated column name. Here we will rename only
        # columns, but those should not conflict with index. We use
        # `__duck_dummy_` prefix.
        copy = df.copy(deep=False)
        copy.columns = [
            f"__fireducks_dummy_{i}" for i in range(len(df.columns))
        ]
        f = fireducks.core.make_available_value(copy, ir.Ty_pyobj)
        metadata = create_metadata(df)
        # logger.debug('_from_pandas_frame: metadata=%s', metadata)
        m = fireducks.core.make_available_value(metadata, ir.Ty_metadata)
        return ir.from_pandas_frame_metadata(f, m)
    else:
        f = fireducks.core.make_available_value(df, ir.Ty_pyobj)
        return ir.from_pandas_dataframe(f)


def _is_columns_dict(obj):
    if not isinstance(obj, dict):
        return False

    return all([irutils.is_column_name(x) for x in obj.keys()]) and all(
        [isinstance(x, Series) for x in obj.values()]
    )


@_setup_DataFrame
class DataFrame(FireDucksPandasCompat):
    _constructor_sliced: type[Series] = Series
    _metadata = []

    def __init__(self, *args, **kwargs):
        """
        Three types of constructors.

        1. Construct from fire.Value
             Used when kwargs has `_value`
        2. Construct from pandas.DataFrame
             Used when kwargs has `__fireducks_from_pandas`
        3. Construct from pandas-like arguments
             Used in other cases
        """
        logger.debug("DataFrame.__init__")
        value = kwargs.get("_value")

        if value is not None:
            return super().__init__(value)

        if len(kwargs) == 0 and len(args) == 1 and _is_columns_dict(args[0]):
            value = ir.create_table_from_columns(
                columns=irutils.make_tuple_of_tables(args[0].values()),
                column_names=irutils.make_tuple_of_column_names(
                    args[0].keys()
                ),
            )
            return super().__init__(value)

        obj = kwargs.pop("__fireducks_from_pandas", None)
        if obj is None:
            reason = "args of DataFrame.__init__"
            tmp = [_unwrap(x, reason=reason) for x in args]
            obj = pandas.DataFrame(*tmp, **_unwrap(kwargs))
        assert isinstance(obj, pandas.DataFrame)
        value = _from_pandas_frame(obj)
        super().__init__(value, pandas_object=obj)

    def __dir__(self):
        reason = "DataFrame.__dir__ is called"
        return self._fallback_call("__dir__", __fireducks_reason=reason)

    def __finalize__(self, other, method=None):
        logger.debug("DataFrame.__finalize__: method=%s", method)
        if isinstance(other, DataFrame):
            for name in set(self._metadata) & set(other._metadata):
                assert isinstance(name, str)
                logger.debug("DataFrame.__finalize__: setattr name=%s", name)
                object.__setattr__(self, name, getattr(other, name, None))
        return self

    def __getattr__(self, name):
        logger.debug("DataFrame.__getattr__: name=%s", name)

        # Because fireducks.DataFrame do not explicitly define all
        # pandas.DataFrame API, undefined API reaches here when it is called.
        # It should be handled as API, not as column name, we have to check if
        # it is API.
        if name not in pandas.DataFrame.__dict__:
            if self._is_column_name(name):
                return self[name]

        reason = f"{type(self).__name__}.__getattr__ for {name} is called"
        return utils.fallback_attr(self._unwrap, name, reason)

    def __len__(self):
        return self.shape[0]

    def __iter__(self):
        return iter(self._get_column_names())

    def __abs__(self):
        return self.abs()

    def __neg__(self):
        return DataFrame._create(ir.negate(self._value))

    def __round__(self, decimals=0):
        return self.round(decimals)

    def __invert__(self):
        return DataFrame._create(ir.invert(self._value))

    def __setattr__(self, name, value):
        logger.debug("DataFrame.__setattr__: name=%s", name)

        # Known fireducks.DataFrame properties
        # Because columns is property, __setattr__ is called when columns = ..
        if name in ["_value", "columns"]:
            return object.__setattr__(self, name, value)

        if name in ["attrs", "index"]:
            return self._fallback_mutating_method(
                "__setattr__", args=[name, value]
            )

        # Existing user-defined properties
        try:
            object.__getattribute__(self, name)
            return object.__setattr__(self, name, value)
        except AttributeError:
            pass

        if name in self.columns:
            return self.__setitem__(name, value)

        # New user-defined properties
        object.__setattr__(self, name, value)

    @classmethod
    def _create(cls, value):
        assert value.type() == ir.TableType
        return DataFrame(_value=value)

    def _create_or_inplace(self, value, inplace):
        inplace = validate_bool_kwarg(inplace, "inplace")
        if inplace:
            return self._rebind(value, invalidate_cache=True)
        return DataFrame._create(value).__finalize__(self)

    @classmethod
    def _get_axis_number(self, axis):
        return pandas.DataFrame._get_axis_number(axis)

    def _get_column_names(self):
        # To prevent fallback, cache is explicitly checked here
        if self._fireducks_meta.is_cached():
            return list(self._fireducks_meta.get_cache().columns)
        else:
            if fireducks.core.get_ir_prop().has_metadata:
                return self._get_metadata().column_names
            return list(self.columns)

    def _is_column_name(self, name):
        return name in self._get_column_names()

    # fireducks method for debug
    def _print(self):
        ch = ir.print_table(self._value)
        fireducks.core.evaluate([ch])

    # def _build_row_func(self, func) -> fire.Value:
    #     return fire.make_available_value(func, ir.Ty_pyobj)

    def _to_pandas(self, options=None):
        if fireducks.core.get_ir_prop().has_metadata:
            result = _to_pandas_frame_metadata(self._value)
        else:
            value = ir.to_pandas(self._value)
            result = fireducks.core.evaluate([value], options)[0]
        assert isinstance(
            result, pandas.DataFrame
        ), f"{type(result)} is not pandas.DataFrame"

        return result

    @classmethod
    def from_pandas(cls, df):
        if not isinstance(df, pandas.DataFrame):
            raise RuntimeError(
                "DataFrame.from_pandas: illegal argument: "
                f"{df.__class__.__name__}"
            )
        return DataFrame(__fireducks_from_pandas=df)

    #
    # Pandas methods (alphabetical)
    #

    # fireducks.DataFrame.__getitem__ returns Series even when DataFrame has
    # multilevel column index. This method can force returning DataFrame.
    def _project(self, key, as_frame=False):
        cls = Series
        if as_frame or isinstance(key, list):
            cls = DataFrame

        if isinstance(key, list):
            key = irutils.make_vector_or_scalar_of_column_name(key)
            return cls._create(ir.project(self._value, key)).__finalize__(
                self, method="project"
            )

        key = irutils.make_vector_or_scalar_of_column_name(key)
        return cls._create(ir.project(self._value, key))

    def __getitem__(self, key):
        logger.debug("DataFrame.__getitem__: type(key)=%s", type(key))
        if isinstance(key, Series):
            dtype = utils._deduce_dtype(key)
            if dtype is not None and dtype == bool:
                return DataFrame._create(ir.filter(self._value, key._value))
            return self._fallback_call("__getitem__", _unwrap(key))

        elif isinstance(key, slice) and utils.is_int_or_none_slice(key):
            if key.step is None or key.step == 1:
                return self._slice(key)

        if irutils.is_column_name(key) or (
            isinstance(key, list)
            and all([irutils.is_column_name(x) for x in key])
        ):
            return self._project(key)

        reason = f"Unsupported key type: {type(key)}"
        return self._fallback_call(
            "__getitem__", key, __fireducks_reason=reason
        )

    def __setitem__(self, key: str, value):
        logger.debug("DataFrame.__setitem__")

        def _fallback(key=key, value=value, reason=None):
            self._fallback_mutating_method(
                "__setitem__",
                args=[_unwrap(key, reason="unwrap key of __setitem__"), value],
                reason=reason,
            )

        if not (isinstance(key, str) or irutils._is_str_list(key)):
            return _fallback(reason="key is neither str nor list of str")

        if irutils.irable_scalar(value):
            key = irutils.make_vector_or_scalar_of_column_name(key)
            value = irutils.make_vector_or_scalar_of_scalar(value)
            self._rebind(
                ir.assign_scalar(self._value, key, value),
                invalidate_cache=True,
            )
            return self

        from_list = False
        from_ndarray = False
        if isinstance(value, list):
            # See GT #1864
            unwrap_not_required = all(
                [isinstance(x, (int, float, str)) for x in value]
            )
            if unwrap_not_required:
                # To bypass unwrap in Series.__init__, create pandas.Series.
                value = Series.from_pandas(pandas.Series(value))
                from_list = True

        if isinstance(value, np.ndarray) and value.ndim == 1:
            value = Series(value)
            from_ndarray = True

        if isinstance(value, (pandas.Index, range)):
            value = Series(value)
            from_ndarray = True  # just to perform size check at backend

        if not isinstance(value, FireDucksPandasCompat):
            return _fallback(reason="value is not FireDucksPandasCompat")

        keys = irutils.make_vector_or_scalar_of_str(key)
        self._rebind(
            ir.setitem(
                self._value, keys, value._value, from_list, from_ndarray
            ),
            invalidate_cache=True,
        )
        return self

    def abs(self):
        return DataFrame._create(ir.abs(self._value))

    def aggregate(self, func=None, axis=0, *args, **kwargs):
        axis = self._get_axis_number(axis)
        reason = None

        if irutils._is_scalar_or_list_or_tuple_of(func, str):
            targets = [func] if isinstance(func, str) else func
            if axis == 1:
                supported_func_on_axis_1 = ["sum", "all", "any"]
                if any([f not in supported_func_on_axis_1 for f in targets]):
                    reason = (
                        f"unsupported aggregate function: {func} on axis=1"
                    )
            else:
                if not is_supported_df_agg_funcs(targets):
                    reason = (
                        f"unsupported aggregate function: {func} on axis=0"
                    )
            if not reason:
                funcs = irutils.make_vector_or_scalar_of_str(func)
                value = ir.aggregate(self._value, funcs, axis)
                if isinstance(func, str):  # scalar
                    return Series._create(value)
                return DataFrame._create(value)

        if axis == 1:  # not supported for dict, args, kwargs cases
            reason = "unsupported aggregated args on axis=1"
        else:
            aggArgs = make_agg_args(func, *args, **kwargs)
            if aggArgs is None:
                reason = "unsupported aggregated args"

        if not reason:
            if not is_supported_df_agg_funcs(aggArgs.funcs):
                reason = (
                    "all or few agg functions are not supported"
                    f" {aggArgs.funcs}"
                )

        if reason is not None:
            return self._fallback_call(
                "aggregate",
                func,
                axis,
                *args,
                **kwargs,
                __fireducks_reason=reason,
            )

        funcs, columns, relabels = aggArgs.to_ir()
        value = ir.aggregate_specified(
            self._value, funcs, columns, relabels, axis
        )

        if not kwargs and all(
            [isinstance(func, str) for func in aggArgs.funcs]
        ):
            return Series._create(value)  # Series when all funcs are scalar
        return DataFrame._create(value)

    agg = aggregate

    def apply(self, func, axis=0, **kwargs):
        if callable(func):

            def wrapper(*args, **kwargs):
                # Because func will be called by pandas, args and kwargs might
                # be pandas's object. func might use fireducks's data or func
                # itself is fireducks's function, args and kwargs should be
                # converted to ducks's one.
                args = utils._wrap(args)
                kwargs = utils._wrap(kwargs)
                return _unwrap(func(*args, **kwargs))

            return self._fallback_call("apply", wrapper, axis, **kwargs)
        else:
            return self._fallback_call("apply", func, axis, **kwargs)
        # pandas.DataFrame.apply(func) returns a DataFrame instead of a Series
        # depending on the return value of func.
        #
        # if axis != 1:
        #   logger.warn(
        #       'fireducks.DataFrame.apply is currently only supported'
        #       ' if axis is 1')
        # assert callable(func)
        # func = self._build_row_func(func)
        # return Series._create(ir.apply_row(self._value, func))

    def assign(self, **kwargs):
        data = self.copy()
        for k, v in kwargs.items():
            data[k] = v(data) if callable(v) else v
        return data

    def _set_column_index_names(self, names):  # inplace
        logger.debug("DataFrame._set_column_index_names")
        names = irutils.make_tuple_of_scalars(names)
        value = ir.set_column_index_names(self._value, names)
        self._rebind(value, invalidate_cache=True)

    @property
    def columns(self):
        """The column labels of the DataFrame."""
        logger.debug("DataFrame.columns")
        columns = utils.fallback_attr(
            self._unwrap, "columns", reason=f"{type(self).__name__}.columns"
        )
        columns._set_fireducks_frame(self)
        return columns

    @columns.setter
    def columns(self, value):
        logger.debug("columns: type=%s", type(value))
        # fireducks: GT #710
        if not irutils._is_str_list(value):
            return self._fallback_mutating_method(
                "__setattr__", args=["columns", value]
            )
        cols = irutils.make_tuple_of_scalars(value)
        self._rebind(ir.rename(self._value, cols), invalidate_cache=True)
        return self

    def corr(self, *args, **kwargs):
        arg = utils.decode_args(args, kwargs, pandas.DataFrame.corr)
        if arg.numeric_only == pandas_lib.no_default:
            arg.numeric_only = True
        arg.numeric_only = validate_bool_kwarg(
            arg.numeric_only, "numeric_only"
        )
        reason = []

        supported_methods = ["pearson"]
        if isinstance(arg.method, str):
            if arg.method not in supported_methods:
                reason.append(f"unsupported method={arg.method}")
        else:
            reason.append(
                "unsupported 'method' of type ="
                f"'{type(arg.method).__name__}'"
            )

        if arg.min_periods is None:
            arg.min_periods = 1
        elif not isinstance(arg.min_periods, int):
            reason.append(f"unsupported min_periods={arg.min_periods}")

        if len(reason) > 0:
            return self._fallback_call(
                "corr",
                *args,
                **kwargs,
                __fireducks_reason="; ".join(reason),
            )

        return DataFrame._create(
            ir.table_corr(
                self._value, arg.method, arg.min_periods, arg.numeric_only
            )
        )

    def diff(self, *args, **kwargs):
        arg = utils.decode_args(args, kwargs, pandas.DataFrame.diff)
        if arg.axis == 0 or arg.axis == "index":
            if not isinstance(arg.periods, int):
                reason = "periods is not int"
            else:
                return DataFrame._create(ir.diff(self._value, arg.periods))
        else:
            reason = "unsupported argument"

        return self._fallback_call(
            "diff", *args, **kwargs, __fireducks_reason=reason
        )

    @deprecate_nonkeyword_arguments(
        version=None, allowed_args=["self", "labels"]
    )
    def drop(self, *args, **kwargs):
        arg = utils.decode_args(args, kwargs, pandas.DataFrame.drop)
        arg.inplace = validate_bool_kwarg(arg.inplace, "inplace")

        if arg.labels is not None:
            if arg.index is not None or arg.columns is not None:
                raise ValueError(
                    "Cannot specify both 'labels' and 'index'/'columns'"
                )
            if arg.axis == 1:
                arg.columns = arg.labels
            else:
                arg.index = arg.labels
        elif arg.index is None and arg.columns is None:
            raise ValueError(
                "Need to specify at least one of "
                "'labels', 'index' or 'columns'"
            )

        reason = arg.is_not_default(["index", "level", "errors"])
        if reason is None:
            if isinstance(arg.columns, str):
                arg.columns = [arg.columns]

            if irutils._is_str_list(arg.columns):
                arg.columns = irutils.make_tuple_of_column_names(arg.columns)
                value = ir.drop_columns(self._value, arg.columns)
                return self._create_or_inplace(value, arg.inplace)
            else:
                reason = "columns is not a list of str"

        return self._fallback_may_inplace(
            "drop", args, kwargs, pos=5, reason=reason
        )

    def drop_duplicates(self, *args, **kwargs):
        arg = utils.decode_args(args, kwargs, pandas.DataFrame.drop_duplicates)
        arg.inplace = validate_bool_kwarg(arg.inplace, "inplace")
        arg.ignore_index = validate_bool_kwarg(
            arg.ignore_index, "ignore_index"
        )
        supported_keep = {"first", "last", False}

        if (
            (
                arg.subset is None
                or isinstance(arg.subset, str)
                or (irutils._is_str_list(arg.subset) and len(arg.subset) > 0)
            )
            and arg.keep in supported_keep
            and not arg.inplace
            and not arg.ignore_index
        ):
            if arg.subset is None:
                arg.subset = []  # empty means all column
            if isinstance(arg.subset, str):
                arg.subset = [arg.subset]
            logger.debug(f"subset.size={len(arg.subset)}")
            arg.subset = irutils.make_tuple_of_column_names(arg.subset)
            arg.keep = "none" if not arg.keep else arg.keep
            return DataFrame._create(
                ir.drop_duplicates(self._value, arg.subset, arg.keep)
            )

        return self._fallback_may_inplace(
            "drop_duplicates",
            args,
            kwargs,
            pos=3,
            reason="unsupported argument",
        )

    def dropna(self, *args, **kwargs):
        arg = utils.decode_args(args, kwargs, pandas.DataFrame.dropna)
        if arg.axis == 0 or arg.axis == "index":
            if (
                arg.subset is None
                or isinstance(arg.subset, str)
                or (irutils._is_str_list(arg.subset) and len(arg.subset) > 0)
            ):
                if arg.subset is None:
                    arg.subset = []  # empty means all column
                if isinstance(arg.subset, str):
                    arg.subset = [arg.subset]
                logger.debug(f"subset.size={len(arg.subset)}")
                subset = irutils.make_tuple_of_column_names(arg.subset)

                if arg.thresh is pandas_lib.no_default:
                    if arg.how == pandas_lib.no_default or arg.how == "any":
                        value = ir.dropna(self._value, subset, True, 0)
                        return self._create_or_inplace(value, arg.inplace)
                    elif arg.how == "all":
                        value = ir.dropna(self._value, subset, False, 1)
                        return self._create_or_inplace(value, arg.inplace)

                else:
                    if arg.how is pandas_lib.no_default:
                        value = ir.dropna(
                            self._value, subset, False, arg.thresh
                        )
                        return self._create_or_inplace(value, arg.inplace)

        return self._fallback_may_inplace(
            "dropna",
            args,
            kwargs,
            pos=3,
            reason="unsupported argument",
        )

    def duplicated(self, *args, **kwargs):
        arg = utils.decode_args(args, kwargs, pandas.DataFrame.duplicated)
        supported_keep = {"first", "last", False}

        if (
            arg.subset is None
            or isinstance(arg.subset, str)
            or (irutils._is_str_list(arg.subset) and len(arg.subset) > 0)
        ) and arg.keep in supported_keep:
            if arg.subset is None:
                arg.subset = []  # empty means all column
            if isinstance(arg.subset, str):
                arg.subset = [arg.subset]
            logger.debug(f"subset.size={len(arg.subset)}")
            arg.subset = irutils.make_tuple_of_column_names(arg.subset)
            arg.keep = "none" if not arg.keep else arg.keep
            return Series._create(
                ir.duplicated(self._value, arg.subset, arg.keep)
            )

        return self._fallback_call(
            "duplicated",
            arg.subset,
            arg.keep,
            __fireducks_reason="unsupported argument",
        )

    @property
    def dtypes(self):
        # This method returns PandasWrapper, not fireducks.Series because
        # contents of Series is numpy.dtype, i.e. python object, which can not
        # be converted to arrow.

        def wrap(obj):
            return utils.PandasWrapper(obj, Series)

        if self._fireducks_meta.is_cached():
            return wrap(self._fireducks_meta.get_cache().dtypes)

        if fireducks.core.get_ir_prop().has_metadata:
            dtypes, unsupported = self._get_metadata().dtypes
            if len(unsupported) == 0:
                return wrap(dtypes)
            reason = "DataFrame.dtypes includes unsupported type: " + ",".join(
                unsupported
            )
        else:
            reason = "IR does not support metadata"

        return utils.fallback_attr(
            self._unwrap, "dtypes", reason=reason, wrap_func=wrap
        )

    def explode(self, column, ignore_index=False):
        if isinstance(column, list):
            if not column:
                raise ValueError("column must be nonempty")
            is_supported_names = all(
                [irutils.is_column_name(x) for x in column]
            )
            if is_supported_names and len(column) > len(set(column)):
                raise ValueError("column must be unique")
        else:
            is_supported_names = irutils.is_column_name(column)

        if not is_supported_names:
            reason = f"unsupported column of type: {type(column).__name__}"
            return self._fallback_call(
                "explode", column, ignore_index, __fireducks_reason=reason
            )

        column = [column] if not isinstance(column, list) else column
        column = irutils.make_tuple_of_column_names(column)
        # according to pandas behavior. all true values would be treated
        # as true. e.g., ignore_index="a" would be treated as ignore_index=True
        ignore_index = bool(ignore_index)
        return DataFrame._create(ir.explode(self._value, column, ignore_index))

    def eval(self, *args, **kwargs):
        kwargs["level"] = kwargs.pop("level", 0) + 5
        return self._fallback_call("eval", *args, **kwargs)

    def filter(self, *args, **kwargs):
        arg = utils.decode_args(args, kwargs, pandas.DataFrame.filter)
        if arg.axis is None:
            arg.axis = 1

        reason = arg.is_not_default(["like", "regex"])
        if reason:
            pass
        elif not irutils._is_scalar_or_list_or_tuple_of(arg.items, str):
            reason = "items is not a list of str"
        elif not (arg.axis == 1 or arg.axis == "columns"):
            reason = "axis is not 1"
        else:
            labels = self._get_column_names()
            cols = [r for r in arg.items if r in labels]
            return self[cols]

        return self._fallback_call(
            "filter", *args, **kwargs, __fireducks_reason=reason
        )

    def groupby(self, by=None, *args, **kwargs):
        logger.debug("groupby: type(by)=%s", type(by))
        from fireducks.pandas.groupby import DataFrameGroupBy

        return DataFrameGroupBy(self, by=by, *args, **kwargs)

    def insert(self, *args, **kwargs):
        # TODO: unwrap args when it includes fireducks.padans.Sereis
        self._fallback_mutating_method("insert", args, kwargs)

    def isna(self):
        return DataFrame._create(ir.isnull(self._value))

    def isnull(self):
        return DataFrame._create(ir.isnull(self._value))

    def melt(self, *args, **kwargs):
        arg = utils.decode_args(args, kwargs, pandas.DataFrame.melt)
        reason = arg.is_not_default(["col_level"])
        if reason is not None:
            return self._fallback_call(
                "melt", *args, **kwargs, __fireducks_reason=reason
            )

        arg.id_vars = irutils.make_vector_or_scalar_of_column_name(arg.id_vars)
        arg.value_vars = irutils.make_vector_or_scalar_of_column_name(
            arg.value_vars
        )
        arg.var_name = irutils.make_column_name(arg.var_name)
        arg.value_name = irutils.make_column_name(arg.value_name)
        value = ir.melt(
            self._value,
            arg.id_vars,
            arg.value_vars,
            arg.var_name,
            arg.value_name,
            arg.ignore_index,
        )
        return DataFrame._create(value)

    def items(self):
        df = self.to_pandas()
        for label, column in df.items():
            yield label, utils._wrap(column)

    def merge(
        self,
        right,
        how="inner",
        on=None,
        left_on=None,
        right_on=None,
        left_index=False,
        right_index=False,
        sort=False,
        suffixes=("_x", "_y"),
        **kwargs,
    ):
        class MergeOperation:
            def __init__(self, left, right):
                self.left = left
                self.right = right

        op = MergeOperation(self, right)

        def to_list(x):
            return x if isinstance(x, list) else [x]

        if not (
            isinstance(suffixes, (list, tuple))
            and len(suffixes) == 2
            and all([isinstance(x, (str, type(None))) for x in suffixes])
        ):
            pass  # suffixes error
        elif not isinstance(left_index, bool) or not isinstance(
            right_index, bool
        ):
            pass
        elif isinstance(left_on, np.ndarray) or isinstance(
            right_on, np.ndarray
        ):
            pass
        elif (
            how in ("left", "right", "inner", "outer")
            and not sort
            and len(kwargs) == 0
        ):
            left_suffix, right_suffix = [
                # Replace None with "\0" so that IR can recognize the
                # difference between None and ""(empty string).
                s if s is not None else chr(0)
                for s in suffixes
            ]
            if (
                (isinstance(left_on, str) or irutils._is_str_list(left_on))
                and not on
                and not left_index
            ):
                if not right_on and right_index:
                    left_on = to_list(left_on)
                    left_on = irutils.make_tuple_of_column_names(left_on)
                    on = right_on = irutils.make_tuple_of_column_names([])
                    return DataFrame._create(
                        ir.join(
                            self._value,
                            right._value,
                            how,
                            on,
                            left_on,
                            False,
                            right_on,
                            True,
                            left_suffix,
                            right_suffix,
                        )
                    ).__finalize__(op, "merge")
                if right_on and not right_index:
                    left_on = to_list(left_on)
                    right_on = to_list(right_on)
                    left_on = irutils.make_tuple_of_column_names(left_on)
                    right_on = irutils.make_tuple_of_column_names(right_on)
                    on = irutils.make_tuple_of_column_names([])
                    return DataFrame._create(
                        ir.join(
                            self._value,
                            right._value,
                            how,
                            on,
                            left_on,
                            False,
                            right_on,
                            False,
                            left_suffix,
                            right_suffix,
                        )
                    ).__finalize__(op, "merge")

            if left_index and not on and not left_on:
                if not right_on and right_index:
                    on = irutils.make_tuple_of_column_names([])
                    left_on = right_on = on
                    return DataFrame._create(
                        ir.join(
                            self._value,
                            right._value,
                            how,
                            on,
                            left_on,
                            True,
                            right_on,
                            True,
                            left_suffix,
                            right_suffix,
                        )
                    ).__finalize__(op, "merge")
                if right_on and not right_index:
                    right_on = to_list(right_on)
                    right_on = irutils.make_tuple_of_column_names(right_on)
                    on = left_on = irutils.make_tuple_of_column_names([])
                    return DataFrame._create(
                        ir.join(
                            self._value,
                            right._value,
                            how,
                            on,
                            left_on,
                            True,
                            right_on,
                            False,
                            left_suffix,
                            right_suffix,
                        )
                    ).__finalize__(op, "merge")

            if (
                (isinstance(on, str) or irutils._is_str_list(on))
                and not left_on
                and not right_on
                and not left_index
                and not right_index
            ):
                on = to_list(on)
                on = irutils.make_tuple_of_column_names(on)
                left_on = right_on = irutils.make_tuple_of_column_names([])
                return DataFrame._create(
                    ir.join(
                        self._value,
                        right._value,
                        how,
                        on,
                        left_on,
                        False,
                        right_on,
                        False,
                        left_suffix,
                        right_suffix,
                    )
                ).__finalize__(op, "merge")

            if (
                not on
                and not left_on
                and not right_on
                and not left_index
                and not right_index
            ):
                on = left_on = right_on = irutils.make_tuple_of_column_names(
                    []
                )
                return DataFrame._create(
                    ir.join(
                        self._value,
                        right._value,
                        how,
                        on,
                        left_on,
                        False,
                        right_on,
                        False,
                        left_suffix,
                        right_suffix,
                    )
                ).__finalize__(op, "merge")

        return self._fallback_call(
            "merge",
            right,
            how,
            on,
            left_on,
            right_on,
            left_index,
            right_index,
            sort=sort,
            suffixes=suffixes,
            **kwargs,
        ).__finalize__(op, "merge")

    def notna(self):
        return ~self.isnull()

    def notnull(self):
        return ~self.isnull()

    def quantile(self, *args, **kwargs):
        reason = None
        arg = utils.decode_args(args, kwargs, pandas.DataFrame.quantile)

        axis = self._get_axis_number(arg.axis)
        if axis == 1:
            reason = f"unsupported quantile on axis = {arg.axis}"

        # arrow implementation of nearest seems not to
        # return same value as in pandas
        supported_interpolation = {
            "linear",
            "lower",
            "higher",
            "midpoint",
            # "nearest",
        }
        if arg.interpolation not in supported_interpolation:
            reason = f"unsupported 'interpolation' = {arg.interpolation}"

        # dfkl treats default as True
        if arg.numeric_only is pandas_lib.no_default:
            arg.numeric_only = True
        supported_numeric_only = [None, True]
        if arg.numeric_only not in supported_numeric_only:
            reason = f"unsupported 'numeric_only' = {arg.numeric_only}"

        if arg.method not in {"single", "table"}:
            reason = f"unsupported 'method' = {arg.method}"

        if reason:
            return self._fallback_call_packed(
                "quantile", args, kwargs, reason=reason
            )

        is_scalar = irutils.irable_scalar(arg.q)
        if is_scalar:
            arg.q = float(arg.q)
            CONS = Series._create
        else:
            arg.q = [float(e) for e in arg.q]
            CONS = DataFrame._create
        qs = irutils.make_vector_or_scalar_of_scalar(arg.q)
        return CONS(ir.quantile(self._value, qs, arg.interpolation))

    def query(self, expr, *, inplace=False, local_dict=None, **kwargs):
        reason = None

        if inplace:
            reason = "query with inplace"

        # parameters 'engine' and 'parser' get ignored internally,
        # when some valid values are given.Otherwise, falls back
        # to pandas for error handling etc.
        from pandas.core.computation.check import NUMEXPR_INSTALLED

        known_engines = {"python"}
        if NUMEXPR_INSTALLED:
            known_engines.add("numexpr")
        engine = kwargs.get("engine")
        if engine is None:
            engine = "python"
        if engine not in known_engines:
            reason = f"unknown engine = {engine}"

        known_parsers = {"pandas"}
        parser = kwargs.get("parser")
        if parser is None:
            parser = "pandas"  # default in pandas.eval
        if parser not in known_parsers:
            reason = f"unknown parser = {parser}"

        known_kwargs = {"engine", "parser", "level"}
        tmp = set(kwargs.keys()) - known_kwargs
        if len(tmp) != 0:
            reason = f"unsupported kwargs: {tmp}"

        if not reason:
            level = kwargs.get("level", 0) + 2
            try:
                parser = QueryParser(self, level, local_dict=local_dict)
                key = parser.visit(expr)
                if isinstance(key, Series):
                    dtype = utils._deduce_dtype(key)
                    if dtype is not None and dtype == bool:
                        return DataFrame._create(
                            ir.filter(self._value, key._value)
                        )
                    else:
                        reason = "non-boolean key is given"
                else:
                    reason = (
                        "Non-series parser output of type: "
                        f"{type(key).__name__}"
                    )
            except Exception as e:
                reason = "QueryParser exception: " + str(e)

        kwargs["level"] = kwargs.pop("level", 0) + 4
        return self._fallback_call(
            "query",
            expr,
            inplace=inplace,
            local_dict=local_dict,
            **kwargs,
            __fireducks_reason=reason,
        )

    def rename(
        self,
        mapper=None,
        *,
        index=None,
        columns=None,
        inplace=False,
        axis=None,
        copy=None,
        level=None,
        errors="ignore",
    ):
        mapper, index, columns, axis, copy, level, errors = _unwrap(
            [mapper, index, columns, axis, copy, level, errors]
        )

        reason = None
        _columns = None

        if axis:
            if columns or index:
                raise TypeError(
                    "Cannot specify both 'axis' "
                    "and any of 'index' or 'columns'"
                )

        if mapper:
            if columns or index:
                raise TypeError(
                    "Cannot specify both 'mapper' "
                    "and any of 'index' or 'columns'"
                )
            if axis == 1:
                _columns = mapper

        if columns:
            if index:
                reason = "Unsupported rename with both columns and index"
            _columns = columns

        if isinstance(_columns, dict):
            if errors != "ignore":  # TODO support at kernel side
                reason = f"Unsupported rename with errors='{errors}'"
            if level:
                reason = f"Unsupported rename with level='{level}'"
            if copy is not None and not copy:
                reason = f"Unsupported rename with copy='{copy}'"

            for k in _columns.keys():
                if isinstance(k, tuple):
                    reason = f"MultiIndex key: {k} is not supported"
                    break

            if not reason:
                cols = irutils.make_tuple_of_column_names(
                    list(_columns.keys())
                )
                newcols = irutils.make_tuple_of_column_names(
                    list(_columns.values())
                )
                ret = ir.rename_specified(self._value, cols, newcols)
                return self._create_or_inplace(ret, inplace)
        else:
            reason = (
                "Unsupported rename using columns of "
                + f"type: '{type(_columns).__name__}'"
            )

        fallback = self._get_fallback(inplace)
        return fallback(
            "rename",
            kwargs={
                "mapper": mapper,
                "index": index,
                "columns": columns,
                "inplace": inplace,
                "axis": axis,
                "copy": copy,
                "level": level,
                "errors": errors,
            },
            reason=reason,
        )

    def rolling(self, *args, **kwargs):
        from fireducks.pandas.rolling import Rolling

        ns = utils.decode_args(args, kwargs, pandas.DataFrame.rolling)
        reason = ns.is_not_default(["win_type"])
        if reason:
            return self._fallback_call_packed(
                "rolling", args, kwargs, reason=reason
            )
        return Rolling(self, args, kwargs)

    def round(self, decimals=0, *args, **kwargs):
        reason = None
        if args or kwargs:
            reason = "args or kwargs is given"
        if not isinstance(decimals, int):
            reason = (
                "unsupported type for 'decimals' "
                f"parameter: {type(decimals).__name__}"
            )

        if reason:
            return self._fallback_call(
                "round",
                decimals,
                *args,
                **kwargs,
                __fireducks_reason=reason,
            )
        return DataFrame._create(ir.round(self._value, decimals))

    def set_flags(self, *args, **kwargs):
        # Incompatibility: 023
        warnings.warn("set_flags is not supported", DeprecationWarning)
        return self._fallback_call("set_flags", *args, **kwargs)

    @deprecate_nonkeyword_arguments(
        version=None, allowed_args=["self", "keys"]
    )
    def set_index(self, *args, **kwargs):
        arg = utils.decode_args(args, kwargs, pandas.DataFrame.set_index)
        reason = arg.is_not_default(["drop", "append", "verify_integrity"])
        if not reason and not irutils._is_scalar_or_list_of(
            arg.keys, (str, int)
        ):
            reason = "keys is not a list of str or int"

        if reason:
            return self._fallback_may_inplace(
                "set_index", args, kwargs, pos=3, reason=reason
            )

        arg.keys = irutils.make_tuple_of_scalars(arg.keys)
        value = ir.set_index(self._value, arg.keys)
        return self._create_or_inplace(value, arg.inplace)

    @deprecate_nonkeyword_arguments(
        version=None, allowed_args=["self", "level"]
    )
    def reset_index(self, *args, **kwargs):
        arg = utils.decode_args(args, kwargs, pandas.DataFrame.reset_index)
        arg.inplace = validate_bool_kwarg(arg.inplace, "inplace")
        arg.drop = validate_bool_kwarg(arg.drop, "drop")

        # TODO GT #1689
        reason = arg.is_not_default(
            ["level", "col_level", "col_fill", "allow_duplicates", "names"]
        )
        if reason:
            return self._fallback_may_inplace(
                "reset_index", args, kwargs, pos=2, reason=reason
            )

        value = ir.reset_index(self._value, arg.drop, False)
        return self._create_or_inplace(value, arg.inplace)

    @property
    def shape(self) -> tuple[int, int]:
        value = ir.get_shape(self._value)
        shape = fireducks.core.evaluate([value])[0]
        return shape.y, shape.x

    @property
    def size(self) -> int:
        return np.prod(self.shape)

    @property
    def ndim(self) -> int:
        return 2

    @deprecate_nonkeyword_arguments(version=None, allowed_args=["self", "by"])
    def sort_values(self, *args, **kwargs):
        arg = utils.decode_args(args, kwargs, pandas.DataFrame.sort_values)
        known_kinds = ["quicksort", "mergesort", "heapsort", "stable"]
        if arg.axis != 0 and arg.axis != "index":
            reason = "axis is not 0"
        elif not isinstance(arg.inplace, bool):
            reason = "inplace is not bool"
        elif arg.kind not in known_kinds:
            reason = "kind is not in [quicksort, mergesort, heapsort, stable]"
        elif arg.na_position != "first" and arg.na_position != "last":
            reason = "na_position is not in [first, last]"
        else:
            reason = arg.is_not_default(["ignore_index", "key"])

        if reason:
            if callable(arg.key):

                def wrapper(*args, **kwargs):
                    return _unwrap(arg.key(*args, **kwargs))

                kwargs["key"] = wrapper

            return self._fallback_may_inplace(
                "sort_values", args, kwargs, pos=3, reason=reason
            )

        if not isinstance(arg.by, list):
            arg.by = [arg.by]
        keys = irutils.make_tuple_of_column_names(arg.by)
        if not isinstance(arg.ascending, list):
            lst = len(arg.by) if isinstance(arg.by, list) else 1
            arg.ascending = [arg.ascending for i in range(lst)]
        orders = ir.make_tuple_i1([bool(a) for a in arg.ascending])
        na_pos = False if arg.na_position == "first" else True
        value = ir.sort_values(self._value, keys, orders, na_pos, False)
        return self._create_or_inplace(value, arg.inplace)

    #
    # End of python API
    #

    def _build_binop(
        self, rhs, op_str: str, op_original: str, args, kwargs, inplace: bool
    ):
        logger.debug("DataFrame._build_binop: %s", op_str)

        def _fallback(reason, rhs_=rhs):
            fallback = self._get_fallback(inplace)
            return fallback(op_original, (rhs_,) + args, kwargs, reason=reason)

        arg = utils.decode_args(
            (rhs, *args), kwargs, getattr(pandas.DataFrame, op_original)
        )

        # Methods beginning with an underscore do not have 'axis', 'level',
        # and 'fill_value', arguments.
        if not hasattr(arg, "axis"):
            arg.axis = 1
        else:
            # pandas API doc does not menthon about axis=None, but
            # implemetation supports it and pandas_tests also uses it.
            arg.axis = (
                self._get_axis_number(arg.axis) if arg.axis is not None else 1
            )

        rhs_t = type(rhs).__name__
        reason = None
        opc = None

        if hasattr(arg, "level") and arg.level is not None:
            reason = "level is not None"
        elif hasattr(arg, "fill_value") and arg.fill_value is not None:
            reason = "fill_value is not None"
        elif isinstance(
            rhs,
            (
                bool,
                int,
                float,
                str,
                np.bool_,
                np.int32,
                np.int64,
                np.float32,
                np.float64,
            ),
        ):
            opc = get_binop_table_scalar(op_str)
            rhs = irutils.make_scalar(rhs)
        elif isinstance(rhs, _Scalar):
            opc = get_binop_table_scalar(op_str)
            rhs = rhs._value
        elif isinstance(rhs, Series):
            if arg.axis == 1:
                reason = "binop among Series with axis=1"
            else:
                opc = get_binop_table_vector(op_str)
                rhs = rhs._value
        elif isinstance(rhs, DataFrame):
            opc = get_binop_table_table(op_str)
            rhs = rhs._value

        if reason is None and opc is None:
            reason = f"unknown op: '{op_str}' on 'DataFrame' and '{rhs_t}'"

        if reason is not None:
            return _fallback(reason)

        op = fireducks.core.build_op(
            opc, [ir.TableType], [self._value, rhs], chaining=True
        )

        if inplace:
            self._rebind(op.outs[0], invalidate_cache=True)
            return self
        return DataFrame._create(op.outs[0])

    def to_csv(self, path_or_buf=None, *args, **kwargs):
        if not args and (not kwargs or kwargs.keys() == {"index"}):
            index = kwargs.get("index", True)
            if path_or_buf is None:
                result = ir.to_csv(self._value, index)
                return fireducks.core.evaluate([result])[0]
            if isinstance(path_or_buf, os.PathLike):
                path_or_buf = path_or_buf.__fspath__()
            if isinstance(path_or_buf, str):
                chain = ir.write_csv(self._value, path_or_buf, index)
                fireducks.core.evaluate([chain])
                return
        return self._fallback_call("to_csv", path_or_buf, *args, **kwargs)


def _to_pandas_frame_metadata(value, options=None):
    v0, v1 = ir.to_pandas_frame_metadata(value)
    df, meta = fireducks.core.evaluate([v0, v1], options=options)
    logger.debug("to_pandas_frame_metadata: meta=%s", meta)
    with tracing.scope(tracing.Level.VERBOSE, "to_pandas:metadata.apply"):
        return IRMetadataWrapper(meta).apply(df)
