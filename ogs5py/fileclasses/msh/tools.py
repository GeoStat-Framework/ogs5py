# -*- coding: utf-8 -*-
"""Tools for the ogs5py mesh package."""
from copy import deepcopy as dcp
import numpy as np
from ogs5py.tools.types import ELEM_NAMES, EMPTY_MSH
from ogs5py.tools.tools import (
    unique_rows,
    replace,
    rotation_matrix,
    volume,
    centroid,
)


### modifying routines


def combine(mesh_1, mesh_2, decimals=4, fast=True):
    """
    Combine mesh_1 and mesh_2 to one single mesh.

    The node list will be updated to eliminate duplicates.
    Element intersections are not checked.

    Parameters
    ----------
    mesh_1,mesh_2 : dict
        dictionaries that contain one '#FEM_MSH' block each
        with the following information
            mesh_data : dict
                containing optional information about
                    - AXISYMMETRY (bool)
                    - CROSS_SECTION (bool)
                    - PCS_TYPE (str)
                    - GEO_TYPE (str)
                    - GEO_NAME (str)
                    - LAYER (int)
            nodes : ndarray
                Array with all node postions
            elements : dictionary
                contains array of nodes for elements sorted by element types
            material_id : dictionary
                contains material ids for each element sorted by element types
            element_id : dictionary
                contains element ids for each element sorted by element types
    decimals : int, optional
        Number of decimal places to round the nodes to (default: 3).
        This will not round the output, it is just for comparison of the
        node vectors.
    fast : bool, optional
        If fast is True, the vector comparison is executed by a
        decimal comparison. If fast is False, all pairwise distances
        are calculated. Default: True

    Returns
    -------
    out : dict
        dictionary containing one '#FEM_MSH' block of the mesh file
        with the following information
            mesh_data : dict
                taken from mesh_1
            nodes : ndarray
                Array with all unique node postions
            elements : dictionary
                contains array of nodes for elements sorted by element types
            material_id : dictionary
                contains material ids for each element sorted by element types
            element_id : dictionary
                contains element ids for each element sorted by element types
    """
    # hack to prevent numerical errors from decimal rounding (random shift)
    shift = np.random.rand(3)
    shift_mesh(mesh_1, shift)
    shift_mesh(mesh_2, shift)
    # combine the node lists and make them unique
    nodes, __, ixr = unique_rows(
        np.vstack((mesh_1["nodes"], mesh_2["nodes"])),
        decimals=decimals,
        fast=fast,
    )
    node_id_repl = range(len(ixr))
    node_offset = mesh_1["nodes"].shape[0]

    elements = {}
    material_id = {}
    element_id = {}
    offset = no_of_elements(mesh_1)

    # combine the element lists and replace the new node IDs
    for elem in ELEM_NAMES:
        if elem not in mesh_1["elements"] and elem not in mesh_2["elements"]:
            continue
        elif elem in mesh_1["elements"] and elem not in mesh_2["elements"]:
            tmp = dcp(mesh_1["elements"][elem])
            elements[elem] = replace(tmp, node_id_repl, ixr)
            material_id[elem] = mesh_1["material_id"][elem]
            element_id[elem] = mesh_1["element_id"][elem]
        elif elem not in mesh_1["elements"] and elem in mesh_2["elements"]:
            tmp = mesh_2["elements"][elem] + node_offset
            elements[elem] = replace(tmp, node_id_repl, ixr)
            material_id[elem] = mesh_2["material_id"][elem]
            element_id[elem] = mesh_2["element_id"][elem] + offset
        else:
            tmp = np.vstack(
                (
                    mesh_1["elements"][elem],
                    mesh_2["elements"][elem] + node_offset,
                )
            )
            elements[elem] = replace(tmp, node_id_repl, ixr)
            material_id[elem] = np.hstack(
                (mesh_1["material_id"][elem], mesh_2["material_id"][elem])
            )
            element_id[elem] = np.hstack(
                (
                    mesh_1["element_id"][elem],
                    mesh_2["element_id"][elem] + offset,
                )
            )
    # create the ouput dict
    out = {
        "mesh_data": mesh_1["mesh_data"],
        "nodes": nodes,
        "elements": elements,
        "material_id": material_id,
        "element_id": element_id,
    }

    # back shifting of the meshes
    shift_mesh(out, -shift)
    shift_mesh(mesh_1, -shift)
    shift_mesh(mesh_2, -shift)

    return out


