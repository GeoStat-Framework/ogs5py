# -*- coding: utf-8 -*-
"""
Helper functions for the tecplot readers in ogs5py
"""
from __future__ import division, print_function, absolute_import
import os
import re
import numpy as np
from vtk import (
    vtkTecplotReader,
    vtkUnstructuredGridReader,
    vtkStructuredGridReader,
    vtkStructuredPointsReader,
    vtkPolyDataReader,
    vtkRectilinearGridReader,
)
from ogs5py.reader.vtkhelper import (
    _unst_grid_read,
    _stru_grid_read,
    _stru_point_read,
    _poly_data_read,
    _rect_grid_read,
)
from ogs5py.tools.types import PCS_TYP

tecreader_dict = {
    "vtkUnstructuredGrid": (vtkUnstructuredGridReader, _unst_grid_read),
    "vtkStructuredGrid": (vtkStructuredGridReader, _stru_grid_read),
    "vtkStructuredPoints": (vtkStructuredPointsReader, _stru_point_read),
    "vtkPolyData": (vtkPolyDataReader, _poly_data_read),
    "vtkRectilinearGrid": (vtkRectilinearGridReader, _rect_grid_read),
}


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
    retrive ogs-infos from filename for tecplot-polyline output
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
    retrive ogs-infos from filename for tecplot-polyline output
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


###############################################################################
# Helper Class to inspect a tecplot file
###############################################################################


class inspect_tecplot(object):
    """
    a simple inspector for multiblock data tecplot files
    """

    def __init__(self, infile, get_zone_sizes=True):
        """
        a simple inspector for multiblock data tecplot files
        """
        self.infile = infile
        # get metainfo with vtk
        reader = vtkTecplotReader()
        reader.SetFileName(infile)
        reader.Update()
        # get title
        self.title = reader.GetDataTitle()
        # get variable names
        self.var_ct = reader.GetNumberOfDataArrays()
        self.var_names = [
            reader.GetDataArrayName(i).strip() for i in range(self.var_ct)
        ]
        # get block_names
        self.block_ct = reader.GetNumberOfBlocks()
        self.block_names = [
            reader.GetBlockName(i).strip() for i in range(self.block_ct)
        ]
        # get the zone positions within the file
        self.start = []
        self.zone_lines = []
        self.zone_length = []
        self.skip = []
        if get_zone_sizes:
            self._get_zone_ct()
            self._get_zone_sizes()

    def _get_zone_ct(self):
        """
        Get number and names of zones in file
        """
        self.zone_ct = 0
        self.zone_names = []
        with open(self.infile, "r") as f:
            line = f.readline()
            while line:
                split = line.split()
                if split[0] == "ZONE":
                    self.zone_ct += 1
                    self.zone_names.append(split[1].split('"')[1])
                line = f.readline()

    def _get_zone_sizes(self):
        """
        Get positions of the zones within the tecplot file.
        Only necessary for table/data tecplot files, since they are not
        supported by the vtk-package before version 7.0.
        """
        self.start = []
        self.zone_lines = []
        self.zone_length = []

        #        if self.zone_ct == 0:
        #            return

        # workaround for empty zones
        empty_zone = False

        with open(self.infile, "r") as f:
            line = f.readline()
            line_ct = 1
            for _ in range(self.zone_ct):
                # print("zone", _)
                # find the next ZONE
                while True:
                    if line.strip().startswith("ZONE"):
                        line = f.readline()
                        line_ct += 1
                        break
                    line = f.readline()
                    line_ct += 1
                # find the start of the data block in this ZONE
                while line and not line.strip()[0].isdigit():
                    if line.strip().startswith("ZONE"):
                        # this means, the zones don't contain data.
                        empty_zone = True
                        break
                        # return [0]*self.zone_ct
                    line = f.readline()
                    line_ct += 1
                if not line:
                    empty_zone = True
                self.start.append(line_ct - 1)
                # count the lines that start with a digit
                if empty_zone:
                    self.zone_lines.append(0)
                    self.zone_length.append(0)
                else:
                    self.zone_lines.append(1)
                    while line and line.strip()[0].isdigit():
                        line = f.readline()
                        line_ct += 1
                        self.zone_lines[-1] += 1
                    # matrix size is line_ct*name_ct
                    self.zone_length.append(self.zone_lines[-1] * self.var_ct)
                empty_zone = False

        if self.zone_ct > 0:
            # calculate the block-sizes between the data-blocks
            self.skip = [self.start[0]]
            for i in range(1, self.zone_ct):
                self.skip.append(
                    self.start[i]
                    - self.start[i - 1]
                    - self.zone_lines[i - 1]
                    + 1
                )

    def get_zone_table_data(self):
        """
        read the zone data by hand from the tecplot table file
        """
        zone_data = []
        # read all zones to numpy arrays
        with open(self.infile, "r") as f:
            for i in range(self.zone_ct):
                # skip header
                for _ in range(self.skip[i]):
                    f.readline()
                # read matrix with np.fromfile (fastest numpy file reader)
                data = np.fromfile(
                    f, dtype=float, count=self.zone_length[i], sep=" "
                )
                # reshape matrix acording to the number of variables
                zone_data.append(data.reshape((-1, self.var_ct)))

        return zone_data

    def get_zone_block_data(self):
        """
        read the zone mesh-data with the aid of VTK from the tecplot file
        """
        zone_data = []
        reader = vtkTecplotReader()
        reader.SetFileName(self.infile)
        reader.Update()
        file_blocks = reader.GetOutput()
        # iterate over all blocks
        for i in range(self.block_ct):
            # get the i-th block which is an instance of class vtkDataObject
            block = file_blocks.GetBlock(i)
            # read the single block
            reader_found = False
            for datasettype in tecreader_dict:
                if block.IsA(datasettype):
                    block_reader = tecreader_dict[datasettype][1]
                    reader_found = True
                    break
            if not reader_found:
                print(self.infile + ": file not valid")
                return {}
            else:
                zone_data.append(block_reader(block))

        return zone_data


