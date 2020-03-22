# -*- coding: utf-8 -*-
"""Viewer for an ogs5py mesh."""
import os
import numpy as np
from ogs5py.fileclasses.msh.msh_io import export_mesh
from ogs5py.tools.download import TemporaryDirectory

# os.environ["QT_API"] = "pyqt"
# os.environ["ETS_TOOLKIT"] = "qt4"

MAYA_AVAIL = True
try:
    from mayavi import mlab
except ImportError:
    MAYA_AVAIL = False


def show_mesh(
    mesh,
    show_cell_data=None,
    show_material_id=False,
    show_element_id=False,
    log_scale=False,
):
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
    show_cell_data : ndarray or dict, optional
        Here you can specify additional element/cell data sorted by their IDs.
        It can be a dictionary with data-name as key and the ndarray as value.
        Default: None
    show_material_id : bool, optional
        Here you can specify if the material_id should be shown.
        Default: False
    show_element_id : bool, optional
        Here you can specify if the element_id should be shown.
        Default: False
    log_scale : bool, optional
        State if the cell_data should be shown in log scale.
        Default: False

    Notes
    -----
    This routine needs "mayavi" to display the mesh.
    (see here: https://github.com/enthought/mayavi)
    """
    # stop if mayavi is not installed
    if not MAYA_AVAIL:
        print("Could not import 'mayavi'!")
        return None

    if show_cell_data is not None:
        if not isinstance(show_cell_data, dict):
            cell_data_name = "add_data"
        else:
            cell_data_name = list(show_cell_data)[0]

    # new mayavi scenes
    mlab.figure()
    with TemporaryDirectory() as tmpdirname:
        vtkfile = os.path.join(tmpdirname, "data.vtk")
        # export the mesh to the temp vtk file
        export_mesh(
            vtkfile,
            mesh,
            export_material_id=show_material_id,
            export_element_id=show_element_id,
            cell_data_by_id=show_cell_data,
        )
        # load the vtk file to mayavi's mlab
        data_source = mlab.pipeline.open(vtkfile)
        # create a surface out of the vtk source
        surface = mlab.pipeline.surface(data_source)
    # make the edges visible
    surface.actor.property.edge_visibility = True
    surface.actor.property.line_width = 1.0
    surface.actor.property.interpolation = "flat"
    if show_cell_data is not None:
        surface.parent.parent._cell_scalars_name_changed(cell_data_name)
        surface.parent.parent.update()
        surface.parent.scalar_lut_manager.shadow = True
        surface.actor.property.edge_visibility = False
        surface.parent.scalar_lut_manager.lut_mode = "RdYlBu"
        surface.parent.scalar_lut_manager.show_scalar_bar = True
        if log_scale:
            surface.parent.scalar_lut_manager.lut.scale = "log10"
    elif show_material_id:
        # set the bounds for the color range
        min_id = np.inf
        max_id = 0.0
        for matid in mesh["material_id"]:
            min_id = int(np.min((min_id, np.min(mesh["material_id"][matid]))))
            max_id = int(np.max((max_id, np.max(mesh["material_id"][matid]))))
        id_no = int(max_id - min_id + 1)
        surface.parent.parent._cell_scalars_name_changed("material_id")
        surface.parent.parent.update()
        surface.parent.scalar_lut_manager.use_default_range = False
        surface.parent.scalar_lut_manager.data_range = [min_id, max_id + 1]
        surface.parent.scalar_lut_manager.number_of_colors = max(id_no, 2)
        surface.parent.scalar_lut_manager.number_of_labels = 2
        surface.parent.scalar_lut_manager.use_default_name = False
        surface.parent.scalar_lut_manager.data_name = "Material ID"
        surface.parent.scalar_lut_manager.shadow = True
        surface.parent.scalar_lut_manager.lut_mode = "rainbow"
        surface.parent.scalar_lut_manager.show_scalar_bar = True
        surface.parent.scalar_lut_manager.scalar_bar.label_format = "%.0f"
    elif show_element_id:
        surface.parent.parent._cell_scalars_name_changed("element_id")
        surface.parent.parent.update()
        surface.parent.scalar_lut_manager.number_of_labels = 2
        surface.parent.scalar_lut_manager.use_default_name = False
        surface.parent.scalar_lut_manager.data_name = "Element ID"
        surface.parent.scalar_lut_manager.shadow = True
        surface.parent.scalar_lut_manager.lut_mode = "RdYlBu"
        surface.parent.scalar_lut_manager.show_scalar_bar = True
        surface.parent.scalar_lut_manager.scalar_bar.label_format = "%.0f"
    else:
        surface.actor.mapper.scalar_visibility = False
    # give it a name
    surface.name = "OGS mesh"
    # show it
    mlab.show()
    return surface
