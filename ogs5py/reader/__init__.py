"""
ogs5py-read Python Package


Get help on each function by typing
>>> import ogs5py-read
>>> help(ogs5py-read.function)


Copyright 2017 Sebastian Mueller


History
 -------
Written,  SM, 2017
"""
from __future__ import absolute_import

from ogs5py.reader.reader import readvtk, readpvd, readtec_point, readtec_polyline

__all__ = ["readvtk", "readpvd", "readtec_point", "readtec_polyline"]
