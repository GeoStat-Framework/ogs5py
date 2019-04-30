# -*- coding: utf-8 -*-
"""
tools for the ogs5py package

.. currentmodule:: ogs5py.tools.tools

Classes
^^^^^^^

.. autosummary::
   Output

File related
^^^^^^^^^^^^

.. autosummary::
   search_mkey
   uncomment
   is_key
   is_mkey
   is_skey
   get_key
   find_key_in_list
   format_dict
   format_content
   format_content_line
   guess_type
   search_task_id
   split_file_path
   is_str_array

Geometric tools
^^^^^^^^^^^^^^^

.. autosummary::
   rotate_points
   shift_points
   transform_points
   hull_deform
   rotation_matrix
   volume

Array tools
^^^^^^^^^^^

.. autosummary::
   unique_rows
   replace
   by_id

----
"""
from __future__ import division, print_function, absolute_import
import os
import sys
import glob
import collections
import ast
import itertools
from copy import deepcopy as dcp
import numpy as np

from ogs5py.tools.types import STRTYPE, OGS_EXT


class Output(object):
    """A class to duplicate an output stream to stdout.

    Parameters
    ----------
    file_or_name : filename or open filehandle (writable)
        File that will be duplicated
    print_log : bool, optional
        State if log should be printed. Default: True
    """

    def __init__(self, file_or_name, print_log=True):
        if hasattr(file_or_name, "write") and hasattr(file_or_name, "seek"):
            self.file = file_or_name
        else:
            self.file = open(file_or_name, "w")
        self._closed = False
        self.encoding = sys.stdout.encoding
        if not self.encoding:
            self.encoding = "utf-8"
        self.print_log = print_log
        self.last_line = ""

    def close(self):
        """Close the file and restore the channel."""
        self.flush()
        self.file.close()
        self._closed = True

    def write(self, data):
        """Write data to both channels."""
        self.last_line = data.decode(self.encoding)
        self.file.write(self.last_line)
        if self.print_log:
            sys.stdout.write(self.last_line)
            sys.stdout.flush()

    def flush(self):
        """Flush both channels."""
        self.file.flush()
        if self.print_log:
            sys.stdout.flush()

    def __del__(self):
        if not self._closed:
            self.close()


def search_mkey(fin):
    """
    Search for the first main keyword in a given file-stream.

    Parameters
    ----------
    fin : stream
        given opened file
    """
    mkey = ""
    for line in fin:
        # remove comments
        sline = uncomment(line)
        if not sline:
            continue
        if is_mkey(sline):
            mkey = get_key(sline)
            break
    return mkey


def uncomment(line):
    """
    Remove OGS comments from a given line of an OGS file.
    Comments are indicated by ";". The line is then splitted by whitespaces.

    Parameters
    ----------
    line : str
        given line
    """
    return line.split(";")[0].split("//")[0].split()


def is_key(sline):
    """
    Check if the given splitted line is an OGS key

    Parameters
    ----------
    sline : list of str
        given splitted line
    """
    return sline[0][0] in ["$", "#"]


def is_mkey(sline):
    """
    Check if the given splitted line is a main key

    Parameters
    ----------
    sline : list of str
        given splitted line
    """
    return sline[0][0] == "#"


def is_skey(sline):
    """
    Check if the given splitted line is a sub key

    Parameters
    ----------
    sline : list of str
        given splitted line
    """
    return sline[0][0] == "$"


def get_key(sline):
    """
    Get the key of a splitted line if there is any. Else return ""

    Parameters
    ----------
    sline : list of str
        given splitted line
    """
    key = sline[0][1:] if is_key(sline) else ""
    # space between #/$ and key --> workaround
    if not key and is_key(sline) and len(sline) > 1:
        key = sline[1]
    # typos occure
    while key.startswith("#") or key.startswith("$"):
        key = key[1:]
    return key


def find_key_in_list(key, key_list):
    """
    Look for the right corresponding key in a list.

    key has to start with an given key from the list and the longest key
    will be returned.

    Parameters
    ----------
    key : str
        Given key.
    key_list : list of str
        Valid keys to be checked against.

    Returns
    -------
    found_key : :class:`str` or :class:`None`
        The best match. None if nothing was found.
    """
    found = []
    for try_key in key_list:
        if key.startswith(try_key):
            found.append(try_key)
    if found:
        found_key = max(found, key=len)
        # "" would be allowed for any given key
        if found_key:
            return found_key
    return None


