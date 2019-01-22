# -*- coding: utf-8 -*-
"""
Simple interface to pygmsh.
"""
from __future__ import division, print_function, absolute_import


def gmsh_code(path_or_code):
    """
    Generate mesh with gmsh.
    """
    try:
        from pygmsh import Geometry
    except ImportError:
        from pygmsh.built_in import Geometry

    geo = Geometry()
    if isinstance(path_or_code, list):
        code = map(str, path_or_code)
    else:
        try:
            with open(path_or_code, "r") as gmsh_f:
                code = gmsh_f.readlines()
        except (OSError, IOError):
            print("gmsh_code: could not read file...")
            return geo
    geo.add_raw_code(code)
    return geo


def gmsh_block_adapt3D(xy_dim=10.0, z_dim=5.0, in_res=1.0):
    """
    Generate the mesh adapter.
    """
    try:
        from pygmsh import Geometry
    except ImportError:
        from pygmsh.built_in import Geometry

    geo = Geometry()
    code = [
        "xydim = {};".format(xy_dim),
        "zdim = {};".format(z_dim),
        "innerres = {};".format(in_res),
        "Point(1) = {0,      0,      0, innerres};",
        "Point(2) = {xydim,  0,      0, innerres};",
        "Point(3) = {xydim,  xydim,  0, xydim};",
        "Point(4) = {0,      xydim,  0, xydim};",
        "Line(1) = {1, 2};",
        "Line(2) = {2, 3};",
        "Line(3) = {3, 4};",
        "Line(4) = {4, 1};",
        "Transfinite Line{1} = xydim/innerres + 1;",
        "Transfinite Line{2, 3, 4} = 2;",
        "Line Loop(1) = {4, 1, 2, 3};",
        "Plane Surface(1) = {1};",
        "Extrude{0,0,zdim}{Surface{1};Layers{1};Recombine;};",
    ]
    geo.add_raw_code(code)
    return geo


