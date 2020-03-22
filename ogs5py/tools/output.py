# -*- coding: utf-8 -*-
"""Tools for ogs5py output files (independent from VTK package)."""
import os
import glob
import re
import xml.etree.ElementTree as ET
import numpy as np
from ogs5py.tools.types import PCS_TYP


###############################################################################
# retrieve infos from ogs-filenames
###############################################################################


def split_pnt_path(
    infile,
    task_id=None,
    pnt_name=None,
    PCS_name=None,
    split_extra=False,
    guess_PCS=False,
):
    """
    Retrive ogs-infos from filename for tecplot-polyline output.

    {id}_time_{pnt}[_{PCS+extra}].tec
    """
    # create a workaround for empty PCS string (which is valid)
    if PCS_name == "":
        temp_id, temp_pnt, temp_PCS, __ = split_pnt_path(
            infile=infile,
            task_id=task_id,
            pnt_name=None,
            PCS_name=None,
            split_extra=False,
            guess_PCS=False,
        )
        if temp_id is None:
            return 4 * (None,)
        endstring = temp_pnt + temp_PCS
        PCS = ""
        if pnt_name is None:
            if split_extra:
                # here we have to guess the POINT name and maybe an extra suf
                # POINT name is guessed as a name without "_"
                # the rest will be set as extra
                split_pnt = endstring.find("_")
                if split_pnt > -1:
                    pnt = endstring[: endstring.find("_")]
                    extra = endstring[endstring.find("_") + 1 :]
                else:
                    pnt = endstring
                    extra = ""
            else:
                pnt = endstring
                extra = ""
        else:
            if endstring.startswith(pnt_name):
                pnt = pnt_name
                extra = endstring[len(pnt) :]
                if not split_extra and extra != "":
                    return 4 * (None,)
        return temp_id, pnt, PCS, extra

    # remove the directory-part from the filepath to get the basename
    name = os.path.basename(infile)
    # search for the suffix (aka file ending)
    suffix_pat = re.compile(r"\.tec$")
    suffix_match = suffix_pat.search(name)
    # check for the task_id
    if task_id is None:
        prefix_pat = re.compile("_time_")
        prefix_match = prefix_pat.search(name)
        if prefix_match is None:
            return 4 * (None,)
        id_name = name[: prefix_match.span()[0]]
    else:
        prefix_pat = re.compile("^" + re.escape(task_id) + "_time_")
        id_name = task_id
    prefix_match = prefix_pat.search(name)
    if prefix_match is None:
        return 4 * (None,)

    if pnt_name is not None:
        midtrm_pat = re.compile(
            "^"
            + re.escape(id_name)
            + "_time_"
            + re.escape(pnt_name)
            + r"+[\._]"
        )
        midtrm_match = midtrm_pat.search(name)
        if midtrm_match is None:
            return 4 * (None,)
        PCS = name[midtrm_match.span()[1] : suffix_match.span()[0]]
        # check PCS
        if PCS_name is None:
            pcs_found = False
            for pcs_sgl in PCS_TYP[1:]:
                if PCS.startswith(pcs_sgl):
                    pcs_found = True
                    extra = PCS[len(pcs_sgl) :]
                    PCS = pcs_sgl
                    break
            if not pcs_found:
                extra = ""
        else:
            if PCS.startswith(PCS_name):
                extra = PCS[len(PCS_name) :]
                PCS = PCS_name
                if not split_extra and extra != "":
                    return 4 * (None,)
            else:
                return 4 * (None,)
    else:
        # serch for the PCS
        if PCS_name is None:
            pcs_found = False
            for pcs_sgl in PCS_TYP[1:]:
                # create a pattern to search the actual pcs_type
                midtrm_pat = re.compile(
                    "^"
                    + re.escape(id_name)
                    + "_time_[^_]+.*_"
                    + re.escape(pcs_sgl)
                )
                midtrm_match = midtrm_pat.search(name)
                # if found retrive the PCS name
                if midtrm_match is not None:
                    pcs_found = True
                    PCS = name[
                        midtrm_match.span()[1]
                        - len(pcs_sgl) : suffix_match.span()[0]
                    ]
                    # cut off extra suffix from PCS
                    extra = PCS[len(pcs_sgl) :]
                    PCS = PCS[: len(pcs_sgl)]
                    # retrive the pnt name from the file-path
                    PCS_pat = re.compile(
                        "_" + re.escape(PCS + extra) + r"\.tec$"
                    )
                    PCS_match = PCS_pat.search(name)
                    pnt = name[prefix_match.span()[1] : PCS_match.span()[0]]
                    break
            if not pcs_found:
                if guess_PCS:
                    # here we have to guess the POINT name and maybe a PCS type
                    # POINT name is guessed as a name without "_"
                    # the rest will be set as PCS
                    midtrm_pat = re.compile(
                        "^" + re.escape(id_name) + r"_time_[^_]+[\._]"
                    )
                    midtrm_match = midtrm_pat.search(name)
                    if midtrm_match is None:
                        return 4 * (None,)
                    pnt = name[
                        prefix_match.span()[1] : midtrm_match.span()[1] - 1
                    ]
                    PCS = name[midtrm_match.span()[1] : suffix_match.span()[0]]
                    extra = ""
                else:
                    pnt = name[prefix_match.span()[1] : suffix_match.span()[0]]
                    PCS = ""
                    extra = ""
        else:
            PCS_pat = re.compile("_" + re.escape(PCS_name))  # +".*\.tec$")
            PCS_match = PCS_pat.search(name)
            if PCS_match is None:
                return 4 * (None,)
            pnt = name[prefix_match.span()[1] : PCS_match.span()[0]]
            extra = name[PCS_match.span()[1] : suffix_match.span()[0]]
            # PCS was given, extras should not be split and extra != ""
            # thus we get a contradiction
            if (not split_extra) and extra != "":
                return 4 * (None,)

    if not split_extra:
        PCS = PCS + extra
        extra = ""
    elif extra.startswith("_"):
        extra = extra[1:]
    elif extra != "":
        # if PCS starts with given PCS but there's an extra suffix not
        # separated by an "_" return None
        return 4 * (None,)

    return id_name, pnt, PCS, extra


