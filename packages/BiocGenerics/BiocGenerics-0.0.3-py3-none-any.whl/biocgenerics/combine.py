from functools import singledispatch
from itertools import chain
from typing import Any
from warnings import warn

from numpy import concatenate, ndarray

from .combine_rows import combine_rows
from .utils import (
    _convert_1d_sparse_to_dense,
    _is_1d_dense_arrays,
    _is_1d_sparse_arrays,
    is_list_of_type,
)

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


@singledispatch
def combine(*x: Any):
    """Combine vector-like objects (1-dimensional arrays).

    Custom classes may implement their own ``combine`` method.

    If the first element in ``x`` contains a ``combine`` method,
    the rest of the arguments are passed to that method.

    If all elements are 1-dimensional :py:class:`~numpy.ndarray`,
    we combine them using numpy's :py:func:`~numpy.concatenate`.

    If all elements are either 1-dimensional :py:class:`~scipy.sparse.spmatrix` or
    :py:class:`~scipy.sparse.sparray`, these objects are combined
    using scipy's :py:class:`~scipy.sparse.hstack`.

    If all elements are :py:class:`~pandas.Series` objects, they are combined using
    :py:func:`~pandas.concat`.

    For all other scenario's, all elements are coerced to a :py:class:`~list` and
    combined.

    Args:
        x (Any): Array of vector-like objects to combine.

            All elements of ``x`` are expected to be the same class or
            atleast compatible with each other.

    Raises:
        TypeError: If any object in the list cannot be coerced to a list.

    Returns:
        A combined object, typically the same type as the first element in ``x``.
        If the elements are a mix of dense and sparse objects, a :py:class:`~numpy.ndarray` is returned.
        A list if one of the objects is a list.
    """

    first_object = x[0]
    if hasattr(first_object, "combine"):
        return first_object.combine(*x[1:])

    raise NotImplementedError("`combine` method is not implemented for objects.")


def _generic_combine_dense_sparse(x):
    elems = []

    for elem in x:
        if not isinstance(elem, ndarray):
            elem = _convert_1d_sparse_to_dense(elem)

        elems.append(elem)

    if _is_1d_dense_arrays(elems) is not True:
        warn("Not all elements are 1-dimensional arrays, using `combine_rows` instead.")
        combine_rows(*x)

    return concatenate(elems)


def _generic_coerce_list(x):
    elems = []

    for elem in x:
        if isinstance(elem, ndarray):
            elems.append(list(elem))
        elif hasattr(elem, "shape"):  # probably a sparse
            elems.append(list(_convert_1d_sparse_to_dense(elem)))
        elif isinstance(elem, (list, tuple)):  # do nothing
            elems.append(elem)
        else:  # not sure what else
            elems.append(elem)

    return combine(*elems)


@combine.register(list)
def _combine_lists(*x: list):
    return list(chain(*x))


@combine.register(ndarray)
def _combine_dense_arrays(*x: ndarray):
    if is_list_of_type(x, ndarray):
        if _is_1d_dense_arrays(x) is not True:
            warn(
                "Not all elements are 1-dimensional arrays, using `combine_rows` instead."
            )
            combine_rows(*x)

        return concatenate(x)

    warn("Not all elements are numpy ndarrays.")

    if all([hasattr(y, "shape") for y in x]) is True:
        # assuming it's a mix of numpy and scipy arrays
        return _generic_combine_dense_sparse(x)

    # coerce everything to a list and combine
    return _generic_coerce_list(x)


try:
    import scipy.sparse as sp

    def _combine_sparse_arrays(*x):
        if is_list_of_type(x, (sp.sparray, sp.spmatrix)):
            sp_conc = sp.hstack(x)

            if _is_1d_sparse_arrays(x) is not True:
                warn(
                    "Not all elements are 1-dimensional arrays, using `combine_rows` instead."
                )
                combine_rows(*x)

            first = x[0]
            if isinstance(first, (sp.csr_matrix, sp.csr_array)):
                return sp_conc.tocsr()
            elif isinstance(first, (sp.csc_matrix, sp.csc_array)):
                return sp_conc.tocsc()
            elif isinstance(first, (sp.bsr_matrix, sp.bsr_array)):
                return sp_conc.tobsr()
            elif isinstance(first, (sp.coo_matrix, sp.coo_array)):
                return sp_conc.tocoo()
            elif isinstance(first, (sp.dia_matrix, sp.dia_array)):
                return sp_conc.todia()
            elif isinstance(first, (sp.lil_matrix, sp.lil_array)):
                return sp_conc.tolil()
            else:
                return sp_conc

        warn("Not all elements are scipy sparse arrays.")

        if is_list_of_type(x, (ndarray, sp.sparray, sp.spmatrix)):
            return _generic_combine_dense_sparse(x)

        return _generic_coerce_list(x)

    combine.register(sp.sparray, _combine_sparse_arrays)
    combine.register(sp.spmatrix, _combine_sparse_arrays)
except Exception:
    pass


try:
    import pandas as pd

    def _combine_pandas_series(*x):
        if is_list_of_type(x, pd.Series):
            return pd.concat(x)

        # not everything is a Series
        if any([isinstance(y, list) for y in x]) is True:
            elems = []
            for elem in x:
                if isinstance(elem, list):
                    elems.append(pd.Series(elem))
                else:
                    elems.append(elem)

            return pd.concat(elems)

        raise TypeError("All elements must be Pandas Series objects.")

    combine.register(pd.Series, _combine_pandas_series)
except Exception:
    pass
