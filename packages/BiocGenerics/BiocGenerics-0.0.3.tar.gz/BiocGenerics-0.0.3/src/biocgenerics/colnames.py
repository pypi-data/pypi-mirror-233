from functools import singledispatch
from typing import List

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


@singledispatch
def colnames(x) -> list:
    """Access column names from 2-dimensional representations.

    Args:
        x: Any object.

    Raises:
        NotImplementedError: If ``x`` is not a supported type.

    Returns:
        list: List of column names.
    """
    if hasattr(x, "colnames"):
        return x.colnames

    raise NotImplementedError(f"`colnames` is not supported for class: '{type(x)}'.")


try:
    from pandas import DataFrame

    @colnames.register(DataFrame)
    def _colnames_dataframe(x: DataFrame) -> list:
        return x.columns

except Exception:
    pass


@singledispatch
def set_colnames(x, names: List[str]):
    """Set column names.

    Args:
        x: Any object.
        names (List[str]): New names.

    Raises:
        NotImplementedError: if type is not supported.

    Returns:
        An object with the same type as ``x``.
    """
    raise NotImplementedError(
        f"`set_colnames` is not supported for class: '{type(x)}'."
    )


try:
    from pandas import DataFrame

    @set_colnames.register(DataFrame)
    def _set_colnames_dataframe(x: DataFrame, names: List[str]):
        x.columns = names

        return x

except Exception:
    pass
