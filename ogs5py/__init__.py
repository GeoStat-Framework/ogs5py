"""
ogs5py Python Package

Get help on each function by typing

>>> import ogs5py
>>> help(ogs5py.function)

BC  - Boundary Condition
CCT - Communication Table
FCT - Function
GEM - geochemical thermodynamic modeling coupling
GLI - Geometry
IC  - Initial Condition
KRC - Kinetric Reaction
MCP - reactive components for modelling chemical processes
MFP - Fluid Properties
MMP - Medium Properties
MPD - Distributed Properties
MSH - Mesh
MSP - Solid Properties
NUM - Settings for the numerical solver
OUT - Output Settings
PCS - Process settings
PQC - Phreqqc coupling (just a line-wise file with no comfort)
REI - Reaction Interface
RFD - definition of time-curves for variing BCs or STs
ST  - Source Term
TIM - Time settings
"""

from __future__ import absolute_import

from ogs5py.ogs import OGS
from ogs5py.fileclasses import (
    BC,
    CCT,
    DDC,
    FCT,
    GEM,
    GEMinit,
    GLI,
    GLIext,
    IC,
    RFR,
    KRC,
    MCP,
    MFP,
    MMP,
    MPD,
    MSH,
    MSP,
    NUM,
    OUT,
    PCS,
    PCT,
    PQC,
    PQCdat,
    REI,
    RFD,
    ST,
    TIM,
)
from ogs5py.tools.tools import search_task_id
from ogs5py.tools._types import OGS_EXT, PCS_TYP, PRIM_VAR_BY_PCS

# from ogs5py.reader import (readvtk,
#                            readpvd,
#                            readtec_point,
#                            readtec_polyline)
# indentation of subkeywords
SUB_IND = "  "
# indentation of content
CON_IND = "   "

__version__ = "0.3.0"

__all__ = ["OGS"]
__all__ += [
    "BC",
    "CCT",
    "DDC",
    "FCT",
    "GEM",
    "GEMinit",
    "GLI",
    "GLIext",
    "IC",
    "RFR",
    "KRC",
    "MCP",
    "MFP",
    "MMP",
    "MPD",
    "MSH",
    "MSP",
    "NUM",
    "OUT",
    "PCS",
    "PCT",
    "PQC",
    "PQCdat",
    "REI",
    "RFD",
    "ST",
    "TIM",
]
__all__ += ["search_task_id"]
__all__ += ["OGS_EXT", "PCS_TYP", "PRIM_VAR_BY_PCS"]
__all__ += ["SUB_IND", "CON_IND"]
# __all__ += ["readvtk", "readpvd", "readtec_point", "readtec_polyline"]
