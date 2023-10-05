# Copyright (c) 2023 NEC Corporation. All Rights Reserved.

from datetime import datetime, timezone
from typing import Tuple
import logging

import re
import numpy as np
import pandas
from pandas.util._decorators import deprecate_nonkeyword_arguments
from pandas.util._validators import validate_bool_kwarg
from pandas.core.accessor import CachedAccessor

from fireducks import ir, irutils
from fireducks import pandas as fireducks_pandas
import fireducks.core
from fireducks.pandas.generic import (
    FireDucksPandasCompat,
    _Scalar,
    _install_binops,
    _install_unary_op_fallbacks,
    _wrap_pandas,
)
import fireducks.pandas.utils as utils
from fireducks.pandas.utils import _unwrap

from fireducks.pandas.binop import (
    get_binop_vector_scalar,
    get_binop_vector_vector,
)

logger = logging.getLogger(__name__)


def add_extractors(fields):
    def adder(cls):
        for field in fields:

            def getter(self, name=field):
                return Series._create(
                    ir.datetime_extract(self.obj._value, name)
                )

            prop = property(fget=getter)  # TODO: fset is required?
            setattr(cls, field, prop)
        return cls

    return adder


@add_extractors(
    [
        "year",
        "month",
        "day",
        "hour",
        "minute",
        "second",
        "day_of_week",
        "day_of_year",
        "quarter",
        # days_in_month # is not found in arrow?
        # "microsecond", # may different from arrow's
        "nanosecond",
    ]
)
class DatetimeMethods(utils.ReadOnlyAccessor):
    def __init__(self, obj):
        object.__setattr__(self, "obj", obj)

    def _unwrap(self, reason):
        return utils.fallback_attr(
            self.obj._unwrap, "dt", reason="DatetimeMethods._unwrap"
        )


DatetimeMethods.dayofweek = DatetimeMethods.day_of_week
DatetimeMethods.weekday = DatetimeMethods.day_of_week
DatetimeMethods.dayofyear = DatetimeMethods.day_of_year


