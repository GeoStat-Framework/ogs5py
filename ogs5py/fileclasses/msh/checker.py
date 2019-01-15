# -*- coding: utf-8 -*-
"""
tools for the ogs5py-mesh package

@author: sebastian
"""
from __future__ import division, print_function, absolute_import
import numpy as np
from ogs5py.fileclasses.msh.tools import no_of_elements
from ogs5py.tools.types import (
    STRTYPE,
    NODE_NO,
    MESH_KEYS,
    MESH_DATA_KEYS,
    ELEMENT_KEYS,
)


def check_mesh_list(meshlist, verbose=True):
    """
    Check if a given mesh dictonary is valid in the sence, that the
    contained data is consistent.
    Checks for correct element definitions or Node duplicates
    are not carried out.

    Parameters
    ----------
    meshlist : list of dict
        each dictionary contains one '#FEM_MSH' block from the mesh file
        with the following information
            mesh_data : dictionary containing information about
                AXISYMMETRY (bool)
                CROSS_SECTION (bool)
                PCS_TYPE (str)
                GEO_TYPE (str)
                GEO_NAME (str)
                LAYER (int)
            nodes : ndarray
                Array with all node postions
            elements : dictionary
                contains nodelists for elements sorted by element types
            material_id : dictionary
                contains material ids for each element sorted by element types
            element_id : dictionary
                contains element ids for each element sorted by element types
    verbose : bool, optional
        Print information for the executed checks. Default: True

    Returns
    -------
    result : bool
        Validity of the given meshlist.
    """
    if not isinstance(meshlist, list):
        if verbose:
            print(" meshlist is not of type list")
        return False

    for mesh in meshlist:
        if not check_mesh_dict(mesh, verbose):
            return False
    return True


