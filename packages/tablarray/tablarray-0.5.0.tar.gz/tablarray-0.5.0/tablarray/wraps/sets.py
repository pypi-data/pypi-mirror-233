#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
"""

import numpy as _np

from . import misc


def _unpack_from_tablaset(tset, *args):
    '''
    For args of type str which are in the TablaSet arg tset, get elements out
    of tset.

    Parameters
    ----------
    tset : TablaSet
        a set where some args may be derived
    *args : *tuple
        original args

    Returns
    -------
    args2 : tuple
        new args, same length as args
    keys : list of str
        what the args were named in tset
    '''
    args2 = []
    keys = []
    for arg in args:
        if type(arg) is str and arg in tset:
            args2.append(tset[arg])
            keys.append(arg)
        else:
            args2.append(arg)
    return tuple(args2), keys


class Wraptool_Depend_Independ():
    def __init__(self, *args):
        '''
        Dereferences TablArray vectors.

        Signatures::

            (x, z)
            (x, y, z)
            (x, y, z, t)
            (XY, z)
            (XYZ, t)
            (XYZ, V)
            (x, V)
            (x, y, V)
            (x, y, z, V)
            (tset, 'key1', 'key2', ...)

        Properties
        ----------
        
        '''
        from .set import TablaSet
        self.keymeaning = len(args) >= 2 and misc.istablaset(args[0])
        if self.keymeaning:
            args, keys = _unpack_from_tablaset(*args)
        self._is_TA = [misc.istablarray(arg) for arg in args]
        n_TA = _np.sum(self.is_TA)
        index, = _np.nonzero(self.is_TA)
        if not self.keymeaning:
            keys = [('a%d') % i for i in index]
        # first pass, setup a TablaSet
        self.as_set = TablaSet()
        for i in index:
            arg = args[i]
            key = keys[i]
            self.as_set[key] = arg
        self.keys = keys
        self.xdata = dict(n_TA=n_TA, ind_TA=index)
        self._args = list(args)
        self.index = index
        self.n_TA = n_TA
