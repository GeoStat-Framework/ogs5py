#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
definition of element-type names and their encoding

List of elements in ogs mesh file: int int char int int int int int int int int

@author: Sebastian Mueller
"""
from __future__ import division, print_function
import sys

# stringtype for python 2 and 3
if sys.version_info[0] == 2:
    _strtype = basestring
else:
    _strtype = str

# all names for element types in ogs 5
elem_names = ["line", "tri", "quad", "tet", "pyra", "pris", "hex"]

# all pcs types supported by ogs 5
pcs_typ = ["",                  # special case for no specified pcs in "*.out"
           "NO_PCS",            # ...used in Benchmarks
           "GROUNDWATER_FLOW",  # HEAD
           "LIQUID_FLOW",       # PRESSURE1
           "RICHARDS_FLOW",     # PRESSURE1
           "AIR_FLOW",          # PRESSURE1 TEMPERATURE1
           "MULTI_PHASE_FLOW",  # PRESSURE1, PRESSURE2
           "PS_GLOBAL",         # PRESSURE1, SATURATION2
           "HEAT_TRANSPORT",    # TEMPERATURE1
           "DEFORMATION",       # DISPLACEMENT_X1, -_Y1, -_Z1
           "MASS_TRANSPORT",    # varying (#COMP_PROP*.mcp 7 CONCENTRATION)
           "OVERLAND_FLOW",     # HEAD
           "FLUID_MOMENTUM",    # VELOCITY1_X, VELOCITY1_Y, VELOCITY1_Z
           "RANDOM_WALK"]       # with particles in *.pct file

# file extensions by pcs type (and the unspecified case "")
pcs_ext = [""]+["_"+pcs for pcs in pcs_typ[1:]]

# coresponding vtk-types by their number encoding
vtk_typ = {3: "line",  # vtk.VTK_LINE == 3
           5: "tri",   # vtk.VTK_TRIANGLE == 5
           9: "quad",  # vtk.VTK_QUAD == 9
           10: "tet",   # vtk.VTK_TETRA == 10
           14: "pyra",  # vtk.VTK_PYRAMID == 14
           13: "pris",  # vtk.VTK_WEDGE == 13
           12: "hex",   # vtk.VTK_HEXAHEDRON == 12
           "line": 3,
           "tri": 5,
           "quad": 9,
           "tet": 10,
           "pyra": 14,
           "pris": 13,
           "hex": 12}

# number of nodes per element-type (sorted by name and number-encoding)
node_no = {0: 2,
           1: 3,
           2: 4,
           3: 4,
           4: 5,
           5: 6,
           6: 8,
           "line": 2,
           "tri": 3,
           "quad": 4,
           "tet": 4,
           "pyra": 5,
           "pris": 6,
           "hex": 8}