def format_dict(dict_in):
    """
    format the dictionary to use upper-case keys

    Parameters
    ----------
    dict_in : dict
        input dictionary
    """
    dict_out = {}
    for key in dict_in:
        new_key = str(key).upper()
        if new_key != key and new_key in dict_in:
            print("Your given OGS-keywords are not unique: " + new_key)
            print("  --> DATA WILL BE LOST")
        dict_out[new_key] = dict_in[key]
    return dict_out


def guess_type(string):
    """
    guess the type of a value given as string and return it accordingly

    Parameters
    ----------
    string : str
        given string containing the value
    """
    string = str(string)
    try:
        value = ast.literal_eval(string)
    except:  # SyntaxError or ValueError
        return string
    else:
        return value


def format_content_line(content):
    """
    format a line of content to be a list of values

    Parameters
    ----------
    content : anything
        Single object, or list of objects
    """
    # assure that content is a list of strings
    content = list(np.array(content, dtype=str).reshape(-1))
    # if the content is given as string with whitespaces, split it
    content = list(itertools.chain(*[con.split() for con in content]))
    # guess types of values
    content = list(map(guess_type, content))
    return content


def format_content(content):
    """
    format the content to be added to a 2D linewise array

    Parameters
    ----------
    content : anything
        Single object, or list of objects, or list of lists of objects.
    """
    # strings could be detected as iterable, so check this first
    if isinstance(content, STRTYPE):
        return [[content]]
    # convert iterators (like zip)
    if isinstance(content, collections.Iterator):
        content = list(content)
    # check for a single content thats not a string
    try:
        iter(content)
    except TypeError:
        return [[content]]
    # check if any list in in the given list
    # if so, we handle each entry as a line
    found_list = False
    for con in content:
        found_list = False
        # check for a list
        try:
            iter(con)
        except TypeError:
            pass
        else:
            if not isinstance(con, STRTYPE):
                found_list = True
                break
    # if a list is found, we take the content as multiple lines
    if found_list:
        return content
    # else we handle the content as single line
    return [content]


def search_task_id(task_root, search_ext=None):
    """
    Search for OGS model names in the given path

    Parameters
    ----------
    task_root : str
        Path to the destiny folder.
    search_ext : str
        OGS extension that should be searched for. Default: All known.

    Returns
    -------
    found_ids : list of str
        List of all found task_ids.
    """
    if search_ext is None:
        search_ext = OGS_EXT
    found_ids = []
    # iterate over all ogs file-extensions
    for ext in search_ext:
        # search for files with given extension
        files = glob.glob(os.path.join(task_root, "*" + ext))
        # take the first found file if there are multiple
        for fil in files:
            tmp_id = os.path.splitext(os.path.basename(fil))[0]
            if tmp_id not in found_ids:
                found_ids.append(tmp_id)
    return found_ids


def split_file_path(path, abs_path=False):
    """
    decompose a path to a file into the dir-path, the basename
    and the file-extension

    Parameters
    ----------
    path : string
        string containing the path to a file
    abs_path: bool, optional
        convert the path to an absolut path. Default: False

    Returns
    -------
    result : tuple of strings
        tuple containing the dir-path, basename and file-extension
    """
    if abs_path:
        path = os.path.abspath(path)
    return os.path.split(path)[:1] + os.path.splitext(os.path.basename(path))


def is_str_array(array):
    """
    A routine to check if an array contains strings

    Parameters
    ----------
    array : iterable
        array to check

    Returns
    -------
    bool
    """
    array = np.asanyarray(array)

    if array.dtype.kind in {"U", "S"}:
        return True

    if array.dtype.kind == "O":
        for val in array.reshape(-1):
            if not isinstance(val, STRTYPE):
                return False
        return True

    return False


def rotate_points(
    points,
    angle,
    rotation_axis=(0.0, 0.0, 1.0),
    rotation_point=(0.0, 0.0, 0.0),
):
    """
    Rotate points around a given rotation point and axis with a given angle.

    Parameters
    ----------
    points : ndarray
        Array with all points postions.
    angle : float
        rotation angle given in radial length
    rotation_axis : array_like, optional
        Array containing the vector for ratation axis. Default: (0,0,1)
    rotation_point : array_like, optional
        Array containing the vector for ratation base point. Default: (0,0,0)

    Returns
    -------
    new_array : ndarray
        rotated array
    """
    rot = rotation_matrix(rotation_axis, angle)
    new_points = shift_points(points, -1.0 * np.array(rotation_point))
    new_points = np.inner(rot, new_points).T
    new_points = shift_points(new_points, rotation_point)
    return new_points


