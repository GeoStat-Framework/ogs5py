# -*- coding: utf-8 -*-
"""
Viewer for ogs5py-mesh.

@author: sebastian
"""
from __future__ import division, print_function, absolute_import
import os
import tempfile
import numpy as np
from ogs5py.fileclasses.msh.tools import export_mesh

os.environ["QT_API"] = "pyqt"
os.environ["ETS_TOOLKIT"] = "qt4"

MAYA_AVAIL = True
try:
    from mayavi import mlab
except ImportError:
    MAYA_AVAIL = False


def show_mesh(mesh, show_element_id=True):
    """
    Display a given mesh colored by its material ID.

    Parameters
    ----------
    mesh : dict
        dictionary contains one '#FEM_MSH' block of the mesh file
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
                contains array of nodelists for elements sorted by element type
            material_id : dictionary
                contains material ids for each element sorted by element types
            element_id : dictionary
                contains element ids for each element sorted by element types
    show_element_id : bool, optional
        Here you can specify if the mesh should be colored by material_id.
        Default: True

    Notes
    -----
    This routine needs "mayavi" to display the mesh.
    (see here: https://github.com/enthought/mayavi)
    """
    # stop if mayavi is not installed
    if not MAYA_AVAIL:
        print("Could not import 'mayavi'!")
        print(
            "..if you are running an IPython console"
            + ", don't run it under qt5. Mayavi still uses qt4."
        )
        return

    # close all mayavi scenes
    mlab.close(all=True)
    # set the bounds for the color range
    min_id = np.inf
    max_id = 0.0
    for matid in mesh["material_id"]:
        min_id = np.min((min_id, np.min(mesh["material_id"][matid])))
        max_id = np.max((max_id, np.max(mesh["material_id"][matid])))
    id_no = int(max_id - min_id + 1)
    # create a temp-file which contains a vtk version of the mesh
    vtkfile = tempfile.NamedTemporaryFile(suffix=".vtk")
    # export the mesh to the temp vtk file
    export_mesh(vtkfile.name, mesh, export_material_id=show_element_id)
    print("temp vtk file for mayavi:")
    print(vtkfile.name)
    # load the vtk file to mayavi's mlab
    data_source = mlab.pipeline.open(vtkfile.name)
    # create a surface out of the vtk source
    surface = mlab.pipeline.surface(data_source)
    # make the edges visible
    surface.actor.property.edge_visibility = True
    surface.actor.property.line_width = 1.0
    surface.actor.property.interpolation = "flat"
    # settings for the material ID
    #    surface.parent.scalar_lut_manager.lut_mode = "Set1"
    if show_element_id:
        surface.parent.scalar_lut_manager.use_default_range = False
        surface.parent.scalar_lut_manager.data_range = [min_id, max_id]
        surface.parent.scalar_lut_manager.number_of_colors = max(id_no, 2)
        surface.parent.scalar_lut_manager.number_of_labels = min(id_no, 64)
        surface.parent.scalar_lut_manager.use_default_name = False
        surface.parent.scalar_lut_manager.data_name = "Material ID"
        surface.parent.scalar_lut_manager.shadow = True
        surface.parent.scalar_lut_manager.show_scalar_bar = True
        surface.parent.scalar_lut_manager.scalar_bar.label_format = "%.0f"
    #        mlab.colorbar(surface, orientation='vertical', label_fmt='%.0f')
    # give it a name
    surface.name = "OGS mesh"
    # show it
    mlab.show()
    # close the temp file and delete it
    vtkfile.close()
