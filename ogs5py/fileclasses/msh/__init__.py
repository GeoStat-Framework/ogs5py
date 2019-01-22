# -*- coding: utf-8 -*-
"""
Class for the ogs MESH file.

.. currentmodule:: ogs5py.fileclasses.msh

File Class
^^^^^^^^^^

.. autosummary::
   MSH

Generator
^^^^^^^^^

.. autosummary::
   rectengular
   radial
   grid_adapter2D
   grid_adapter3D
   block_adapter3D
   generate_gmsh

----
"""
from __future__ import absolute_import

from ogs5py.fileclasses.msh.core import MSH
from ogs5py.fileclasses.msh.generator import (
    rectengular,
    radial,
    grid_adapter2D,
    grid_adapter3D,
    block_adapter3D,
    generate_gmsh,
)
__all__ = ["MSH"]
__all__ += [
    "rectengular",
    "radial",
    "grid_adapter2D",
    "grid_adapter3D",
    "block_adapter3D",
    "generate_gmsh",
]
