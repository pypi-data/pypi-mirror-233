# Copyright (c) 2023 NEC Corporation. All Rights Reserved.
"""
fireducks.pandas provides pandas-like API on top of fireducks.
"""

import os
import sys

env = os.environ.get("FIREDUCKS_DISABLE")
if env is not None:
    from pandas import *  # noqa
else:
    import logging

    from fireducks import __version__, __dfkl_version__

    from fireducks.pandas.api import (
        from_pandas,
        concat,
        isna,
        isnull,
        melt,
        merge,
        notna,
        notnull,
        read_csv,
        read_parquet,
        to_parquet,
        to_pickle,
    )
    from fireducks.pandas.frame import DataFrame
    from fireducks.pandas.series import Series

    # FireDucks original API
    from fireducks.pandas.feat import (  # noqa
        aggregation,
        multi_target_encoding,
    )

    import fireducks.pandas.utils as _utils
    from fireducks.pandas.utils import (  # noqa
        prohibit_fallback,
        _get_pandas_module,
    )

    from fireducks.pandas.wrappers import (
        Categorical,
        CategoricalIndex,
        DatetimeIndex,
        Index,
        Int64Index,
        UInt64Index,
        Float64Index,
        IntervalIndex,
        MultiIndex,
        NumericIndex,
        PeriodIndex,
        RangeIndex,
        TimedeltaIndex,
    )

    logger = logging.getLogger(__name__)

    # 3.7 or later supports module's __getattr__
    if sys.version_info.major > 3 or (
        sys.version_info.major == 3 and sys.version_info.minor >= 7
    ):
        # Borrow unknown attribute from pandas
        def __getattr__(name):
            logger.debug("Borrow %s from pandas", name)
            reason = f"borrow {name} from pandas"
            return _utils.fallback_attr(
                _get_pandas_module, name, reason=reason
            )

    else:
        m = sys.modules[__name__]

        class Wrapper:
            def __getattr__(self, name):
                logger.debug("Borrow %s from pandas", name)
                return _utils.fallback_attr(_get_pandas_module, name)

        w = Wrapper()
        names = [
            "from_pandas",
            "read_csv",
            "to_pickle",
            "DataFrame",
            "Series",
            "prohibit_fallback",
            "__path__",
            "__spec__",
        ]
        for name in names:
            setattr(w, name, getattr(m, name))
        w.__name__ = "fireducks.pandas"
        sys.modules[__name__] = w

    __all__ = (
        __dfkl_version__,
        from_pandas,
        # pandas api
        __version__,
        DataFrame,
        Series,
        Categorical,
        CategoricalIndex,
        DatetimeIndex,
        Index,
        Int64Index,
        UInt64Index,
        Float64Index,
        IntervalIndex,
        MultiIndex,
        NumericIndex,
        PeriodIndex,
        RangeIndex,
        TimedeltaIndex,
        concat,
        isna,
        isnull,
        melt,
        merge,
        notna,
        notnull,
        read_csv,
        read_parquet,
        to_parquet,
        to_pickle,
    )
