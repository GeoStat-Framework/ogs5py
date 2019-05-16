# -*- coding: utf-8 -*-
"""
Base Class for an OGS5 run.

.. currentmodule:: ogs5py.ogs

OGS Class
^^^^^^^^^

.. autosummary::
   OGS

----
"""
from __future__ import absolute_import, division, print_function
import os
import shutil
import glob
import sys
import time
import warnings
from copy import deepcopy as dcp
from whichcraft import which
import pexpect
from pexpect.popen_spawn import PopenSpawn
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
    RFR,
    ST,
    TIM,
)
from ogs5py.tools.types import OGS_EXT
from ogs5py.tools.tools import search_task_id, Output
from ogs5py.tools.script import gen_script
from ogs5py.fileclasses.base import TOP_COM, BOT_COM, CWD

# pexpect.spawn just runs on unix-like systems
if sys.platform == "win32":
    OGS_NAME = "ogs.exe"
    CmdRun = PopenSpawn
else:
    OGS_NAME = "ogs"
    CmdRun = pexpect.spawn


class OGS(object):
    """Class for an OGS5 model.

    In this class everything for an OGS5 model can be specified.

    Parameters
    ----------
    task_root : :class:`str`, optional
        Path to the destiny model folder.
        Default: cwd+"ogs5model"
    task_id : :class:`str`, optional
        Name for the ogs task.
        Default: "model"
    output_dir : :class:`str` or :class:`None`, optional
        Path to the output directory.
        Default: :class:`None`

    Notes
    -----
    The following Classes are present as attributes
        bc  : Boundary Condition
            Information of the Boundary Conditions for the model.
        cct : Communication Table
            Information of the Communication Table for the model.
        fct : Function
            Information of the Function definitions for the model.
        gem : geochemical thermodynamic modeling coupling
            Information of the geochemical thermodynamic modeling
            coupling for the model.
        gli : Geometry
            Information of the Geometry for the model.
        ic  : Initial Condition
            Information of the Initial Conditions for the model.
        krc : Kinetric Reaction
            Information of the Kinetric Reaction for the model.
        mcp : reactive components for modelling chemical processes
            Information of the reactive components for
            modelling chemical processes for the model.
        mfp : Fluid Properties
            Information of the Fluid Properties for the model.
        mmp : Medium Properties
            Information of the Medium Properties for the model.
        msh : Mesh
            Information of the Mesh for the model.
        msp : Solid Properties
            Information of the Solid Properties for the model.
        num : Settings for the numerical solver
            Information of the numerical solver for the model.
        out : Output Settings
            Information of the Output Settings for the model.
        pcs : Process settings
            Information of the Process settings for the model.
        pct : Particle Definition for Random walk
            Information of the Particles defined for Randomwalk setting.
        pqc : Phreqqc coupling (not supported yet)
            Information of the Boundary Conditions for the model.
        pqcdat : Phreqqc coupling (the phreeqc.dat file)
            phreeqc.dat file for the model.
            (just a line-wise file with no comfort)
        rei : Reaction Interface
            Information of the Reaction Interface for the model.
        rfd : definition of time-curves for variing BCs or STs
            Information of the time curves for the model.
        st  : Source Term
            Information of the Source Term for the model.
        tim : Time settings
            Information of the Time settings for the model.

    Additional
        mpd : Distributed Properties (list of files)
            Information of the Distributed Properties for the model.
        gli_ext : list for external Geometry definition
            External definition of surfaces (TIN) or polylines (POINT_VECTOR)
        rfr : list of restart files
            RESTART files as defined in the INITIAL_CONDITION
        gem_init : list of GEMS3K input files (lst file)
            given as GEMinit classes
        asc : list of ogs ASC files
            This file type comes either from .tim .pcs or .gem
        copy_files : list of path-strings
            Files that should be copied to the destiny folder.
    """

    def __init__(
        self,
        task_root=os.path.join(CWD, "ogs5model"),
        task_id="model",
        output_dir=None,
    ):
        self._task_root = os.path.normpath(task_root)
        self._task_id = task_id
        self._output_dir = None
        self.output_dir = output_dir

        self.bc = BC(task_root=task_root, task_id=task_id)
        self.cct = CCT(task_root=task_root, task_id=task_id)
        self.ddc = DDC(task_root=task_root, task_id=task_id)
        self.fct = FCT(task_root=task_root, task_id=task_id)
        self.gem = GEM(task_root=task_root, task_id=task_id)
        self.gli = GLI(task_root=task_root, task_id=task_id)
        self.ic = IC(task_root=task_root, task_id=task_id)
        self.krc = KRC(task_root=task_root, task_id=task_id)
        self.mcp = MCP(task_root=task_root, task_id=task_id)
        self.mfp = MFP(task_root=task_root, task_id=task_id)
        self.mmp = MMP(task_root=task_root, task_id=task_id)
        self.msh = MSH(task_root=task_root, task_id=task_id)
        self.msp = MSP(task_root=task_root, task_id=task_id)
        self.num = NUM(task_root=task_root, task_id=task_id)
        self.out = OUT(task_root=task_root, task_id=task_id)
        self.pcs = PCS(task_root=task_root, task_id=task_id)
        self.pct = PCT(task_root=task_root, task_id=task_id)
        self.pqc = PQC(task_root=task_root, task_id=task_id)
        self.pqcdat = PQCdat(task_root=task_root, task_id=task_id)
        self.rei = REI(task_root=task_root, task_id=task_id)
        self.rfd = RFD(task_root=task_root, task_id=task_id)
        self.st = ST(task_root=task_root, task_id=task_id)
        self.tim = TIM(task_root=task_root, task_id=task_id)

        # create a list for mpd files
        self.mpd = []
        # create a list for external Geometry definition (TIN and POINT_VECTOR)
        self.gli_ext = []
        # create a list for RESTART files in the INITIAL_CONDITION
        self.rfr = []
        # create a list for GEMS3K input files (lst file)
        self.gem_init = []
        # create a list for ASC files
        self.asc = []
        # create a list of arbitrary files to be copied (names will be same)
        self.copy_files = []
        # store the Top Comment
        self._top_com = TOP_COM
        # store the Bottom Comment
        self._bot_com = BOT_COM

    @property
    def top_com(self):
        """
        Get and set the top comment for the ogs files.
        """
        return self._top_com

    @top_com.setter
    def top_com(self, value):
        self._top_com = value
        for ext in OGS_EXT:
            # workaround to get access to class-members by name
            getattr(self, ext[1:]).top_com = value

    @property
    def bot_com(self):
        """
        Get and set the bottom comment for the ogs files.
        """
        return self._bot_com

    @bot_com.setter
    def bot_com(self, value):
        self._bot_com = value
        for ext in OGS_EXT:
            # workaround to get access to class-members by name
            getattr(self, ext[1:]).bot_com = value

    @property
    def task_root(self):
        """
        Get and set the task_root path of the ogs model.
        """
        return self._task_root

    @task_root.setter
    def task_root(self, value):
        self._task_root = value
        for ext in OGS_EXT:
            # workaround to get access to class-members by name
            getattr(self, ext[1:]).task_root = value
        for i in range(len(self.mpd)):
            self.mpd[i].task_root = value
        for i in range(len(self.gli_ext)):
            self.gli_ext[i].task_root = value
        for i in range(len(self.rfr)):
            self.rfr[i].task_root = value
        for i in range(len(self.gem_init)):
            self.gem_init[i].task_root = value
        for i in range(len(self.asc)):
            self.asc[i].task_root = value
        self.pqcdat.task_root = value

    @property
    def task_id(self):
        """
        :class:`str`: task_id (name) of the ogs model.
        """
        return self._task_id

    @task_id.setter
    def task_id(self, value):
        for i in range(len(self.asc)):
            self.asc[i].file_name = (
                value + self.asc[i].file_name[len(self._task_id) :]
            )
        self._task_id = value
        for ext in OGS_EXT:
            getattr(self, ext[1:]).task_id = value

    @property
    def output_dir(self):
        """
        :class:`str`: output directory path of the ogs model.
        """
        return self._output_dir

    @output_dir.setter
    def output_dir(self, value):
        if value is None:
            self._output_dir = None
        else:
            self._output_dir = os.path.normpath(value)
            if not os.path.isabs(self._output_dir):
                # if not, put the outputfolder in the task_root
                self._output_dir = os.path.join(
                    os.path.abspath(self.task_root), self._output_dir
                )

    @property
    def has_output_dir(self):
        """
        :class:`bool`: State if the model has a separate output directory.
        """
        return self.output_dir is not None

    def add_copy_file(self, path):
        """
        Method to add an arbitrary file that should be copied.

        The base-name of the file will be keept and it will be copied to
        the task-root when the "write" routine is called.
        """
        if os.path.isfile(path):
            self.copy_files.append(os.path.abspath(path))
        else:
            print("OGS.add_copy_file: given file is not valid: " + str(path))

    def del_copy_file(self, index=None):
        """
        Method to delete a copy-file.

        Parameters
        ----------
        index : int or None, optional
            The index of the copy-file that should be deleted. If None, all
            copy-files are deleted. Default: None
        """
        if index is None:
            self.copy_files = []
        elif -len(self.copy_files) <= index < len(self.copy_files):
            del self.copy_files[index]
        else:
            print("OGS.del_copy_file: given index is not valid.")

    def add_mpd(self, mpd_file):
        """
        Method to add an ogs MEDIUM_PROPERTIES_DISTRIBUTED file to the model.
        This is used for disributed information in the MMP file.

        See ogs5py.MPD for further information
        """
        if isinstance(mpd_file, MPD):
            mpd_file.task_root = self.task_root
            self.mpd.append(mpd_file)

    def del_mpd(self, index=None):
        """
        Method to delete MEDIUM_PROPERTIES_DISTRIBUTED file.

        Parameters
        ----------
        index : int or None, optional
            The index of the mpd-file that should be deleted. If None, all
            mpd-files are deleted. Default: None
        """
        if index is None:
            self.mpd = []
        elif -len(self.mpd) <= index < len(self.mpd):
            del self.mpd[index]
        else:
            print("OGS.del_mpd: given index is not valid.")

    def add_gli_ext(self, gli_ext_file):
        """
        Method to add an external Geometry definition file to the model.
        This is used for TIN definition in SURFACE or POINT_VECTOR definition
        in POLYLINE in the GLI file.

        See ogs5py.GLI for further information
        """
        if isinstance(gli_ext_file, GLIext):
            gli_ext_file.task_root = self.task_root
            self.gli_ext.append(gli_ext_file)

    def del_gli_ext(self, index=None):
        """
        Method to delete external Geometry file.

        Parameters
        ----------
        index : int or None, optional
            The index of the external gli file that should be deleted.
            If None, all external gli files are deleted. Default: None
        """
        if index is None:
            self.gli_ext = []
        elif -len(self.gli_ext) <= index < len(self.gli_ext):
            del self.gli_ext[index]
        else:
            print("OGS.del_gli_ext: given index is not valid.")

    def add_rfr(self, rfr_file):
        """
        Method to add an ogs RESTART file to the model.
        This is used for disributed information in the IC file.

        See ogs5py.IC for further information
        """
        if isinstance(rfr_file, RFR):
            rfr_file.task_root = self.task_root
            self.rfr.append(rfr_file)

    def del_rfr(self, index=None):
        """
        Method to delete RESTART file.

        Parameters
        ----------
        index : int or None, optional
            The index of the RESTART file that should be deleted.
            If None, all RESTART files are deleted. Default: None
        """
        if index is None:
            self.rfr = []
        elif -len(self.rfr) <= index < len(self.rfr):
            del self.rfr[index]
        else:
            print("OGS.del_rfr: given index is not valid.")

    def add_gem_init(self, gem_init_file):
        """
        Method to add a GEMS3K input file.
        This is usually generated by GEM-SELEKTOR.

        See ogs5py.GEM and ogs5py.GEMinit for further information
        """
        if isinstance(gem_init_file, GEMinit):
            gem_init_file.task_root = self.task_root
            self.gem_init.append(gem_init_file)

    def del_gem_init(self, index=None):
        """
        Method to delete GEMS3K input file.

        Parameters
        ----------
        index : int or None, optional
            The index of the GEMS3K file that should be deleted.
            If None, all GEMS3K files are deleted. Default: None
        """
        if index is None:
            self.gem_init = []
        elif -len(self.gem_init) <= index < len(self.gem_init):
            del self.gem_init[index]
        else:
            print("OGS.del_rfr: given index is not valid.")

    def add_asc(self, asc_file):
        """
        Method to add a ASC file.

        See ogs5py.ASC for further information
        """
        if isinstance(asc_file, ASC):
            asc_file.task_root = self.task_root
            self.asc.append(asc_file)

    def del_asc(self, index=None):
        """
        Method to delete a ASC file.

        Parameters
        ----------
        index : int or None, optional
            The index of the ASC file that should be deleted.
            If None, all ASC files are deleted. Default: None
        """
        if index is None:
            self.asc = []
        elif -len(self.asc) <= index < len(self.asc):
            del self.asc[index]
        else:
            print("OGS.del_rfr: given index is not valid.")

    def reset(self):
        """
        Delete every content.
        """
        for ext in OGS_EXT:
            # workaround to get access to class-members by name
            getattr(self, ext[1:]).reset()
        self.pqcdat.reset()
        self.mpd = []
        self.gli_ext = []
        self.rfr = []
        self.gem_init = []
        self.asc = []
        self.copy_files = []

        # reset to initial attributes
        self.task_root = self._task_root
        self.task_id = self._task_id
        self.top_com = self._top_com
        self.bot_com = self._bot_com

    def write_input(self):
        """
        method to call all write_file() methods that are initialized
        """
        for ext in OGS_EXT:
            # workaround to get access to class-members by name
            ogs_file = getattr(self, ext[1:])
            if ogs_file.is_empty and ogs_file.force_writing:
                warnings.warn(
                    self.task_id
                    + ext
                    + ": file is empty, but forced to be written!"
                )
            getattr(self, ext[1:]).write_file()

        self.pqcdat.write_file()

        for mpd_file in self.mpd:
            mpd_file.write_file()

        for gli_ext_file in self.gli_ext:
            gli_ext_file.write_file()

        for rfr_file in self.rfr:
            rfr_file.write_file()

        for gem_init_file in self.gem_init:
            gem_init_file.write_file()

        for asc_file in self.asc:
            asc_file.write_file()

        for copy_file in self.copy_files:
            base = os.path.basename(copy_file)
            shutil.copyfile(copy_file, os.path.join(self.task_root, base))

    def gen_script(
        self,
        script_dir=os.path.join(os.getcwd(), "ogs_script"),
        script_name="model.py",
        ogs_cls_name="model",
        task_root=None,
        task_id=None,
        output_dir=None,
        separate_files=None,
    ):
        """
        Generate a python script for the given model

        Parameters
        ----------
        script_dir : str
            target directory for the script
        script_name : str
            name for the script file (including .py ending)
        ogs_cls_name : str
            name of the model in the script
        task_root : str
            used task_root in the script
        task_id : str
            used task_id in the script
        output_dir : str
            used output_dir in the script
        separate_files : list of str or None
            list of files, that should be written to separate files and
            then loaded from the script

        Notes
        -----
        This will only create BlockFiles from the script. GLI and MSH files
        as well as every other file are stored separately.
        """
        gen_script(
            self,
            script_dir,
            script_name,
            ogs_cls_name,
            task_root,
            task_id,
            output_dir,
            separate_files,
        )

    def load_model(
        self,
        task_root,
        task_id=None,
        use_task_root=False,
        use_task_id=False,
        skip_files=None,
        skip_ext=None,
        encoding=None,
        verbose=False,
        search_ext=None,  # (".pcs"),
    ):
        """
        Load an existing OGS5 model.

        Parameters
        ----------
        task_root : str
            Path to the destiny folder.
        task_id : str or None, optional
            Task ID of the model to load. If None is given, it will be
            determind by the found files. If multiple possible task_ids were
            found, the first one in alphabetic order will be used.
            Default: None
        use_task_root : Bool, optional
            State if the given task_root should be used for this model.
            Default: False
        use_task_id : Bool, optional
            State if the given task_id should be used for this model.
            Default: False
        skip_files : list or None, optional
            List of file-names, that should not be read. Default: None
        skip_ext : list or None, optional
            List of file-extensions, that should not be read. Default: None
        encoding : str or None, optional
            encoding of the given files. If ``None`` is given, the system
            standard is used. Default: ``None``
        verbose : bool, optional
            Print information of the reading process. Default: False
        search_ext : str
            OGS extension that should be searched for. Default: ".pcs"

        Notes
        -----
        This method will search for all known OGS5 file-extensions in the
        given path (task_root).
        Additional files from:

            - GLI (POINT_VECTOR + TIN)
            - MMP (distributed media properties)
            - IC (RESTART)
            - GEM (GEM3SK init file)

        will be read automatically.

        If you get an ``UnicodeDecodeError`` try loading with:

            ``encoding="ISO-8859-15"``
        """
        self.reset()

        if skip_files is None:
            skip_files = []
        if skip_ext is None:
            skip_ext = []
        # search for possible task_ids in the directory
        found_ids = search_task_id(task_root, search_ext)
        if not found_ids:
            raise ValueError(
                "ogs5py.OGS.laod_model - nothing was found at: " + task_root
            )
        if verbose:
            print("ogs5py.OGS.laod_model - found ids: " + str(found_ids))
        # take the first found task_id
        if task_id is None:
            # take the first found task_id
            task_id = found_ids[0]
        # check if the given task_id is found
        elif task_id not in found_ids:
            raise ValueError(
                "ogs5py.OGS.load_model - didn't find given task_id ("
                + task_id
                + ") at: "
                + task_root
            )
        if verbose:
            print("ogs5py.OGS.laod_model - use id: " + task_id)
        # overwrite the task_root
        if use_task_root:
            self.task_root = task_root
        # overwrite the task_id
        if use_task_id:
            self.task_id = task_id

        # iterate over all ogs file-extensions
        for ext in OGS_EXT:
            if verbose:
                print(ext, end=" ")
            # skip certain file extensions if wanted
            if ext in skip_ext or ext[1:] in skip_ext:
                continue
            # search for files with given extension
            files = glob.glob(os.path.join(task_root, task_id + ext))
            # if nothing was found, skip
            if not files:
                continue
            # take the first found file if there are multiple
            fil = files[0]
            # skip file if wanted
            if os.path.basename(fil) in skip_files or fil in skip_files:
                continue
            # workaround to get access to class-members by name
            getattr(self, ext[1:]).read_file(
                fil, encoding=encoding, verbose=verbose
            )

            # append GEOMETRY defnitions
            if ext == ".gli":
                for ply in self.gli.POLYLINES:
                    # POINT_VECTOR definition of a POLYLINE
                    ext_name = ply["POINT_VECTOR"]
                    if ext_name is not None:
                        raw_file_name = os.path.basename(ext_name)
                        f_name, f_ext = os.path.splitext(raw_file_name)
                        ext_file = GLIext(
                            typ="POINT_VECTOR",
                            file_name=f_name,
                            file_ext=f_ext,
                            task_root=self.task_root,
                        )
                        path = os.path.join(task_root, ext_name)
                        ext_file.read_file(path, encoding=encoding)
                        self.gli_ext.append(dcp(ext_file))
                for srf in self.gli.SURFACES:
                    # Triangulation definition of a SURFACE
                    ext_name = srf["TIN"]
                    if ext_name is not None:
                        raw_file_name = os.path.basename(ext_name)
                        f_name, f_ext = os.path.splitext(raw_file_name)
                        ext_file = GLIext(
                            typ="TIN",
                            file_name=f_name,
                            file_ext=f_ext,
                            task_root=self.task_root,
                        )
                        path = os.path.join(task_root, ext_name)
                        ext_file.read_file(path, encoding=encoding)
                        self.gli_ext.append(dcp(ext_file))

            # append MEDIUM_PROPERTIES_DISTRIBUTED defnitions
            if ext == ".mmp":
                for i in range(len(self.mmp.mainkw)):
                    # external PERMEABILITY_DISTRIBUTION
                    if "PERMEABILITY_DISTRIBUTION" in self.mmp.subkw[i]:
                        index = self.mmp.subkw[i].index(
                            "PERMEABILITY_DISTRIBUTION"
                        )
                        ext_name = self.mmp.cont[i][index][0][0]
                        raw_file_name = os.path.basename(ext_name)
                        f_name, f_ext = os.path.splitext(raw_file_name)
                        ext_file = MPD(
                            file_name=f_name,
                            file_ext=f_ext,
                            task_root=self.task_root,
                        )
                        path = os.path.join(task_root, ext_name)
                        ext_file.read_file(path, encoding=encoding)
                        self.mpd.append(dcp(ext_file))
                    # external POROSITY_DISTRIBUTION
                    if "POROSITY_DISTRIBUTION" in self.mmp.subkw[i]:
                        index = self.mmp.subkw[i].index(
                            "POROSITY_DISTRIBUTION"
                        )
                        ext_name = self.mmp.cont[i][index][0][0]
                        raw_file_name = os.path.basename(ext_name)
                        f_name, f_ext = os.path.splitext(raw_file_name)
                        ext_file = MPD(
                            file_name=f_name,
                            file_ext=f_ext,
                            task_root=self.task_root,
                        )
                        path = os.path.join(task_root, ext_name)
                        ext_file.read_file(path, encoding=encoding)
                        self.mpd.append(dcp(ext_file))
                    # external GEOMETRY_AREA
                    if "GEOMETRY_AREA" in self.mmp.subkw[i]:
                        index = self.mmp.subkw[i].index("GEOMETRY_AREA")
                        if self.mmp.cont[i][index][0][0] == "FILE":
                            ext_name = self.mmp.cont[i][index][0][1]
                            raw_file_name = os.path.basename(ext_name)
                            f_name, f_ext = os.path.splitext(raw_file_name)
                            ext_file = MPD(
                                file_name=f_name,
                                file_ext=f_ext,
                                task_root=self.task_root,
                            )
                            path = os.path.join(task_root, ext_name)
                            ext_file.read_file(path, encoding=encoding)
                            self.mpd.append(dcp(ext_file))

            # append GEMS3K init file
            if ext == ".gem":
                for i in range(len(self.gem.mainkw)):
                    if "GEM_INIT_FILE" in self.gem.subkw[i]:
                        index = self.gem.subkw[i].index("GEM_INIT_FILE")
                        ext_name = self.gem.cont[i][index][0][0]
                        ext_file = GEMinit(
                            lst_name=ext_name, task_root=self.task_root
                        )
                        path = os.path.join(task_root, ext_name)
                        ext_file.read_file(path, encoding=encoding)
                        self.gem_init.append(dcp(ext_file))

            # append RESART defnitions
            if ext == ".ic":
                for i in range(len(self.ic.mainkw)):
                    if "DIS_TYPE" in self.ic.subkw[i]:
                        index = self.ic.subkw[i].index("DIS_TYPE")
                        if self.ic.cont[i][index][0][0] != "RESTART":
                            continue
                        ext_name = self.ic.cont[i][index][0][1]
                        raw_file_name = os.path.basename(ext_name)
                        f_name, f_ext = os.path.splitext(raw_file_name)
                        ext_file = RFR(
                            file_name=f_name,
                            file_ext=f_ext,
                            task_root=self.task_root,
                        )
                        path = os.path.join(task_root, ext_name)
                        ext_file.read_file(path, encoding=encoding)
                        self.rfr.append(dcp(ext_file))

            # read phreeqc.dat
            if ext == ".pqc":  # phreeqc.dat or Phreeqc.dat
                pqcfiles = glob.glob(os.path.join(task_root, "*hreeqc.dat"))
                self.pqcdat.read_file(
                    path=pqcfiles[0], encoding=encoding, verbose=verbose
                )

        # load ASC files
        files = glob.glob(os.path.join(task_root, task_id + "*.asc"))
        for fil in files:
            raw_file_name = os.path.basename(fil)
            f_name, f_ext = os.path.splitext(raw_file_name)
            ext_file = ASC(
                file_name=self.task_id + f_name[len(task_id) :],
                task_root=self.task_root,
            )
            path = os.path.join(task_root, fil)
            ext_file.read_file(path, encoding=encoding)
            self.asc.append(dcp(ext_file))

        return True

    def readvtk(self, pcs="ALL", output_dir=None):
        r"""
        Reader for vtk outputfiles of this OGS5 model

        Parameters
        ----------
        pcs : string or None, optional
            specify the PCS type that should be collected
            Possible values are:

                - None/"" (no PCS_TYPE specified in \*.out)
                - "NO_PCS"
                - "GROUNDWATER_FLOW"
                - "LIQUID_FLOW"
                - "RICHARDS_FLOW"
                - "AIR_FLOW"
                - "MULTI_PHASE_FLOW"
                - "PS_GLOBAL"
                - "HEAT_TRANSPORT"
                - "DEFORMATION"
                - "MASS_TRANSPORT"
                - "OVERLAND_FLOW"
                - "FLUID_MOMENTUM"
                - "RANDOM_WALK"

            You can get a list with all known PCS-types by setting PCS="ALL"
            Default : None
        output_dir : :any:'None' or :class:'str', optional
            Sometimes OGS5 doesn't put the output in the right directory.
            You can specify a separate output directory here in this case.
            Default: :any:'None'

        Returns
        -------
        result : dict
            keys are the point names and the items are the data from the
            corresponding files
            if pcs="ALL", the output is a dictionary with the PCS-types as keys
        """
        from ogs5py.reader import readvtk as read

        if output_dir is not None:
            root = output_dir
        elif self.has_output_dir:
            root = self.output_dir
        else:
            root = self.task_root
        return read(task_root=root, task_id=self.task_id, pcs=pcs)

    def readpvd(self, pcs="ALL", output_dir=None):
        r"""
        read the paraview pvd files of this OGS5 model

        All concerned files are converted to a dictionary containing their data

        Parameters
        ----------
        pcs : string or None, optional
            specify the PCS type that should be collected
            Possible values are:

                - None/"" (no PCS_TYPE specified in \*.out)
                - "NO_PCS"
                - "GROUNDWATER_FLOW"
                - "LIQUID_FLOW"
                - "RICHARDS_FLOW"
                - "AIR_FLOW"
                - "MULTI_PHASE_FLOW"
                - "PS_GLOBAL"
                - "HEAT_TRANSPORT"
                - "DEFORMATION"
                - "MASS_TRANSPORT"
                - "OVERLAND_FLOW"
                - "FLUID_MOMENTUM"
                - "RANDOM_WALK"

            You can get a list with all known PCS-types by setting PCS="ALL"
            Default : "ALL"
        output_dir : :any:'None' or :class:'str', optional
            Sometimes OGS5 doesn't put the output in the right directory.
            You can specify a separate output directory here in this case.
            Default: :any:'None'

        Returns
        -------
        result : dict
            keys are the point names and the items are the data from the
            corresponding files
            if pcs="ALL", the output is a dictionary with the PCS-types as keys
        """
        from ogs5py.reader import readpvd as read

        if output_dir is not None:
            root = output_dir
        elif self.has_output_dir:
            root = self.output_dir
        else:
            root = self.task_root
        return read(task_root=root, task_id=self.task_id, pcs=pcs)

    def readtec_point(self, pcs="ALL", output_dir=None):
        r"""
        collect TECPLOT point output from this OGS5 model

        Parameters
        ----------
        pcs : string or None, optional
            specify the PCS type that should be collected
            Possible values are:

                - None/"" (no PCS_TYPE specified in \*.out)
                - "NO_PCS"
                - "GROUNDWATER_FLOW"
                - "LIQUID_FLOW"
                - "RICHARDS_FLOW"
                - "AIR_FLOW"
                - "MULTI_PHASE_FLOW"
                - "PS_GLOBAL"
                - "HEAT_TRANSPORT"
                - "DEFORMATION"
                - "MASS_TRANSPORT"
                - "OVERLAND_FLOW"
                - "FLUID_MOMENTUM"
                - "RANDOM_WALK"

            You can get a list with all known PCS-types by setting PCS="ALL"
            Default : "ALL"
        output_dir : :any:'None' or :class:'str', optional
            Sometimes OGS5 doesn't put the output in the right directory.
            You can specify a separate output directory here in this case.
            Default: :any:'None'

        Returns
        -------
        result : dict
            keys are the point names and the items are the data from the
            corresponding files
            if pcs="ALL", the output is a dictionary with the PCS-types as keys
        """
        from ogs5py.reader import readtec_point as read

        if output_dir is not None:
            root = output_dir
        elif self.has_output_dir:
            root = self.output_dir
        else:
            root = self.task_root
        return read(task_root=root, task_id=self.task_id, pcs=pcs)

    def readtec_polyline(self, pcs="ALL", trim=True, output_dir=None):
        r"""
        collect TECPLOT polyline output from this OGS5 model

        Parameters
        ----------
        pcs : string or None, optional
            specify the PCS type that should be collected
            Possible values are:

                - None/"" (no PCS_TYPE specified in \*.out)
                - "NO_PCS"
                - "GROUNDWATER_FLOW"
                - "LIQUID_FLOW"
                - "RICHARDS_FLOW"
                - "AIR_FLOW"
                - "MULTI_PHASE_FLOW"
                - "PS_GLOBAL"
                - "HEAT_TRANSPORT"
                - "DEFORMATION"
                - "MASS_TRANSPORT"
                - "OVERLAND_FLOW"
                - "FLUID_MOMENTUM"
                - "RANDOM_WALK"

            You can get a list with all known PCS-types by setting pcs="ALL"
            Default : "ALL"
        output_dir : :any:'None' or :class:'str', optional
            Sometimes OGS5 doesn't put the output in the right directory.
            You can specify a separate output directory here in this case.
            Default: :any:'None'
        trim : Bool, optional
            if the ply_ids are not continuous, there will be "None" values in
            the output list. If trim is "True" these values will be eliminated.
            If there is just one output for a polyline, the list will
            be eliminated and the output will be the single dict.
            Default : True

        Returns
        -------
        result : dict
            keys are the Polyline names and the items are lists sorted by the
            ply_id (it is assumed, that the ply_ids are continuous, if not, the
            corresponding list entries are "None")
            if pcs="ALL", the output is a dictionary with the PCS-types as keys
        """
        from ogs5py.reader import readtec_polyline as read

        if output_dir is not None:
            root = output_dir
        elif self.has_output_dir:
            root = self.output_dir
        else:
            root = self.task_root
        return read(task_root=root, task_id=self.task_id, pcs=pcs, trim=trim)

    def run_model(
        self,
        ogs_root=None,
        ogs_name=OGS_NAME,
        print_log=True,
        save_log=True,
        log_path=None,
        log_name=None,
        timeout=None,
    ):
        """
        Run the defined OGS5 model.

        Parameters
        ----------
        ogs_root : str or None, optional
            path to the ogs executable. If ``None`` is given, the default sys
            path will be searched with ``which``. Default: None
        ogs_name : str or None, optional
            Name of to the ogs executable to search for.
            Just used if ,ogs_root is ``None``. Default: ``"ogs"``
        print_log : bool, optional
            state if the ogs output should be displayed in the terminal.
            Default: True
        save_log : bool, optional
            state if the ogs output should be saved to a file.
            Default: True
        log_path : str or None, optional
            Path, where the log file should be saved. Default: None
            (the defined output directory or the task_root directory)
        log_name : str or None, optional
            Name of the log file. Default: None
            (task_id+time+"_log.txt")
        timeout : int or None, optional
            Time to wait for OGS5 to finish in seconds. Default: None

        Returns
        -------
        success : bool
            State if OGS5 returned, that it terminated 'normally'.
        """
        # look for the standard ogs executable in the standard-path
        if ogs_root is None:
            check_ogs = which(ogs_name)
            if check_ogs is None:
                print(
                    "Please put the ogs executable in the default sys path: "
                    + str(os.defpath.split(os.pathsep))
                )
                print("Or provide the path to your executable")
                return False
            ogs_root = check_ogs
        else:
            if sys.platform == "win32" and ogs_root[-4:] == ".lnk":
                print("Don't use file links under windows...")
                return False
            if os.path.islink(ogs_root):
                ogs_root = os.path.realpath(ogs_root)
            if os.path.exists(ogs_root):
                if not os.path.isfile(ogs_root):
                    ogs_root = os.path.join(ogs_root, ogs_name)
            else:
                print("The given ogs_root does not exist...")
                return False
        # use absolute path since we change the cwd in the ogs call
        ogs_root = os.path.abspath(ogs_root)

        # create the command to call ogs
        args = [ogs_root, self.task_id]
        # add optional output directory
        # check if output directory is an absolute path with os.path.isabs
        # otherwise set it in the task_root directory
        if self.has_output_dir:
            # format the outputdir
            output_dir = os.path.normpath(self.output_dir)
            # check if outputdir is given as absolut path
            if not os.path.isabs(output_dir):
                # if not, put the outputfolder in the task_root
                output_dir = os.path.join(
                    os.path.abspath(self.task_root), output_dir
                )
            # create the outputdir
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            # append the outputdir to the ogs-command
            args.append("--output-directory")
            args.append(output_dir)
        else:
            output_dir = os.path.abspath(self.task_root)

        # prevent eraising files...
        if not save_log:
            log_name = None

        # set standard log_name
        if log_name is None:
            log_name = (
                self.task_id
                + "_"
                + time.strftime("%Y-%m-%d_%H-%M-%S")
                + "_log.txt"
            )
        # put the logfile in the defined output-dir
        if log_path is None:
            log_path = output_dir
        log = os.path.join(log_path, log_name)

        # create a splitted output stream (to file and stdout)
        out = Output(log, print_log=print_log)
        # call ogs with pexpect
        child = CmdRun(
            " ".join(args),
            timeout=timeout,
            logfile=out,
            cwd=os.path.abspath(self.task_root),
        )
        # wait for ogs to finish
        child.expect(pexpect.EOF)
        # close the output stream
        out.close()

        success = "Simulation time" in out.last_line

        if not save_log:
            os.remove(log)

        return success
