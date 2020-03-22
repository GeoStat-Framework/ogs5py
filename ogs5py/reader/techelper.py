# -*- coding: utf-8 -*-
"""Helper functions for the tecplot readers in ogs5py."""
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

tecreader_dict = {
    "vtkUnstructuredGrid": (vtkUnstructuredGridReader, _unst_grid_read),
    "vtkStructuredGrid": (vtkStructuredGridReader, _stru_grid_read),
    "vtkStructuredPoints": (vtkStructuredPointsReader, _stru_point_read),
    "vtkPolyData": (vtkPolyDataReader, _poly_data_read),
    "vtkRectilinearGrid": (vtkRectilinearGridReader, _rect_grid_read),
}


###############################################################################
# Helper Class to inspect a tecplot file
###############################################################################


class inspect_tecplot(object):
    """A simple inspector for multiblock data tecplot files."""

    def __init__(self, infile, get_zone_sizes=True):
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
        """Get number and names of zones in file."""
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
        """Read the zone data by hand from the tecplot table file."""
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
        """Read the zone mesh-data with the aid of VTK from the tec-file."""
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
    """Reader for a single ZONE tecplot table file with ogs point output."""
    # inspect the tecplot file
    info = inspect_tecplot(infile)
    zone_data = info.get_zone_table_data()[0]
    # sort values by Variable names
    out = {}
    for i, name in enumerate(info.var_names):
        out[name] = zone_data[:, i]

    return out


def readtec_multi_table(infile):
    """Reader for a multi ZONE tecplot table file with ogs polyline output."""
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
    """Read a vtk-compatible tecplot file to a dictionary with its data."""
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
