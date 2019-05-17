# -*- coding: utf-8 -*-
"""
ogs5py subpackage providing reader for the ogs5 output

.. currentmodule:: ogs5py.reader

Reader
^^^^^^

.. autosummary::
   readvtk
   readpvd
   readtec_point
   readtec_polyline
   VTK_ERR

----
"""
from __future__ import absolute_import

from ogs5py.reader.reader import (
    readvtk,
    readpvd,
    readtec_point,
    readtec_polyline,
    VTK_ERR,
)

__all__ = [
    "readvtk", "readpvd", "readtec_point", "readtec_polyline", "VTK_ERR"
]
