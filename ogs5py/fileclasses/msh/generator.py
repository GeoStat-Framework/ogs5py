# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
Generators for the ogs MESH file.

.. currentmodule:: ogs5py.fileclasses.msh.generator

Generators
^^^^^^^^^^
These generators can be called with :any:`MSH.generate`

.. autosummary::
   rectangular
   radial
   grid_adapter2D
   grid_adapter3D
   block_adapter3D
   generate_gmsh

----
"""
from __future__ import division, print_function, absolute_import

import numpy as np

from ogs5py.fileclasses.msh.tools import (
    convert_meshio,
    combine,
    gen_std_elem_id,
    gen_std_mat_id,
)
from ogs5py.fileclasses.msh.gmsh import (
    gmsh_grid_adapt2D,
    gmsh_grid_adapt3D,
    gmsh_block_adapt3D,
    gmsh_code,
)


def rectangular(
    dim=2,
    mesh_origin=(0.0, 0.0, 0.0),
    element_no=(10, 10, 10),
    element_size=(1.0, 1.0, 1.0),
):
    """
    generate a rectangular grid in 2D or 3D

    Parameters
    ----------
    dim : int, optional
        Dimension of the resulting mesh, either 2 or 3. Default: 3
    mesh_origin : list of float, optional
        Origin of the mesh Default: [0.0, 0.0, 0.0]
    element_no : list of int, optional
        Number of elements in each direction. Default: [10, 10, 10]
    element_size : list of float, optional
        Size of an element in each direction. Default: [1.0 ,1.0 ,1.0]

    Returns
    -------
    result : dictionary
        Result contains one '#FEM_MSH' block of the OGS mesh file
        with the following information (sorted by keys):

            mesh_data : dict
                dictionary containing information about

                - AXISYMMETRY (bool)
                - CROSS_SECTION (bool)
                - PCS_TYPE (str)
                - GEO_TYPE (str)
                - GEO_NAME (str)
                - LAYER (int)

            nodes : ndarray
                Array with all node postions
            elements : dict
                contains nodelists for elements sorted by element types
            material_id : dict
                contains material ids for each element sorted by element types
            element_id : dict
                contains element ids for each element sorted by element types
    """
    x_no = element_no[0]
    dx = element_size[0]
    x0 = mesh_origin[0]
    y_no = element_no[1]
    dy = element_size[1]
    y0 = mesh_origin[1]
    if len(mesh_origin) > 2:
        z0 = mesh_origin[2]
    else:
        z0 = 0.0

    if dim == 2:
        z_no = 0
        dz = 0.0
        node_no = (x_no + 1) * (y_no + 1)
        node_per_elem = 4
        element_no = x_no * y_no
    elif dim == 3:
        z_no = element_no[2]
        dz = element_size[2]
        node_no = (x_no + 1) * (y_no + 1) * (z_no + 1)
        node_per_elem = 8
        element_no = x_no * y_no * z_no
    else:
        raise ValueError("generator.rectangular: dim has to be either 2 or 3")

    node_arr = np.zeros((node_no, 3))
    element_arr = np.zeros((element_no, node_per_elem), dtype=int)

    node_arr[:, 0] = (
        dx * ((np.arange(node_no) % ((x_no + 1) * (y_no + 1))) % (x_no + 1))
        + x0
    )
    node_arr[:, 1] = (
        dy * ((np.arange(node_no) % ((x_no + 1) * (y_no + 1))) // (x_no + 1))
        + y0
    )
    node_arr[:, 2] = (
        dz * (np.arange(node_no) // ((x_no + 1) * (y_no + 1))) + z0
    )

    if dim == 2:
        element_arr[:, 0] = np.arange(element_no)
        element_arr[:, 0] += np.arange(element_no) // (x_no)
        element_arr[:, 1] = element_arr[:, 0] + 1
        element_arr[:, 2] = element_arr[:, 0]
        element_arr[:, 2] += 2 + x_no
        element_arr[:, 3] = element_arr[:, 2] - 1
        element_dict = {"quad": element_arr}
    else:
        element_arr[:, 0] = np.arange(element_no)
        element_arr[:, 0] += (x_no + y_no + 1) * (
            np.arange(element_no) // (x_no * y_no)
        )
        element_arr[:, 0] += (np.arange(element_no) % (x_no * y_no)) // (x_no)
        element_arr[:, 1] = element_arr[:, 0] + 1
        element_arr[:, 2] = element_arr[:, 0]
        element_arr[:, 2] += 2 + x_no
        element_arr[:, 3] = element_arr[:, 2] - 1
        element_arr[:, 4] = element_arr[:, 0]
        element_arr[:, 4] += (1 + x_no) * (1 + y_no)
        element_arr[:, 5] = element_arr[:, 4] + 1
        element_arr[:, 6] = element_arr[:, 4]
        element_arr[:, 6] += 2 + x_no
        element_arr[:, 7] = element_arr[:, 6] - 1
        element_dict = {"hex": element_arr}

    out = {
        "mesh_data": {},
        "nodes": node_arr,
        "elements": element_dict,
        "material_id": gen_std_mat_id(element_dict),
        "element_id": gen_std_elem_id(element_dict),
    }

    return out


def radial(
    dim=3,
    mesh_origin=(0.0, 0.0, 0.0),
    angles=16,
    rad=np.arange(11),
    z_arr=-np.arange(2),
):
    """
    generate a radial grid in 2D or 3D

    Parameters
    ----------
    dim : int, optional
        Dimension of the resulting mesh, either 2 or 3. Default: 3
    mesh_origin : list of float, optional
        Origin of the mesh Default: [0.0, 0.0, 0.0]
    angles : int, optional
        Number of elements in each direction. Default: [10, 10, 10]
    rad : array, optional
        array of radii to set in the mesh
    z_arr : array, optional
        array of z values to set the layers in the mesh (only needed for dim=3)
        needs to be sorted in negative z direction

    Returns
    -------
    result : dictionary
        Result contains one '#FEM_MSH' block of the OGS mesh file
        with the following information (sorted by keys):

            mesh_data : dict
                dictionary containing information about

                - AXISYMMETRY (bool)
                - CROSS_SECTION (bool)
                - PCS_TYPE (str)
                - GEO_TYPE (str)
                - GEO_NAME (str)
                - LAYER (int)

            nodes : ndarray
                Array with all node postions
            elements : dict
                contains nodelists for elements sorted by element types
            material_id : dict
                contains material ids for each element sorted by element types
            element_id : dict
                contains element ids for each element sorted by element types
    """

    if z_arr is not None and dim > 2:
        assert (
            all(z_arr[i] > z_arr[i + 1] for i in range(len(z_arr) - 1))
        ) or (
            all(z_arr[i] < z_arr[i + 1] for i in range(len(z_arr) - 1))
        ), "The z-array needs to be sorted"
        # flip the z_array if it is sorted downwards
        if all(z_arr[i] > z_arr[i + 1] for i in range(len(z_arr) - 1)):
            z_arr = z_arr[::-1]

    assert all(
        rad[i] < rad[i + 1] for i in range(len(rad) - 1)
    ), "The radii need to be sorted"

    if len(mesh_origin) > 2:
        x0, y0, z0 = mesh_origin
    else:
        x0, y0, z0 = mesh_origin + (0.0,)

    if float(rad[0]) == 0.0:
        closed = True
        rad = rad[1:]
    else:
        closed = False
    r_no = len(rad)
    if z_arr is not None and dim > 2:
        z_no = len(z_arr)
    else:
        z_no = 0
    lay_no = r_no * angles

    if dim == 2:
        node_no = angles * r_no
        element_no = angles * (r_no - 1)
        if closed:
            node_no += 1
            elem_mid_arr = np.zeros((angles, 3), dtype=np.int)

        element_arr = np.zeros((element_no, 4), dtype=np.int)
        node_arr = np.zeros((node_no, 3))

        for ri, re in enumerate(rad):
            for n in range(angles):
                no = n + ri * angles
                node_arr[no, :] = [
                    x0 + re * np.cos(n / angles * 2 * np.pi),
                    y0 + re * np.sin(n / angles * 2 * np.pi),
                    z0,
                ]

        if closed:
            node_arr[-1, :] = [x0, y0, z0]

        element_arr[:, 0] = np.arange(element_no)
        element_arr[:, 3] = np.arange(element_no) // angles * angles
        element_arr[:, 3] += (np.arange(element_no) % angles + 1) % angles
        element_arr[:, 2] = element_arr[:, 3] + angles
        element_arr[:, 1] = element_arr[:, 0] + angles
        element_dict = {"quad": element_arr}
        if closed:
            elem_mid_arr[:, 0] = np.arange(angles)
            elem_mid_arr[:, 1] = (np.arange(angles) + 1) % angles
            elem_mid_arr[:, 2] = node_no - 1
            element_dict["tri"] = elem_mid_arr

    elif dim == 3:
        node_no = angles * r_no * z_no
        element_no = angles * (r_no - 1) * (z_no - 1)
        if closed:
            node_no += z_no
            elem_mid_arr = np.zeros((angles * (z_no - 1), 6), dtype=np.int)

        element_arr = np.zeros((element_no, 8), dtype=np.int)
        node_arr = np.zeros((node_no, 3))

        # write nodes
        for z in range(z_no):
            for ri, re in enumerate(rad):
                for n in range(angles):
                    no = n + ri * angles + z * r_no * angles
                    node_arr[no, :] = [
                        x0 + re * np.cos(n / angles * 2 * np.pi),
                        y0 + re * np.sin(n / angles * 2 * np.pi),
                        z0 + z_arr[z],
                    ]
        # add center as last points
        if closed:
            node_arr[-z_no:, 0] = x0
            node_arr[-z_no:, 1] = y0
            node_arr[-z_no:, 2] = z_arr

        # write elements
        for z in range(z_no - 1):
            for r in range(r_no - 1):
                for n in range(angles):
                    no = n + r * angles + z * (r_no - 1) * angles
                    no1 = n + r * angles + z * r_no * angles
                    no2 = no1 + angles
                    no4 = (n + 1) % angles + r * angles + z * r_no * angles
                    no3 = no4 + angles
                    element_arr[no, :] = [
                        no1,
                        no2,
                        no3,
                        no4,
                        no1 + lay_no,
                        no2 + lay_no,
                        no3 + lay_no,
                        no4 + lay_no,
                    ]
        element_dict = {"hex": element_arr}

        # add the center pris
        if closed:
            for z in range(z_no - 1):
                for n in range(angles):
                    no = n + z * angles
                    no1 = n + z * r_no * angles
                    no2 = node_no - z_no + z
                    no3 = (n + 1) % angles + z * r_no * angles
                    elem_mid_arr[no, :] = [
                        no1 + lay_no,
                        no2 + 1,
                        no3 + lay_no,
                        no1,
                        no2,
                        no3,
                    ]
            element_dict["pris"] = elem_mid_arr

    out = {
        "mesh_data": {},
        "nodes": node_arr,
        "elements": element_dict,
        "material_id": gen_std_mat_id(element_dict),
        "element_id": gen_std_elem_id(element_dict),
    }

    return out


def grid_adapter2D(
    out_dim=(100.0, 100.0),
    in_dim=(50.0, 50.0),
    out_res=(10.0, 10.0),
    in_res=(1.0, 1.0),
    out_pos=(0.0, 0.0),
    in_pos=(25.0, 25.0),
    z_pos=0.0,
    in_mat=0,
    out_mat=0,
    fill=False,
):
    """
    generate a grid adapter in 2D from an outer grid resolution
    to an inner grid resolution with gmsh.

    Parameters
    ----------
    out_dim : list of 2 float
        xy-Dimension of the outer block
    in_dim : list of 2 float
        xy-Dimension of the inner block
    out_res : list of 2 float
        Grid resolution of the outer block
    in_res : list of 2 float
        Grid resolution of the inner block
    out_pos : list of 2 float
        xy-Position of the origin of the outer block
    in_pos : list of 2 float
        xy-Position of the origin of the inner block
    z_pos : float
        z-Position of the origin of the whole block
    in_mat : integer
        Material-ID of the inner block
    out_mat : integer
        Material-ID of the outer block
    fill : bool, optional
        State if the inner block should be filled with a rectangular mesh.
        Default: False.

    Returns
    -------
    result : dictionary
        Result contains one '#FEM_MSH' block of the OGS mesh file
        with the following information (sorted by keys):

            mesh_data : dict
                dictionary containing information about

                - AXISYMMETRY (bool)
                - CROSS_SECTION (bool)
                - PCS_TYPE (str)
                - GEO_TYPE (str)
                - GEO_NAME (str)
                - LAYER (int)

            nodes : ndarray
                Array with all node postions
            elements : dict
                contains nodelists for elements sorted by element types
            material_id : dict
                contains material ids for each element sorted by element types
            element_id : dict
                contains element ids for each element sorted by element types

    """
    import pygmsh as pg

    geo = gmsh_grid_adapt2D(
        out_dim, in_dim, out_res, in_res, out_pos, in_pos, z_pos
    )
    mesh = pg.generate_mesh(geo, dim=2)
    out = convert_meshio(mesh.points, mesh.cells, import_dim=2)
    out["material_id"] = gen_std_mat_id(out["elements"], out_mat)

    if fill:
        element_no = [int(in_dim[0] / in_res[0]), int(in_dim[1] / in_res[1])]
        mesh_in = rectangular(
            dim=2,
            mesh_origin=in_pos + (z_pos,),
            element_no=element_no,
            element_size=in_res,
        )
        mesh_in["material_id"] = gen_std_mat_id(mesh_in["elements"], in_mat)
        dec = int(np.ceil(-np.log10(min(min(in_res), min(out_res)))) + 2.0) * 2
        out = combine(mesh_in, out, dec)

    return out


def grid_adapter3D(
    out_dim=(100.0, 100.0),
    in_dim=(50.0, 50.0),
    z_dim=-10.0,
    out_res=(10.0, 10.0, 10.0),
    in_res=(5.0, 5.0, 5.0),
    out_pos=(0.0, 0.0),
    in_pos=(25.0, 25.0),
    z_pos=0.0,
    in_mat=0,
    out_mat=0,
    fill=False,
):
    """
    generate a grid adapter in 3D from an outer grid resolution
    to an inner grid resolution with gmsh.

    Parameters
    ----------
    out_dim : list of 2 float
        xy-Dimension of the outer block
    in_dim : list of 2 float
        xy-Dimension of the inner block
    z_dim : float
        z-Dimension of the whole block
    out_res : list of 3 float
        Grid resolution of the outer block
    in_res : list of 3 float
        Grid resolution of the inner block
    out_pos : list of 2 float
        xy-Position of the origin of the outer block
    in_pos : list of 2 float
        xy-Position of the origin of the inner block
    z_dim : float
        z-Position of the origin of the whole block
    in_mat : integer
        Material-ID of the inner block
    out_mat : integer
        Material-ID of the outer block
    fill : bool, optional
        State if the inner block should be filled with a rectangular mesh.
        Default: False.

    Returns
    -------
    result : dictionary
        Result contains one '#FEM_MSH' block of the OGS mesh file
        with the following information (sorted by keys):

            mesh_data : dict
                dictionary containing information about

                - AXISYMMETRY (bool)
                - CROSS_SECTION (bool)
                - PCS_TYPE (str)
                - GEO_TYPE (str)
                - GEO_NAME (str)
                - LAYER (int)

            nodes : ndarray
                Array with all node postions
            elements : dict
                contains nodelists for elements sorted by element types
            material_id : dict
                contains material ids for each element sorted by element types
            element_id : dict
                contains element ids for each element sorted by element types

    """
    import pygmsh as pg

    geo = gmsh_grid_adapt3D(
        out_dim, in_dim, z_dim, out_res, in_res, out_pos, in_pos, z_pos
    )
    mesh = pg.generate_mesh(geo)
    out = convert_meshio(mesh.points, mesh.cells, import_dim=3)
    out["material_id"] = gen_std_mat_id(out["elements"], out_mat)

    if fill:
        element_no = [
            int(in_dim[0] / in_res[0]),
            int(in_dim[1] / in_res[1]),
            int(abs(z_dim) / in_res[2]),
        ]
        mesh_in = rectangular(
            dim=3,
            mesh_origin=in_pos + (z_pos + min(z_dim, 0.0),),
            element_no=element_no,
            element_size=in_res,
        )
        mesh_in["material_id"] = gen_std_mat_id(mesh_in["elements"], in_mat)
        dec = int(np.ceil(-np.log10(min(min(in_res), min(out_res)))) + 2.0) * 2
        out = combine(mesh_in, out, dec)

    return out


def block_adapter3D(xy_dim=10.0, z_dim=5.0, in_res=1.0):
    """
    generate a block adapter that has a given resolution at the
    southern side with gmsh.

    Parameters
    ----------
    xy_dim : float
        xy-Dimension of the whole block
    z_dim : float
        z-Dimension of the whole block
    in_res : float
        Grid resolution at the southern side of the block

    Returns
    -------
    result : dictionary
        Result contains one '#FEM_MSH' block of the OGS mesh file
        with the following information (sorted by keys):

            mesh_data : dict
                dictionary containing information about

                - AXISYMMETRY (bool)
                - CROSS_SECTION (bool)
                - PCS_TYPE (str)
                - GEO_TYPE (str)
                - GEO_NAME (str)
                - LAYER (int)

            nodes : ndarray
                Array with all node postions
            elements : dict
                contains nodelists for elements sorted by element types
            material_id : dict
                contains material ids for each element sorted by element types
            element_id : dict
                contains element ids for each element sorted by element types
    """
    import pygmsh as pg

    geo = gmsh_block_adapt3D(xy_dim, z_dim, in_res)
    mesh = pg.generate_mesh(geo)
    out = convert_meshio(mesh.points, mesh.cells, import_dim=3)
    return out


def generate_gmsh(path_or_code, import_dim=(1, 2, 3)):
    """
    generate mesh from gmsh code or gmsh .geo file.

    Parameters
    ----------
    path_or_code : str or list of str
        Either path to the gmsh .geo file or list of codelines for a .geo file.
    import_dim : iterable of int or single int, optional
        State which elements should be imported by dimensionality.
        Default: (1, 2, 3)

    Returns
    -------
    result : dictionary
        Result contains one '#FEM_MSH' block of the OGS mesh file
        with the following information (sorted by keys):

            mesh_data : dict
                dictionary containing information about

                - AXISYMMETRY (bool)
                - CROSS_SECTION (bool)
                - PCS_TYPE (str)
                - GEO_TYPE (str)
                - GEO_NAME (str)
                - LAYER (int)

            nodes : ndarray
                Array with all node postions
            elements : dict
                contains nodelists for elements sorted by element types
            material_id : dict
                contains material ids for each element sorted by element types
            element_id : dict
                contains element ids for each element sorted by element types
    """
    import pygmsh as pg

    geo = gmsh_code(path_or_code)
    mesh = pg.generate_mesh(geo)
    out = convert_meshio(mesh.points, mesh.cells, import_dim=import_dim)
    return out
