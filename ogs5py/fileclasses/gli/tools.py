# -*- coding: utf-8 -*-
"""
tools for the ogs5py-gli package

@author: sebastian
"""
from __future__ import division, print_function, absolute_import
from copy import deepcopy as dcp
import numpy as np
from ogs5py.tools.types import (
    PLY_KEY_LIST,
    PLY_TYPES,
    SRF_KEY_LIST,
    SRF_TYPES,
    VOL_KEY_LIST,
    VOL_TYPES,
    GLI_KEY_LIST,
    EMPTY_GLI,
    EMPTY_PLY,
    EMPTY_SRF,
    EMPTY_VOL,
)
from ogs5py.tools.tools import uncomment


def load_ogs5gli(filepath, verbose=True, encoding=None):
    """
    load a given OGS5 gli file

    Parameters
    ----------
    filepath : :class:`str`
        path to the '*.msh' OGS5 gli file to load
    verbose : :class:`bool`, optional
        Print information of the reading process. Default: True
    encoding : :class:`str` or :class:`None`, optional
        encoding of the given file. If :class:`None` is given, the system
        standard is used. Default: :class:`None`

    Returns
    -------
    gli : :class:`dict`
        dictionary containing the gli file
        Includes the following information (sorted by keys):
            points : ndarray
                Array with all point postions
            point_names : ndarray (of strings)
                Array with all point names
            point_md : ndarray
                Array with all Material-densities at the points
                if point_md should be undefined it takes the value -np.inf
            polylines : list of dict, each containing information about
                - ``ID`` (int or None)
                - ``NAME`` (str)
                - ``POINTS`` (ndarray)
                - ``EPSILON`` (float or None)
                - ``TYPE`` (int or None)
                - ``MAT_GROUP`` (int or None)
                - ``POINT_VECTOR`` (str or None)
            surfaces : list of dict, each containing information about
                - ``ID`` (int or None)
                - ``NAME`` (str)
                - ``POLYLINES`` (list of str)
                - ``EPSILON`` (float or None)
                - ``TYPE`` (int or None)
                - ``MAT_GROUP`` (int or None)
                - ``TIN`` (str or None)
            volumes : list of dict, each containing information about
                - ``NAME`` (str)
                - ``SURFACES`` (list of str)
                - ``TYPE`` (int or None)
                - ``MAT_GROUP`` (int or None)
                - ``LAYER`` (int or None)

    """
    # in python3 open was replaced with io.open
    from io import open

    out = dcp(EMPTY_GLI)

    with open(filepath, "r", encoding=encoding) as gli:
        # looping variable for reading
        reading = True
        # read the first line
        line = gli.readline().strip()
        found_first = False
        while reading:
            # if end of file without '#STOP' keyword reached, raise Error
            filepos = gli.tell()
            if not gli.readline() and not line.startswith("#STOP"):
                raise EOFError("reached end of file... unexpected")
            gli.seek(filepos)
            # skip blank lines
            if not line:
                line = gli.readline().strip()
                continue
            # skip header
            if not found_first and not line.startswith("#"):
                line = gli.readline().strip()
                continue

            # check for points
            elif line.startswith("#POINTS"):
                found_first = True
                if verbose:
                    print("found 'POINTS'")
                pnts = np.empty((0, 3), dtype=float)
                ids = []  # workaround for bad ordering
                names = []
                mds = []
                line = gli.readline().strip()
                while line and line[0].isdigit():
                    ln_splt = line.split()
                    # need a list around map in python3 (map gives iterator)
                    pnt = np.array(list(map(float, ln_splt[1:4])))
                    ids.append(int(ln_splt[0]))
                    pnts = np.vstack((pnts, pnt))
                    if "$NAME" in ln_splt:
                        names.append(ln_splt[ln_splt.index("$NAME") + 1])
                    else:
                        names.append("")
                    if "$MD" in ln_splt:
                        mds.append(float(ln_splt[ln_splt.index("$MD") + 1]))
                    else:
                        # use -inf as standard md, if none is given
                        mds.append(-np.inf)
                    line = gli.readline().strip()
                # the list of point-ids (should be: 0 1 2 3 ...)
                ids = np.array(ids, dtype=int)
                if len(np.unique(ids)) != len(ids):
                    raise ValueError(
                        filepath
                        + ": GLI: point ids are not unique: "
                        + str(ids)
                    )
                if pnts.shape[0] > 0:
                    # hack to shift the ids acordingly (if not ascending)
                    id_shift = np.zeros(np.max(ids) + 1, dtype=int)
                    id_shift[ids] = np.arange(ids.shape[0])
                # save points
                out["points"] = pnts
                out["point_names"] = np.array(names, dtype=object)
                out["point_md"] = np.array(mds, dtype=float)
                continue

            # check for polyline
            elif line.startswith("#POLYLINE"):
                found_first = True
                if verbose:
                    print("found 'POLYLINE'")
                ply = dcp(EMPTY_PLY)
                line = gli.readline().strip()
                # assure, that we are reading one polyline
                while not any([line.startswith(key) for key in GLI_KEY_LIST]):
                    need_new_line = True
                    key = uncomment(line)[0][1:] if uncomment(line) else ""
                    if key in PLY_KEY_LIST:
                        if key == "POINTS":
                            ply["POINTS"] = []
                            line = gli.readline().strip()
                            while line and line.split()[0].isdigit():
                                ply["POINTS"].append(int(line.split()[0]))
                                line = gli.readline().strip()
                            if line in (
                                GLI_KEY_LIST + ["$" + k for k in PLY_KEY_LIST]
                            ):
                                need_new_line = False
                            tmp_pnt = np.array(ply["POINTS"], dtype=int)
                            # hack to shift point_ids (if not ascending)
                            tmp_pnt = id_shift[tmp_pnt]
                            ply["POINTS"] = tmp_pnt
                        else:
                            ply_typ = PLY_TYPES[PLY_KEY_LIST.index(key)]
                            ply[key] = ply_typ(gli.readline().split()[0])
                    if need_new_line:
                        line = gli.readline().strip()
                out["polylines"].append(ply)
                continue

            # check for surface
            elif line.startswith("#SURFACE"):
                found_first = True
                if verbose:
                    print("found 'SURFACE'")
                srf = dcp(EMPTY_SRF)
                line = gli.readline().strip()
                # assure, that we are reading one surface
                while not any([line.startswith(key) for key in GLI_KEY_LIST]):
                    need_new_line = True
                    key = uncomment(line)[0][1:] if uncomment(line) else ""
                    if key in SRF_KEY_LIST:
                        if key == "POLYLINES":
                            srf["POLYLINES"] = []
                            line = gli.readline().strip()
                            while line and line not in (
                                GLI_KEY_LIST + ["$" + k for k in SRF_KEY_LIST]
                            ):
                                srf["POLYLINES"].append(str(line.split()[0]))
                                line = gli.readline().strip()
                            if line in (
                                GLI_KEY_LIST + ["$" + k for k in SRF_KEY_LIST]
                            ):
                                need_new_line = False
                        else:
                            srf_typ = SRF_TYPES[SRF_KEY_LIST.index(key)]
                            srf[key] = srf_typ(gli.readline().split()[0])
                    if need_new_line:
                        line = gli.readline().strip()
                out["surfaces"].append(srf)
                continue

            # check for volume
            elif line.startswith("#VOLUME"):
                found_first = True
                if verbose:
                    print("found 'VOLUME'")
                vol = dcp(EMPTY_VOL)
                line = gli.readline().strip()
                # assure, that we are reading one volume
                while not any([line.startswith(key) for key in GLI_KEY_LIST]):
                    need_new_line = True
                    key = uncomment(line)[0][1:] if uncomment(line) else ""
                    if key in VOL_KEY_LIST:
                        if key == "SURFACES":
                            vol["SURFACES"] = []
                            line = gli.readline().strip()
                            while line and line not in (
                                GLI_KEY_LIST + ["$" + k for k in VOL_KEY_LIST]
                            ):
                                vol["SURFACES"].append(str(line.split()[0]))
                                line = gli.readline().strip()
                            if line in (
                                GLI_KEY_LIST + ["$" + k for k in VOL_KEY_LIST]
                            ):
                                need_new_line = False
                        else:
                            vol_typ = VOL_TYPES[VOL_KEY_LIST.index(key)]
                            vol[key] = vol_typ(gli.readline().split()[0])
                    if need_new_line:
                        line = gli.readline().strip()
                out["volumes"].append(vol)
                continue

            # check for STOP
            elif line.startswith("#STOP"):
                if verbose:
                    print("found '#STOP'")
                # stop reading the file
                reading = False

            # handle unknown infos
            else:
                raise ValueError(
                    filepath
                    + ": GLI: file contains unknown infos: "
                    + line.strip()
                )

    return out


