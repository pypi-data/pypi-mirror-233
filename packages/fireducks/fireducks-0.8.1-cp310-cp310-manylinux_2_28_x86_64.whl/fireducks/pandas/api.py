# Copyright (c) 2023 NEC Corporation. All Rights Reserved.

from collections import abc
import os
import logging

from pandas.io.common import is_url
from pandas.core.dtypes.common import is_scalar
import pandas._libs.missing as libmissing

from firefw import tracing

with tracing.scope(tracing.Level.DEFAULT, "import pandas"):
    import pandas
    import pandas._libs.lib as pandas_lib

from fireducks import ir, irutils
import fireducks.core
from fireducks.pandas.frame import DataFrame
from fireducks.pandas.series import Series
import fireducks.pandas.utils as utils

logger = logging.getLogger(__name__)

#
# FireDucks API
#


def from_pandas(obj):
    logger.debug("from_pandas: %s", type(obj))

    if isinstance(obj, pandas.DataFrame):
        return DataFrame.from_pandas(obj)
    elif isinstance(obj, pandas.Series):
        return Series.from_pandas(obj)
    raise RuntimeError(
        "fireducks.from_panad: unknown object is given: " f"{type(obj)}"
    )


#
# Pandas copmat API
#


def concat(
    objs,
    *,
    axis=0,
    join="outer",
    ignore_index=False,
    keys=None,
    levels=None,
    names=None,
    verify_integrity=False,
    sort=False,
    copy=True,
):
    class Concat:
        def __init__(self, objs, keys):
            if isinstance(objs, abc.Mapping):
                if keys is None:
                    keys = list(objs.keys())
                self.objs = [objs[k] for k in keys]
            else:
                self.objs = list(objs)

    op = Concat(objs, keys)

    cls = None
    if all([isinstance(obj, DataFrame) for obj in objs]):
        cls = DataFrame
    if all([isinstance(obj, Series) for obj in objs]):
        cls = Series

    if (
        cls is not None
        and axis == 0
        and join == "outer"
        and keys is None
        and levels is None
        and names is None
        and not verify_integrity
        and not sort
    ):
        objs = irutils.make_tuple_of_tables(objs)
        return cls._create(
            ir.concat(objs, ignore_index=ignore_index)
        ).__finalize__(op, method="concat")

    return utils.fallback_call(
        utils._get_pandas_module,
        "concat",
        objs,
        axis=axis,
        join=join,
        ignore_index=ignore_index,
        keys=keys,
        levels=levels,
        names=names,
        verify_integrity=verify_integrity,
        sort=sort,
        copy=copy,
    ).__finalize__(op, method="concat")


def isnull(obj):
    if is_scalar(obj):
        return libmissing.checknull(obj)
    elif isinstance(obj, type):
        return False
    elif isinstance(obj, (DataFrame, Series)):
        return obj.isnull()

    return utils.fallback_call(
        utils._get_pandas_module,
        "isnull",
        obj,
        __fireducks_reason="obj is not DataFrame or Series",
    )


isna = isnull


def melt(frame, *args, **kwargs):
    if isinstance(frame, DataFrame):
        return frame.melt(*args, **kwargs)

    return utils.fallback_call(
        utils._get_pandas_module,
        "melt",
        frame,
        *args,
        __fireducks_reason="obj is not DataFrame",
        **kwargs,
    )


def merge(left, right, **kwargs):
    return left.merge(right, **kwargs)


def notna(obj):
    if isinstance(obj, (DataFrame, Series)):
        return ~(obj.isnull())

    return utils.fallback_call(
        utils._get_pandas_module,
        "notna",
        obj,
        __fireducks_reason="obj is not DataFrame or Series",
    )


notnull = notna


