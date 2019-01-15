# -*- coding: utf-8 -*-
"""
definition of element-type names and their encoding

List of elements in ogs mesh file: int int char int int int int int int int int

@author: Sebastian Mueller
"""
from __future__ import division, print_function, absolute_import
import sys
import numpy as np

# stringtype for python 2 and 3
if sys.version_info[0] == 2:
    STRTYPE = basestring
else:
    STRTYPE = str

# keylists for the gli entries and templates for entries
EMPTY_GLI = {
    "points": None,
    "point_names": None,
    "point_md": None,
    "polylines": [],
    "surfaces": [],
    "volumes": [],
}
GLI_KEY_LIST = ["#POINTS", "#POLYLINE", "#SURFACE", "#VOLUME", "#STOP"]
# https://github.com/ufz/ogs5/blob/e704a791391a233084c3d74e1335f50206c5eb76/GEO/geo_ply.cpp#L577
PLY_KEY_LIST = [
    "ID",  # int
    "NAME",  # str
    "TYPE",  # int
    "EPSILON",  # float
    "MAT_GROUP",  # int
    "POINTS",  # list
    "POINT_VECTOR",  # str
]
PLY_TYPES = [int, str, int, float, int, list, str]
# https://github.com/ufz/ogs5/blob/e704a791391a233084c3d74e1335f50206c5eb76/GEO/geo_sfc.cpp#L996
SRF_KEY_LIST = [
    "ID",  # int
    "NAME",  # str
    "EPSILON",  # float
    "TYPE",  # int
    "TIN",  # str
    "MAT_GROUP",  # int
    "POLYLINES",  # list
]
SRF_TYPES = [int, str, float, int, str, int, list]
# https://github.com/ufz/ogs5/blob/e704a791391a233084c3d74e1335f50206c5eb76/GEO/geo_vol.cpp#L130
VOL_KEY_LIST = [
    "NAME",  # str
    "TYPE",  # str
    "SURFACES",  # list
    "MAT_GROUP",  # str
    "LAYER",  # int
]
VOL_TYPES = [str, str, list, str, int]
EMPTY_PLY = {}
for key in PLY_KEY_LIST:
    EMPTY_PLY[key] = None
EMPTY_SRF = {}
for key in SRF_KEY_LIST:
    EMPTY_SRF[key] = None
EMPTY_VOL = {}
for key in VOL_KEY_LIST:
    EMPTY_VOL[key] = None
