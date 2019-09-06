# -*- coding: utf-8 -*-
"""
Generators for the ogs GEOMETRY file.

.. currentmodule:: ogs5py.fileclasses.gli.generator

Generators
^^^^^^^^^^
These generators can be called with :any:`GLI.generate`

.. autosummary::
   rectangular
   radial

----
"""
from __future__ import division, print_function, absolute_import

import numpy as np

from ogs5py.fileclasses.gli.core import GLI as gli


def rectangular(
    dim=2, ori=(0.0, 0.0, 0.0), size=(10.0, 10.0, 10.0), name="boundary"
):
    """
    Generate a rectangular boundary for a grid in 2D or 3D as gli.

    Parameters
    ----------
    dim : int, optional
        Dimension of the resulting mesh, either 2 or 3. Default: 3
    ori : list of float, optional
        Origin of the mesh Default: [0.0, 0.0, 0.0]
    size : list of float, optional
        Size of the mesh Default: [10.0, 10.0, 10.0]
    name : str, optional
        Name of the boundary. In 3D there will be 4 surfaces where the
        names are generated by adding an ID: "_0", "_1", "_2", "_3"
        Default: "boundary"

    Returns
    -------
    result : gli
    """
    ori = np.array(ori)
    if ori.shape[0] == 2:
        ori = np.hstack((ori, 0.0))
    size = np.array(size)
    if size.shape[0] == 2:
        size = np.hstack((size, 0.0))
    size_x = np.array([size[0], 0.0, 0.0])
    size_y = np.array([0.0, size[1], 0.0])
    size_z = np.array([0.0, 0.0, size[2]])
    size_xy = size_x + size_y
    size_xz = size_x + size_z
    size_yz = size_y + size_z
    size_xyz = np.array(size)
    out = gli()
    if dim == 2:
        points = np.array([ori, ori + size_x, ori + size_xy, ori + size_y])
        out.add_polyline(name, points, closed=True)
    if dim == 3:
        pnt = []
        #        directions = ["s", "w", "n", "e"]
        directions = ["0", "1", "2", "3"]
        pnt.append(np.array([ori, ori + size_x, ori + size_xz, ori + size_z]))
        pnt.append(
            np.array(
                [ori + size_x, ori + size_xy, ori + size_xyz, ori + size_xz]
            )
        )
        pnt.append(
            np.array(
                [ori + size_xy, ori + size_y, ori + size_yz, ori + size_xyz]
            )
        )
        pnt.append(np.array([ori + size_y, ori, ori + size_z, ori + size_yz]))
        ply_names = [name + "_ply_" + direction for direction in directions]

        for i, ply_name in enumerate(ply_names):
            out.add_polyline(ply_name, pnt[i], closed=True)
            out.add_surface(name + "_" + directions[i], [ply_name])

    return out()


def radial(
    dim=3,
    ori=(0.0, 0.0, 0.0),
    angles=16,
    rad_out=10.0,
    rad_in=None,
    z_size=-1.0,
    name_out="boundary",
    name_in="well",
):
    """
    Generate a radial boundary for a grid in 2D or 3D.

    Parameters
    ----------
    dim : int, optional
        Dimension of the resulting mesh, either 2 or 3. Default: 3
    ori : list of float, optional
        Origin of the mesh Default: [0.0, 0.0, 0.0]
    angles : int, optional
        Number of angles. Default: 16
    rad_out : float, optional
        Radius of the outer boundary, Default: 10.
    rad_out : float or None, optional
        Radius of the inner boundary if needed. (i.e. the well)
    z_size : float, optional
        size of the mesh in z-direction
    name_out : str, optional
        Name of the outer boundary. In 3D there will be as many surfaces as
        angles are given. Their names are generated by adding the angle
        number: "_0", "_1", ...
        Default: "boundary"
    name_in : str, optional
        Name of the inner boundary. In 3D there will be as many surfaces as
        angles are given. Their names are generated by adding the angle
        number: "_0", "_1", ...
        Default: "well"

    Returns
    -------
    result : gli
    """
    out = gli()

    if dim == 2:
        points = np.array(
            [
                [
                    ori[0] + rad_out * np.cos(n / angles * 2 * np.pi),
                    ori[1] + rad_out * np.sin(n / angles * 2 * np.pi),
                    ori[2],
                ]
                for n in range(angles)
            ]
        )
        out.add_polyline(name_out, points, closed=True)

        if rad_in is not None:
            points = np.array(
                [
                    [
                        ori[0] + rad_in * np.cos(n / angles * 2 * np.pi),
                        ori[1] + rad_in * np.sin(n / angles * 2 * np.pi),
                        ori[2],
                    ]
                    for n in range(angles)
                ]
            )
            out.add_polyline(name_in, points, closed=True)

    if dim == 3:
        pnt_top = np.array(
            [
                [
                    ori[0] + rad_out * np.cos(n / angles * 2 * np.pi),
                    ori[1] + rad_out * np.sin(n / angles * 2 * np.pi),
                    ori[2],
                ]
                for n in range(angles)
            ]
        )
        pnt_top = np.vstack((pnt_top, pnt_top[0]))
        pnt_bot = np.copy(pnt_top)
        pnt_bot[:, 2] += z_size

        if rad_in is not None:
            pnt_top_in = np.array(
                [
                    [
                        ori[0] + rad_in * np.cos(n / angles * 2 * np.pi),
                        ori[1] + rad_in * np.sin(n / angles * 2 * np.pi),
                        ori[2],
                    ]
                    for n in range(angles)
                ]
            )
            pnt_top_in = np.vstack((pnt_top_in, pnt_top_in[0]))
            pnt_bot_in = np.copy(pnt_top_in)
            pnt_top_in[:, 2] += z_size

        for i in range(angles):
            pnt = np.array(
                [pnt_top[i], pnt_top[i + 1], pnt_bot[i + 1], pnt_bot[i]]
            )
            out.add_polyline(name_out + "_ply_" + str(i), pnt, closed=True)
            out.add_surface(
                name_out + "_" + str(i), [name_out + "_ply_" + str(i)]
            )
            if rad_in is not None:
                pnt = np.array(
                    [
                        pnt_top_in[i],
                        pnt_top_in[i + 1],
                        pnt_bot_in[i + 1],
                        pnt_bot_in[i],
                    ]
                )
                out.add_polyline(name_in + "_ply_" + str(i), pnt, closed=True)
                out.add_surface(
                    name_in + "_" + str(i), [name_in + "_ply_" + str(i)]
                )

    return out()
