# -*- coding: utf-8 -*-
"""IO routines for the ogs5py mesh package."""
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
from ogs5py.tools.tools import uncomment
from ogs5py.fileclasses.msh.tools import (
    no_of_elements,
    gen_std_mat_id,
    gen_std_elem_id,
)

### IO routines


def load_ogs5msh(
    filepath, verbose=True, ignore_unknown=False, max_node_no=8, encoding=None
):
    """
    Load a given OGS5 mesh file.

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
                    if verbose:
                        print(filepath + ": unsupported cell-types found:")
                        print(np.unique(tmp[np.invert(check_elem), pos_ele]))
                    if not ignore_unknown:
                        raise ValueError("file contains unknown element types")
                    if verbose:
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
    elif not out:
        if verbose:
            print(filepath + ": no 'FEM_MSH' found.. try to read old format")
        out = load_ogs5msh_old(filepath, verbose, max_node_no, encoding)

    return out


def load_ogs5msh_old(filepath, verbose=True, max_node_no=8, encoding=None):
    """
    Load a given old-style OGS5 mesh file.

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
    r"""
    Save a given OGS5 mesh file.

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

    sub_ind = kwargs.get("sub_ind", SUB_IND)
    con_ind = kwargs.get("con_ind", CON_IND)

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
    filepath,
    file_format=None,
    ignore_unknown=False,
    import_dim=(1, 2, 3),
    element_id_name="element_id",
    material_id_name="material_id",
):
    """
    Import an external unstructured mesh from diffrent file-formats.

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
    element_id_name : str, optional
        The name of the cell-data containing the element IDs if present.
        Default: "element_id"
    material_id_name : str, optional
        The name of the cell-data containing the material IDs if present.
        Default: "material_id"

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
    out = convert_meshio(
        mesh, ignore_unknown, import_dim, element_id_name, material_id_name
    )

    return out


def export_mesh(
    filepath,
    mesh,
    file_format=None,
    export_material_id=True,
    export_element_id=True,
    cell_data_by_id=None,
    point_data=None,
    field_data=None,
):
    """
    Export an ogs mesh to diffrent file-formats.

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
    export_element_id : bool, optional
        Here you can specify if the element_id should be exported.
        Default: True
    cell_data_by_id : ndarray or dict, optional
        Here you can specify additional element/cell data sorted by their IDs.
        It can be a dictionary with data-name as key and the ndarray as value.
        Default: None
    point_data : ndarray or dict, optional
        Here you can specify additional point data sorted by their IDs.
        It can be a dictionary with data-name as key and the ndarray as value.
        Default: None
    field_data : ndarray or dict, optional
        Here you can specify additional field data of the mesh.
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
    if cell_data_by_id is not None and not isinstance(cell_data_by_id, dict):
        cell_data_by_id = {"add_data": cell_data_by_id}

    # prepare dict
    if export_material_id:
        cell_data["material_id"] = []
    if export_element_id:
        cell_data["element_id"] = []
    if cell_data_by_id is not None:
        for data in cell_data_by_id:
            cell_data[data] = []

    for elemi, eleme in enumerate(ELEM_NAMES):
        # skip elements not present in the mesh
        if eleme not in mesh["elements"]:
            continue
        # write cell definitions in meshio style
        cells[MESHIO_NAMES[elemi]] = dcp(mesh["elements"][eleme])
        # export material ID if stated
        if export_material_id:
            cell_data["material_id"].append(
                np.array(mesh["material_id"][eleme], dtype=np.int32)
            )
        # export element ID if stated
        if export_element_id:
            cell_data["element_id"].append(
                np.array(mesh["element_id"][eleme], dtype=np.int32)
            )
        # write additional data
        if cell_data_by_id is not None:
            for data in cell_data_by_id:
                cell_data[data].append(
                    cell_data_by_id[data][mesh["element_id"][eleme]],
                )

    if not cell_data:
        cell_data = None

    mesh_out = mio.Mesh(
        points=points,
        cells=cells,
        point_data=point_data,
        cell_data=cell_data,
        field_data=field_data,
    )
    mio.write(filepath, mesh_out, file_format=file_format)


def convert_meshio(
    mesh,
    ignore_unknown=False,
    import_dim=(1, 2, 3),
    element_id_name="element_id",
    material_id_name="material_id",
):
    """
    Convert points and cells from meshio to ogs format.

    Parameters
    ----------
    mesh : meshio mesh class
        The given mesh by meshio
    ignore_unknown : bool, optional
        Unknown data in the file will be ignored. Default: False
    import_dim : iterable of int or single int, optional
        State which elements should be imported by dimensionality.
        Default: (1, 2, 3)
    element_id_name : str, optional
        The name of the cell-data containing the element IDs if present.
        Default: "element_id"
    material_id_name : str, optional
        The name of the cell-data containing the material IDs if present.
        Default: "material_id"

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
    nodes = mesh.points
    cells = mesh.cells_dict
    cell_data = mesh.cell_data_dict
    print(cells)
    print(cell_data)
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
    material_id = {}
    element_id = {}
    for elm_i, elm_e in enumerate(MESHIO_NAMES):
        if elm_e not in cells:
            continue
        elements[ELEM_NAMES[elm_i]] = cells[elm_e]
        if material_id_name in cell_data:
            material_id[ELEM_NAMES[elm_i]] = cell_data[material_id_name][elm_e]
        if element_id_name in cell_data:
            element_id[ELEM_NAMES[elm_i]] = cell_data[element_id_name][elm_e]

    if not material_id:
        material_id = gen_std_mat_id(elements)
    if not element_id:
        element_id = gen_std_elem_id(elements)

    out = {
        "mesh_data": {},
        "nodes": nodes,
        "elements": elements,
        "material_id": material_id,
        "element_id": element_id,
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
    This will keep the element ids order.
    """
    if not isinstance(remove, (set, list, tuple)):
        remove = [remove]
    edited = False
    ele_no = no_of_elements(mesh)
    removed_ele_id = []
    for i in remove:
        if i not in range(1, 4):
            continue
        for elem in ELEM_DIM[i - 1]:
            if elem in mesh["elements"]:
                edited = True
                del mesh["elements"][elem]
                removed_ele_id.append(mesh["element_id"][elem])
                del mesh["element_id"][elem]
                del mesh["material_id"][elem]
    if edited:
        removed_ele_id = np.concatenate(removed_ele_id)
        ids = np.arange(ele_no)
        del_id = np.setdiff1d(np.arange(ele_no), removed_ele_id)
        new_id = np.argsort(del_id)
        # trick: replace old IDs with new ones
        ids[del_id] = new_id
        for elem in mesh["element_id"]:
            mesh["element_id"][elem] = ids[mesh["element_id"][elem]]
        # mesh["element_id"] = gen_std_elem_id(mesh["elements"])
