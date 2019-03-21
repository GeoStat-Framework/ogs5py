# -*- coding: utf-8 -*-
"""
Helper functions for the vtk readers in ogs5py
"""

from __future__ import absolute_import, division, print_function

from vtk import (
    vtkUnstructuredGridReader,
    vtkStructuredGridReader,
    vtkStructuredPointsReader,
    vtkPolyDataReader,
    vtkRectilinearGridReader,
    vtkXMLUnstructuredGridReader,
    vtkXMLStructuredGridReader,
    vtkXMLPolyDataReader,
    vtkXMLRectilinearGridReader,
)
from vtk.util.numpy_support import vtk_to_numpy as vtk2np
import numpy as np
from ogs5py.tools.types import VTK_TYP, NODE_NO


###############################################################################
# helper functions
###############################################################################


def _get_data(data):
    """
    extract data as numpy arrays from a vtkObject
    """
    arr_dict = {}
    no_of_arr = data.GetNumberOfArrays()
    for i in range(no_of_arr):
        arr = data.GetArray(i)
        if arr:
            arr_dict[arr.GetName()] = vtk2np(arr)
    return arr_dict


def _deflat_data(arr):
    """
    creat list of arrays from flat numpy-data from a vtkObject
    """
    arr_list = []
    stop_ct = len(arr)
    i = 0
    while i < stop_ct:
        len_i = arr[i]
        arr_list.append(arr[i + 1 : i + len_i + 1])
        i += len_i + 1
    return arr_list


def _get_cells(obj):
    """
    extract cells and cell_data from a vtkDataSet
    and sort it by cell types
    """
    cells, cell_data = {}, {}
    data = _get_data(obj.GetCellData())
    arr = vtk2np(obj.GetCells().GetData())
    loc = vtk2np(obj.GetCellLocationsArray())
    types = vtk2np(obj.GetCellTypesArray())

    for typ in VTK_TYP:
        if not isinstance(typ, int):
            continue
        cell_name = VTK_TYP[typ]
        n_no = NODE_NO[cell_name]
        cell_loc_i = np.where(types == typ)[0]
        loc_i = loc[cell_loc_i]
        # if there are no cells of the actual type continue
        if len(loc_i) == 0:
            # if not loc_i:
            continue
        arr_i = np.empty((len(loc_i), n_no), dtype=int)
        for i in range(n_no):
            arr_i[:, i] = arr[loc_i + i + 1]
        cells[cell_name] = arr_i
        cell_data_i = {}
        for data_i in data:
            cell_data_i[data_i] = data[data_i][cell_loc_i]
        if cell_data_i != {}:
            cell_data[cell_name] = cell_data_i

    return cells, cell_data


###############################################################################
# vtk-objects readers
###############################################################################


def _unst_grid_read(obj):
    """
    a reader for vtk unstructured grid objects
    """
    output = {}
    output["field_data"] = _get_data(obj.GetFieldData())
    output["points"] = vtk2np(obj.GetPoints().GetData())
    output["point_data"] = _get_data(obj.GetPointData())
    output["cells"], output["cell_data"] = _get_cells(obj)
    return output


def _stru_grid_read(obj):
    """
    a reader for vtk structured grid objects
    """
    raise NotImplementedError("Structured Grid Reader not yet implemented")


def _stru_point_read(obj):
    """
    a reader for vtk structured points objects
    """
    output = {}
    output["dimensions"] = np.array(obj.GetDimensions())
    output["origin"] = np.array(obj.GetOrigin())
    output["spacing"] = np.array(obj.GetSpacing())
    output["field_data"] = _get_data(obj.GetFieldData())
    output["point_data"] = _get_data(obj.GetPointData())
    output["cell_data"] = _get_data(obj.GetCellData())
    # reshape cell and point data according to the give dimensions
    dim = output["dimensions"]
    for arr in output["cell_data"]:
        output["cell_data"][arr] = np.squeeze(
            np.reshape(
                output["cell_data"][arr], np.maximum(dim - 1, 1), order="F"
            )
        )
    for arr in output["point_data"]:
        output["point_data"][arr] = np.reshape(
            output["point_data"][arr], dim, order="F"
        )
    return output


def _poly_data_read(obj):
    """
    a reader for vtk polygonal data objects
    """
    output = {}
    output["points"] = vtk2np(obj.GetPoints().GetData())
    output["verts"] = _deflat_data(vtk2np(obj.GetVerts().GetData()))
    output["lines"] = _deflat_data(vtk2np(obj.GetLines().GetData()))
    output["polygons"] = _deflat_data(vtk2np(obj.GetPolys().GetData()))
    output["strips"] = _deflat_data(vtk2np(obj.GetStrips().GetData()))
    output["point_data"] = _get_data(obj.GetPointData())
    output["cell_data"] = _get_data(obj.GetCellData())
    output["field_data"] = _get_data(obj.GetFieldData())
    return output


def _rect_grid_read(obj):
    """
    a reader for vtk rectangular grid objects
    """
    output = {}
    output["dimensions"] = np.array(obj.GetDimensions())
    output["x"] = vtk2np(obj.GetXCoordinates())
    output["y"] = vtk2np(obj.GetYCoordinates())
    output["z"] = vtk2np(obj.GetZCoordinates())
    output["field_data"] = _get_data(obj.GetFieldData())
    output["point_data"] = _get_data(obj.GetPointData())
    output["cell_data"] = _get_data(obj.GetCellData())
    # reshape cell and point data according to the give dimensions
    dim = output["dimensions"]
    for arr in output["cell_data"]:
        output["cell_data"][arr] = np.squeeze(
            np.reshape(
                output["cell_data"][arr], np.maximum(dim - 1, 1), order="F"
            )
        )
    for arr in output["point_data"]:
        output["point_data"][arr] = np.reshape(
            output["point_data"][arr], dim, order="F"
        )
    return output


###############################################################################
# reader dictonaries
###############################################################################


vtkreader_dict = {
    "unstructured_grid": (vtkUnstructuredGridReader, _unst_grid_read),
    "structured_grid": (vtkStructuredGridReader, _stru_grid_read),
    "structured_points": (vtkStructuredPointsReader, _stru_point_read),
    "polydata": (vtkPolyDataReader, _poly_data_read),
    "rectilinear_grid": (vtkRectilinearGridReader, _rect_grid_read),
}

XMLreader_dict = {
    "UnstructuredGrid": (vtkXMLUnstructuredGridReader, _unst_grid_read),
    "StructuredGrid": (vtkXMLStructuredGridReader, _stru_grid_read),
    "PolyData": (vtkXMLPolyDataReader, _poly_data_read),
    "RectilinearGrid": (vtkXMLRectilinearGridReader, _rect_grid_read),
}
