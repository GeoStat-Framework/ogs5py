'''
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
PQC - Phreqqc coupling (not supported)
REI - Reaction Interface
RFD - definition of time-curves for variing BCs or STs
ST  - Source Term
TIM - Time settings
'''

from __future__ import absolute_import

from ogs5py.ogs import (
    OGS,
    search_task_id,
)
from ogs5py.fileclasses import (
    BC,
    CCT,
    FCT,
    GEM,
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
    REI,
    RFD,
    ST,
    TIM,
)
from ogs5py.tools._types import (
    PCS_TYP,
    PRIM_VAR_BY_PCS,
)
# from ogs5py.reader import (readvtk,
#                            readpvd,
#                            readtec_point,
#                            readtec_polyline)

__version__ = '0.2.0'

__all__ = [
    "BC",
    "CCT",
    "FCT",
    "GEM",
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
    "REI",
    "RFD",
    "ST",
    "TIM",
]
__all__ += [
    "OGS",
    "search_task_id",
]
__all__ += [
    "PCS_TYP",
    "PRIM_VAR_BY_PCS",
]
# __all__ += ["readvtk", "readpvd", "readtec_point", "readtec_polyline"]