def read_csv(
    filepath_or_buffer,
    sep=pandas_lib.no_default,
    delimiter=None,
    names=None,
    index_col=None,
    usecols=None,
    dtype=None,
    **kwargs,
):
    reason = None
    if names is not None and not irutils._is_str_list(names):
        reason = "names is not a list of string"
    elif not isinstance(filepath_or_buffer, str):
        reason = "filepath_or_buffer is not filepath"
    elif index_col is not None and not isinstance(index_col, int):
        reason = "index_col is not int or None"
    elif kwargs:
        reason = f"unsupported kwargs is used: {kwargs}"
    elif usecols is not None and not irutils._is_str_list(usecols):
        reason = "usecols is not a list of string"
    elif (
        dtype is not None
        and not isinstance(dtype, dict)
        and not irutils.is_supported_dtype(dtype)
    ):
        reason = f"dtype is not supported: {dtype}"
    elif isinstance(dtype, dict):
        for key, typ in dtype.items():
            if not isinstance(key, str):
                reason = f"column name of dtype is not string: {key}"
            elif not irutils.is_supported_dtype(typ):
                reason = f"dtype is not supported: {typ}"
        if hasattr(dtype, "default_factory"):  # defaultdict
            default_dtype = dtype.default_factory()
            if not irutils.is_supported_dtype(default_dtype):
                reason = f"default dtype is not supported: {default_dtype}"

    if reason is not None:
        return utils.fallback_call(
            utils._get_pandas_module,
            "read_csv",
            filepath_or_buffer,
            sep=sep,
            delimiter=delimiter,
            names=names,
            index_col=index_col,
            usecols=usecols,
            dtype=dtype,
            **kwargs,
            __fireducks_reason=reason,
        )

    # when include_columns is empty, all columns are returned
    include_columns = [] if usecols is None else usecols

    from fireducks.fireducks_ext import ReadCSVOptions

    options = ReadCSVOptions()
    if names:
        options.names = names
    if index_col is not None:
        options.index_col = index_col
    if include_columns:
        options.include_columns = include_columns
    if delimiter is None:
        delimiter = sep
    if delimiter is pandas_lib.no_default:
        delimiter = ","
    options.delimiter = delimiter

    if isinstance(dtype, dict):
        for k, v in dtype.items():
            options.set_column_type(k, irutils.to_supported_dtype(v))
        if hasattr(dtype, "default_factory"):  # defaultdict
            options.default_dtype = irutils.to_supported_dtype(
                dtype.default_factory()
            )
    elif dtype is not None:
        options.default_dtype = irutils.to_supported_dtype(dtype)

    options = fireducks.core.make_available_value(
        options, ir.ReadCSVOptionsType
    )
    value = ir.read_csv(filepath_or_buffer, options)

    return DataFrame._create(value)


def read_parquet(path, engine="auto", *args, **kwargs):
    reason = None

    # engine=pyarrow should be supported?
    if engine != "auto" and engine != "pyarrow":
        reason = f"engine is not auto: {engine}"

    if not isinstance(path, str) or args or kwargs:
        reason = "args or kwargs is used"

    if isinstance(path, str):
        path = os.path.expanduser(path)
        if os.path.isdir(path):
            reason = "path is directory"
        if is_url(path):
            reason = "path is url"

    if reason is not None:
        return utils.fallback_call(
            utils._get_pandas_module,
            "read_parquet",
            path,
            engine,
            *args,
            **kwargs,
            __fireducks_reason=reason,
        )

    return DataFrame._create(ir.read_parquet(path))


# pandas.io.to_parquet is not found in the API document as far as we know. But
# pandas_tests uses it. We provide it as fireducks.pandas.to_parquet because
# fireducks does not provide fireducks.pandas.io package at the moment.
def to_parquet(*args, **kwargs):
    def get_module(reason=None):
        from pandas.io import parquet

        return parquet

    return utils.fallback_call(
        get_module,
        "to_parquet",
        *args,
        **kwargs,
        __fireducks_reason="to_parquet is fallback",
    )


def to_pickle(obj, *args, **kwargs):
    logger.debug("to_pickle")
    pandas.to_pickle(utils._unwrap(obj), *args, **kwargs)
