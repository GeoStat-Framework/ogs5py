# -*- coding: utf-8 -*-
"""
ogs5py subpackage providing reader for the ogs5 output.

.. currentmodule:: ogs5py.reader

Reader
^^^^^^

.. autosummary::
   :toctree:

   readvtk
   readpvd
   readtec_point
   readtec_polyline
   VTK_ERR

----
"""
from ogs5py.reader.reader import (
    VTK_ERR,
    readpvd,
    readtec_point,
    readtec_polyline,
    readvtk,
)

__all__ = [
    "readvtk",
    "readpvd",
    "readtec_point",
    "readtec_polyline",
    "VTK_ERR",
]