def shift_points(points, vector):
    """
    Shift points with a given vector.

    Parameters
    ----------
    points : ndarray
        Array with all points postions.
    vector : ndarray
        array containing the shifting vector

    Returns
    -------
    new_array : ndarray
        shifted array
    """
    new_points = dcp(points)
    for i in range(3):
        new_points[:, i] += vector[i]
    return new_points


def transform_points(points, xyz_func, **kwargs):
    r"""
    Transform points with a given function "xyz_func".
    kwargs will be forwarded to "xyz_func".

    Parameters
    ----------
    points : ndarray
        Array with all points postions.
    xyz_func : function
        the function transforming the points
        x_new, y_new, z_new = f(x_old, y_old, z_old, \**kwargs)

    Returns
    -------
    new_array : ndarray
        transformed array
    """
    trans = xyz_func(points[:, 0], points[:, 1], points[:, 2], **kwargs)
    return np.array(trans).T


def hull_deform(
    x_in,
    y_in,
    z_in,
    niv_top=10.0,
    niv_bot=0.0,
    func_top=None,
    func_bot=None,
    direction="z",
):
    """
    Providing a transformation function to deform a given mesh in a given
    direction by self defined hull-functions ``z = func(x, y)``.
    Could be used with ``transform_mesh`` and ``transform_points``.

    Parameters
    ----------
    x_in : ndarray
        Array of the x-positions
    y_in : ndarray
        Array of the y-positions
    z_in : ndarray
        Array of the z-positions
    niv_top : float
        height of the top niveau to be deformed by func_top
    niv_bot : float
        height of the bottom niveau to be deformed by func_bot
    func_top : function or float
        function deforming the top niveau: ``z_top = func_top(x, y)``
    func_bot : function or float
        function deforming the bottom niveau: ``z_bot = func_bot(x, y)``
    direction : string, optional
        defining the direction of deforming. This direction will be used as
        z-value. Default: "z"

    Returns
    -------
    x_out, y_out, z_out : ndarray
        transformed arrays
    """

    if direction == "x":
        x1_in = y_in
        x2_in = z_in
        x3_in = x_in
    elif direction == "y":
        x1_in = x_in
        x2_in = z_in
        x3_in = y_in
    else:
        x1_in = x_in
        x2_in = y_in
        x3_in = z_in

    if func_top is None:
        func_top = niv_top

    if func_bot is None:
        func_bot = niv_bot

    if isinstance(func_top, (float, int)):

        def func_top_redef(x_in, __):
            """redefining func_top for constant value"""
            return float(func_top) * np.ones_like(x_in)

        func_t = func_top_redef
    else:
        func_t = func_top

    if isinstance(func_bot, (float, int)):

        def func_bot_redef(x_in, __):
            """redefining func_bot for constant value"""
            return float(func_bot) * np.ones_like(x_in)

        func_b = func_bot_redef
    else:
        func_b = func_bot

    scale = (x3_in - niv_bot) / (niv_top - niv_bot)
    x3_out = scale * (func_t(x1_in, x2_in) - func_b(x1_in, x2_in)) + func_b(
        x1_in, x2_in
    )

    if direction == "x":
        return x3_out, x1_in, x2_in
    if direction == "y":
        return x1_in, x3_out, x2_in
    if direction == "z":
        return x1_in, x2_in, x3_out


#####################
# helping functions #
#####################


def rotation_matrix(vector, angle):
    """
    Create a rotation matrix for rotation around a given vector with a given
    angle.

    Parameters
    ----------
    vector : ndarray
        array containing the vector for ratation axis
    angle : float
        rotation angle given in radial length

    Returns
    -------
    result : ndarray
        matrix to be used for matrix multiplication with vectors to be
        rotated.
    """
    # vector has to be normed
    vector = np.asfarray(vector) / np.linalg.norm(vector)
    mat = np.cross(np.eye(3), vector)
    cosa = np.cos(angle)
    sina = np.sin(angle)
    return (
        cosa * np.eye(3) + sina * mat + (1 - cosa) * np.outer(vector, vector)
    )


def replace(arr, inval, outval):
    """
    replace certain values of 'arr' defined in 'inval' with values defined
    in 'outval'

    Parameters
    ----------
    arr : ndarray
        array containing the input data
    inval : ndarray
        values appearing in 'arr' that should be replaced
    outval : ndarray
        values that should be written in 'arr' instead of values in 'inval'

    Returns
    -------
    result : ndarray
        array of the same shape as 'arr' containing the new data
    """
    # convert input to numpy array
    inval = np.array(inval).reshape(-1)
    outval = np.array(outval).reshape(-1)
    arrtmp = np.copy(arr).reshape(-1)
    # sort inval and outval according to inval (needed for searchsorted)
    sort = np.argsort(inval)
    inval = inval[sort]
    outval = outval[sort]
    # replace values
    mask = np.in1d(arrtmp, inval)
    arrtmp[mask] = outval[np.searchsorted(inval, arrtmp[mask])]

    return arrtmp.reshape(arr.shape)


