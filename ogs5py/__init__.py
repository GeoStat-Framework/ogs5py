# -*- coding: utf-8 -*-
"""
Purpose
=======

ogs5py is A python-API for the OpenGeoSys 5 scientific modeling package.

The following functionalities are directly provided on module-level.

Subpackages
===========

.. autosummary::
    fileclasses
    reader
    tools

Classes
=======

OGS model Base Class
^^^^^^^^^^^^^^^^^^^^
Class to setup an ogs model

.. currentmodule:: ogs5py.ogs

.. autosummary::
   OGS

File Classes
^^^^^^^^^^^^
Classes for all OGS5 Files. See: :any:`ogs5py.fileclasses`

.. currentmodule:: ogs5py.fileclasses

.. autosummary::

   ASC
   BC
   CCT
   DDC
   FCT
   GEM
   GEMinit
   GLI
   GLIext
   IC
   RFR
   KRC
   MCP
   MFP
   MMP
   MPD
   MSH
   MSP
   NUM
   OUT
   PCS
   PCT
   PQC
   PQCdat
   REI
   RFD
   ST
   TIM

Functions
=========

.. currentmodule:: ogs5py.tools.tools

Searching
^^^^^^^^^
Routine to search for a valid ogs id in a directory

.. autosummary::
   search_task_id

Formatting
^^^^^^^^^^
Routines to format data in the right way for the input

.. autosummary::
   by_id
"""
from __future__ import absolute_import

from ogs5py._version import __version__
from ogs5py.ogs import OGS
from ogs5py.fileclasses import (
    ASC,
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
from ogs5py.tools.tools import search_task_id, by_id
from ogs5py.tools.types import OGS_EXT, PCS_TYP, PRIM_VAR_BY_PCS

# from ogs5py.reader import (readvtk,
#                            readpvd,
#                            readtec_point,
#                            readtec_polyline)
# indentation of subkeywords
SUB_IND = "  "
# indentation of content
CON_IND = "   "

__all__ = ["__version__"]
__all__ += ["OGS"]
__all__ += [
    "ASC",
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
__all__ += ["search_task_id", "by_id"]
__all__ += ["OGS_EXT", "PCS_TYP", "PRIM_VAR_BY_PCS"]
__all__ += ["SUB_IND", "CON_IND"]
# __all__ += ["readvtk", "readpvd", "readtec_point", "readtec_polyline"]