def save_ogs5gli(
    filepath, gli, top_com=None, bot_com=None, verbose=True, **kwargs
):
    """
    save a given OGS5 mesh file

    Parameters
    ----------
    filepath : string
        path to the '*.msh' OGS5 mesh file to save
    gli : dict
        Dictionary containing the gli file.
        Includes the following information (sorted by keys):
            points : ndarray
                Array with all point postions
            point_names : ndarray (of strings)
                Array with all point names
            point_md : ndarray
                Array with all Material-densities at the points
                if point_md should be undefined it takes the value -np.inf
            polylines : list of dict, each containing information about
                - ``ID`` (int or None)
                - ``NAME`` (str)
                - ``POINTS`` (ndarray)
                - ``EPSILON`` (float or None)
                - ``TYPE`` (int or None)
                - ``MAT_GROUP`` (int or None)
                - ``POINT_VECTOR`` (str or None)
            surfaces : list of dict, each containing information about
                - ``ID`` (int or None)
                - ``NAME`` (str)
                - ``POLYLINES`` (list of str)
                - ``EPSILON`` (float or None)
                - ``TYPE`` (int or None)
                - ``MAT_GROUP`` (int or None)
                - ``TIN`` (str or None)
            volumes : list of dict, each containing information about
                - ``NAME`` (str)
                - ``SURFACES`` (list of str)
                - ``TYPE`` (int or None)
                - ``MAT_GROUP`` (int or None)
                - ``LAYER`` (int or None)
    top_com : str, optional
        Comment to be added as header to the file, Default: None
    bot_com : str, optional
        Comment to be added at the bottom to the file, Default: None
    verbose : bool, optional
        Print information of the writing process. Default: True
    **kwargs
        These can contain ``sub_ind`` and ``con_ind`` for indentation
        definition for sub-keys and content
    """
    from ogs5py import SUB_IND, CON_IND

    if "sub_ind" in kwargs:
        sub_ind = kwargs["sub_ind"]
    else:
        sub_ind = SUB_IND
    if "con_ind" in kwargs:
        con_ind = kwargs["con_ind"]
    else:
        con_ind = CON_IND

    with open(filepath, "w") as gli_f:
        if top_com:
            if verbose:
                print("write top comment")
            print(str(top_com), file=gli_f)

        if verbose:
            print("write #POINTS")
        if gli["points"] is not None:
            print("#POINTS", file=gli_f)
            # write all points
            for pnt_i, pnt in enumerate(gli["points"]):
                # generate NAME
                if gli["point_names"][pnt_i]:
                    name = " $NAME " + str(gli["point_names"][pnt_i])
                else:
                    name = ""
                # generate MD
                if gli["point_md"][pnt_i] == -np.inf:
                    pnt_md = ""
                else:
                    pnt_md = " $MD {}".format(gli["point_md"][pnt_i])
                # generate string for actual point
                tupl = (pnt_i,) + tuple(pnt) + (name, pnt_md)
                print("{} {} {} {}{}{}".format(*tupl), file=gli_f)

        if verbose:
            print("write #POLYLINES")
        # write all polylines
        if gli["polylines"] is not None:
            for ply in gli["polylines"]:
                print("#POLYLINE", file=gli_f)
                # generate polyline
                for key in PLY_KEY_LIST:
                    if key != "POINTS" and ply[key] is not None:
                        print(sub_ind + "$" + key, file=gli_f)
                        print(con_ind + "{}".format(ply[key]), file=gli_f)
                    elif ply[key] is not None:
                        print(sub_ind + "$POINTS", file=gli_f)
                        for pnt in ply["POINTS"]:
                            print(con_ind + "{}".format(pnt), file=gli_f)

        if verbose:
            print("write #SURFACES")
        # write all surfaces
        if gli["surfaces"] is not None:
            for srf in gli["surfaces"]:
                print("#SURFACE", file=gli_f)
                # generate surface
                for key in SRF_KEY_LIST:
                    if key != "POLYLINES" and srf[key] is not None:
                        print(sub_ind + "$" + key, file=gli_f)
                        print(con_ind + "{}".format(srf[key]), file=gli_f)
                    elif srf[key] is not None:
                        print(sub_ind + "$POLYLINES", file=gli_f)
                        for ply in srf["POLYLINES"]:
                            print(con_ind + "{}".format(ply), file=gli_f)

        if verbose:
            print("write #VOLUMES")
        # write all volumes
        if gli["volumes"] is not None:
            for vol in gli["volumes"]:
                print("#VOLUME", file=gli_f)
                # generate volume
                for key in VOL_KEY_LIST:
                    if key != "SURFACES" and vol[key] is not None:
                        print(sub_ind + "$" + key, file=gli_f)
                        print(con_ind + "{}".format(vol[key]), file=gli_f)
                    elif vol[key] is not None:
                        print(sub_ind + "$SURFACES", file=gli_f)
                        for srf in vol["SURFACES"]:
                            print(con_ind + "{}".format(srf), file=gli_f)

        if verbose:
            print("write #STOP")
        if bot_com:
            print("#STOP", file=gli_f)
            print(bot_com, end="", file=gli_f)
        else:
            print("#STOP", end="", file=gli_f)