# keys for the gli-dict
GLI_KEYS = {
    "points",
    "point_names",
    "point_md",
    "polylines",
    "surfaces",
    "volumes",
}
PLY_KEYS = {
    "ID",
    "NAME",
    "POINTS",
    "EPSILON",
    "TYPE",
    "MAT_GROUP",
    "POINT_VECTOR",
}
SRF_KEYS = {"ID", "NAME", "POLYLINES", "EPSILON", "TYPE", "MAT_GROUP", "TIN"}
VOL_KEYS = {"NAME", "SURFACES", "TYPE", "MAT_GROUP", "LAYER"}
# names sorted by dimensionality
ELEM_1D = ["line"]
ELEM_2D = ["tri", "quad"]
ELEM_3D = ["tet", "pyra", "pris", "hex"]
# names sorted by dim
ELEM_DIM = [ELEM_1D, ELEM_2D, ELEM_3D]
# all names for element types in ogs 5
ELEM_NAMES = ELEM_1D + ELEM_2D + ELEM_3D
# keys for the mesh-dict
MESH_KEYS = {"mesh_data", "nodes", "elements", "material_id", "element_id"}
MESH_DATA_KEYS = {
    "AXISYMMETRY",
    "CROSS_SECTION",
    "PCS_TYPE",
    "GEO_TYPE",
    "GEO_NAME",
    "LAYER",
}
ELEMENT_KEYS = set(ELEM_NAMES)
EMPTY_MSH = {
    "mesh_data": {},
    "nodes": np.empty((0, 3)),
    "elements": {},
    "element_id": {},
    "material_id": {},
}
# coresponding names for types in meshio
MESHIO_NAMES = [
    "line",
    "triangle",
    "quad",
    "tetra",
    "pyramid",
    "wedge",
    "hexahedron",
]
# number encoding for element types (obsolete)
ELEM_TYP = {
    0: "line",
    1: "tri",
    2: "quad",
    3: "tet",
    4: "pyra",
    5: "pris",
    6: "hex",
    "line": 0,
    "tri": 1,
    "quad": 2,
    "tet": 3,
    "pyra": 4,
    "pris": 5,
    "hex": 6,
}
# number encoding sorted by dimensionality
ELEM_TYP1D = {0: "line", "line": 0}
ELEM_TYP2D = {1: "tri", 2: "quad", "tri": 1, "quad": 2}
ELEM_TYP3D = {
    3: "tet",
    4: "pyra",
    5: "pris",
    6: "hex",
    "tet": 3,
    "pyra": 4,
    "pris": 5,
    "hex": 6,
}
# coresponding vtk-types by their number encoding
VTK_TYP = {
    3: "line",  # vtk.VTK_LINE == 3
    5: "tri",  # vtk.VTK_TRIANGLE == 5
    9: "quad",  # vtk.VTK_QUAD == 9
    10: "tet",  # vtk.VTK_TETRA == 10
    14: "pyra",  # vtk.VTK_PYRAMID == 14
    13: "pris",  # vtk.VTK_WEDGE == 13
    12: "hex",  # vtk.VTK_HEXAHEDRON == 12
    "line": 3,
    "tri": 5,
    "quad": 9,
    "tet": 10,
    "pyra": 14,
    "pris": 13,
    "hex": 12,
}
# number of nodes per element-type (sorted by name and number-encoding)
NODE_NO = {
    0: 2,
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
    "hex": 8,
}
# all pcs types supported by OGS5
# https://ogs5-keywords.netlify.com/ogs/wiki/public/doc-auto/by_ext/pcs/s_pcs_type
PCS_TYP = [
    "",  # special case for no specified pcs in "*.out"
    "GROUNDWATER_FLOW",  # HEAD
    "LIQUID_FLOW",  # PRESSURE1
    "RICHARDS_FLOW",  # PRESSURE1
    "AIR_FLOW",  # PRESSURE1 TEMPERATURE1
    "MULTI_PHASE_FLOW",  # PRESSURE1, PRESSURE2
    "PS_GLOBAL",  # PRESSURE1, SATURATION2
    "HEAT_TRANSPORT",  # TEMPERATURE1
    "DEFORMATION",  # DISPLACEMENT_X1, -_Y1, -_Z1
    "MASS_TRANSPORT",  # varying (#COMP_PROP*.mcp 7 CONCENTRATION)
    "OVERLAND_FLOW",  # HEAD
    "FLUID_MOMENTUM",  # VELOCITY1_X, VELOCITY1_Y, VELOCITY1_Z
    "RANDOM_WALK",  # with particles in *.pct file
    "NO_PCS",  # ...used in Benchmarks
    "TNEQ",  # ...used in Benchmarks
    "TES",  # ...used in Benchmarks
    "DEFORMATION_SINGLEFLOW_MONO",  # ...used in Benchmarks
    "MULTI_COMPONENTIAL_FLOW",  # ...used in Benchmarks
]
# file extensions by pcs type (and the unspecified case "")
PCS_EXT = [""] + ["_" + pcs for pcs in PCS_TYP[1:]]
# all PRIMARY_VARIABLE types supported by OGS5 (sorted by PCS_TYP)
PRIM_VAR = [
    [""],
    ["HEAD"],
    ["PRESSURE1"],
    ["PRESSURE1"],
    ["PRESSURE1", "TEMPERATURE1"],
    ["PRESSURE1", "PRESSURE2"],
    ["PRESSURE1, SATURATION2"],
    ["TEMPERATURE1"],
    ["DISPLACEMENT_X1", "DISPLACEMENT_Y1", "DISPLACEMENT_Z1"],
    [""],  # varying (#COMP_PROP*.mcp 7 CONCENTRATION)
    ["HEAD"],
    ["VELOCITY1_X", "VELOCITY1_Y", "VELOCITY1_Z"],
    [""],  # with particles in *.pct file
    [""],
    [""],
    [""],
    [""],
    [""],
]
PRIM_VAR_BY_PCS = {}
for i, pcs in enumerate(PCS_TYP):
    PRIM_VAR_BY_PCS[pcs] = PRIM_VAR[i]
# file extensions of ogs5 input files (without mpd, gli_ext, rfr files)
OGS_EXT = [
    ".bc",  # Boundary Condition
    ".cct",  # Communication Table
    ".ddc",  # MPI domain decomposition
    ".fct",  # Function
    ".gem",  # geochemical thermodynamic modeling coupling
    ".gli",  # Geometry
    ".ic",  # Initial Condition
    ".krc",  # Kinetric Reaction
    ".mcp",  # reactive components for modelling chemical processes
    ".mfp",  # Fluid Properties
    ".mmp",  # Medium Properties
    ".msh",  # Mesh
    ".msp",  # Solid Properties
    ".num",  # Settings for the numerical solver
    ".out",  # Output Settings
    ".pcs",  # Process settings
    ".pct",  # Particle Definition for RANDOM_WALK
    ".pqc",  # Phreqqc coupling
    ".rei",  # Reaction Interface
    ".rfd",  # definition of time-curves for variing BCs or STs
    ".st",  # Source Term
    ".tim",  # Time settings
]
