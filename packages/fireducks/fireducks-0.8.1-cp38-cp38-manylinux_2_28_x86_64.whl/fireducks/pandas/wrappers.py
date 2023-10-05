# Copyright (c) 2023 NEC Corporation. All Rights Reserved.

import pandas
from fireducks.pandas.utils import (
    PandasClassWrapper,
    _unwrap,
    _fireducks_class,
)

import logging

logger = logging.getLogger(__name__)


class Categorical(PandasClassWrapper):
    _pandas_cls = pandas.core.arrays.categorical.Categorical


class Index(PandasClassWrapper):
    _pandas_cls = pandas.core.indexes.base.Index

    def __new__(cls, *args, _pandas_obj=None, **kwargs):
        if _pandas_obj is None:
            _pandas_obj = cls._pandas_cls(*_unwrap(args), **_unwrap(kwargs))
            cls = _fireducks_class(type(_pandas_obj))
        self = object.__new__(cls)
        PandasClassWrapper.__init__(self, _pandas_obj=_pandas_obj)
        return self

    def __init__(self, *args, _pandas_obj=None, name=None, **kwargs):
        object.__setattr__(self, "_fireducks_frame", None)

    def __setattr__(self, name, value):
        if name == "name":
            self._pandas_obj.name = value
            if self._fireducks_frame is not None:
                logger.debug("Detected columns.name update: %s", value)
                self._fireducks_frame._set_column_index_names([value])
            return
        super().__setattr__(name, value)

    def _set_fireducks_frame(self, fireducks_frame):
        object.__setattr__(self, "_fireducks_frame", fireducks_frame)


class CategoricalIndex(Index):
    _pandas_cls = pandas.core.indexes.category.CategoricalIndex


class DatetimeIndex(Index):
    _pandas_cls = pandas.core.indexes.datetimes.DatetimeIndex


class IntervalIndex(Index):
    _pandas_cls = pandas.core.indexes.interval.IntervalIndex


class MultiIndex(Index):
    _pandas_cls = pandas.core.indexes.multi.MultiIndex


class NumericIndex(Index):
    _pandas_cls = pandas.core.indexes.numeric.NumericIndex


class Int64Index(Index):
    _pandas_cls = pandas.core.indexes.numeric.Int64Index


class UInt64Index(Index):
    _pandas_cls = pandas.core.indexes.numeric.UInt64Index


class Float64Index(Index):
    _pandas_cls = pandas.core.indexes.numeric.Float64Index


class PeriodIndex(Index):
    _pandas_cls = pandas.core.indexes.period.PeriodIndex


class RangeIndex(Index):
    _pandas_cls = pandas.core.indexes.range.RangeIndex


class TimedeltaIndex(Index):
    _pandas_cls = pandas.core.indexes.timedeltas.TimedeltaIndex
