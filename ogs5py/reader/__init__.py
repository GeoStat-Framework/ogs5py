"""
ogs5py.reader
-------------

ogs5py subpackage to read the OGS5 output.
"""
from __future__ import absolute_import

from ogs5py.reader.reader import (
    readvtk,
    readpvd,
    readtec_point,
    readtec_polyline,
)

__all__ = ["readvtk", "readpvd", "readtec_point", "readtec_polyline"]
