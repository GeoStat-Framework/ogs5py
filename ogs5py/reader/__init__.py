"""
ogs5py.reader
-------------

ogs5py subpackage to read the OGS5 output.

Get help on each function by typing
>>> import ogs5py.reader
>>> help(ogs5py.reader.function)


Copyright 2017 Sebastian Mueller


History
 -------
Written,  SM, 2017
"""
from __future__ import absolute_import

from ogs5py.reader.reader import (
    readvtk,
    readpvd,
    readtec_point,
    readtec_polyline,
)

__all__ = ["readvtk", "readpvd", "readtec_point", "readtec_polyline"]
