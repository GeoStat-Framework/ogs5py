# -*- coding: utf-8 -*-
"""
tools for the ogs5py-mesh package

@author: sebastian
"""
from __future__ import division, print_function, absolute_import
from copy import deepcopy as dcp
import numpy as np
import meshio as mio
from ogs5py.tools.types import (
    ELEM_NAMES,
    NODE_NO,
    MESHIO_NAMES,
    ELEM_DIM,
    EMPTY_MSH,
)
from ogs5py.tools.tools import (
    unique_rows,
    replace,
    rotation_matrix,
    uncomment,
    volume,
)


### IO routines


def load_ogs5msh(
    filepath, verbose=True, ignore_unknown=False, max_node_no=8, encoding=None
):
    """
    load a given OGS5 mesh file

    Parameters
    ----------
    filepath : string
        path to the '*.msh' OGS5 mesh file to load
    verbose : bool, optional
        Print information of the reading process. Default: True
    ignore_unknown : bool, optional
        Unknown data in the file will be ignored. Default: False
    max_node_no : int, optional
        If you know the maximal node number per elements in the mesh file,
        you can optimise the reading a bit. By default the algorithm will
        assume hexahedrons as 'largest' elements in the mesh. Default: 8
    encoding : str or None, optional
        encoding of the given file. If ``None`` is given, the system
        standard is used. Default: ``None``

    Returns
    -------
    out : list of dictionaries
        each dictionary contains one ``#FEM_MSH`` block of the mesh file
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

    Notes
    -----
    The $AREA keyword within the Nodes definition is NOT supported
    and will violate the read data if present.
    """
    import pandas as pd

    # in python3 open was replaced with io.open
    from io import open

    # initilize the output
    out = []
    # set the mesh-count to -1, it works as index for the output
    no_msh = -1

    with open(filepath, "r", encoding=encoding) as msh:
        # looping variable for reading
        reading = True
        while reading:
            # read the next line
            line = msh.readline()

            # if end of file without '#STOP' keyword reached, raise Error
            if not line:
                # raise EOFError(filepath+": reached end of file.. unexpected")
                if verbose:
                    print(filepath + ": reached end of file... unexpected")
                break

            # skip blank lines
            elif not uncomment(line):
                continue

            # check for keywords
            elif uncomment(line)[0] == "#FEM_MSH":
                # increase mesh count since FEM_MSH was found
                no_msh += 1
                # creat new empty output-dictionary
                out.append(dcp(EMPTY_MSH))
                if verbose:
                    print("found 'FEM_MSH' number: " + str(no_msh))

            elif uncomment(line)[0] == "$AXISYMMETRY":
                if no_msh == -1:
                    raise ValueError("no 'FEM_MSH' found")
                if verbose:
                    print("read 'AXISYMMETRY'")
                out[no_msh]["mesh_data"]["AXISYMMETRY"] = True

            elif uncomment(line)[0] == "$CROSS_SECTION":
                if no_msh == -1:
                    raise ValueError("no 'FEM_MSH' found")
                if verbose:
                    print("read 'CROSS_SECTION'")
                out[no_msh]["mesh_data"]["CROSS_SECTION"] = True

            elif uncomment(line)[0] == "$PCS_TYPE":
                if no_msh == -1:
                    raise ValueError("no 'FEM_MSH' found")
                if verbose:
                    print("read 'PCS_TYPE'")
                line = msh.readline()
                out[no_msh]["mesh_data"]["PCS_TYPE"] = uncomment(line)[0]

            elif uncomment(line)[0] == "$GEO_NAME":
                if no_msh == -1:
                    raise ValueError("no 'FEM_MSH' found")
                if verbose:
                    print("read 'GEO_NAME'")
                line = msh.readline()
                out[no_msh]["mesh_data"]["GEO_NAME"] = uncomment(line)[0]

            elif uncomment(line)[0] == "$GEO_TYPE":
                if no_msh == -1:
                    raise ValueError("no 'FEM_MSH' found")
                if verbose:
                    print("read 'GEO_TYPE'")
                line = msh.readline()
                # GEO_TYPE contains 2 infos: "geo_type_name" and "geo_name"
                # geo_name overwrites the "$GEO_NAME" key like in OGS5
                # out[no_msh]["mesh_data"]["GEO_TYPE"] = uncomment(line)[:2]
                out[no_msh]["mesh_data"]["GEO_TYPE"] = uncomment(line)[0]
                out[no_msh]["mesh_data"]["GEO_NAME"] = uncomment(line)[1]

            elif uncomment(line)[0] == "$LAYER":
                if no_msh == -1:
                    raise ValueError("no 'FEM_MSH' found")
                if verbose:
                    print("read 'LAYER'")
                line = msh.readline()
                out[no_msh]["mesh_data"]["LAYER"] = int(line)

            elif uncomment(line)[0] == "$NODES":
                if no_msh == -1:
                    raise ValueError("no 'FEM_MSH' found")
                line = msh.readline()
                no_nodes = int(line)
                if verbose:
                    print("read 'NODES'")
                    print(no_nodes)
                # read points with numpys fromfile (which is quite fast)
                out[no_msh]["nodes"] = np.fromfile(
                    msh, count=no_nodes * 4, sep=" "
                ).reshape((no_nodes, 4))[:, 1:]

            elif uncomment(line)[0] == "$ELEMENTS":
                if no_msh == -1:
                    raise ValueError("no 'FEM_MSH' found")
                line = msh.readline()
                no_elements = int(line)
                if verbose:
                    print("read 'ELEMENTS'")
                    print(no_elements)
                # save actual position to rewind the file after pandas read
                filepos = msh.tell()
                # read the elements with pandas
                # names=range(max_node_no) to assure rectangular shape by cols
                tmp = pd.read_csv(
                    msh,
                    engine="c",
                    delim_whitespace=True,
                    nrows=no_elements,
                    names=range(max_node_no + 4),  # +4 for the "-1" entry
                ).values
                # check if all given element-typs are OGS known
                pos_ele = 2  # can be shift to right, if "-1" occures
                check_elem = np.in1d(tmp[:, pos_ele], ELEM_NAMES)
                if not np.all(check_elem):
                    pos_ele = 3  # skip the "-1" entry (What is that?!)
                check_elem = np.in1d(tmp[:, pos_ele], ELEM_NAMES)
                if not np.all(check_elem):
                    if verbose or True:
                        print(filepath + ": unsupported cell-types found:")
                        print(np.unique(tmp[np.invert(check_elem), pos_ele]))
                    if not ignore_unknown:
                        raise ValueError("file contains unknown element types")
                    elif verbose:
                        print("...they will be skipped!")
                # read the elements
                # read the Material-ID as material_id
                # read the Elements-ID as element_id
                out[no_msh]["elements"] = {}
                out[no_msh]["material_id"] = {}
                out[no_msh]["element_id"] = {}
                # iterate over all valid given element-types
                for elem in np.unique(tmp[check_elem, pos_ele]):
                    pos = tmp[:, pos_ele] == elem
                    out[no_msh]["elements"][elem] = tmp[
                        pos, pos_ele + 1 : pos_ele + 1 + NODE_NO[elem]
                    ].astype(int)
                    out[no_msh]["material_id"][elem] = tmp[pos, 1].astype(int)
                    out[no_msh]["element_id"][elem] = tmp[pos, 0].astype(int)
                # rewind file
                msh.seek(filepos)
                # skip the elements-definition
                # since pandas reads to EOF (why?!)
                # the np.fromfile doesn't do that
                # (maybe pandas iterates numpy not)
                for __ in range(no_elements):
                    msh.readline()

            elif uncomment(line)[0] == "#STOP":
                if verbose:
                    print("found '#STOP'")
                # stop reading the file
                reading = False

            # handle unknown infos
            else:
                if ignore_unknown:
                    if verbose:
                        print("file contains unknown infos: " + line.strip())
                else:
                    raise ValueError(
                        "file contains unknown infos: " + line.strip()
                    )

    # if a single mesh is found, return it directly
    if len(out) == 1:
        out = out[0]
    # if no mesh was found, return an empty one
    elif len(out) == 0:
        if verbose:
            print(filepath + ": no 'FEM_MSH' found.. try to read old format")
        out = load_ogs5msh_old(filepath, verbose, max_node_no, encoding)

    return out


