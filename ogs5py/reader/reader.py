# -*- coding: utf-8 -*-
"""
Reader for the OGS5 Output.
"""

from __future__ import absolute_import, division, print_function

import os
import glob
import xml.etree.ElementTree as ET
import numpy as np
from vtk import (
    vtkDataReader,
    vtkXMLFileReadTester,
    vtkStringOutputWindow,
    vtkOutputWindow,
)
from ogs5py.tools.types import PCS_TYP
from ogs5py.reader.vtkhelper import vtkreader_dict, XMLreader_dict
from ogs5py.reader.techelper import (
    split_ply_path,
    split_pnt_path,
    readtec_single_table,
    readtec_multi_table,
)
from ogs5py.tools.tools import split_file_path

# redirect VTK error to a string
VTK_ERR = vtkStringOutputWindow()
"""VTK Error output. Accessible with ``VTK_ERR.GetOutput()``"""

VTK_STD_OUT = vtkOutputWindow()
VTK_STD_OUT.SetInstance(VTK_ERR)


###############################################################################
# vtk readers
###############################################################################


def readvtk_single(infile):
    """
    read an arbitrary vtk/vtkXML file to a dictionary containing its data
    """
    xml_checker = vtkXMLFileReadTester()
    xml_checker.SetFileName(infile)
    is_xml = bool(xml_checker.TestReadFile())
    if is_xml:
        # check for vtk-XML-type
        xml_type = xml_checker.GetFileDataType()
        if xml_type in XMLreader_dict:
            reader = XMLreader_dict[xml_type]
        else:
            print(
                infile + ": XML file not valid (Type '" + str(xml_type) + "')"
            )
            if xml_type == "Collection":
                print("...try the 'readpvd' function")
            return {}
    else:
        # check for vtk-type
        checker = vtkDataReader()
        checker.SetFileName(infile)
        # get the right reader depending on the datasettype
        reader_found = False
        for datasettype in vtkreader_dict:
            if checker.IsFileValid(datasettype):
                reader = vtkreader_dict[datasettype]
                reader_found = True
                break
        if not reader_found:
            print(infile + ": vtk file not valid")
            checker.CloseVTKFile()
            return {}
        checker.CloseVTKFile()

    # read in the vtk object
    vtk_reader = reader[0]()
    vtk_reader.SetFileName(infile)
    if not is_xml:
        # https://stackoverflow.com/a/35018175/6696397
        vtk_reader.ReadAllScalarsOn()
        vtk_reader.ReadAllVectorsOn()
        vtk_reader.ReadAllNormalsOn()
        vtk_reader.ReadAllTensorsOn()
        vtk_reader.ReadAllColorScalarsOn()
        vtk_reader.ReadAllTCoordsOn()
        vtk_reader.ReadAllFieldsOn()
    vtk_reader.Update()
    file_obj = vtk_reader.GetOutput()

    # convert vtk object to a dictionary of numpy arrays
    output = reader[1](file_obj)
    if not is_xml:
        output["header"] = vtk_reader.GetHeader()
    else:
        output["header"] = "vtk-XML file"

    return output


def readvtk(task_root=".", task_id=None, pcs="ALL", single_file=None):
    r"""
    a genearal reader for OGS vtk outputfiles
    give a dictionary containing their data

    the Filename of the pvd is structured the following way:
    {task_id}[_{PCS}]xxxx.vtk
    thereby the "_{PCS}" is optional and just present if a PCS_TYPE is
    specified in the \*.out file

    Parameters
    ----------
    task_root : string, optional
        string containing the path to the directory containing the ogs output
        Default : "."
    task_id : string, optional
        string containing the file name of the ogs task without extension
        Default : None
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
    single_file : string or None, optional
        If you want to read just a single file, you can set the path here.
        Default : None
    Returns
    -------
    result : dict
        keys are the point names and the items are the data from the
        corresponding files
        if pcs="ALL", the output is a dictionary with the PCS-types as keys
    """
    # for a single file return the output immediately
    if single_file is not None:
        return readvtk_single(single_file)
    if pcs is None:
        pcs = ""
    # if pcs is "ALL" iterate over all known PCS types
    if pcs == "ALL":
        out = {}
        for pcs_single in PCS_TYP:
            out_single = readvtk(task_root, task_id, pcs_single)
            if out_single:
                out[pcs_single] = out_single
        return out
    # in the filename, there is a underscore before the PCS-type
    if pcs != "":
        pcs = "_" + pcs
    # YEAHAA.. inconsistency
    if pcs == "_RANDOM_WALK":
        pcs = "_RWPT"
    output = {}
    # format task_root proper as directory path
    task_root = os.path.normpath(task_root)
    # get a list of all output files "{id}0000.vtk" ... "{id}999[...]9.vtk"
    # if pcs is RWPT the name-sheme is different
    if pcs == "_RWPT":
        infiles = glob.glob(
            os.path.join(task_root, task_id + pcs + "_[0-9]*.particles.vtk")
        )
    else:
        infiles = glob.glob(
            os.path.join(
                task_root, task_id + pcs + "[0-9][0-9][0-9]*[0-9].vtk"
            )
        )

    # sort input files by name, since they are sorted by timesteps
    infiles.sort()
    # iterate over all input files
    time = []
    data = []
    if not infiles:
        return output
    for infile in infiles:
        # read the single vtk-file
        out = readvtk_single(infile)
        # in the RWPT files the TIME is not given as field_data but in header
        if pcs == "_RWPT" and "header" in out:
            if out["header"] and "=" in out["header"]:
                # ndmin = 1 to match the standard format
                out["field_data"]["TIME"] = np.array(
                    float(out["header"].split("=")[1]), ndmin=1
                )
        if "field_data" in out and "TIME" in out["field_data"]:
            time.append(out["field_data"]["TIME"])
            data.append(out)
        else:
            raise ValueError("vtk file not valid: " + infile)

    # sort the time-steps
    time = np.squeeze(time)
    time_sort = np.argsort(time)
    time = time[time_sort]
    data_sort = []
    for new_pos in time_sort:
        data_sort.append(data[new_pos])

    # sort output by timesteps
    output["TIME"] = time
    output["DATA"] = data_sort

    return output


