#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  8 15:52:31 2022

@author: chris
"""

import functools
from matplotlib import pyplot
import numpy as np

from . import misc
#from .np2ta import passwrap as pw
from .set import TablaSet


class _MeshfilterArgs():
    def __init__(self, *args, returnbaseonly=True):
        '''
        For each arg which is TablArray type, add it to a temporary TablaSet,
        then extract all such args using TablaSet.meshtile.

        * All args of TablArray-type must be broadcast compatible.
        * Then after the return, the args will be meshed to flesh out
        their mutual broadcast shape.

        Primarily this is useful for calling plots. So, tablarray has duplicate
        plot methods that should look familiar from matplotlib.pyplot, e.g.
        tablarray.contourf and .plot. Those are wrapped with automeshtile,
        making explicit meshing unnecessary for tablarray users.
        '''
        self._returnbaseonly = returnbaseonly
        keys = None
        if len(args) >= 2 and misc.istablaset(args[0]):
            args, keys = misc._unpack_from_tablaset(*args)
            self.keymeaning = True
        self.is_TA = [misc.istablarray(arg) for arg in args]
        n_TA = np.sum(self.is_TA)
        index, = np.nonzero(self.is_TA)
        if keys is None:
            keys = [('a%d') % i for i in index]
            self.keymeaning = False
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

    def args(self):
        # second pass, pull args from the temp_set.meshtile
        for i in self.index:
            key = self.keys[i]
            if self._returnbaseonly:
                arg = self.as_set.meshtile(key).base
            else:
                arg = self.as_set.meshtile(key)
            self._args[i] = arg
        return self._args

    def dim_reduced(self):
        # should the return value be another MeshFilterAargs
        # or same as args?
        if self.n_TA <= 1:
            return False, self
        main = self.keys[self.index[-1]]
        degeneracy = self.as_set.degeneracy(main)
        # 
        keys = []
        slices = [slice(None)] * self.n_TA
        for i in self.index:
            ax, _ = self.as_set.axis_of(self.keys[i])
            if (ax is not None) and degeneracy[ax]:
                print('found a degeneracy at arg %d, ax %d' % (i, ax))
                slices[ax] = 0
            else:
                keys.append(self.keys[i])
        # for each degeneracy, kill off the arg, AND reshape without that dim
        print(tuple(keys + slices))
        reduced_set = self.as_set.bcast.__getitem__(tuple(keys + slices))
        print(reduced_set)
        reduced_mfa = _MeshfilterArgs(reduced_set, *tuple(keys),
                                      returnbaseonly=self._returnbaseonly)
        return reduced_mfa


#=== plots which use TablaSet.meshtile then fall back on ndarray only ===/

def _wrap_automesh(func):
    """
    wrapper that filters args using automeshtile
    """
    @functools.wraps(func)
    def automeshed(*args, **kwargs):
        mfa = _MeshfilterArgs(*args)
        args2 = mfa.args()
        func(*args2, **kwargs)
        # maybe FIXME: consider maybe using mfa.keymeaning or not
    automeshed.__doc__ = (
        "**automeshed TablArray/TablaSet (passthrough)** %s\n\n" % func.__name__
        + "Where inputs are TablArray-compatible and meshing may be\n"
        + "implied as long as the inputs are broadcast-able.\n\n"
        + automeshed.__doc__)
    return automeshed


bar = _wrap_automesh(pyplot.bar)
barbs = _wrap_automesh(pyplot.barbs)
boxplot = _wrap_automesh(pyplot.boxplot)
contour = _wrap_automesh(pyplot.contour)
contourf = _wrap_automesh(pyplot.contourf)
csd = _wrap_automesh(pyplot.csd)
hist = _wrap_automesh(pyplot.hist)
plot = _wrap_automesh(pyplot.plot)
polar = _wrap_automesh(pyplot.polar)
psd = _wrap_automesh(pyplot.psd)
#quiver = _wrap_automesh(pyplot.quiver)
scatter = _wrap_automesh(pyplot.scatter)
#triplot = _wrap_automesh(pyplot.triplot)


#=== plots which use TablArray and TablaSet features ===/

def quiver2d(*args, **kwargs):
    '''
    Plot a 2d field of arrows.

    See matplotlib.quiver, now wrapped for TablArray

    Call signature::

        quiver([X, Y], UV, [C], **kwargs)

    Where X, Y, Z inputs are TablArray-compatible and meshing may be
    implied as long as the inputs are broadcast-able.    

    Parameters
    ----------
    X, Y : TablArray
        arrow base locations
    UV : TablArray
        2d arrow vectors, i.e. cellular shape c(2,)
    C : ndarray or TablArray
        optionally sets the color
    '''
    mfa = _MeshfilterArgs(*args, returnbaseonly=False)
    args = mfa.args()
    if len(args) == 1:
        uv = args[0]
        # factor uv vector for tuple
        u = uv.cell[0]
        v = uv.cell[1]
        args2 = u, v
    elif len(args) == 2:
        uv, c = args
        u = uv.cell[0]
        v = uv.cell[1]
        args2 = u, v, c
    elif len(args) == 3:
        x, y, uv = args
        u = uv.cell[0]
        v = uv.cell[1]
        args2 = x, y, u, v
    elif len(args) == 4:
        x, y, uv, c = args
        u = uv.cell[0]
        v = uv.cell[1]
        args2 = x, y, u, v, c
    else:
        raise ValueError
    pyplot.quiver(*args2, **kwargs)


def quiver3d(*args, **kwargs):
    '''
    Plot a 3d field of arrows.

    Call signature::

        quiver3d([X, Y, Z], UVW, [C], **kwargs)

    See ax.quiver for 3d, esp. kwargs like length

    Where X, Y, Z, UVW are TablArray-compatible and meshing may be
    implied as long as the inputs are broadcast-able.    

    Parameters
    ----------
    X, Y, Z: TablArray
        arrow base locations
    UVW : TablArray
        3d arrow vectors, i.e. cellular shape c(3,)
    C : ndarray or TablArray
        optionally sets the color
    '''
    mfa = _MeshfilterArgs(*args, returnbaseonly=False)
    args = mfa.args()
    if len(args) == 1:
        uvw = args[0]
        # factor uv vector for tuple
        u = uvw.cell[0]
        v = uvw.cell[1]
        w = uvw.cell[2]
        args2 = u, v, w
    elif len(args) == 2:
        uvw, c = args
        u = uvw.cell[0]
        v = uvw.cell[1]
        w = uvw.cell[2]
        args2 = u, v, c
    elif len(args) == 4:
        x, y, z, uvw = args
        u = uvw.cell[0]
        v = uvw.cell[1]
        w = uvw.cell[2]
        args2 = x, y, z, u, v, w
    elif len(args) == 5:
        x, y, z, uvw, c = args
        u = uvw.cell[0]
        v = uvw.cell[1]
        w = uvw.cell[2]
        args2 = x, y, z, u, v, w, c
    else:
        raise ValueError
    fig = pyplot.figure()
    ax = fig.add_subplot(projection='3d')
    ax.quiver(*args2, **kwargs)


def plot3d(*args, **kwargs):
    '''
    plot on 3d projected axes

    Where inputs are TablArray-compatible and meshing may be
    implied as long as the inputs are broadcast-able.    
    '''
    mfa = _MeshfilterArgs(*args, returnbaseonly=False)
    args = mfa.args()
    args2 = []
    for arg in args:
        arg2 = arg.base.ravel() if misc.istablarray(arg) else arg
        args2.append(arg2)
    ax = pyplot.axes(projection='3d')
    ax.plot(*tuple(args2), **kwargs)


def scatter3d(*args, c=None, **kwargs):
    '''
    plot on 3d projected axes

    Where inputs are TablArray-compatible and meshing may be
    implied as long as the inputs are broadcast-able.    
    '''
    if c is not None:
        mfa = _MeshfilterArgs(*args, c, returnbaseonly=False)
        args0 = mfa.args()
        #args0, _ = _automeshtile(*args, c)
        c = args0[-1]
        args = args0[:-1]
    else:
        mfa = _MeshfilterArgs(*args, returnbaseonly=False)
        args = mfa.args()
        #args, _ = _automeshtile(*args)
    args2 = []
    for arg in args:
        arg2 = arg.base.ravel() if misc.istablarray(arg) else arg
        args2.append(arg2)
    ax = pyplot.axes(projection='3d')
    if c is not None:
        kwargs['c'] = c
    img = ax.scatter(*tuple(args2), **kwargs)
    if c is not None:
        fig = pyplot.gcf()
        fig.colorbar(img)


def contour3d_box(*args, cbargs={'pad': 0.1}, **kwargs):
    '''
    Contour plots in 3d, i.e. for (x, y, z, scalar-data), display as a 3d
    box with 2d contours along the 3 forward edge surfaces.

    Where inputs are TablArray-compatible and meshing may be
    implied as long as the inputs are broadcast-able.    

    Note that arrays must be 3dim in cartesian coordinates, and the solid
    must be rectangular.
    '''
    #args, xdata = _automeshtile(*args)
    #tset = xdata['temp_set']
    #keys = xdata['keys']
    mfa = _MeshfilterArgs(*args, returnbaseonly=False)
    args = mfa.args()
    tset = mfa.as_set
    keys = mfa.keys
    x, y, z, data = args[:4]
    # determine slicing
    def _get_sliceat(ax, position):
        ax_dim, xdata = tset.axis_of(keys[ax])
        N = xdata['N']
        sign = xdata['sign']
        if sign > 0:
            i = int(position * (N - 1) + .5)
            mn = xdata['beg']
            mx = xdata['end']
        else:
            i = int((1 - position) * (N - 1) + .5)
            mn = xdata['end']
            mx = xdata['beg']
        slice0 = [slice(None), slice(None), slice(None)]
        slice0[ax_dim] = i
        sliced_set = tset.__getitem__(tuple(keys + slice0))
        x0, y0, z0, data0 = sliced_set.meshtile(*tuple(keys))
        return x0, y0, z0, data0, mn, mx
    # plot args
    d_mn = data.min()
    d_mx = data.max()
    plot_kwargs = dict(
        vmin=d_mn, vmax=d_mx, levels=np.linspace(d_mn, d_mx, 11))
    # do the contour plots
    ax = pyplot.axes(projection='3d')
    x0, y0, _, data0, zmn, zmx = _get_sliceat(2, 1)
    ax.contourf(x0, y0, data0, zdir='z', offset=zmx, **plot_kwargs, **kwargs)
    x0, _, z0, data0, ymn, ymx = _get_sliceat(1, 0)
    ax.contourf(x0, data0, z0, zdir='y', offset=ymn, **plot_kwargs, **kwargs)
    _, y0, z0, data0, xmn, xmx = _get_sliceat(0, 1)
    C = ax.contourf(data0, y0, z0, zdir='x', offset=xmx, **plot_kwargs, **kwargs)
    # plot the edges
    kw_edges = dict(color='0.1', linewidth=1, zorder=1e3)
    ax.plot([xmx, xmx], [ymn, ymx], [zmx, zmx], **kw_edges)
    ax.plot([xmn, xmx], [ymn, ymn], [zmx, zmx], **kw_edges)
    ax.plot([xmx, xmx], [ymn, ymn], [zmn, zmx], **kw_edges)
    # the colorbar
    pyplot.colorbar(C, ax=ax, **cbargs)