def load_ogs5msh_old(filepath, verbose=True, max_node_no=8, encoding=None):
    """
    load a given old-style OGS5 mesh file

    Parameters
    ----------
    filepath : string
        path to the '*.msh' OGS5 mesh file to load
    verbose : bool, optional
        Print information of the reading process. Default: True
    max_node_no : int, optional
        If you know the maximal node number per elements in the mesh file,
        you can optimise the reading a bit. By default the algorithm will
        assume hexahedrons as 'largest' elements in the mesh. Default: 8
    encoding : str or None, optional
        encoding of the given file. If ``None`` is given, the system
        standard is used. Default: ``None``

    Returns
    -------
    out : dict
        dictionary contains one '#FEM_MSH' block of the mesh file
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
    import pandas as pd

    # in python3 open was replaced with io.open
    from io import open

    # initilize the output
    out = dcp(EMPTY_MSH)

    with open(filepath, "r", encoding=encoding) as msh:

        head = msh.readline()
        if head.strip().startswith("#0#0#0#1#"):
            if verbose:
                print("got right header:")
                print(head)
            # first line should contain 3 numbers: 0 no_nodes no_elements
            line = msh.readline()
            no_nodes = int(uncomment(line)[1])
            no_elements = int(uncomment(line)[2])

            # read NODES
            if verbose:
                print("read 'NODES'")
                print(no_nodes)
            # read points with numpys fromfile (which is quite fast)
            out["nodes"] = np.fromfile(
                msh, count=no_nodes * 4, sep=" "
            ).reshape((no_nodes, 4))[:, 1:]

            # read ELEMENTS
            if verbose:
                print("read 'ELEMENTS'")
                print(no_elements)
            # read the elements with pandas
            # names=range(max_node_no) to assure rectangular shape by cols
            tmp = pd.read_csv(
                msh,
                engine="c",
                delim_whitespace=True,
                nrows=no_elements,
                names=range(max_node_no + 4),  # +4 for the "-1" entry
            ).values
            # check if all given element-typs are OGS known
            pos_ele = 2  # can be shift to right, if "-1" occures
            check_elem = np.in1d(tmp[:, pos_ele], ELEM_NAMES)
            if not np.all(check_elem):
                pos_ele = 3  # skip the "-1" entry (What is that?!)
            check_elem = np.in1d(tmp[:, pos_ele], ELEM_NAMES)
            if not np.all(check_elem):
                if verbose:
                    print(filepath + ": unsupported cell-types found:")
                    print(np.unique(tmp[np.invert(check_elem), pos_ele]))
                    print("...they will be skipped")
            # read the elements
            # read the Material-ID as material_id
            # read the Elements-ID as element_id
            out["elements"] = {}
            out["material_id"] = {}
            out["element_id"] = {}
            # iterate over all valid given element-types
            for elem in np.unique(tmp[check_elem, pos_ele]):
                pos = tmp[:, pos_ele] == elem
                out["elements"][elem] = tmp[
                    pos, pos_ele + 1 : pos_ele + 1 + NODE_NO[elem]
                ].astype(int)
                out["material_id"][elem] = tmp[pos, 1].astype(int)
                out["element_id"][elem] = tmp[pos, 0].astype(int)

        # handle unknown infos
        elif verbose:
            print(filepath + ": no 'old' mesh found...")

    return out


def save_ogs5msh(
    filepath, mesh, top_com=None, bot_com=None, verbose=True, **kwargs
):
    """
    save a given OGS5 mesh file

    Parameters
    ----------
    filepath : string
        path to the '\*.msh' OGS5 mesh file to save
    mesh : list of dictionaries or single dict
        each dictionary contains one '#FEM_MSH' block of the mesh file
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

    top_com : str, optional
        Comment to be added as header to the file, Default: None
        (The MSH file doesn't allow comments as header)
    bot_com : str, optional
        Comment to be added at the bottom to the file, Default: None
    verbose : bool, optional
        Print information of the writing process. Default: True
    **kwargs
        These can contain ``sub_ind`` and ``con_ind`` for indentation
        definition for sub-keys and content
    """
    import pandas as pd
    from ogs5py import SUB_IND, CON_IND

    if "sub_ind" in kwargs:
        sub_ind = kwargs["sub_ind"]
    else:
        sub_ind = SUB_IND
    if "con_ind" in kwargs:
        con_ind = kwargs["con_ind"]
    else:
        con_ind = CON_IND

    if not isinstance(mesh, (list, tuple)):
        mesh = [mesh]

    # top comment not allowed in .msh files.
    top_com = None

    with open(filepath, "w") as msh:
        if top_com:
            if verbose:
                print("write top comment")
            print(str(top_com), file=msh)

        for i, mesh_i in enumerate(mesh):

            if verbose:
                print("write 'FEM_MSH' number: " + str(i))
            msh.write("#FEM_MSH\n")

            for key in mesh_i["mesh_data"]:
                if verbose:
                    print("write " + key)
                if (
                    key in ["AXISYMMETRY", "CROSS_SECTION"]
                    and mesh_i["mesh_data"][key]
                ):
                    msh.write(sub_ind + "$" + key + "\n")
                elif key == "GEO_TYPE":
                    msh.write(sub_ind + "$" + key + "\n")
                    geo_type = mesh_i["mesh_data"]["GEO_TYPE"]
                    geo_name = mesh_i["mesh_data"]["GEO_NAME"]
                    msh.write(geo_type + " " + geo_name + "\n")
                else:
                    msh.write(sub_ind + "$" + key + "\n")
                    msh.write(con_ind + str(mesh_i["mesh_data"][key]) + "\n")

            if verbose:
                print("write NODES")
            msh.write(sub_ind + "$NODES\n")
            no_nodes = mesh_i["nodes"].shape[0]
            msh.write(con_ind + str(no_nodes) + "\n")
            data = pd.DataFrame(
                index=np.arange(no_nodes), columns=np.arange(4)
            )
            data[0] = np.arange(no_nodes)
            data[np.arange(1, 4)] = mesh_i["nodes"]
            data.to_csv(msh, header=None, index=None, sep=" ", mode="a")

            if verbose:
                print("write ELEMENTS")
            msh.write(sub_ind + "$ELEMENTS\n")
            no_el = no_of_elements(mesh_i)
            msh.write(con_ind + str(no_el) + "\n")
            data = pd.DataFrame(
                index=np.arange(no_el), columns=np.arange(8 + 3)
            )
            # initialize the offset for each element-type
            o_s = 0
            for elem in ELEM_NAMES:
                if elem not in mesh_i["elements"]:
                    continue
                no_el = mesh_i["elements"][elem].shape[0]
                data.loc[np.arange(o_s, o_s + no_el), 0] = mesh_i[
                    "element_id"
                ][elem]
                data.loc[np.arange(o_s, o_s + no_el), 1] = mesh_i[
                    "material_id"
                ][elem]
                data.loc[np.arange(o_s, o_s + no_el), 2] = elem
                data.loc[
                    np.arange(o_s, o_s + no_el),
                    np.arange(3, 3 + NODE_NO[elem]),
                ] = mesh_i["elements"][elem]
                o_s += no_el
            # sort the elements by their ID
            data.sort_values(by=0, inplace=True)
            data.to_csv(msh, header=None, index=None, sep=" ", mode="a")

            # add lines between LAYERS
            if i < len(mesh) - 1:
                msh.write("\n")

        if verbose:
            print("writing finished: STOP")
        if bot_com:
            print("#STOP", file=msh)
            print(bot_com, end="", file=msh)
        else:
            print("#STOP", end="", file=msh)


def import_mesh(
    filepath, file_format=None, ignore_unknown=False, import_dim=(1, 2, 3)
):
    """
    import an external unstructured mesh from diffrent file-formats

    Parameters
    ----------
    filepath : string
        path to the mesh file to import
    file_format : str, optional
        Here you can specify the fileformat. If 'None' it will be
        determined by file extension. Default: None
    ignore_unknown : bool, optional
        Unknown data in the file will be ignored. Default: False
    import_dim : iterable of int or single int, optional
        State which elements should be imported by dimensionality.
        Default: (1, 2, 3)

    Returns
    -------
    out : dict
        dictionary contains one '#FEM_MSH' block of the mesh file
        with the following information
            mesh_data : dictionary containing information about
                Is empty by default and can be filled later.
            nodes : ndarray
                Array with all node postions
            elements : dictionary
                contains array of nodes for elements sorted by element types
            material_id : dictionary
                contains material ids for each element sorted by element types
            element_id : dictionary
                contains element ids for each element sorted by element types

    Notes
    -----
    This routine calls the 'read' function from the meshio package
    and converts the output (see here: https://github.com/nschloe/meshio)
    If there is any "vertex" in the element data, it will be removed.
    """

    mesh = mio.read(filepath, file_format=file_format)
    out = convert_meshio(mesh.points, mesh.cells, ignore_unknown, import_dim)

    return out


def export_mesh(
    filepath,
    mesh,
    file_format=None,
    export_material_id=True,
    add_data_by_id=None,
):
    """
    export an ogs mesh to diffrent file-formats

    Parameters
    ----------
    filepath : string
        path to the file to export
    mesh : dict
        dictionary contains one '#FEM_MSH' block of the mesh file
        with the following information
            mesh_data : dictionary containing information about
                - AXISYMMETRY (bool)
                - CROSS_SECTION (bool)
                - PCS_TYPE (str)
                - GEO_TYPE (str)
                - GEO_NAME (str)
                - LAYER (int)
            nodes : ndarray
                Array with all node postions
            elements : dictionary
                contains array of nodelists for elements sorted by element type
            material_id : dictionary
                contains material ids for each element sorted by element types
            element_id : dictionary
                contains element ids for each element sorted by element types
    file_format : str, optional
        Here you can specify the fileformat. If 'None' it will be
        determined by file extension. Default: None
    export_material_id : bool, optional
        Here you can specify if the material_id should be exported.
        Default: True
    add_data_by_id : ndarray or dict, optional
        Here you can specify additional element data sorted by their IDs.
        It can be a dictionary with data-name as key and the ndarray as value.
        Default: None

    Notes
    -----
    This routine calls the 'write' function from the meshio package
    and converts the input (see here: https://github.com/nschloe/meshio)
    """
    points = dcp(np.ascontiguousarray(mesh["nodes"]))
    cells = {}
    cell_data = {}
    # assure we have a dict for the additional data
    if add_data_by_id is not None and not isinstance(add_data_by_id, dict):
        add_data_by_id = {"add_data": add_data_by_id}
    for elemi, eleme in enumerate(ELEM_NAMES):
        # skip elements not present in the mesh
        if eleme not in mesh["elements"]:
            continue
        # write cell definitions in meshio style
        cells[MESHIO_NAMES[elemi]] = dcp(mesh["elements"][eleme])
        # export material ID if stated
        if export_material_id:
            cell_data[MESHIO_NAMES[elemi]] = {
                "material_id": dcp(mesh["material_id"][eleme])
            }
        # write additional data
        if add_data_by_id is not None:
            # if material ID was written, the dictionary already exists
            if MESHIO_NAMES[elemi] in cell_data:
                for data in add_data_by_id:
                    cell_data[MESHIO_NAMES[elemi]][data] = add_data_by_id[
                        data
                    ][mesh["element_id"][eleme]]
            # if material ID was not written, create a dictionary
            else:
                for data in add_data_by_id:
                    cell_data[MESHIO_NAMES[elemi]] = {
                        data: add_data_by_id[data][mesh["element_id"][eleme]]
                    }

    if not export_material_id and add_data_by_id is None:
        cell_data = None

    mesh_out = mio.Mesh(
        points, cells, point_data=None, cell_data=cell_data, field_data=None
    )
    mio.write(filepath, mesh_out, file_format=file_format)


def convert_meshio(points, cells, ignore_unknown=False, import_dim=(1, 2, 3)):
    """
    convert points and cells from meshio to ogs format

    Parameters
    ----------
    points : ndarray
        points as given by meshio
    cells : dict
        cells as given by meshio
    ignore_unknown : bool, optional
        Unknown data in the file will be ignored. Default: False
    import_dim : iterable of int or single int, optional
        State which elements should be imported by dimensionality.
        Default: (1, 2, 3)

    Returns
    -------
    out : dict
        dictionary contains one '#FEM_MSH' block of the mesh file
        with the following information
            mesh_data : dictionary containing information about
                Is empty by default and can be filled later.
            nodes : ndarray
                Array with all node postions
            elements : dictionary
                contains array of nodes for elements sorted by element types
            material_id : dictionary
                contains material ids for each element sorted by element types
            element_id : dictionary
                contains element ids for each element sorted by element types

    Notes
    -----
    This routine uses the meshio data structure.
    (see here: https://github.com/nschloe/meshio)
    If there is any "vertex" in the element data, it will be removed.
    """
    if not isinstance(import_dim, (set, list, tuple)):
        import_dim = [import_dim]

    # remove 0D elements
    if "vertex" in cells:
        del cells["vertex"]

    # check if element types are supported
    keylist = np.array(list(cells))
    keys = [key in MESHIO_NAMES for key in keylist]
    valid = all(keys)

    if not valid:
        print("Some element types in the file are not supported by OGS:")
        print(keylist[np.logical_not(keys)])
        if ignore_unknown:
            print("... but they will be ignored")
        else:
            raise ValueError("import_mesh: Unsupported element types")

    elements = {}
    for elm_i, elm_e in enumerate(MESHIO_NAMES):
        if elm_e not in cells:
            continue
        elements[ELEM_NAMES[elm_i]] = cells[elm_e]

    out = {
        "mesh_data": {},
        "nodes": points,
        "elements": elements,
        "material_id": gen_std_mat_id(elements),
        "element_id": gen_std_elem_id(elements),
    }

    rem_dim = {1, 2, 3} - set(import_dim)
    remove_dim(out, rem_dim)

    return out


def remove_dim(mesh, remove):
    """
    Remove elements by given dimensions from a mesh.

    Parameters
    ----------
    mesh : dict
        dictionary that contains one '#FEM_MSH' block each
        with at least the following information
            elements : dictionary
                contains array of nodes for elements sorted by element types
            material_id : dictionary
                contains material ids for each element sorted by element types
            element_id : dictionary
                contains element ids for each element sorted by element types
    remove : iterable of int or single int
        State which elements should be removed by dimensionality (1, 2, 3).

    Notes
    -----
    This will reset the element ids to default (ordered by element types)
    """
    if not isinstance(remove, (set, list, tuple)):
        remove = [remove]
    edited = False
    for i in remove:
        if i not in range(1, 4):
            continue
        for elem in ELEM_DIM[i - 1]:
            if elem in mesh["elements"]:
                edited = True
                del mesh["elements"][elem]
                del mesh["material_id"][elem]
    if edited:
        mesh["element_id"] = gen_std_elem_id(mesh["elements"])


### modifying routines


def combine(mesh_1, mesh_2, decimals=4, fast=True):
    """
    Combine mesh_1 and mesh_2 to one single mesh. The node list will be
    updated to eliminate duplicates. Element intersections are not checked.

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
    Make the node-list of the given mesh unique if there are duplicates

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
    calculate the centroids of the given elements

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
    calculate the volumes of the given elements

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
    calculate the center of the given mesh

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
    Rotate a given mesh around a given rotation point and axis
    with a given angle.

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
