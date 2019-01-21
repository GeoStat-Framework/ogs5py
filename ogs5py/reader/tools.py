# -*- coding: utf-8 -*-
"""
tools for the ogs5py.reader package
"""
from __future__ import division, print_function, absolute_import
from numpy import ascontiguousarray as ascont
from vtk import vtkStructuredPoints, vtkStructuredPointsWriter, vtkFieldData
from vtk.util.numpy_support import numpy_to_vtk as np2vtk


def save_vtk_stru_point(path, vtk_dict, verbose=True):
    """
    A routine to save a structured point vtk file given by a dictionary.

    Parameters
    ----------
    path : string
        Path for the file to be saved to.
    vtk_dict : dict
        Dictionary containing information of a structured point vtk file.
        The following keywords are allowed:

        * ``"dimensions"``: (int, int, int)
        * ``"origin"``: (float, float, float)
        * ``"spacing"``: (float, float, float)
        * ``"header"``: string
        * ``"field_data"``: dict of {"name": array}
        * ``"point_data"``: dict of {"name": array}
        * ``"cell_data"``: dict of {"name": array}

    verbose : bool, optional
        Print information of the writing process. Default: True

    Notes
    -----
    All data is assumed to be scalar.
    """
    out = vtkStructuredPoints()
    if verbose:
        print("Set 'dimensions', 'origin', 'spacing'")
    out.SetDimensions(vtk_dict["dimensions"])
    out.SetOrigin(vtk_dict["origin"])
    out.SetSpacing(vtk_dict["spacing"])

    if vtk_dict["field_data"]:
        if verbose:
            print("Set 'field_data'")
        data = vtkFieldData()
        for sgl_data in vtk_dict["field_data"]:
            if verbose:
                print("  Set '" + sgl_data + "'")
            arr = np2vtk(
                ascont(vtk_dict["field_data"][sgl_data].reshape(-1, order="F"))
            )
            arr.SetName(sgl_data)
            data.AddArray(arr)
        out.SetFieldData(data)

    if vtk_dict["point_data"]:
        if verbose:
            print("Set 'point_data'")
        data = out.GetPointData()
        for sgl_data in vtk_dict["point_data"]:
            if verbose:
                print("  Set '" + sgl_data + "'")
            arr = np2vtk(
                ascont(vtk_dict["point_data"][sgl_data].reshape(-1, order="F"))
            )
            arr.SetName(sgl_data)
            data.AddArray(arr)

    if vtk_dict["cell_data"]:
        if verbose:
            print("Set 'cell_data'")
        data = out.GetCellData()
        for sgl_data in vtk_dict["cell_data"]:
            if verbose:
                print("  Set '" + sgl_data + "'")
            arr = np2vtk(
                ascont(vtk_dict["cell_data"][sgl_data].reshape(-1, order="F"))
            )
            arr.SetName(sgl_data)
            data.AddArray(arr)

    writer = vtkStructuredPointsWriter()
    writer.SetFileName(path)
    writer.SetInputData(out)
    if "header" in vtk_dict:
        writer.SetHeader(vtk_dict["header"])
    writer.Write()
