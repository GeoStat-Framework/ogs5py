# -*- coding: utf-8 -*-
"""
Class for the ogs GEOMETRY file.

.. currentmodule:: ogs5py.fileclasses.gli

File Classes
^^^^^^^^^^^^

.. autosummary::
   GLI
   GLIext

Generator
^^^^^^^^^

.. autosummary::
   rectengular
   radial

----
"""
from __future__ import absolute_import

from ogs5py.fileclasses.gli.core import GLI, GLIext
from ogs5py.fileclasses.gli.generator import rectengular, radial

__all__ = ["GLI", "GLIext"]
__all__ += ["rectengular", "radial"]