def unique_nodes(mesh, decimals=3):
    """
    Make the node-list of the given mesh unique if there are duplicates.

    Parameters
    ----------
    mesh : dict
        dictionary that contains one '#FEM_MSH' block
        with the following information
            mesh_data : dict
                containing optional information about
                AXISYMMETRY (bool)
                CROSS_SECTION (bool)
                PCS_TYPE (str)
                GEO_TYPE (str)
                GEO_NAME (str)
                LAYER (int)
            nodes : ndarray
                Array with all node postions
            elements : dictionary
                contains array of nodes for elements sorted by element types
            material_id : dictionary
                contains material ids for each element sorted by element types
            element_id : dictionary
                contains element ids for each element sorted by element types
    decimals : int, optional
        Number of decimal places to round the nodes to (default: 3).
        This will not round the output, it is just for comparison of the
        node vectors.
    """
    mesh = combine(mesh, EMPTY_MSH, decimals)


### geometric routines


def get_centroids(mesh):
    """
    Calculate the centroids of the given elements.

    Parameters
    ----------
    mesh : list of dicts or single dict
        each dict containing
        at least the following keywords
            nodes : ndarray
                Array with all node postions.
            elements : dict of ndarrays
                Contains array of nodes for elements sorted by element types.

    Returns
    -------
    result : list of dictionaries or single dict of ndarrays (like 'mesh')
        Centroids of elements sorted by element types.
    """
    single = False
    if not isinstance(mesh, (list, tuple)):
        tmp_mesh = [mesh]
        single = True
    else:
        tmp_mesh = mesh

    result = []
    for mesh_i in tmp_mesh:
        out = {}
        for elem in ELEM_NAMES:
            if elem not in mesh_i["elements"]:
                continue
            points = mesh_i["nodes"][mesh_i["elements"][elem]]
            # node number needs to be first for "centroid()"
            points = np.swapaxes(points, 0, 1)
            out[elem] = centroid(elem, points)
            # this was just the centroid of the element nodes
            # out[elem] = np.mean(points, axis=1)
        result.append(out)

    if single:
        result = result[0]

    return result


def get_node_centroids(mesh):
    """
    Calculate the node centroids of the given elements.

    Parameters
    ----------
    mesh : list of dicts or single dict
        each dict containing
        at least the following keywords
            nodes : ndarray
                Array with all node postions.
            elements : dict of ndarrays
                Contains array of nodes for elements sorted by element types.

    Returns
    -------
    result : list of dictionaries or single dict of ndarrays (like 'mesh')
        Centroids of elements sorted by element types.
    """
    single = False
    if not isinstance(mesh, (list, tuple)):
        tmp_mesh = [mesh]
        single = True
    else:
        tmp_mesh = mesh

    result = []
    for mesh_i in tmp_mesh:
        out = {}
        for elem in ELEM_NAMES:
            if elem not in mesh_i["elements"]:
                continue
            points = mesh_i["nodes"][mesh_i["elements"][elem]]
            out[elem] = np.mean(points, axis=1)
        result.append(out)

    if single:
        result = result[0]

    return result


def get_volumes(mesh):
    """
    Calculate the volumes of the given elements.

    Parameters
    ----------
    mesh : list of dicts or single dict
        each dict containing
        at least the following keywords
            nodes : ndarray
                Array with all node postions.
            elements : dict of ndarrays
                Contains array of nodes for elements sorted by element types.

    Returns
    -------
    result : list of dictionaries or single dict of ndarrays (like 'mesh')
        Volumes of elements sorted by element types.
    """
    single = False
    if not isinstance(mesh, (list, tuple)):
        tmp_mesh = [mesh]
        single = True
    else:
        tmp_mesh = mesh

    result = []
    for mesh_i in tmp_mesh:
        out = {}
        for elem in ELEM_NAMES:
            if elem not in mesh_i["elements"]:
                continue
            points = mesh_i["nodes"][mesh_i["elements"][elem]]
            # node number needs to be first for "volume()"
            points = np.swapaxes(points, 0, 1)
            out[elem] = volume(elem, points)
        result.append(out)

    if single:
        result = result[0]

    return result


def get_mesh_center(mesh):
    """
    Calculate the center of the given mesh.

    Parameters
    ----------
    mesh : list of dicts or single dict
        each dict containing
        at least the following keywords
            nodes : ndarray
                Array with all node postions.
            elements : dict of ndarrays
                Contains array of nodes for elements sorted by element types.

    Returns
    -------
    result : list of dictionaries or single dict of ndarrays (like 'mesh')
        Centroids of elements sorted by element types.
    """
    if not isinstance(mesh, (list, tuple)):
        tmp_mesh = [mesh]
    else:
        tmp_mesh = mesh

    node_stack = np.empty((0, 3))
    for mesh_i in tmp_mesh:
        if mesh_i["nodes"] is not None:
            node_stack = np.vstack((node_stack, mesh_i["nodes"]))

    if node_stack.shape[0] == 0:
        return None

    return np.mean(node_stack, axis=0)