class StringMethods(utils.ReadOnlyAccessor):
    def __init__(self, obj):
        object.__setattr__(self, "obj", obj)

    def _unwrap(self, reason):
        return utils.fallback_attr(
            self.obj._unwrap,
            "str",
            reason="StringMethods._unwrap",
            stacklevel=8,
        )

    def _with(self, x, op, pat, na):
        reason = []

        if not isinstance(pat, str):
            reason.append(f"{x} with first argument is not of string-type")

        supported_na = {None, True, False}
        if na not in supported_na:
            reason.append(f"{x} with unsupported na: {na}")

        if len(reason) > 0:
            return utils.fallback_call(
                self._unwrap, x, pat, __fireducks_reason="; ".join(reason)
            )

        na_ = -1 if na is None else int(na)
        return Series._create(op(self.obj._value, pat, na_))

    def __getitem__(self, key):
        if isinstance(key, slice):
            return self.slice(start=key.start, stop=key.stop, step=key.step)
        reason = "key is not slice"
        return utils.fallback_call(
            self._unwrap, "__getitem__", key, __fireducks_reason=reason
        )

    def contains(self, pat, case=True, flags=0, na=None, regex=True):
        reason = []

        if not isinstance(pat, str):
            reason.append("contains with first argument is not of string-type")

        supported_flags = {0, re.IGNORECASE}
        if flags not in supported_flags:
            reason.append(f"contains with unsupported flags: {flags}")

        supported_na = {None, True, False}
        if na not in supported_na:
            reason.append(f"contains with unsupported na: {na}")

        if len(reason) > 0:
            return utils.fallback_call(
                self._unwrap,
                "contains",
                pat,
                case,
                flags,
                na,
                regex,
                __fireducks_reason="; ".join(reason),
            )

        # flags=re.IGNORECASE has more priority over "case" parameter
        ignorecase = True if flags == re.IGNORECASE else not case
        na_ = -1 if na is None else int(na)

        return Series._create(
            ir.str_contains(self.obj._value, pat, ignorecase, na_, regex)
        )

    def cat(self, others=None, sep=None, na_rep=None, join="left"):
        reason = []

        if others is None:
            reason.append("Unsupported 'others' = None")
        elif isinstance(others, (np.ndarray, tuple, list, pandas.Index)):
            others = Series(others)
        elif not isinstance(others, (Series, fireducks_pandas.DataFrame)):
            reason.append(
                f"Unsupported 'others' of type {type(others).__name__}"
            )

        if sep is None:
            sep = ""
        elif not isinstance(sep, str):
            reason.append(f"Unsupported 'sep' of type {type(sep).__name__}")

        if na_rep is not None:
            reason.append("'na_rep' is not None")

        if join != "left":
            reason.append(f"Unsupported 'join' = {join}")

        if len(reason) > 0:
            return utils.fallback_call(
                self._unwrap,
                "cat",
                others,
                sep,
                na_rep,
                join,
                __fireducks_reason="; ".join(reason),
            )

        return Series._create(
            ir.str_concat(self.obj._value, others._value, sep)
        )

    def endswith(self, pat, na=None):
        return self._with("endswith", ir.str_endswith, pat, na)

    def slice(self, start=None, stop=None, step=None):
        start = start or 0
        stop = stop or 2**63 - 1  # int64 max.
        step = step or 1
        return Series._create(ir.str_slice(self.obj._value, start, stop, step))

    def _split(
        self, pat=None, *, n=-1, expand=False, regex=None, reverse=False
    ):
        reason = []

        if pat is None:
            pat = " "
        elif not isinstance(pat, str):
            reason.append(f"Unsupported 'pat' of type {type(pat).__name__}")

        if not isinstance(n, int):
            reason.append(f"Unsupported 'n' of type {type(n).__name__}")

        if expand is not False:
            reason.append(f"Unsupported 'expand' = {expand}")

        if len(reason) > 0:
            if not reverse:
                return utils.fallback_call(
                    self._unwrap,
                    "split",
                    pat,
                    n,
                    expand,
                    regex,
                    __fireducks_reason="; ".join(reason),
                )
            else:
                # pandas rsplit doesn't have parameter "regex"
                return utils.fallback_call(
                    self._unwrap,
                    "rsplit",
                    pat,
                    n,
                    expand,
                    __fireducks_reason="; ".join(reason),
                )

        n = max(-1, n)
        if regex in {True, False, None}:
            regex = len(pat) > 1 if regex is None else regex
        else:
            # according to pandas behavior. all true values would be treated
            # as true. e.g., regex=2.3 would be treated as regex=True
            regex = bool(regex)

        return Series._create(
            ir.str_split(self.obj._value, pat, n, regex, reverse)
        )

    def split(self, pat=None, *, n=-1, expand=False, regex=None):
        return self._split(pat, n=n, expand=expand, regex=regex, reverse=False)

    def rsplit(self, pat=None, *, n=-1, expand=False, regex=None):
        return self._split(pat, n=n, expand=expand, regex=regex, reverse=True)

    def startswith(self, pat, na=None):
        return self._with("startswith", ir.str_startswith, pat, na)

    def pad(self, width, side="left", fillchar=" "):
        """
        Pad strings in the Series/Index up to width.
        """
        if not isinstance(width, int):
            raise TypeError(
                f"width must be of integer type, not {type(width).__name__}"
            )
        if side not in ("left", "right", "both"):
            raise ValueError(f"Invalid side: {side}")
        if isinstance(fillchar, str) and len(fillchar) > 1:
            raise TypeError("fillchar must be a character, not str")
        if side != "both":
            return Series._create(
                ir.str_pad(self.obj._value, max(0, width), side, fillchar)
            )
        reason = "pad with side=both"
        return utils.fallback_call(
            self._unwrap,
            "pad",
            width,
            side,
            fillchar,
            __fireducks_reason=reason,
        )

    def zfill(self, width):
        """
        Pad strings in the Series/Index by prepending ‘0’ characters.
        """
        return self.pad(width, side="left", fillchar="0")

    def _strip(self, to_strip, side):
        if to_strip is None:
            return Series._create(ir.str_trim_wsp(self.obj._value, side))
        elif isinstance(to_strip, str):
            return Series._create(ir.str_trim(self.obj._value, to_strip, side))
        else:
            reason = f"to_strip of type: {type(to_strip).__name__}"
            func = (
                "lstrip"
                if side == "left"
                else ("rstrip" if side == "right" else "strip")
            )
            return utils.fallback_call(
                self._unwrap, func, to_strip, __fireducks_reason=reason
            )

    def strip(self, to_strip=None):
        """
        Remove leading and trailing characters.
        """
        return self._strip(to_strip, side="both")

    def lstrip(self, to_strip=None):
        """
        Remove leading characters.
        """
        return self._strip(to_strip, side="left")

    def rstrip(self, to_strip=None):
        """
        Remove trailing characters.
        """
        return self._strip(to_strip, side="right")

    def replace(self, pat, repl, n=-1, case=None, flags=0, regex=False):
        reason = []

        if not isinstance(pat, str):
            reason.append("replace with 'pat' is not of string-type")

        if not isinstance(repl, str):
            reason.append("replace with 'repl' is not of string-type")

        if not isinstance(n, int):
            reason.append("replace with 'n' is not of integer-type")

        if flags != 0:
            reason.append("replace with non-zero 'flags'")

        supported_case = {None, True}
        if case not in supported_case:
            reason.append(f"replace with unsupported case: {case}")

        if len(reason) > 0:
            return utils.fallback_call(
                self._unwrap,
                "replace",
                pat,
                repl,
                n,
                case,
                flags,
                regex,
                __fireducks_reason="; ".join(reason),
            )

        # according to pandas behavior. all true values would be treated
        # as true. e.g., regex=2.3 would be treated as regex=True
        regex = bool(regex)
        n = max(-1, n)

        return Series._create(
            ir.str_replace(self.obj._value, pat, repl, n, regex)
        )

    def _str_unary_method(self, method, return_bool=False):
        if return_bool:
            value = ir.str_unary_bool_returning_method(self.obj._value, method)
        else:
            value = ir.str_unary_method(self.obj._value, method)
        return Series._create(value)

    def lower(self):
        """
        Converts all characters to lowercase
        """
        return self._str_unary_method("lower")

    def upper(self):
        """
        Converts all characters to uppercase
        """
        return self._str_unary_method("upper")

    def capitalize(self):
        """
        Converts all the Strings in the target Series to be capitalized.
        """
        return self._str_unary_method("capitalize")

    def title(self):
        """
        Converts all the Strings in the target Series to titlecase.
        """
        return self._str_unary_method("title")

    def swapcase(self):
        """
        Converts all the Strings in the target Series to swapcase.
        """
        return self._str_unary_method("swapcase")

    # this method is not available in native pandas, but added in fireducks
    # pandas way of reversing string column:
    # df[cname].str.apply(lambda x: x[::-1])
    def reverse(self):
        """
        Reverses all the Strings in the target Series.
        """
        return self._str_unary_method("reverse")

    def len(self):
        """
        Computes the length of each element
        """
        return self._str_unary_method("len")

    def islower(self):
        """
        Checks whether all characters in each string are lowercase.
        """
        return self._str_unary_method("islower", return_bool=True)

    def isupper(self):
        """
        Checks whether all characters in each string are uppercase.
        """
        return self._str_unary_method("isupper", return_bool=True)

    def isalnum(self):
        """
        Checks whether all characters in each string are alphanumeric.
        """
        return self._str_unary_method("isalnum", return_bool=True)

    def isalpha(self):
        """
        Checks whether all characters in each string are alphabetic.
        """
        return self._str_unary_method("isalpha", return_bool=True)

    def isnumeric(self):
        """
        Checks whether all characters in each string are numeric.
        """
        return self._str_unary_method("isnumeric", return_bool=True)

    def isdecimal(self):
        """
        Checks whether all characters in each string are decimal.
        """
        return self._str_unary_method("isdecimal", return_bool=True)

    def isspace(self):
        """
        Checks whether all characters in each string are whitespace.
        """
        return self._str_unary_method("isspace", return_bool=True)

    def istitle(self):
        """
        Checks whether all characters in each string are titlecase.
        """
        return self._str_unary_method("istitle", return_bool=True)