###############################################################################
# Low level Tecplot reader
###############################################################################


def readtec_single_table(infile):
    """
    Reader for a single ZONE tecplot table file containing ogs point output.
    """
    # inspect the tecplot file
    info = inspect_tecplot(infile)
    zone_data = info.get_zone_table_data()[0]
    # sort values by Variable names
    out = {}
    for i, name in enumerate(info.var_names):
        out[name] = zone_data[:, i]

    return out


def readtec_multi_table(infile):
    """
    Reader for a multi ZONE tecplot table file containing ogs polyline output.
    """
    # inspect the tecplot file
    info = inspect_tecplot(infile)
    zone_data = info.get_zone_table_data()
    # get the time-steps from the zone_names (e.g. ZONE T="TIME=0.0")
    time = np.array(
        [float(info.zone_names[i][5:]) for i in range(info.zone_ct)]
    )
    # sort values by Variable names
    out = {"TIME": time}
    for i, name in enumerate(info.var_names):
        out[name] = np.vstack(
            [zone_data[n][:, i].T for n in range(info.zone_ct)]
        )

    return out


def readtec_block(infile):
    """
    read a vtk-compatible tecplot file to a dictionary containing its data
    """
    # inspect the tecplot file
    info = inspect_tecplot(infile, get_zone_sizes=False)
    zone_data = info.get_zone_block_data()
    if info.block_ct == 1 and info.block_names[0] == "DEFAULT":
        return zone_data[0]
    # get the time-steps from the zone_names (e.g. ZONE T="TIME=0.0")
    # if that doesn't work, just give the zone-names as "time"
    try:
        time = np.array(
            [float(info.block_names[i][:-1]) for i in range(info.block_ct)]
        )
    except Exception:
        time = info.block_names
    # separate the time-variable and store blocks in DATA
    return {"TIME": time, "DATA": zone_data}