def check_mesh_dict(mesh, verbose=True):
    """
    Check if a given mesh dictonary is valid in the sence, that the
    contained data is consistent.
    Checks for correct element definitions or Node duplicates
    are not carried out.

    Parameters
    ----------
    mesh : dict
        dictionary contains one '#FEM_MSH' block from the mesh file
        with the following information
            mesh_data : dictionary containing information about
                AXISYMMETRY (bool)
                CROSS_SECTION (bool)
                PCS_TYPE (str)
                GEO_TYPE (str)
                GEO_NAME (str)
                LAYER (int)
            nodes : ndarray
                Array with all node postions
            elements : dictionary
                contains nodelists for elements sorted by element types
            material_id : dictionary
                contains material ids for each element sorted by element types
            element_id : dictionary
                contains element ids for each element sorted by element types
    verbose : bool, optional
        Print information for the executed checks. Default: True

    Returns
    -------
    result : bool
        Validity of the given mesh.
    """
    if verbose:
        print("")
        print("checking mesh for validity")
        print("--------------------------")
    # check if dict
    if not isinstance(mesh, dict):
        if verbose:
            print(" mesh is not of type dict")
        return False

    in_mesh_keys = set(mesh)
    # check for keys in mesh dict
    if in_mesh_keys == MESH_KEYS:
        if verbose:
            print(" mesh keys are valid")
            print("")
    else:
        if verbose:
            print(" mesh keys are not valid!")
            print(" needs: " + " ".join(MESH_KEYS))
            print(" found: " + " ".join(map(str, in_mesh_keys)))
            print(" missing: " + " ".join(map(str, MESH_KEYS - in_mesh_keys)))
            print(
                " corrupted: " + " ".join(map(str, in_mesh_keys - MESH_KEYS))
            )
        return False
    # check if mesh_data is dict
    if not isinstance(mesh["mesh_data"], dict):
        if verbose:
            print(" mesh['mesh_data'] is not of type dict")
        return False
    # check if elements is dict
    if not isinstance(mesh["elements"], dict):
        if verbose:
            print(" mesh['elements'] is not of type dict")
        return False
    # check if material_id is dict
    if not isinstance(mesh["material_id"], dict):
        if verbose:
            print(" mesh['material_id'] is not of type dict")
        return False
    # check if element_id is dict
    if not isinstance(mesh["element_id"], dict):
        if verbose:
            print(" mesh['element_id'] is not of type dict")
        return False
    # get all keys
    in_mesh_data_keys = set(mesh["mesh_data"])
    in_element_keys = set(mesh["elements"])
    in_material_keys = set(mesh["material_id"])
    in_elementid_keys = set(mesh["element_id"])
    # check for keys in mesh_data dict
    if in_mesh_data_keys <= MESH_DATA_KEYS:
        if verbose:
            print(" mesh['mesh_data'] keys are valid")
            print("")
    else:
        if verbose:
            print(" mesh['mesh_data'] keys are not valid!")
            print(" only allowed: " + " ".join(MESH_DATA_KEYS))
            print(" found: " + " ".join(map(str, in_mesh_data_keys)))
            corrupt = in_mesh_data_keys - MESH_DATA_KEYS
            print(" corrupted: " + " ".join(map(str, corrupt)))
        return False
    # check AXISYMMETRY
    if "AXISYMMETRY" in in_mesh_data_keys:
        if isinstance(mesh["mesh_data"]["AXISYMMETRY"], bool):
            if verbose:
                print(" mesh['mesh_data']['AXISYMMETRY'] valid")
                print("")
        else:
            if verbose:
                print(" mesh['mesh_data']['AXISYMMETRY'] not valid.")
                print(" Should be bool.")
            return False
    # check CROSS_SECTION
    if "CROSS_SECTION" in in_mesh_data_keys:
        if isinstance(mesh["mesh_data"]["CROSS_SECTION"], bool):
            if verbose:
                print(" mesh['mesh_data']['CROSS_SECTION'] valid")
                print("")
        else:
            if verbose:
                print(" mesh['mesh_data']['CROSS_SECTION'] not valid.")
                print(" Should be bool.")
            return False
    # check PCS_TYPE
    if "PCS_TYPE" in in_mesh_data_keys:
        if (
            isinstance(mesh["mesh_data"]["PCS_TYPE"], STRTYPE)
            and " " not in mesh["mesh_data"]["PCS_TYPE"]
        ):
            if verbose:
                print(" mesh['mesh_data']['PCS_TYPE'] valid")
                print("")
        else:
            if verbose:
                print(" mesh['mesh_data']['PCS_TYPE'] not valid.")
                print(" Should be str not containing spaces.")
            return False
    # check GEO_TYPE
    if "GEO_TYPE" in in_mesh_data_keys:
        if (
            isinstance(mesh["mesh_data"]["GEO_TYPE"], STRTYPE)
            and " " not in mesh["mesh_data"]["GEO_TYPE"]
        ):
            if verbose:
                print(" mesh['mesh_data']['GEO_TYPE'] valid")
                print("")
        else:
            if verbose:
                print(" mesh['mesh_data']['GEO_TYPE'] not valid.")
                print(" Should be str not containing spaces.")
            return False
    # check GEO_NAME
    if "GEO_NAME" in in_mesh_data_keys:
        if (
            isinstance(mesh["mesh_data"]["GEO_NAME"], STRTYPE)
            and " " not in mesh["mesh_data"]["GEO_NAME"]
        ):
            if verbose:
                print(" mesh['mesh_data']['GEO_NAME'] valid")
                print("")
        else:
            if verbose:
                print(" mesh['mesh_data']['GEO_NAME'] not valid.")
                print(" Should be str not containing spaces.")
            return False
    # check LAYER
    if "LAYER" in in_mesh_data_keys:
        if (
            isinstance(mesh["mesh_data"]["LAYER"], int)
            and mesh["mesh_data"]["LAYER"] >= 0
        ):
            if verbose:
                print(" mesh['mesh_data']['LAYER'] valid")
                print("")
        else:
            if verbose:
                print(" mesh['mesh_data']['LAYER'] not valid.")
                print(" Should be non-negativ int.")
            return False
    # check for keys in elements dict
    if in_element_keys <= ELEMENT_KEYS:
        if verbose:
            print(" mesh['elements'] keys are valid")
            print("")
    else:
        if verbose:
            print(" mesh['elements'] keys are not valid!")
            print(" only allowed: " + " ".join(ELEMENT_KEYS))
            print(" found: " + " ".join(map(str, in_element_keys)))
            corrupt = in_element_keys - ELEMENT_KEYS
            print(" corrupted: " + " ".join(map(str, corrupt)))
        return False
    # check for keys in material_id dict
    if in_material_keys == in_element_keys:
        if verbose:
            print(" mesh['material_id'] keys are valid")
            print("")
    else:
        if verbose:
            print(" mesh['material_id'] keys are not valid!")
            print(
                " need to match 'elements' keys: " + " ".join(in_element_keys)
            )
            print(" found: " + " ".join(map(str, in_material_keys)))
            missing = in_element_keys - in_material_keys
            corrupt = in_material_keys - in_element_keys
            print(" missing: " + " ".join(map(str, missing)))
            print(" corrupted: " + " ".join(map(str, corrupt)))
        return False
    # check for keys in element_id dict
    if in_elementid_keys == in_element_keys:
        if verbose:
            print(" mesh['element_id'] keys are valid")
            print("")
    else:
        if verbose:
            print(" mesh['element_id'] keys are not valid!")
            print(
                " need to match 'elements' keys: " + " ".join(in_element_keys)
            )
            print(" found: " + " ".join(map(str, in_elementid_keys)))
            missing = in_element_keys - in_elementid_keys
            corrupt = in_elementid_keys - in_element_keys
            print(" missing: " + " ".join(map(str, missing)))
            print(" corrupted: " + " ".join(map(str, corrupt)))
        return False
    # check nodes
    if mesh["nodes"] is None and len(in_element_keys) == 0:
        node_cnt = 0
        if verbose:
            print(
                " mesh['nodes'] are none, "
                + " which is valid since no elements are given"
            )
            print("")
    elif mesh["nodes"] is None and len(in_element_keys) > 0:
        if verbose:
            print(
                " mesh['nodes'] are none, "
                + " which is not valid since there are elements given"
            )
        return False
    else:
        # see https://github.com/numpy/numpy/pull/9505 for issubdtype
        if (
            isinstance(mesh["nodes"], np.ndarray)
            and np.issubdtype(mesh["nodes"].dtype, np.floating)
            and mesh["nodes"].ndim == 2
            and mesh["nodes"].shape[1] == 3
        ):
            node_cnt = mesh["nodes"].shape[0]
            if verbose:
                print(" mesh['nodes'] valid")
                print("")
        else:
            if verbose:
                print(" mesh['nodes'] not valid")
            return False
    # check elements, material_id and element_id
    element_id_stack = np.array([], dtype=int)
    material_id_stack = np.array([], dtype=int)
    for elem in in_element_keys:
        # see https://github.com/numpy/numpy/pull/9505 for issubdtype
        if (
            isinstance(mesh["elements"][elem], np.ndarray)
            and np.issubdtype(mesh["elements"][elem].dtype, np.integer)
            and mesh["elements"][elem].ndim == 2
            and mesh["elements"][elem].shape[1] == NODE_NO[elem]
            and np.min(mesh["elements"][elem]) >= 0
            and np.max(mesh["elements"][elem]) < node_cnt
        ):
            if verbose:
                print(" mesh['elements']['" + elem + "'] valid")
        else:
            if verbose:
                print(" mesh['elements']['" + elem + "'] not valid")
            return False
        # see https://github.com/numpy/numpy/pull/9505 for issubdtype
        if (
            isinstance(mesh["material_id"][elem], np.ndarray)
            and np.issubdtype(mesh["material_id"][elem].dtype, np.integer)
            and mesh["material_id"][elem].ndim == 1
            and mesh["material_id"][elem].shape[0]
            == mesh["elements"][elem].shape[0]
            and np.min(mesh["material_id"][elem]) >= -1
        ):
            if verbose:
                print(" mesh['material_id']['" + elem + "'] valid")
        else:
            if verbose:
                print(" mesh['material_id']['" + elem + "'] not valid")
            return False
        # see https://github.com/numpy/numpy/pull/9505 for issubdtype
        if (
            isinstance(mesh["element_id"][elem], np.ndarray)
            and np.issubdtype(mesh["element_id"][elem].dtype, np.integer)
            and mesh["element_id"][elem].ndim == 1
            and mesh["element_id"][elem].shape[0]
            == mesh["elements"][elem].shape[0]
        ):
            if verbose:
                print(" mesh['element_id']['" + elem + "'] valid")
        else:
            if verbose:
                print(" mesh['element_id']['" + elem + "'] not valid")
            return False
        # stack material_id and element_id for checking
        material_id_stack = np.hstack(
            (material_id_stack, mesh["material_id"][elem])
        )
        element_id_stack = np.hstack(
            (element_id_stack, mesh["element_id"][elem])
        )
    # check ranges of material_id and element_id
    if len(material_id_stack) > 0:
        if set(material_id_stack) == set(
            np.arange(np.max(material_id_stack) + 1)
        ):
            if verbose:
                print(" mesh['material_id'] has valid range")
        else:
            if verbose:
                print(" mesh['material_id'] range has gaps, which is ignored")
            # return False
    if len(element_id_stack) > 0:
        if (
            len(element_id_stack) == no_of_elements(mesh)
            and len(np.unique(element_id_stack)) == no_of_elements(mesh)
            and np.min(element_id_stack) == 0
            and np.max(element_id_stack) == no_of_elements(mesh) - 1
        ):
            if verbose:
                print(" mesh['element_id'] has valid range")
        else:
            if verbose:
                print(" mesh['element_id'] has no valid range")
            return False
    # finally
    if verbose:
        print("-------------")
        print("mesh is valid")
        print("")
    return True
