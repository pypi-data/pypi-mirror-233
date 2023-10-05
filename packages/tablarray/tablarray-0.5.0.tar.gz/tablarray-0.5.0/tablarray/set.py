#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 10 15:44:05 2020

@author: chris
"""

import collections
import numpy as np

# internal imports
# from . import _tabstr
from . import taprint
from . import misc
from .ta import TablArray
from . import re


def _recursive_loader1(lld):
    """given a list of [list of] dict"""
    def _inner_recursive_loader1(key, sub_dataset, sub_lld):
        n = len(sub_lld)
        sub_sub_dataset = []
        for a in range(n):
            sub_sub_lld = sub_lld[a]
            if type(sub_sub_lld) is list:
                _inner_recursive_loader1(key, sub_sub_dataset, sub_sub_lld)
            else:
                sub_sub_dataset.append(sub_sub_lld[key])
        sub_dataset.append(sub_sub_dataset)

    dataset = {}
    keys = misc._get_1st_obj(lld).keys()
    for key in keys:
        dataset[key] = []
        _inner_recursive_loader1(key, dataset[key], lld)
    return dataset


def _recursive_loader2(dataset, lld):
    keys = dataset.keys()

    def _inner_recursive_loader(sub_lld, *indices):
        n = len(sub_lld)
        for a in range(n):
            sub_sub_lld = sub_lld[a]
            if type(sub_sub_lld) is list:
                _inner_recursive_loader(sub_sub_lld, *indices, a)
            else:
                for key in keys:
                    dataset[key].__setitem__((*indices, a),
                                             sub_sub_lld[key])

    _inner_recursive_loader(lld)


class TablaSet(object):
    """
    TablaSet
    --------
    dictionary of broadcast-compatible TablArray's

    E.g.::

        import numpy as np
        import tablarray as ta
        x = ta.TablArray(np.linspace(-2, 2, 4), 0)
        y = ta.TablArray(np.linspace(-1.5, 1.5, 4).reshape(4,1), 0)
        E = ta.zeros((4, 4, 2), cdim=1)
        E.cell[0] = 1.5 / (x**2 + y**2)
        E.cell[1] = -.01 + x * 0
        En = ta.abs(ta.linalg.norm(E)**2)
        Efield = ta.TablaSet(x=x, y=y, E=E, En=En)
        Exslice = Efield['x', 'E', 'En', 2, :]

    As in the last example, TablaSet[] offers intelligent multi-level indexing:
        1. (optional) str keys select elements
            * If a single key, then a TablArray is returend.
            * If multiple keys, a TablaSet is returned.
            * If no keys, a TablaSet with all elements is returned.
        2. (optional) Integer and slices can index within all selected elements.

    Parameters
    ----------
    **kwargs: keyword=TablArray, ..
        name1=tablarray1, name2=tablarray2, ...

    With the addition of element, broadcast compatibility is enforced::

        s1 = ta.TablaSet()
        s1['x'] = ta.TablArray(np.linspace(-1, 3, 5), 0)
        s1['y'] = ta.TablArray([0, 0, 0], 0)
        >>> ValueError: refused to load incompatible shape t(3,)|c() into
        shape t(5,)|c()
    
    Properties
    ----------
    ts : taShape
        describes the max broadcast shape for all elements
    cell : TablaSet
        returns a view of this set with all elements viewed as cells
    table : TablaSet
        returns a view of this set with all elements viewed as tables
    bcast : TablaSet
        returns a view of this set with all elements viewed as broadcast

    Methods
    -------
    keys, items, pop : ()
        adopted from dict
    setview : ('cell' | 'table' | 'bcast' (default))
        sets the view of all elements
    meshtile : (element_key(s))
        Returns an explicitely meshgrid version of element(s) fleshed out to
        the max broadcast shape for this set.
    axis_of : (element_key)
        Returns the dimension
    """

    def __init__(self, view='cell', **kwargs):
        # this is used to track and check broadcastability
        self.ts = None
        # a facade for some dict methods of the table
        self._tablarrays = collections.OrderedDict()
        self.keys = self._tablarrays.keys
        self.items = self._tablarrays.items
        self.pop = self._tablarrays.pop
        self.setview(view)
        for key, val in kwargs.items():
            self[key] = val

    @classmethod
    def from_layered(cls, lld, blank=None, dtype=None):
        """
        Create TablaSet from a 'layered' structure:
            list [of list] of dict of array-like. Where tabular structure is
            implied from the outer list [of list] structure.

        Parameters
        ----------
            lld : list [of list] of dict of array-like
                'layered' input. Note that cdim of TablArrays will be implied
                by the depth of whatever is in dicts
            blank : [default is None] e.g. nan, 0 or 0.0
                Providing a default value for blanks signals that lld might
                have ragged tabular structure. Before creating TablArrays,
                ragged arrays will be padded with this blank value.
                Tabular structure is allowed to be ragged, but cellular
                structure must not be ragged!
            dtype : [default is None] e.g. int, float, bool
                If dtype is None and blank is provided, dtype will be inferred
                from blank. Specify dtype to force the issue.

        Returns
        -------
            dataset : TablaSet
                'unlayered' and cast to TablaSet type
        """
        if type(lld) is not list:
            raise TypeError('lld is not list')
        obj0 = misc._get_1st_obj(lld)
        if type(obj0) is not dict:
            raise TypeError('lld[0]..[0] is not dict')
        keys = obj0.keys()
        cshapes = {}
        for key, val in obj0.items():
            cshapes[key] = np.array(val).shape
        dataset = cls()
        if blank is None:
            tshape = misc._imply_shape(lld)
            unlayered = _recursive_loader1(lld)
            for key, val in unlayered.items():
                dataset[key] = TablArray(val, len(cshapes[key]))
        else:
            tshape = misc._imply_shape_ragged(lld)
            for key in keys:
                array = np.empty((*tshape, *cshapes[key]), dtype=dtype)
                array[:] = blank
                print(tshape, cshapes[key])
                dataset[key] = TablArray(array, len(cshapes[key]))
            _recursive_loader2(dataset, lld)
        return dataset

    def _set_ts(self, new_ts):
        self.ts = new_ts
        # only allow one view
        view = self.view
        if view == 'table' or view == 'bcast':
            self._shape = self.ts.tshape
            self._ndim = self.ts.tdim
            self._size = self.ts.tsize
        elif view == 'cell':
            self._shape = self.ts.cshape
            self._ndim = self.ts.cdim
            self._size = self.ts.csize
        elif view == 'array':
            self._shape = (*self.ts.tshape, *self.ts.cshape)
            self._ndim = self.ts.tdim + self.ts.cdim
            self._size = self.ts.tsize * self.ts.csize
        else:
            raise ValueError

    def __setitem__(self, key, val):
        # note if val is not ATC, we make ts where cdim=ndim!
        # in other words, arrays and ATC's may be mixed, in which case
        # arrays are aligned to the cellular shape of the ATC's
        if isinstance(val, np.ndarray):
            val = TablArray(val, val.ndim)
        elif np.isscalar(val):
            val = TablArray(val, 0)
        if not misc.istablarray(val):
            raise ValueError('values in Array need to be array or TablArray'
                             'type')
        # determine the new master broadcast shape
        ts = val.ts
        if self.ts is None:
            self.ts = ts
        else:
            new_ts, _ = self.ts.combine(ts)
            if new_ts is None:
                raise ValueError(
                    "refused to set incompatible shape %s into shape %s"
                    % (ts, self.ts))
            # keep the broadcasted shape as master
            self._set_ts(new_ts)
        if type(key) is not str:
            raise ValueError('keys must be str type')
        self._tablarrays[key] = val.__view__(self.view)

    def __getitem__(self, args):
        # __getitem__ args are not a tuple if there's only one
        args = args if type(args) is tuple else (args,)
        # sort args into keys (str type) and indices, both are allowed!
        keys = []
        indices = []
        for arg in args:
            if type(arg) is str:
                keys.append(arg)
            else:
                indices.append(arg)
        # but if keys were not specified - get them all!
        if len(keys) == 0:
            keys = list(self.keys())
        # gather return arrays
        rarrays = []
        for key in keys:
            element = self._tablarrays.__getitem__(key)
            if len(indices) == 0:
                rarrays.append(element)
            else:
                rarrays.append((element.bcast.__getitem__(indices)))
        if len(rarrays) == 1:
            # if there's only one key, return the TablArray within
            rval = rarrays[0]
        else:
            # if there's multiple keys, return another TablaSet (view)
            rval = TablaSet()
            for i in range(len(keys)):
                rval[keys[i]] = rarrays[i]
        return rval

    def __contains__(self, key):
        return self._tablarrays.__contains__(key)

    def update(self, **kwargs):
        for key, val in kwargs.items():
            self[key] = val

    __str__ = taprint.tablaset2string

    def __view__(self, view):
        """"""
        new_view = TablaSet(view=view)
        for key in self.keys():
            new_view[key] = self[key]
        return new_view

    def setview(self, view):
        """Set all elements to a view - 'bcast', 'table', 'cell' or 'array'

        see TablArray"""
        self.view = view
        # set all existing values to same view
        for key in self.keys():
            self[key].setview(view)

    @property
    def bcast(self):
        return self.__view__('bcast')

    @property
    def table(self):
        return self.__view__('table')

    @property
    def cell(self):
        return self.__view__('cell')

    @property
    def array(self):
        return self.__view__('array')

    def meshtile(self, *keys):
        """
        Tile an element so that it matches the overarching broadcast table
        shape of the TablaSet, same as it appears when printing a bcast view.
        Often this is the preferred alternate to meshgrid.

        This can be useful e.g. for plotting, while normally bcast view is
        preferred for writing formulas (for memory consumption).

        e.g.::

            # a, b, c are given TablArray's
            tset1 = TablaSet(a=a, b=b, c=c)
            a_m = tset1.meshtile('a')
            b_m, c_m = tset1.meshtile('b', 'c')
        """
        rvals = []
        bcast_tshape = self.ts.tshape
        for key in keys:
            array = self[key]
            tshape = array.ts.tshape
            if bcast_tshape == tshape:
                # skip the rest
                rvals.append(array)
            else:
                # determine the number of repetitions along each axis
                tshape2 = np.ones(self.ts.tdim)
                if array.ts.tdim > 0:
                    tshape2[-array.ts.tdim:] = tshape
                repsArr = np.array(bcast_tshape)
                repsArr[np.equal(tshape2, bcast_tshape)] = 1
                reps = tuple(repsArr)
                rvals.append(re.tile(array.table, reps))
        if len(keys) == 1:
            return rvals[0]
        else:
            return tuple(rvals)

    def degeneracy(self, key):
        """
        Return a truth table indicating which dimensions of master broadcast
        tabular-shape which are degenerate for key. (Ignores cellular shape).
        """
        array = self[key]
        del_dim = self.ts.tdim - array.ts.tdim
        tshape = np.ones(self.ts.tdim)
        tshape[del_dim:] = array.ts.tshape
        bcshape = np.array(self.ts.tshape)
        return bcshape > tshape

    def axis_of(self, key):
        """
        Return the axis number that appear to solely index for key, and
        some ectra intel about that axis.

        The answer is always relative to the tabular tdim of the set, i.e.
        the full shape after broadcasting.

        Parameters
        ----------
        key : str
            element of set

        Returns
        -------
        axis : int or None
            Axis number, or None if key changes along more than one axis.
        xdata : dict
            N, int, length of axis
            sign, +1/-1, indicates ascending or descending order
            beg, end, first and last value of the axis
        """
        isaxis = np.logical_not(self.degeneracy(key))
        if np.sum(isaxis) != 1:
            return None, {}
        ax_dim = np.nonzero(isaxis)[0][0]
        # plus a little useful intel
        N = self.ts.tshape[ax_dim]
        axis = self[key]
        beg = axis.ravel()[0]
        end = axis.ravel()[-1]
        sign = np.sign(end - beg)
        xdata = dict(N=N, sign=sign, beg=beg, end=end)
        return ax_dim, xdata


def _survey_view(args, kwargs):
    """find the most popular view of TablArrays in args and kwargs"""
    views = ['table', 'bcast', 'cell', 'array']
    idx = dict(zip(views, range(4)))
    counts = np.zeros(4, dtype=int)
    for arg in args:
        if misc.istablarray(arg):
            view = arg.view
            counts[idx[view]] += 1
    for _, arg in kwargs.items():
        if misc.istablarray(arg):
            view = arg.view
            counts[idx[view]] += 1
    print('counts %s' % counts)
    popular_idx = np.argsort(counts)[-1]
    return views[popular_idx]
