# -*- coding: utf-8 -*-
"""GMSH helpers."""

import subprocess
import tempfile
from pathlib import Path

import meshio
import numpy

MESHIO_VERSION = list(map(int, meshio.__version__.split(".")[:2]))


def _get_gmsh_exe():
    macos_gmsh_location = Path("/Applications/Gmsh.app/Contents/MacOS/gmsh")
    return macos_gmsh_location if macos_gmsh_location.is_file() else "gmsh"


def generate_mesh(
    geo_code,
    verbose=True,
    dim=3,
    prune_vertices=True,
    gmsh_path=None,
    extra_gmsh_arguments=None,
):
    """
    Generate a mesh with gmsh.

    Return a meshio.Mesh, storing the mesh points, cells, and data, generated by Gmsh
    from the `geo_code`, written to a temporary file, and reread by `meshio`.
    """
    if extra_gmsh_arguments is None:
        extra_gmsh_arguments = []

    with tempfile.NamedTemporaryFile(suffix=".geo") as f:
        geo_filename = f.name

    with open(geo_filename, "w") as f:
        f.write("\n".join(geo_code))

    with tempfile.NamedTemporaryFile(suffix=".msh") as f:
        msh_filename = f.name

    gmsh_executable = gmsh_path if gmsh_path is not None else _get_gmsh_exe()

    args = [
        f"-{dim}",
        geo_filename,
        "-format",
        "msh",
        "-bin",
        "-o",
        msh_filename,
    ] + extra_gmsh_arguments

    # https://stackoverflow.com/a/803421/353337
    try:
        p = subprocess.Popen(
            [gmsh_executable] + args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
    except FileNotFoundError:
        print("Is gmsh installed?")
        raise

    if verbose:
        while True:
            line = p.stdout.readline()
            if not line:
                break
            print(line.decode("utf-8"), end="")

    p.communicate()
    assert (
        p.returncode == 0
    ), "Gmsh exited with error (return code {}).".format(p.returncode)

    mesh = meshio.read(msh_filename)

    if prune_vertices:
        # Make sure to include only those vertices which belong to a cell.
        ncells = numpy.concatenate(
            [
                numpy.concatenate(c[1] if MESHIO_VERSION < [5, 1] else c.data)
                for c in mesh.cells
            ]
        )
        uvertices, uidx = numpy.unique(ncells, return_inverse=True)

        k = 0
        cells = []
        for cellblock in mesh.cells:
            key = cellblock[0] if MESHIO_VERSION < [5, 1] else cellblock.type
            data = cellblock[1] if MESHIO_VERSION < [5, 1] else cellblock.data
            n = numpy.prod(cellblock.data.shape)
            cells.append(
                meshio.CellBlock(
                    key,
                    uidx[k : k + n].reshape(data.shape),
                )
            )
            k += n
        mesh.cells = cells

        mesh.points = mesh.points[uvertices]
        for key in mesh.point_data:
            mesh.point_data[key] = mesh.point_data[key][uvertices]

    # clean up
    Path(msh_filename).unlink()
    Path(geo_filename).unlink()

    return mesh