def unique_rows(data, decimals=4, fast=True):
    """
    unique made row-data with respect to given precision

    this is constructed to work best if point-pairs appear.
    The output is sorted like the input data.
    data needs to be 2D

    Parameters
    ----------
    data : ndarray
        2D array containing the list of vectors that should be made unique
    decimals : int, optional
        Number of decimal places to round the 'data' to (default: 3).
        If decimals is negative, it specifies the number of positions
        to the left of the decimal point.
        This will not round the output, it is just for comparison of the
        vectors.
    fast : bool, optional
        If fast is True, the vector comparison is executed by a decimal
        comparison. If fast is False, all pairwise distances are calculated.
        Default: True

    Returns
    -------
    result : ndarray
        2D array of unique rows of data
    ix : ndarray
        index positions of output in input data (data[ix] = result)
        len(ix) = result.shape[0]
    ixr : ndarray
        reversed index positions of input in output data (result[ixr] = data)
        len(ixr) = data.shape[0]

    Notes
    -----
    This routine will preserve the order within the given array as effectively
    as possible. If you use it with a stack of 2 arrays and the first one is
    already unique, the resulting array will still have the first array at the
    beginning.
    """
    if data.ndim != 2:
        raise ValueError("unique_rows: Wrong input shape. Only 2D allowed!")
    if fast:
        # round the input to the given precicion
        tmp = np.around(data, decimals=decimals)
        # using the 1D numpy 'unique' function by defining a special dtype
        # since numpy 1.13.0 actually not needed anymore (axis parameter added)
        tmp = np.ascontiguousarray(tmp).view(
            np.dtype((np.void, tmp.dtype.itemsize * tmp.shape[1]))
        )
    else:
        # get the tolerance from the given decimals
        tol = np.power(10.0, -decimals)
        # calculate all distances to each other (fancy!)
        dim_i = []
        for i in range(data.shape[1]):
            # is this a bottle neck? ... apparently
            dim_i.append(np.subtract.outer(data[:, i], data[:, i]) ** 2)
        distance = np.sqrt(np.sum(dim_i, axis=0))
        # just use the upper triangle above the diagonal
        distance[np.tril_indices_from(distance)] = np.inf
        # look which points are close
        close = np.where(distance < tol)
        # generate the indizes of the points
        tmp = np.arange(data.shape[0], dtype=np.int64)
        # replace indizes of close points with indizes of the reference points
        # prevent chains/bulks of points by using the first nearest point
        pos, ind = np.unique(close[1], return_index=True)
        val = close[0][ind]
        tmp[pos] = val
    # now sort the indices and make them unique
    __, i_x, i_xr = np.unique(tmp, return_index=True, return_inverse=True)
    out = data[i_x]
    # sort the output according to the input
    sort = np.argsort(i_x)
    ixsort = i_x[sort]
    # this line is a pain in the neck
    ixrsort = replace(i_xr, sort, np.arange(len(i_x)))

    return out[sort], ixsort, ixrsort


def by_id(array, ids=None):
    """
    Return a flattend array side-by-side with the array-element ids

    Parameters
    ----------
    array : array-like
        Input data. will be flattened.
    ids : None or array-like
        You can provide specific ids if needed. As default, the array-ids are
        used. Default: None

    Returns
    -------
    zipped (id, array) object
    """
    array = np.ravel(array)
    if ids is None:
        ids = np.arange(array.shape[0], dtype=int)
    else:
        ids = np.ravel(ids)
        if ids.shape[0] != array.shape[0]:
            raise ValueError("array and ids don't have the same length")
    return zip(ids, array)


