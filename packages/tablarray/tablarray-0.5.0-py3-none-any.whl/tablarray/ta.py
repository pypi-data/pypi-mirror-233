#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 17:39:50 2020

@author: chris
"""

import copy as _copy
import numpy as _np

from .tanumpy import np_func as _np2ta
from . import mmul
from . import re
from . import tashape
from . import taprint
from . import misc
from .wraps.op12swap import op12_swap as _op12_swap


def _ragged_loader(outarray, lla):
    def _inner_ragged_loader(sub_lla, *indices):
        n = len(sub_lla)
        for a in range(n):
            sub_sub_lla = sub_lla[a]
            if type(sub_sub_lla) is list:
                _inner_ragged_loader(sub_sub_lla, *indices, a)
            else:
                outarray.__setitem__((*indices, a),
                                     sub_sub_lla)

    _inner_ragged_loader(lla)


class TablArray(object):
    """
    TablArray (Table-Array)
    -----------------------
    When the best structure of data is any-dimensional cells arranged
    in any-dimensional tables - TablArray provides fast numpy-like array
    operations with broadcasting to handle both cellular-dim (cdim)
    and tabular-dim (tdim) at once. Indexing and slicing follow rules of
    different views; .cell[] .table[] or .array[].

    Selected signatures::

        import tablarray as ta
        a1 = ta.TablArray(a, 1)
        a2 = ta.TablArray.from_tile(cell, (2, 3))
        c = ta.matmul(a2, a1)
        d = c + .03 * a2
        e = ta.cell(d)[0, :]

    Principles
    ----------

    1. (Fast) numeric operations including tablarray.matmul() are oriented to
        cells by default.
        But can also be oriented to other views, i.e.
        a.table.sum(axis=1) or tablarray.sum(a.table, axis=1)
    2. Cells may be any cdim, normally matrices (cdim=2), vectors (cdim=1)
        or scalars (cdim=0).
    3. Tables may be any tdim, separately from cellular cdim.
    4. As much as possible, ATC might be duck-typed as numpy-arrays,
        func(a:array-like, ...) can work with func(a:ATC, ...).
        func should use a.method(...), not numpy.method(a, ...)
    5. Tables support projection onto any axis.

    Parameters
    ----------
    a : numpy.ndarray (or list or tuple)
        an Array to wrap
    cdim : int (0,1,2)
        cellular dim; normally 0 - scalar, 1 - vector, 2 - matrix
        or taShapes type
    """

    def __init__(self, a, cdim, view='cell'):
        # ensure type of self.base
        if isinstance(a, _np.ndarray):
            self.base = a          # based on ndarray
        elif misc.istablarray(a):
            self.base = a.base    # based on ATC type
            cdim = a.ts
        else:
            self.base = _np.array(a)  # try casting to ndarray
        # ts has derived parameters
        if _np.isscalar(cdim):
            self.ts = tashape.taShape((self.base.shape), cdim)
        elif hasattr(cdim, 'cdim') and hasattr(cdim, 'combine'):
            # if cdim is of taShapes type
            self.ts = cdim
        else:
            raise TypeError
        # set the view
        self.setview(view)

    @classmethod
    def from_tile(cls, cell, tshape, view='table'):
        """create a table by tiling a cell"""
        cdim = 0 if _np.isscalar(cell) else cell.ndim
        shape2 = tuple([1] * cdim)
        a = _np.tile(cell, (*tshape, *shape2))
        return cls(a, cdim, view)

    @classmethod
    def from_listarray(cls, lla, blank=None, dtype=None, view='table'):
        """
        create a TablArray from a listarray

        Parameters
        ----------
        lla : list (of list...) of array-like
            cdim will be inferred from the dim of the array-like object
        blank : [default is None] e.g. nan, 0 or 0.0
            Providing a default value for blanks signals that lld might
            have ragged tabular structure. Before creating TablArrays,
            ragged arrays will be padded with this blank value.
            Tabular structure is allowed to be ragged, but cellular
            structure must not be ragged!
        dtype : [default is None] e.g. int, float, bool
            If dtype is None and blank is provided, dtype will be inferred
            from blank. Specify dtype to force the issue.
        view : str
            'table' 'bcast' 'cell' or 'array'
        """
        obj0 = misc._get_1st_obj(lla)
        cshape = _np.shape(obj0)
        if blank is None:
            a = _np.array(lla)
        else:
            tshape = misc._imply_shape_ragged(lla)
            a = _np.empty((*tshape, *cshape), dtype=dtype)
            a[:] = blank
            _ragged_loader(a, lla)
        return cls(a, len(cshape), view)

    def __view__(self, view):
        """returns an ATC with a different .setview(view), using
        pass-by-reference not copy so that changes do affect this original"""
        return TablArray(self.base, self.ts, view)

    def __copy__(self):
        """returns an independent copy"""
        return TablArray(_copy.copy(self.base), self.ts.cdim, self.view)

    def __deepcopy__(self, memo):
        """returns an indepenedent deepcopy"""
        return TablArray(_copy.deepcopy(self.base), self.ts.cdim, self.view)

    __str__ = taprint.tablarray2string

    def __repr__(self):
        return self.__str__()

    def setview(self, view):
        """view='array', 'table', 'cell', or 'bcast'

        Changes the sense of alignment of methods to data.
        """
        self._tabular = False
        self._cellular = False
        self._bcast = False
        # only allow one view
        if view == 'table' or view == 'bcast':
            self._tabular = True
            self._viewdims = tuple(range(self.ts.tdim))
            self._viewcdim = self.ts.cdim
            self.shape = self.ts.tshape
            self.ndim = self.ts.tdim
            self.size = self.ts.tsize
            if view == 'bcast':
                self._bcast = True
        elif view == 'cell':
            self._cellular = True
            ndim = self.ts.tdim + self.ts.cdim
            self._viewdims = tuple(range(self.ts.tdim, ndim))
            self._viewcdim = 0
            self.shape = self.ts.cshape
            self.ndim = self.ts.cdim
            self.size = self.ts.csize
        elif view == 'array':
            ndim = self.ts.tdim + self.ts.cdim
            self._viewdims = tuple(range(ndim))
            self._viewcdim = 0
            self.shape = self.base.shape
            self.ndim = self.base.ndim
            self.size = self.base.size
        else:
            raise ValueError
        # keep the view string handy
        self.view = view

    # ===== 'inheriting' from .base ====
    def __getattr__(self, attr):
        # check in my dictionary first
        if attr in self.__dict__:
            return getattr(self, attr)
        # maybe inherit all else from .base, or maybe not?
        # LOG.warning('Passing self.base.%s ...dangerous?', attr)
        return getattr(self.base, attr)

    def __len__(self):
        return self.shape[0] if len(self.shape) > 0 else 0

    # ==== getters have delayed iteration, for properties which are views
    @property
    def real(self):
        """Return the real part of a complex ATC"""
        return TablArray(self.base.real, self.ts.cdim, self.view)

    @property
    def imag(self):
        """Return the imaginary part of a complex ATC"""
        return TablArray(self.base.imag, self.ts.cdim, self.view)

    # for duck-typing it's often better to use tablarray.bcast(), .table() etc.
    @property
    def bcast(self):
        """Return a view of an ATC with broadcast-style tabular indexing"""
        return self.__view__('bcast')

    @property
    def cell(self):
        """Return a view of an ATC with cullular aligned indexing"""
        return self.__view__('cell')

    @property
    def table(self):
        """Return a view of an ATC with tabular aligned indexing"""
        return self.__view__('table')

    @property
    def array(self):
        """Return a view of a TablArray with simple array indexing"""
        return self.__view__('array')

    def _process_indx(self, indices):
        # we want type list for this process
        type_indx = type(indices)
        if type_indx is list:
            pass
        elif type_indx is tuple:
            indices = list(indices)
        else:
            indices = [indices]
        if self._cellular:
            # cellular spans tabular indices
            indices, cdim = self.ts.cslice(indices)
        elif self._tabular:
            if self._bcast:
                # modify the indices using broadcast rules
                indices = self.ts.bcast(indices)
            # tabular view spans cellular indices
            indices, cdim = self.ts.tslice(indices)
        else:
            indices, cdim = self.ts.aslice(indices)
        return tuple(indices), cdim

    def __getitem__(self, indices):
        if self.ts.tdim == 0 and self._bcast:
            # special case for bcast w tdim=0
            rarray = self.base
            cdim = 0
        else:
            indices, cdim = self._process_indx(indices)
            # once an ATC, always an ATC
            rarray = self.base.__getitem__(indices)
        # return TablArray(rarray, cdim, self.view)
        return misc._rval_once_a_ta(TablArray, rarray, cdim, self.view)

    def __setitem__(self, indices, val):
        if isinstance(val, TablArray):
            # strip ATC types - only numpy.ndarray can be set
            val = val.base
        indices, cdim = self._process_indx(indices)
        return self.base.__setitem__(indices, val)

    # bin_op has numpy binary operators plus an ATC-wrap
    __add__ = _np2ta.add
    __radd__ = _op12_swap(_np2ta.add)
    __sub__ = _np2ta.subtract
    # for non-commutative operations, op12_swap flips order of self,other
    __rsub__ = _op12_swap(_np2ta.subtract)
    __mul__ = _np2ta.multiply
    __rmul__ = _op12_swap(_np2ta.multiply)
    __pow__ = _np2ta.power
    __rpow__ = _op12_swap(_np2ta.power)
    __truediv__ = _np2ta.true_divide
    __rtruediv__ = _op12_swap(_np2ta.true_divide)
    __divmod__ = _np2ta.divmod
    __rdivmod__ = _op12_swap(_np2ta.divmod)
    __floordiv__ = _np2ta.floor_divide
    __eq__ = _np2ta.equal
    __ge__ = _np2ta.greater_equal
    __gt__ = _np2ta.greater
    __le__ = _np2ta.less_equal
    __lt__ = _np2ta.less
    __and__ = _np2ta.logical_and
    __or__ = _np2ta.logical_or
    __xor__ = _np2ta.logical_xor
    # matmul
    __matmul__ = mmul.matmul
    # ax_op has numpy unial operators (axis->scalar), plus an ATC-wrap
    all = _np2ta.all
    any = _np2ta.any
    argmax = _np2ta.argmax
    argmin = _np2ta.argmin
    max = _np2ta.max
    mean = _np2ta.mean
    min = _np2ta.min
    prod = _np2ta.prod
    std = _np2ta.std
    sum = _np2ta.sum
    # === el_op has numpy unial operators (elementwise), plus ATC-wrap
    conj = _np2ta.conj
    conjugate = _np2ta.conjugate
    __abs__ = _np2ta.abs
    __invert__ = _np2ta.invert
    __neg__ = _np2ta.negative
    # cumulative functions
    cumprod = _np2ta.cumprod
    cumsum = _np2ta.cumsum
    # reshaping and flattening that considers TablArray form
    reshape = re.reshape
    ravel = re.ravel

    def flatten(self, order='C'):
        """"Return a copy of the TablArray collapsed
        along tabular or cellular structure into 1 dimension
        """
        return _copy.copy(re.ravel(self, order=order))