def split_ply_path(
    infile, task_id=None, line_name=None, PCS_name=None, split_extra=False
):
    """
    Retrive ogs-infos from filename for tecplot-polyline output.

    {id}_ply_{line}_t{n}[_{PCS+extra}].tec
    """
    # remove the directory-part from the filepath to get the basename
    name = os.path.basename(infile)
    # check for the task_id
    if task_id is None:
        prefix_pat = re.compile("_ply_")
        id_name = name[: prefix_pat.search(name).span()[0]]
    else:
        prefix_pat = re.compile("^" + re.escape(task_id) + "_ply_")
        id_name = task_id
    # search for different parts in the string
    midtrm_pat = re.compile(r"_t\d+[\._]")
    suffix_pat = re.compile(r"\.tec$")
    prefix_match = prefix_pat.search(name)
    midtrm_match = midtrm_pat.search(name)
    suffix_match = suffix_pat.search(name)

    # if anything was not found, return None for everything
    if prefix_match is None or midtrm_match is None or suffix_match is None:
        return 5 * (None,)

    # get the infos from the file-name
    line = name[prefix_match.span()[1] : midtrm_match.span()[0]]
    step = int(name[midtrm_match.span()[0] + 2 : midtrm_match.span()[1] - 1])
    PCS = name[midtrm_match.span()[1] : suffix_match.span()[0]]

    if line_name is not None and line_name != line:
        return 5 * (None,)

    if PCS_name is None:
        pcs_found = False
        for pcs_sgl in PCS_TYP[1:]:
            if PCS.startswith(pcs_sgl):
                pcs_found = True
                extra = PCS[len(pcs_sgl) :]
                PCS = pcs_sgl
                break
        if not pcs_found:
            extra = ""
    else:
        if PCS.startswith(PCS_name):
            extra = PCS[len(PCS_name) :]
            PCS = PCS_name
            if not split_extra and extra != "":
                return 5 * (None,)
        else:
            return 5 * (None,)
    if not split_extra:
        PCS = PCS + extra
        if PCS_name is not None and extra != "":
            return 5 * (None,)
        extra = ""
    elif extra.startswith("_"):
        extra = extra[1:]
    elif extra != "" and PCS_name != "":
        # if PCS starts with given PCS (not "") but there's an extra suffix not
        # separated by an "_" return None
        return 5 * (None,)

    return id_name, line, step, PCS, extra