def unique_rows_old(data, decimals=4):
    """
    returns unique made data with respect to given precision in "decimals"
    The output is sorted like the input data.
    data needs to be 2D

    Parameters
    ----------
    data : ndarray
        2D array containing the list of vectors that should be made unique
    decimals : int, optional
        Number of decimal places to round the 'data' to (default: 3).
        If decimals is negative, it specifies the number of positions
        to the left of the decimal point.
        This will not round the output, it is just for comparison of the
        vectors.

    Returns
    -------
    result : ndarray
        2D array of unique rows of data
    ix : ndarray
        index positions of output in input data (data[ix] = result)
        len(ix) = result.shape[0]
    ixr : ndarray
        reversed index positions of input in output data (result[ixr] = data)
        len(ixr) = data.shape[0]

    Notes
    -----
    This routine will preserve the order within the given array as effectively
    as possible. If you use it with a stack of 2 arrays and the first one is
    already unique, the resulting array will still have the first array at the
    beginning.
    """
    if data.ndim != 2:
        raise ValueError("unique_rows: Wrong input shape. Only 2D allowed!")

    # round the input to the given precicion
    tmp = np.around(data, decimals=decimals)
    # using the 1D numpy 'unique' function by defining a special numpy dtype
    tmp = np.ascontiguousarray(tmp).view(
        np.dtype((np.void, tmp.dtype.itemsize * tmp.shape[1]))
    )
    __, i_x, i_xr = np.unique(tmp, return_index=True, return_inverse=True)
    out = data[i_x]
    # sort the output according to the input
    sort = np.argsort(i_x)
    ixsort = i_x[sort]
    # this line is a pain in the ass/brain
    ixrsort = replace(i_xr, sort, np.arange(len(i_x)))

    return out[sort], ixsort, ixrsort


####################
# volume functions #
####################


def volume(typ, *pnt):
    """
    Volume of a OGS5 Meshelement

    Parameters
    ----------
    typ : string
        OGS5 Meshelement type. Should be one of the following:

            * "line" : 1D element with 2 nodes
            * "tri" : 2D element with 3 nodes
            * "quad" : 2D element with 4 nodes
            * "tet" : 3D element with 4 nodes
            * "pyra" : 3D element with 5 nodes
            * "pris" : 3D element with 6 nodes
            * "hex" : 3D element with 8 nodes

    *pnt : Node Choordinates ``pnt = (x_0, x_1, ...)``
        List of points defining the Meshelement. A point is given as an
        (x,y,z) tuple and for each point, there can be a stack of points, if
        the volume should be calculated for multiple elements of the same type.

    Returns
    -------
    Volume : ndarray
        Array containing the volumes of the give elements.
    """
    # if the pntinates are stacked, divide them
    if len(pnt) == 1:
        np_pnt = np.array(pnt[0], ndmin=3, dtype=float)
        pnt = []
        for i in range(np_pnt.shape[0]):
            pnt.append(np_pnt[i])
    # else assure we got numpy arrays as lists of points (x,y,z)
    else:
        pnt_list = list(pnt)
        pnt = []
        for i in range(len(pnt_list)):
            pnt.append(np.array(pnt_list[i], ndmin=2, dtype=float))

    if typ == "line":
        return _vol_line(*pnt)
    if typ == "tri":
        return _vol_tri(*pnt)
    if typ == "quad":
        return _vol_quad(*pnt)
    if typ == "tet":
        return _vol_tet(*pnt)
    if typ == "pyra":
        return _vol_pyra(*pnt)
    if typ == "pris":
        return _vol_pris(*pnt)
    if typ == "hex":
        return _vol_hex(*pnt)

    print("unknown volume typ: " + str(typ))
    return 0.0


def _vol_line(*pnt):
    return np.linalg.norm(pnt[1] - pnt[0], axis=1)


def _vol_tri(*pnt):
    cross = np.cross(pnt[1] - pnt[0], pnt[2] - pnt[0], axis=1)
    return 0.5 * np.linalg.norm(cross, axis=1)


def _vol_quad(*pnt):
    return _vol_tri(pnt[0], pnt[1], pnt[2]) + _vol_tri(pnt[2], pnt[3], pnt[0])


def _vol_tet(*pnt):
    cross = np.cross(pnt[2] - pnt[0], pnt[3] - pnt[0], axis=1)
    out = np.einsum("ij,ij->i", pnt[1] - pnt[0], cross)
    # See: https://stackoverflow.com/a/39657770/6696397
    #    out = np.sum((pnt[1] - pnt[0]) * cross, axis=1)
    return np.abs(out) / 6.0


def _vol_pyra(*pnt):
    return _vol_tet(pnt[0], pnt[1], pnt[2], pnt[4]) + _vol_tet(
        pnt[0], pnt[2], pnt[3], pnt[4]
    )


def _vol_pris(*pnt):
    return _vol_pyra(pnt[0], pnt[3], pnt[4], pnt[1], pnt[2]) + _vol_tet(
        pnt[3], pnt[4], pnt[5], pnt[2]
    )


def _vol_hex(*pnt):
    return _vol_pris(
        pnt[0], pnt[1], pnt[2], pnt[4], pnt[5], pnt[6]
    ) + _vol_pris(pnt[0], pnt[2], pnt[3], pnt[4], pnt[5], pnt[6], pnt[7])