def gmsh_grid_adapt3D(
    out_dim=(100.0, 100.0),
    in_dim=(50.0, 50.0),
    z_dim=-10.0,
    out_res=(10.0, 10.0, 10.0),
    in_res=(5.0, 5.0, 5.0),
    out_pos=(0.0, 0.0),
    in_pos=(25.0, 25.0),
    z_pos=0.0,
):
    """
    Generate the mesh adapter.
    """
    try:
        from pygmsh import Geometry
    except ImportError:
        from pygmsh.built_in import Geometry

    geo = Geometry()
    code = [
        # "// layer thickness",
        "dimz = {};".format(z_dim),
        # "// size of the outer block",
        "outx = {};".format(out_dim[0]),
        "outy = {};".format(out_dim[1]),
        # "// size of the inner block",
        "inx = {};".format(in_dim[0]),
        "iny = {};".format(in_dim[1]),
        # "// outer grid resolution",
        "grioutx = {};".format(out_res[0]),
        "griouty = {};".format(out_res[1]),
        "grioutz = {};".format(out_res[2]),
        # "// inner grid resolution",
        "grix = {};".format(in_res[0]),
        "griy = {};".format(in_res[1]),
        "griz = {};".format(in_res[2]),
        # "// position of the outer block",
        "obx = {};".format(out_pos[0]),
        "oby = {};".format(out_pos[1]),
        # "// position of the inner block",
        "ibx = {};".format(in_pos[0]),
        "iby = {};".format(in_pos[1]),
        # "// z-position of the block",
        "bz = {};".format(z_pos),
        # "// outer block points",
        "Point(1) = {obx,       oby,        bz,         grioutx};",
        "Point(2) = {obx+outx,  oby,        bz,         grioutx};",
        "Point(3) = {obx+outx,  oby+outy,   bz,         grioutx};",
        "Point(4) = {obx,       oby+outy,   bz,         grioutx};",
        "Point(5) = {obx,       oby,        bz+dimz,    grioutx};",
        "Point(6) = {obx+outx,  oby,        bz+dimz,    grioutx};",
        "Point(7) = {obx+outx,  oby+outy,   bz+dimz,    grioutx};",
        "Point(8) = {obx,       oby+outy,   bz+dimz,    grioutx};",
        # "// inner block points",
        "Point(9) =  {ibx,      iby,        bz,         grix};",
        "Point(10) = {ibx+inx,  iby,        bz,         grix};",
        "Point(11) = {ibx+inx,  iby+iny,    bz,         grix};",
        "Point(12) = {ibx,      iby+iny,    bz,         grix};",
        "Point(13) = {ibx,      iby,        bz+dimz,    grix};",
        "Point(14) = {ibx+inx,  iby,        bz+dimz,    grix};",
        "Point(15) = {ibx+inx,  iby+iny,    bz+dimz,    grix};",
        "Point(16) = {ibx,      iby+iny,    bz+dimz,    grix};",
        # "// outer block lines",
        "Line(1) = {1, 2}; //s top",
        "Line(2) = {2, 3}; //e top",
        "Line(3) = {3, 4}; //n top",
        "Line(4) = {4, 1}; //w top",
        "Line(5) = {5, 6}; //s bottom",
        "Line(6) = {6, 7}; //e bottom",
        "Line(7) = {7, 8}; //n bottom",
        "Line(8) = {8, 5}; //w bottom",
        "Line(9) = {1, 5}; //sw vert",
        "Line(10) = {2, 6}; //se vert",
        "Line(11) = {3, 7}; //ne vert",
        "Line(12) = {4, 8}; //nw vert",
        "// inner block lines",
        "Line(13) = {9, 10}; //s top",
        "Line(14) = {10, 11}; //e top",
        "Line(15) = {11, 12}; //n top",
        "Line(16) = {12, 9}; //w top",
        "Line(18) = {13, 14}; //s top",
        "Line(19) = {14, 15}; //e bottom",
        "Line(20) = {15, 16}; //n bottom",
        "Line(21) = {16, 13}; //w bottom",
        "Line(22) = {9, 13}; //sw vert",
        "Line(23) = {10, 14}; //se vert",
        "Line(24) = {11, 15}; //nw vert",
        "Line(25) = {12, 16}; //ne vert",
        # "// top surface",
        "Line Loop(26) = {1, 2, 3, 4};",
        "Line Loop(27) = {13, 14, 15, 16};",
        "Plane Surface(28) = {26, 27};",
        # "// bottom surface",
        "Line Loop(29) = {5, 6, 7, 8};",
        "Line Loop(30) = {18, 19, 20, 21};",
        "Plane Surface(31) = {29, 30};",
        # "// outer south surface",
        "Line Loop(32) = {1, 10, -5, -9};",
        "Plane Surface(33) = {32};",
        # "// outer east surface",
        "Line Loop(34) = {2, 11, -6, -10};",
        "Plane Surface(35) = {34};",
        # "// outer north surface",
        "Line Loop(36) = {3, 12, -7, -11};",
        "Plane Surface(37) = {36};",
        # "// outer west surface",
        "Line Loop(38) = {4, 9, -8, -12};",
        "Plane Surface(39) = {38};",
        # "// inner south surface",
        "Line Loop(40) = {13, 23, -18, -22};",
        "Plane Surface(41) = {40};",
        # "// inner east surface",
        "Line Loop(42) = {14, 24, -19, -23};",
        "Plane Surface(43) = {42};",
        # "// inner north surface",
        "Line Loop(44) = {15, 25, -20, -24};",
        "Plane Surface(45) = {44};",
        # "// inner west surface",
        "Line Loop(46) = {16, 22, -21, -25};",
        "Plane Surface(47) = {46};",
        # "// make the outer sides rectangular",
        "Transfinite Line{1, 3, 5, 7} = outx/grioutx + 1;",
        "Transfinite Line{2, 4, 6, 8} = outy/griouty + 1;",
        "Transfinite Line{9, 10, 11, 12} = Fabs(dimz)/grioutz + 1;",
        "Transfinite Surface{33};",
        "Transfinite Surface{35};",
        "Transfinite Surface{37};",
        "Transfinite Surface{39};",
        "Recombine Surface{33};",
        "Recombine Surface{35};",
        "Recombine Surface{37};",
        "Recombine Surface{39};",
        # "// make the inner sides rectangular",
        "Transfinite Line{13, 15, 18, 20} = inx/grix + 1;",
        "Transfinite Line{14, 16, 19, 21} = iny/griy + 1;",
        "Transfinite Line{22, 23, 24, 25} = Fabs(dimz)/griz + 1;",
        "Transfinite Surface{41};",
        "Transfinite Surface{43};",
        "Transfinite Surface{45};",
        "Transfinite Surface{47};",
        "Recombine Surface{41};",
        "Recombine Surface{43};",
        "Recombine Surface{45};",
        "Recombine Surface{47};",
        # "// define the volume",
        "Surface Loop(48) = {39, 28, 33, 35, 37, 31, 47, 41, 43, 45};",
        "Volume(49) = {48};",
    ]
    geo.add_raw_code(code)
    return geo