def rotate_mesh(
    mesh, angle, rotation_axis=(0.0, 0.0, 1.0), rotation_point=(0.0, 0.0, 0.0)
):
    """
    Rotate a given mesh.

    Rotation around a given point and axis with a given angle.

    Parameters
    ----------
    mesh : single dict
        dictionary containing
        at least the following keyword
            nodes : ndarray
                Array with all node postions.
    angle : float
        rotation angle given in radial length
    rotation_axis : array_like, optional
        Array containing the vector for ratation axis. Default: (0,0,1)
    rotation_point : array_like, optional
        Array containing the vector for ratation base point. Default:(0,0,0)
    """
    rot = rotation_matrix(rotation_axis, angle)
    shift_mesh(mesh, -1.0 * np.array(rotation_point))
    mesh["nodes"] = np.inner(rot, mesh["nodes"]).T
    shift_mesh(mesh, rotation_point)
    return mesh


def shift_mesh(mesh, vector):
    """
    Shift a given mesh with a given vector.

    Parameters
    ----------
    mesh : single dict
        dictionary containing
        at least the following keyword
            nodes : ndarray
                Array with all node postions.
    vector : ndarray
        array containing the shifting vector
    """
    for i in range(3):
        mesh["nodes"][:, i] += vector[i]
    return mesh


def transform_mesh(mesh, xyz_func, **kwargs):
    """
    Transform a given mesh with a given function "xyz_func".

    kwargs will be forwarded to "xyz_func".

    Parameters
    ----------
    mesh : single dict
        dictionary containing
        at least the following keyword
            nodes : ndarray
                Array with all node postions.
    xyz_func : function
        the function transforming the points:
        ``x_new, y_new, z_new = f(x_old, y_old, z_old, **kwargs)``
    """
    trans = xyz_func(
        mesh["nodes"][:, 0], mesh["nodes"][:, 1], mesh["nodes"][:, 2], **kwargs
    )
    mesh["nodes"] = np.array(trans).T
    return mesh


### misc


def no_of_elements(mesh):
    """
    Calculate the number of elements contained in the given mesh.

    Parameters
    ----------
    mesh : dict
        mesh dict containing
        at least the following keyword
            elements : dict of ndarrays
                Contains array of nodes for elements sorted by element types.

    Returns
    -------
    result : int
        number of elements
    """
    no_elem = 0
    for elem in mesh["elements"]:
        no_elem += mesh["elements"][elem].shape[0]

    return no_elem


def gen_std_elem_id(elements, id_offset=0):
    """
    Generate the standard element ids from given elements.

    Parameters
    ----------
    elements : dict of ndarrays
        Contains array of nodes for elements sorted by element types.
    id_offset : int, optional
        Here you can set a starting ID that will be set to the first element.
        Default: 0

    Returns
    -------
    element_id : dict
        contains element ids for elements, sorted by element types
    """
    element_id = {}
    offset = id_offset
    for elem in ELEM_NAMES:
        if elem not in elements:
            continue
        elem_no = elements[elem].shape[0]
        element_id[elem] = np.arange(elem_no) + offset
        offset += elem_no

    return element_id


def gen_std_mat_id(elements, mat_id=0):
    """
    Generate the standard material ids from given elements.

    Parameters
    ----------
    elements : dict of ndarrays
        Contains array of nodes for elements sorted by element types.
    mat_id : integer, optional
        Define the standard material ID. Default: 0

    Returns
    -------
    material_id : dict
        contains 0 as unique material id for elements, sorted by element types
    """
    material_id = {}
    for elem in elements:
        material_id[elem] = int(mat_id) * np.ones(
            elements[elem].shape[0], dtype=int
        )
    return material_id


def set_mat_id(mesh, mat_id=0):
    """
    Generate the standard material ids from given elements.

    Parameters
    ----------
    mesh : dict
        mesh dict containing
        at least the following keyword
            elements : dict of ndarrays
                Contains array of nodes for elements sorted by element types.

    mat_id : integer, optional
        Define the standard material ID. Default: 0
    """
    mesh["material_id"] = gen_std_mat_id(mesh["elements"], mat_id=mat_id)