###############################################################################
# pvd readers
###############################################################################


def readpvd_single(infile):
    """
    read a paraview pvd file and convert all concerned files
    to a dictionary containing their data
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


def readpvd(task_root=".", task_id=None, pcs="ALL", single_file=None):
    r"""
    read a paraview pvd file and convert all concerned files
    to a dictionary containing their data

    the Filename of the pvd is structured the following way:
    {task_id}[_{PCS}].pvd
    thereby the "_{PCS}" is optional and just present if a PCS_TYPE is
    specified in the \*.out file

    Parameters
    ----------
    task_root : string, optional
        string containing the path to the directory containing the ogs output
        Default : "."
    task_id : string, optional
        string containing the file name of the ogs task without extension
        Default : None
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
    single_file : string or None, optional
        If you want to read just a single file, you can set the path here.
        Default : None
    Returns
    -------
    result : dict
        keys are the point names and the items are the data from the
        corresponding files
        if pcs="ALL", the output is a dictionary with the PCS-types as keys
    """
    # for a single file return the output immediately
    if single_file is not None:
        root, ext = os.path.splitext(single_file)
        if ext != ".pvd":
            print("not a '*.pvd' file")
            return {}
        task_root, task_id = os.path.split(root)
        if task_root == "":
            task_root = "."
        return readpvd(task_root, task_id, pcs="")
    if pcs is None:
        pcs = ""
    # if pcs is "ALL" iterate over all known PCS types
    if pcs == "ALL":
        out = {}
        for pcs_single in PCS_TYP:
            out_single = readpvd(task_root, task_id, pcs_single)
            if out_single != {}:
                out[pcs_single] = out_single
        return out
    # in the filename, there is a underscore before the PCS-type
    if pcs != "":
        pcs = "_" + pcs
    output = {}
    # format task_root proper as directory path
    task_root = os.path.normpath(task_root)
    infile = os.path.join(task_root, task_id + pcs + ".pvd")
    # get the pvd information about the concerned files
    pvd_info = readpvd_single(infile)
    # if pvd is empty: return
    if not pvd_info:
        return output
    # initialize output-time
    time = []
    for info in pvd_info["infos"]:
        time.append(info["timestep"])
    time = np.array(time)
    time_sort = np.argsort(time)
    time = time[time_sort]
    files = []
    for new_pos in time_sort:
        files.append(pvd_info["files"][new_pos])
    data = []
    # iterate over all input files
    for file_i in files:
        # format the file-path
        if split_file_path(file_i)[0] in ["", "."]:
            file_i = os.path.join(
                task_root, "".join(split_file_path(file_i)[1:])
            )
        # read the file
        data.append(readvtk_single(file_i))
    # append the infos stored in the pvd header
    output["TIME"] = time
    output["DATA"] = data

    return output


###############################################################################
# High level Tecplot reader
###############################################################################


def readtec_point(task_root=".", task_id=None, pcs="ALL", single_file=None):
    r"""
    collect TECPLOT point output from OGS5

    the Filenames are structured the following way:
    {task_id}_time_{NAME}[_{PCS+extra}].tec
    thereby the "_{PCS}" is optional and just present if a PCS_TYPE is
    specified in the \*.out file
    the "extra" will not be recognized and will destroy the search-process

    Parameters
    ----------
    task_root : string, optional
        string containing the path to the directory containing the ogs output
        Default : "."
    task_id : string, optional
        string containing the file name of the ogs task without extension
        Default : None
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
    single_file : string or None, optional
        If you want to read just a single file, you can set the path here.
        Default : None
    Returns
    -------
    result : dict
        keys are the point names and the items are the data from the
        corresponding files
        if pcs="ALL", the output is a dictionary with the PCS-types as keys
    """
    # for a single file return the output immediately
    if single_file is not None:
        return readtec_single_table(single_file)
    assert task_id is not None, "You need to specify a task_id"
    # check PCS
    if pcs is None:
        pcs = ""
    # if pcs is "ALL" iterate over all known PCS types
    if pcs == "ALL":
        out = {}
        for pcs_single in PCS_TYP:
            out_single = readtec_point(task_root, task_id, pcs_single)
            if out_single != {}:
                out[pcs_single] = out_single
        return out
    task_root = os.path.normpath(task_root)
    # find point output by keyword "time"
    infiles = glob.glob(os.path.join(task_root, task_id + "_time_*." + "tec"))

    out = {}
    for infile in infiles:
        # get the information from the file-name
        _, pnt_name, file_pcs, _ = split_pnt_path(infile, task_id)
        # check if the given PCS type matches, else skip the file
        if file_pcs != pcs:
            continue
        # read the file
        out[pnt_name] = readtec_single_table(infile)

    return out


def readtec_polyline(
    task_root=".", task_id=None, pcs="ALL", single_file=None, trim=True
):
    r"""
    collect TECPLOT polyline output from OGS5

    the Filenames are structured the following way:
    {task_id}_ply_{NAME}_t{ply_id}[_{PCS}].tec
    thereby the "_{PCS}" is optional and just present if a PCS_TYPE is
    specified in the \*.out file

    Parameters
    ----------
    task_root : string, optional
        string containing the path to the directory containing the ogs output
        Default : "."
    task_id : string, optional
        string containing the file name of the ogs task without extension
        Default : None
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
        Default : None
    single_file : string or None, optional
        If you want to read just a single file, you can set the path here.
        Default : None
    trim : Bool, optional
        if the ply_ids are not continuous, there will be "None" values in
        the output list. If trim is "True" these values will be eliminated.
        If there is just one output for a polyline, the list will be eliminated
        and the output will be the single dict.
        Default : True

    Returns
    -------
    result : dict
        keys are the Polyline names and the items are lists sorted by the
        ply_id (it is assumed, that the ply_ids are continuous, if not, the
        corresponding list entries are "None")
        if pcs="ALL", the output is a dictionary with the PCS-types as keys
    """
    # for a single file return the output immediately
    if single_file is not None:
        return readtec_multi_table(single_file)
    if pcs is None:
        pcs = ""
    # if pcs is "ALL" iterate over all known PCS types
    if pcs == "ALL":
        out = {}
        for pcs_single in PCS_TYP:
            out_single = readtec_polyline(task_root, task_id, pcs_single)
            if out_single != {}:
                out[pcs_single] = out_single
        return out
    # format the root_path
    task_root = os.path.normpath(task_root)
    infiles = glob.glob(
        os.path.join(task_root, task_id + "_ply_?*_t[0-9]*.tec")
    )
    # sort the infiles by name to sort it by timestep (pitfall!!!)
    infiles.sort()

    out = {}
    for infile in infiles:
        # get the information from the file-name
        _, line_name, time_step, file_pcs, _ = split_ply_path(infile, task_id)
        # check if the given PCS type matches, else skip the file
        if file_pcs != pcs:
            continue
        # check if the given polyline is already listed
        if line_name in out:
            cnt = len(out[line_name])
            if cnt <= time_step:
                # if the timesteps are not continous, insert None-values
                out[line_name] += (1 + time_step - cnt) * [None]
        else:
            out[line_name] = (1 + time_step) * [None]
        # add the actual file-data
        out[line_name][time_step] = readtec_multi_table(infile)

    if trim:
        for line in out:
            out[line] = [line_i for line_i in out[line] if line_i is not None]
            if len(out[line]) == 1:
                out[line] = out[line][0]

    return out


def readtec_domain():
    """
    This is a dummy for the TECPLOT-domain output of OGS which is not
    implemented because the output is separated by element types where
    VTK works out much better.
    """
    raise NotImplementedError(
        "Reader for Tecplot domain "
        + "output not yet implemented "
        + "....please(!) generate vtk/pvd here"
    )