def _from_pandas_series(obj: pandas.Series):
    """
    Returns fire.Value
    """
    logger.debug("_from_pandas_series")
    if fireducks.core.get_ir_prop().has_series:
        return ir.from_pandas_series(
            fireducks.core.make_available_value(obj, ir.Ty_pyobj)
        )

    # When Series.name is None, pandas use '0' as column name.
    # To keep it None, it is explicity given.
    if obj.name is None:
        df = pandas.DataFrame({None: obj})
    else:
        df = pandas.DataFrame(obj)
    from fireducks.pandas.frame import _from_pandas_frame

    return _from_pandas_frame(df)


def _setup_Series(cls):
    _install_unary_op_fallbacks(cls, pandas.Series)
    _install_binops(cls, pandas.Series)
    _wrap_pandas(cls, pandas.Series)
    return cls


# Wrap PyTable
@_setup_Series
class Series(FireDucksPandasCompat):
    str = CachedAccessor("str", StringMethods)
    dt = CachedAccessor("dt", DatetimeMethods)

    def __init__(self, *args, **kwargs):
        value = kwargs.get("_value")
        obj = None
        if value is None:
            obj = kwargs.pop("__fireducks_from_pandas", None)
            if obj is None:
                reason = "args of Series.__init__"
                obj = pandas.Series(
                    *utils._unwrap(args, reason=reason),
                    **utils._unwrap(kwargs, reason=reason),
                )
            assert isinstance(obj, pandas.Series)
            value = _from_pandas_series(obj)
        super().__init__(value, pandas_object=obj)

    @classmethod
    def _create(cls, value):
        assert value.type() == ir.TableType
        return Series(_value=value)

    def _create_or_inplace(self, value, inplace):
        inplace = validate_bool_kwarg(inplace, "inplace")
        if inplace:
            return self._rebind(value, invalidate_cache=True)
        return Series._create(value).__finalize__(self)

    @classmethod
    def _get_axis_number(self, axis):
        return pandas.Series._get_axis_number(axis)

    @classmethod
    def from_pandas(cls, obj):
        if not isinstance(obj, pandas.Series):
            raise RuntimeError(
                "Series.from_pandas: illegal argument: "
                f"{obj.__class__.__name__}"
            )
        return Series(__fireducks_from_pandas=obj)

    def _build_binop(
        self, rhs, op_str: str, op_original: str, args, kwargs, inplace: bool
    ):
        def _fallback(reason, rhs_=rhs):
            fallback = self._get_fallback(inplace)
            return fallback(
                op_original,
                args=[utils._unwrap(rhs_)],
                kwargs=kwargs,
                reason=reason,
            )

        rhs_t = type(rhs).__name__
        reason = None
        opc = None

        if args:
            reason = f"args is used: {args}"
        elif kwargs:
            reason = f"kwargs is used: {kwargs}"
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
            opc = get_binop_vector_scalar(op_str)
            rhs = irutils.make_scalar(rhs)
        elif isinstance(rhs, Series):
            opc = get_binop_vector_vector(op_str)
            rhs = rhs._value
        elif isinstance(rhs, _Scalar):
            opc = get_binop_vector_scalar(op_str)
            rhs = rhs._value
        elif isinstance(rhs, datetime) and rhs.tzinfo is None:
            # timezone-naive datetime can be converted to !fireducks.scalar
            opc = get_binop_vector_scalar(op_str)
            ts = int(rhs.replace(tzinfo=timezone.utc).timestamp() * 1e9)
            rhs = ir.make_scalar_time_point_ns(ts)

        if reason is None and opc is None:
            reason = f"unknown op: '{op_str}' on 'Series' and '{rhs_t}'"

        if reason is not None:
            return _fallback(reason)

        logger.debug("build_binop: %s", type(self))
        op = fireducks.core.build_op(
            opc, [ir.TableType], [self._value, rhs], chaining=True
        )

        if inplace:
            self._rebind(op.outs[0], invalidate_cache=True)
            return self
        return Series._create(op.outs[0])

    def __abs__(self):
        return self.abs()

    def _to_pandas(self, options=None):
        ir_prop = fireducks.core.get_ir_prop()

        if (not ir_prop.has_series) and ir_prop.has_metadata:
            from fireducks.pandas.frame import _to_pandas_frame_metadata

            result = _to_pandas_frame_metadata(self._value, options)
            assert isinstance(
                result, pandas.DataFrame
            ), f"{type(result)} is not pandas.DataFrame"
            if len(result.columns) == 0:
                return pandas.Series(index=result.index)
            return result.iloc[:, 0]
        elif ir_prop.has_series:
            value = ir.to_pandas_series(self._value)
            result = fireducks.core.evaluate([value], options)[0]
            assert isinstance(
                result, pandas.Series
            ), f"{type(result)} is not pandas.Series"
            return result

        # Other cases are not supported because no backend requires it.
        assert False, "No supported IR property"

    def __getitem__(self, key):
        logger.debug("Series.__getitem__: type(key)=%s", type(key))
        if isinstance(key, Series):
            dtype = utils._deduce_dtype(key)
            if dtype is not None and dtype == bool:
                return Series._create(ir.filter(self._value, key._value))
            return self._fallback_call("__getitem__", _unwrap(key))

        elif (
            isinstance(key, np.ndarray)
            and key.ndim == 1
            and key.dtype == np.bool_
        ):
            mask = Series(key)
            return Series._create(ir.filter(self._value, mask._value))

        elif isinstance(key, slice) and utils.is_int_or_none_slice(key):
            if key.step is None or key.step == 1:
                return self._slice(key)

        if (
            fireducks.core.get_fireducks_options().fast_fallback
            and self._fireducks_meta.is_cached()
            and not isinstance(key, _Scalar)
        ):
            obj = self._fireducks_meta.get_cache()
            ret = obj.__getitem__(utils._unwrap(key))
            ret = utils._wrap(ret)
            return ret

        reason = f"Unsupported key type: {type(key)}"
        return self._fallback_call(
            "__getitem__", key, __fireducks_reason=reason
        )

    def __invert__(self):
        return Series._create(ir.invert(self._value))

    def __len__(self):
        return self.shape[0]

    def __neg__(self):
        return Series._create(ir.negate(self._value))

    def __round__(self, decimals=0):
        return self.round(decimals)

    def __setattr__(self, name, value):
        logger.debug("Series.__setattr__: name=%s", name)
        if name in ["_value"]:
            object.__setattr__(self, name, value)
        else:
            self._fallback_call("__setattr__", name, value)

    def __setitem__(self, key, value):
        logger.debug("Series.__setitem__")
        reason = "Series.__setitem is always fallback"
        self._fallback_mutating_method(
            "__setitem__", args=[key, value], reason=reason, stacklevel=8
        )

    def abs(self):
        return Series._create(ir.abs(self._value))

    def aggregate(self, func=None, axis=0, *args, **kwargs):
        axis = self._get_axis_number(axis)

        reason = None
        if irutils._is_scalar_or_list_or_tuple_of(func, str):
            targets = [func] if isinstance(func, str) else func
            if not utils.is_supported_df_agg_funcs(targets):
                reason = f"all or few agg functions are not supported: {func}"
        else:
            reason = "'func' is neither string nor a list/tuple of strings"

        if args or kwargs:
            reason = "args or kwargs is specified"

        if reason:
            return self._fallback_call(
                "aggregate",
                func,
                axis,
                *args,
                **kwargs,
                __fireducks_reason=reason,
            )

        if isinstance(func, str):
            value = ir.aggregate_column_scalar(self._value, func)
            return _Scalar(value)
        else:
            func = irutils.make_vector_or_scalar_of_str(func)
            value = ir.aggregate(self._value, func, axis=0)
            return Series._create(value)

    agg = aggregate

    def corr(self, *args, **kwargs):
        arg = utils.decode_args(args, kwargs, pandas.Series.corr)
        reason = []

        if not isinstance(arg.other, Series):
            reason.append(
                "unsupported 'other' of type =" f"'{type(arg.other).__name__}'"
            )

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
        return _Scalar(
            ir.series_corr(
                self._value, arg.other._value, arg.method, arg.min_periods
            )
        )

    def diff(self, *args, **kwargs):
        arg = utils.decode_args(args, kwargs, pandas.Series.diff)
        if not isinstance(arg.periods, int):
            reason = "periods is not int"
        else:
            return Series._create(ir.diff(self._value, arg.periods))

        return self._fallback_call(
            "diff", *args, **kwargs, __fireducks_reason=reason
        )

    def drop_duplicates(self, *args, **kwargs):
        arg = utils.decode_args(args, kwargs, pandas.Series.drop_duplicates)
        arg.inplace = validate_bool_kwarg(arg.inplace, "inplace")
        supported_keep = {"first", "last", False}

        # available since pandas 2.0.0
        """
        arg.ignore_index = validate_bool_kwarg(
            arg.ignore_index, "ignore_index"
        )
        if (
            arg.keep in supported_keep
            and not arg.inplace
            and not arg.ignore_index
        ):
        """
        if arg.keep in supported_keep and not arg.inplace:
            subset = irutils.make_tuple_of_column_names([])  # NA for Series
            arg.keep = "none" if arg.keep is False else arg.keep
            return Series._create(
                ir.drop_duplicates(self._value, subset, arg.keep)
            )

        return self._fallback_may_inplace(
            "drop_duplicates",
            args,
            kwargs,
            pos=2,
            reason="unsupported argument",
        )

    def dropna(self, *args, **kwargs):
        arg = utils.decode_args(args, kwargs, pandas.Series.dropna)
        if arg.axis in (0, "index"):
            subset = irutils.make_tuple_of_column_names([])
            value = ir.dropna(self._value, subset, True, 0)
            return self._create_or_inplace(value, arg.inplace)

        return self._fallback_may_inplace(
            "dropna",
            args,
            kwargs,
            pos=2,
            reason="unsupported argument",
        )

    def duplicated(self, *args, **kwargs):
        arg = utils.decode_args(args, kwargs, pandas.Series.duplicated)

        supported_keep = {"first", "last", False}
        if arg.keep in supported_keep:
            subset = irutils.make_tuple_of_column_names([])  # NA for Series
            arg.keep = "none" if arg.keep is False else arg.keep
            return Series._create(ir.duplicated(self._value, subset, arg.keep))

        return self._fallback_call(
            "duplicated",
            arg.keep,
            __fireducks_reason=f"unsupported keep = {arg.keep}",
        )

    @property
    def dtype(self):
        if self._fireducks_meta.is_cached():
            return self._fireducks_meta.get_cache().dtypes

        if fireducks.core.get_ir_prop().has_metadata:
            dtypes, unsupported = self._get_metadata().dtypes
            if len(unsupported) == 0:
                assert len(dtypes) == 1
                return dtypes[0]
            reason = "Series.dtype is unsupported type: " + ",".join(
                unsupported
            )
        else:
            reason = "IR does not support metadata"

        return utils.fallback_attr(self._unwrap, "dtypes", reason=reason)

    dtypes = dtype

    def explode(self, ignore_index=False):
        column = irutils.make_tuple_of_column_names([])  # NA for Series
        # according to pandas behavior. all true values would be treated
        # as true. e.g., ignore_index="a" would be treated as ignore_index=True
        ignore_index = bool(ignore_index)
        return Series._create(ir.explode(self._value, column, ignore_index))

    def groupby(self, by=None, *args, **kwargs):
        logger.debug("series.groupby: type(by)=%s", type(by))
        from fireducks.pandas.groupby import SeriesGroupBy

        return SeriesGroupBy(self, by=by, *args, **kwargs)

    def isin(self, values):
        if (
            irutils._is_list_or_tuple_of(values, str)
            or irutils._is_list_or_tuple_of(values, int)
            or irutils._is_list_or_tuple_of(values, float)
        ):
            values = irutils.make_tuple_of_scalars(values)
            return Series._create(ir.isin(self._value, values))
        if isinstance(values, Series):
            return Series._create(ir.isin_vector(self._value, values._value))
        return self._fallback_call("isin", values)

    def isna(self):
        return Series._create(ir.isnull(self._value))

    def isnull(self):
        return Series._create(ir.isnull(self._value))

    def map(self, arg, na_action=None):
        if isinstance(arg, dict):
            return utils.apply_dict_on_series(arg, self)
        elif isinstance(arg, type) and arg in (str, int, float):
            return self.astype(arg)
        else:
            reason = "input 'arg' is neither a dict nor a type to be casted"
            return self._fallback_call(
                "map", arg, na_action, __fireducks_reason=reason
            )

    def notna(self):
        return ~self.isnull()

    def notnull(self):
        return ~self.isnull()

    # To unwrap `index` which might be in kwargs, _fallback_may_inplace has to
    # be called explicitly here.
    def rename(self, index=None, **kwargs):
        reason = "Series.rename is fallback"
        return self._fallback_may_inplace(
            "rename", [utils._unwrap(index)], kwargs, reason=reason
        )

    def repeat(self, repeats, axis=None):
        if axis is not None:
            reason = "axis is not None"
            return self._fallback_call(
                "repeat", repeats, axis=axis, __fireducks_reason=reason
            )
        if irutils._is_scalar_or_list_or_tuple_of(
            repeats, int
        ) or irutils._is_scalar_or_list_or_tuple_of(repeats, float):
            repeats = irutils.make_tuple_of_scalars(repeats)
            return Series._create(ir.repeat(self._value, repeats))
        if isinstance(repeats, Series):
            return Series._create(
                ir.repeat_vector(self._value, repeats._value)
            )
        return self._fallback_call("repeat", repeats)

    def reset_index(self, *args, **kwargs):
        arg = utils.decode_args(args, kwargs, pandas.Series.reset_index)
        arg.inplace = validate_bool_kwarg(arg.inplace, "inplace")
        arg.drop = validate_bool_kwarg(arg.drop, "drop")

        reason = arg.is_not_default(["level", "allow_duplicates", "name"])
        if reason:
            return self._fallback_may_inplace(
                "reset_index", args, kwargs, pos=3, reason=reason
            )

        value = ir.reset_index(self._value, arg.drop, True)
        if arg.drop:
            return self._create_or_inplace(value, arg.inplace)
        else:  # DataFrame to be created
            if arg.inplace:
                raise TypeError(
                    "Cannot reset_index inplace on a Series "
                    + "to create a DataFrame"
                )
            return fireducks_pandas.DataFrame._create(value=value)

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
        return Series._create(ir.round(self._value, decimals))

    @property
    def shape(self) -> Tuple[int, ...]:
        if (
            fireducks.core.get_fireducks_options().fast_fallback
            and self._fireducks_meta.is_cached()
        ):
            obj = self._fireducks_meta.get_cache()
            return obj.shape

        value = ir.get_shape(self._value)
        shape = fireducks.core.evaluate([value])[0]
        return (shape.y,)

    @property
    def size(self) -> int:
        return self.shape[0]

    @property
    def ndim(self) -> int:
        return 1

    def value_counts(
        self,
        normalize=False,
        sort=True,
        ascending=False,
        bins=None,
        dropna=True,
    ):
        if not normalize and bins is None:
            return Series._create(
                ir.value_counts(self._value, sort, ascending, dropna)
            )

        reason = "normalize is True or bins is not None"
        return self._fallback_call(
            "value_counts",
            normalize,
            sort,
            ascending,
            bins,
            dropna,
            __fireducks_reason=reason,
        )

    def quantile(self, *args, **kwargs):
        reason = None
        arg = utils.decode_args(args, kwargs, pandas.Series.quantile)

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

        if reason:
            return self._fallback_call_packed(
                "quantile", args, kwargs, reason=reason
            )

        is_scalar = irutils.irable_scalar(arg.q)
        if is_scalar:
            arg.q = float(arg.q)
            return _Scalar(
                ir.quantile_scalar(self._value, arg.q, arg.interpolation)
            )
        else:
            arg.q = [float(e) for e in arg.q]
            qs = irutils.make_vector_or_scalar_of_scalar(arg.q)
            return Series._create(
                ir.quantile(self._value, qs, arg.interpolation)
            )

    @deprecate_nonkeyword_arguments(version=None, allowed_args=["self"])
    def sort_values(self, *args, **kwargs):
        arg = utils.decode_args(args, kwargs, pandas.Series.sort_values)
        known_kinds = ["quicksort", "mergesort", "heapsort", "stable"]
        if not isinstance(arg.inplace, bool):
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

        key = ir.make_tuple_column_name([])
        if not isinstance(arg.ascending, list):
            arg.ascending = [arg.ascending]
        orders = ir.make_tuple_i1([bool(a) for a in arg.ascending])
        na_pos = False if arg.na_position == "first" else True
        value = ir.sort_values(self._value, key, orders, na_pos, True)
        return self._create_or_inplace(value, arg.inplace)

    def to_frame(self, *args, **kwargs):
        ns = utils.decode_args(args, kwargs, pandas.Series.to_frame)
        reason = ns.is_not_default(["name"])
        to_rename = reason is not None
        cname = ns.name if to_rename else ""
        return fireducks_pandas.DataFrame._create(
            ir.to_frame(
                self._value, irutils.make_column_name(cname), to_rename
            )
        )

    def to_numpy(self, *args, **kwargs):
        ns = utils.decode_args(args, kwargs, pandas.Series.to_numpy)

        reason = ns.is_not_default(
            [
                "dtype",
                "na_value",
                # Because ns.copy=False does not ensure no copy in pandas and
                # fireducks always copies, ns.copy can be ignored.
            ]
        )

        if reason is not None:
            return self._fallback_call_packed(
                "to_numpy", args, kwargs, reason=reason
            )

        value = ir.to_numpy(self._value)
        return fireducks.core.evaluate([value])[0]

    def __array__(self, *args, **kwargs):
        ns = utils.decode_args(args, kwargs, pandas.Series.__array__)

        reason = ns.is_not_default(["dtype"])
        if reason is not None:
            return self._fallback_call_packed(
                "__array__", args, kwargs, reason=reason
            )

        return self.to_numpy()
