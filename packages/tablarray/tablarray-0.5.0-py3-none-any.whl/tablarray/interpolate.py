#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 19:22:31 2023

@author: chris
"""

from scipy import interpolate as _interp

import tablarray as ta
from . import misc


def _1d_bivariate_argparse(*args1):
    if len(args1) >= 2 and misc.istablaset(args1[0]):
        args1, _ = misc._unpack_from_tablaset(*args1)
    # make sure x, y, have 1d, and flatten them
    
    # return x, y, z, args


def wrap_BivariateSpline(spline):
    class TA_BivariateSpline():
        def __init__(self, *args, **kwargs):
            x, y, z, args2 = _1d_bivariate_argparse(*args)
            cshape0 = z.cshape
            z_flat = z.cell.ravel()
            splines = []
            for j in z_flat.cell.size:
                z_j = z.cell[j].base  # naw, that's not right
                newspline = spline(x.base, y.base, z_j, *args2, **kwargs)
                splines.append(newspline)
            self._splines = splines
            self._cshape0 = cshape0

        def ev(self, xi, yi, *args, **kwargs):
            z_accum = []
            for spline in self._splines:
                z_j = spline.ev(xi.base, yi.base, *args, **kwargs)
                z_accum.append(z_j.cell)
            zi = ta.stack_bcast(tuple(z_accum), axis=-1)
            return zi.reshape(self._cshape0)
    return TA_BivariateSpline


RectBivariateSpline = wrap_BivariateSpline(_interp.RectBivariateSpline)
SmoothBivariateSpline = wrap_BivariateSpline(_interp.SmoothBivariateSpline)
SmoothSphereBivariateSpline = wrap_BivariateSpline(_interp.SmoothSphereBivariateSpline)


def griddata(X, Y, Xi):
    pass