def readpvd_single(infile):
    """
    Read a paraview pvd file.

    Convert all concerned files to a dictionary containing their data.
    """
    output = {}
    # read the pvd file as XML and extract the needed file infos
    if not os.path.isfile(infile):
        return output
    info_root = ET.parse(infile).getroot()
    pvd_info = info_root.attrib
    files = []
    infos = []
    # iterate through the data collection
    for dataset in info_root[0]:
        files.append(dataset.attrib["file"])
        infos.append(dataset.attrib)
        del infos[-1]["file"]
        if "timestep" in infos[-1]:
            infos[-1]["timestep"] = float(infos[-1]["timestep"])
        if "part" in infos[-1]:
            infos[-1]["part"] = int(infos[-1]["part"])
    output["pvd_info"] = pvd_info
    output["files"] = files
    output["infos"] = infos
    return output


def get_output_files(task_root, task_id, pcs=None, typ="VTK", element=None):
    """
    Get a list of output file paths.

    Parameters
    ----------
    task_root : string
        string containing the path to the directory containing the ogs output
    task_id : string
        string containing the file name of the ogs task without extension
    pcs : string or None, optional
        specify the PCS type that should be collected
        Possible values are:

            - None/"" (no PCS_TYPE specified in *.out)
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

        Default : None
    typ : string, optional
        Type of the output ("VTK", "PVD", "TEC_POINT" or "TEC_POLYLINE").
        Default : "VTK"
    element : string or None, optional
        For tecplot output you can specify the name of the output element.
        (Point-name of Line-name from GLI file)
        Default: None
    """
    typ = typ.upper()
    if pcs is None:
        pcs = ""
    # if pcs is "ALL" iterate over all known PCS types
    if pcs == "ALL":
        raise ValueError("get_output_files: specifiy a single PCS not 'ALL'.")
    # format task_root proper as directory path
    task_root = os.path.normpath(task_root)
    if typ == "VTK":
        # in the filename, there is a underscore before the PCS-type
        if pcs != "":
            pcs = "_" + pcs
        # YEAHAA.. inconsistency
        if pcs == "_RANDOM_WALK":
            pcs = "_RWPT"
        # get a list of all output files "{id}0000.vtk" ... "{id}999[...]9.vtk"
        # if pcs is RWPT the name-sheme is different
        if pcs == "_RWPT":
            files = glob.glob(
                os.path.join(
                    task_root, task_id + pcs + "_[0-9]*.particles.vtk"
                )
            )
        else:
            files = glob.glob(
                os.path.join(
                    task_root, task_id + pcs + "[0-9][0-9][0-9]*[0-9].vtk"
                )
            )
        files.sort()
    elif typ == "PVD":
        # in the filename, there is a underscore before the PCS-type
        if pcs != "":
            pcs = "_" + pcs
        infile = os.path.join(task_root, task_id + pcs + ".pvd")
        # get the pvd information about the concerned files
        pvd_info = readpvd_single(infile)
        # if pvd is empty: return
        if not pvd_info:
            return []
        # initialize output-time
        time = []
        for info in pvd_info["infos"]:
            time.append(info["timestep"])
        time = np.array(time)
        time_sort = np.argsort(time)
        files = []
        for new_pos in time_sort:
            files.append(pvd_info["files"][new_pos])
    elif typ == "TEC_POINT":
        # find point output by keyword "time"
        infiles = glob.glob(
            os.path.join(task_root, task_id + "_time_*." + "tec")
        )
        infiles.sort()
        files = []
        for infile in infiles:
            # get the information from the file-name
            _, pnt_name, file_pcs, _ = split_pnt_path(infile, task_id)
            # check if the given PCS type matches, else skip the file
            if file_pcs == pcs and (element is None or element == pnt_name):
                files.append(infile)
    elif typ == "TEC_POLYLINE":
        infiles = glob.glob(
            os.path.join(task_root, task_id + "_ply_?*_t[0-9]*.tec")
        )
        # sort the infiles by name to sort it by timestep (pitfall!!!)
        infiles.sort()
        files = []
        for infile in infiles:
            # get the information from the file-name
            _, line_name, _, file_pcs, _ = split_ply_path(infile, task_id)
            # check if the given PCS type matches, else skip the file
            if file_pcs == pcs and (element is None or element == line_name):
                files.append(infile)
    else:
        raise ValueError("Unknown output typ: '{}'".format(typ))
    return files
