# -*- coding: utf-8 -*-
"""
ogs5py subpackage providing the file classes

.. currentmodule:: ogs5py.fileclasses

Subpackages
^^^^^^^^^^^

.. autosummary::
   base
   gli
   msh

File Classes
^^^^^^^^^^^^
Classes for all OGS5 Files

.. autosummary::
   asc.ASC
   bc.BC
   cct.CCT
   ddc.DDC
   fct.FCT
   gem.GEM
   gem.GEMinit
   gli.GLI
   gli.GLIext
   ic.IC
   ic.RFR
   krc.KRC
   mcp.MCP
   mfp.MFP
   mmp.MMP
   mpd.MPD
   msh.MSH
   msp.MSP
   num.NUM
   out.OUT
   pcs.PCS
   pct.PCT
   pqc.PQC
   pqc.PQCdat
   rei.REI
   rfd.RFD
   st.ST
   tim.TIM

----
"""
from __future__ import absolute_import

from ogs5py.fileclasses.asc import ASC
from ogs5py.fileclasses.bc import BC
from ogs5py.fileclasses.cct import CCT
from ogs5py.fileclasses.ddc import DDC
from ogs5py.fileclasses.fct import FCT
from ogs5py.fileclasses.gem import GEM
from ogs5py.fileclasses.gem import GEMinit
from ogs5py.fileclasses.gli import GLI
from ogs5py.fileclasses.gli import GLIext
from ogs5py.fileclasses.ic import IC
from ogs5py.fileclasses.ic import RFR
from ogs5py.fileclasses.krc import KRC
from ogs5py.fileclasses.mcp import MCP
from ogs5py.fileclasses.mfp import MFP
from ogs5py.fileclasses.mmp import MMP
from ogs5py.fileclasses.mpd import MPD
from ogs5py.fileclasses.msh import MSH
from ogs5py.fileclasses.msp import MSP
from ogs5py.fileclasses.num import NUM
from ogs5py.fileclasses.out import OUT
from ogs5py.fileclasses.pcs import PCS
from ogs5py.fileclasses.pct import PCT
from ogs5py.fileclasses.pqc import PQC
from ogs5py.fileclasses.pqc import PQCdat
from ogs5py.fileclasses.rei import REI
from ogs5py.fileclasses.rfd import RFD
from ogs5py.fileclasses.st import ST
from ogs5py.fileclasses.tim import TIM

__all__ = [
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