def gmsh_grid_adapt2D(
    out_dim=(100.0, 100.0),
    in_dim=(50.0, 50.0),
    out_res=(10.0, 10.0),
    in_res=(5.0, 5.0),
    out_pos=(0.0, 0.0),
    in_pos=(25.0, 25.0),
    z_pos=0.0,
):
    """
    Generate the 2D mesh adapter.
    """
    try:
        from pygmsh import Geometry
    except ImportError:
        from pygmsh.built_in import Geometry

    geo = Geometry()
    code = [
        # "// size of the outer block",
        "outx = {};".format(out_dim[0]),
        "outy = {};".format(out_dim[1]),
        # "// size of the inner block",
        "inx = {};".format(in_dim[0]),
        "iny = {};".format(in_dim[1]),
        # "// outer grid resolution",
        "grioutx = {};".format(out_res[0]),
        "griouty = {};".format(out_res[1]),
        # "// inner grid resolution",
        "grix = {};".format(in_res[0]),
        "griy = {};".format(in_res[1]),
        # "// position of the outer block",
        "obx = {};".format(out_pos[0]),
        "oby = {};".format(out_pos[1]),
        # "// position of the inner block",
        "ibx = {};".format(in_pos[0]),
        "iby = {};".format(in_pos[1]),
        # "// z-position of the block",
        "bz = {};".format(z_pos),
        # "// outer block points",
        "Point(1) = {obx,       oby,        bz,         grioutx};",
        "Point(2) = {obx+outx,  oby,        bz,         grioutx};",
        "Point(3) = {obx+outx,  oby+outy,   bz,         grioutx};",
        "Point(4) = {obx,       oby+outy,   bz,         grioutx};",
        # "// inner block points",
        "Point(9) =  {ibx,      iby,        bz,         grix};",
        "Point(10) = {ibx+inx,  iby,        bz,         grix};",
        "Point(11) = {ibx+inx,  iby+iny,    bz,         grix};",
        "Point(12) = {ibx,      iby+iny,    bz,         grix};",
        # "// outer block lines",
        "Line(1) = {1, 2}; //s top",
        "Line(2) = {2, 3}; //e top",
        "Line(3) = {3, 4}; //n top",
        "Line(4) = {4, 1}; //w top",
        # "// inner block lines",
        "Line(13) = {9, 10}; //s top",
        "Line(14) = {10, 11}; //e top",
        "Line(15) = {11, 12}; //n top",
        "Line(16) = {12, 9}; //w top",
        # "// top surface",
        "Line Loop(26) = {1, 2, 3, 4};",
        "Line Loop(27) = {13, 14, 15, 16};",
        "Plane Surface(28) = {26, 27};",
        # "// make the outer sides rectangular",
        "Transfinite Line{1, 3} = outx/grioutx + 1;",
        "Transfinite Line{2, 4} = outy/griouty + 1;",
        # "// make the inner sides rectangular",
        "Transfinite Line{13, 15} = inx/grix + 1;",
        "Transfinite Line{14, 16} = iny/griy + 1;",
    ]
    geo.add_raw_code(code)
    return geo
