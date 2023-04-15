# -*- coding: utf-8 -*-
"""Viewer for a vtk file."""
# import os
# os.environ["QT_API"] = "pyqt"
# os.environ["ETS_TOOLKIT"] = "qt4"

MAYA_AVAIL = True
try:
    from mayavi import mlab
except ImportError:
    MAYA_AVAIL = False


def show_vtk(vtkfile, log_scale=False):
    """
    Display a given mesh colored by its material ID.

    Parameters
    ----------
    vtkfile : :class:`str`
        Path to the vtk/vtu file to show.
    log_scale : bool, optional
        State if the data should be shown in log scale.
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
    # new mayavi scenes
    mlab.figure()
    # load the vtk file to mayavi's mlab
    data_source = mlab.pipeline.open(vtkfile)
    # create a surface out of the vtk source
    surface = mlab.pipeline.surface(data_source)
    # make the edges visible
    surface.actor.property.edge_visibility = False
    surface.actor.property.line_width = 1.0
    surface.actor.property.interpolation = "flat"
    # show legend
    try:
        surface.parent.scalar_lut_manager.lut_mode = "viridis"
        surface.parent.scalar_lut_manager.shadow = True
        surface.parent.scalar_lut_manager.show_scalar_bar = True
        if log_scale:
            surface.parent.scalar_lut_manager.lut.scale = "log10"
    except:
        pass
    # give it a name
    surface.name = "VTK-File"
    # show it
    mlab.show()
    return surface
