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

Geometric
^^^^^^^^^
Geometric routines

.. autosummary::
   hull_deform

Searching
^^^^^^^^^
Routine to search for a valid ogs id in a directory

.. autosummary::
   search_task_id

Formatting
^^^^^^^^^^
Routines to format/generate data in the right way for the input

.. autosummary::
   by_id
   specialrange
   generate_time

Downloading
^^^^^^^^^^^

.. currentmodule:: ogs5py.tools.download

Routine to download OGS5.

.. autosummary::
   download_ogs
   add_exe
   reset_download
   OGS5PY_CONFIG

Plotting
^^^^^^^^

.. currentmodule:: ogs5py.tools.vtk_viewer

Routine to download OGS5.

.. autosummary::
   show_vtk

Information
^^^^^^^^^^^

.. currentmodule:: ogs5py.tools.types

.. autosummary::
   OGS_EXT
   PCS_TYP
   PRIM_VAR_BY_PCS
"""
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
from ogs5py.tools.tools import (
    search_task_id,
    by_id,
    hull_deform,
    specialrange,
    generate_time,
)
from ogs5py.tools.types import OGS_EXT, PCS_TYP, PRIM_VAR_BY_PCS
from ogs5py.tools.download import (
    download_ogs,
    add_exe,
    reset_download,
    OGS5PY_CONFIG,
)
from ogs5py.tools.vtk_viewer import show_vtk

# indentation of subkeywords
SUB_IND = "  "
"""str: Indentation of subkeys."""
# indentation of content
CON_IND = "   "
"""str: Indentation of content."""

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
__all__ += ["search_task_id", "by_id", "hull_deform"]
__all__ += ["specialrange", "generate_time"]
__all__ += ["download_ogs", "add_exe", "reset_download", "OGS5PY_CONFIG"]
__all__ += ["show_vtk"]
__all__ += ["OGS_EXT", "PCS_TYP", "PRIM_VAR_BY_PCS"]
__all__ += ["SUB_IND", "CON_IND"]
# __all__ += ["readvtk", "readpvd", "readtec_point", "readtec_polyline"]
