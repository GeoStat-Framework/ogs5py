# -*- coding: utf-8 -*-
"""
checking routines for the ogs5py-GLI package
"""
from __future__ import division, print_function, absolute_import
import numpy as np
from ogs5py.tools.types import STRTYPE, GLI_KEYS, PLY_KEYS, SRF_KEYS, VOL_KEYS


def has_whitespaces(string):
    """
    Check if a given string contains whitespaces.

    Parameters
    ----------
    string : str
        String to be tested

    Returns
    -------
    has_ws : bool
        True if whitespaces apear.
        False if no whitespaces or string ist not of type str.
    """
    if not isinstance(string, STRTYPE):
        print(str(string) + " (" + str(type(string)) + ") is not a string!")
        return False
    has_ws = False
    for char in string:
        has_ws |= char.isspace()
    return has_ws


###############################################################################
# GLI helpers
###############################################################################


def check_polyline(ply, point_cnt, verbose=True):
    """
    Check if a given ply dictonary is valid in the sence, that the
    contained data is consistent.

    Parameters
    ----------
    ply : dict
        dictionary contains one polyline from the gli file
        with the following information
            "ID" (int or None)
            "NAME" (str)
            "POINTS" (ndarray or None)
            "EPSILON" (float or None)
            "TYPE" (int or None)
            "MAT_GROUP" (int or None)
            "POINT_VECTOR" (str or None)
    point_cnt : int
        Number of Points in the gli file.
    verbose : bool, optional
        Print information for the executed checks. Default: True

    Returns
    -------
    result : bool
        Validity of the given ply dict.
    """
    if verbose:
        print("  checking polyline for validity")
        print("  ------------------------------")
    # check if dict
    if not isinstance(ply, dict):
        if verbose:
            print("  ply is not of type dict")
        return False
    # check for keys in gli dict
    in_ply_keys = set(ply)
    if in_ply_keys == PLY_KEYS:
        if verbose:
            print("  ply keys are valid")
    else:
        if verbose:
            print("  ply keys are not valid!")
            print("  needs: " + " ".join(PLY_KEYS))
            print("  found: " + " ".join(map(str, in_ply_keys)))
            print("  missing: " + " ".join(map(str, PLY_KEYS - in_ply_keys)))
            print("  corrupted: " + " ".join(map(str, in_ply_keys - PLY_KEYS)))
        return False
    # check NAME
    if (
        isinstance(ply["NAME"], STRTYPE)
        and not has_whitespaces(ply["NAME"])
        and len(ply["NAME"]) > 0
    ):
        if verbose:
            print("  ply['NAME'] valid")
            print("  NAME: '" + ply["NAME"] + "'")
    else:
        if verbose:
            print("  ply['NAME'] not valid")
        return False
    # check ID
    if ply["ID"] is None or (isinstance(ply["ID"], int) and ply["ID"] >= 0):
        if verbose:
            print("  ply['ID'] valid")
    else:
        if verbose:
            print("  ply['ID'] not valid")
        return False
    # check POINTS
    pnt_avail = True
    # see https://github.com/numpy/numpy/pull/9505 for issubdtype
    if ply["POINTS"] is None or (
        isinstance(ply["POINTS"], np.ndarray)
        and np.issubdtype(ply["POINTS"].dtype, np.integer)
        and ply["POINTS"].ndim == 1
        and ply["POINTS"].shape[0] >= 1
        and np.min(ply["POINTS"]) >= 0
        and np.max(ply["POINTS"]) < point_cnt
    ):
        if ply["POINTS"] is None:
            pnt_avail = False
        if verbose:
            print("  ply['POINTS'] valid")
    # see https://github.com/numpy/numpy/pull/9505 for issubdtype
    elif (
        isinstance(ply["POINTS"], np.ndarray)
        and np.issubdtype(ply["POINTS"].dtype, np.integer)
        and ply["POINTS"].ndim == 1
        and ply["POINTS"].shape[0] == 0
    ):
        pnt_avail = False
        if verbose:
            print("  ply['POINTS'] valid")
    else:
        if verbose:
            print("  ply['POINTS'] not valid")
        return False
    # check EPSILON
    if ply["EPSILON"] is None or (
        isinstance(ply["EPSILON"], float) and ply["EPSILON"] >= 0.0
    ):
        if verbose:
            print("  ply['EPSILON'] valid")
    else:
        if verbose:
            print("  ply['EPSILON'] not valid")
        return False
    # check TYPE
    if ply["TYPE"] is None or isinstance(ply["TYPE"], int):
        if verbose:
            print("  ply['TYPE'] valid")
    else:
        if verbose:
            print("  ply['TYPE'] not valid")
        return False
    # check MAT_GROUP
    if ply["MAT_GROUP"] is None or isinstance(ply["MAT_GROUP"], int):
        if verbose:
            print("  ply['MAT_GROUP'] valid")
    else:
        if verbose:
            print("  ply['MAT_GROUP'] not valid")
        return False
    # check POINT_VECTOR
    if ply["POINT_VECTOR"] is None or isinstance(ply["POINT_VECTOR"], STRTYPE):
        if verbose:
            print("  ply['POINT_VECTOR'] valid")
    else:
        if verbose:
            print("  ply['POINT_VECTOR'] not valid")
        return False
    # check if at least POINT_VECTOR or POINTS are given
    if (ply["POINT_VECTOR"] is None) == (not pnt_avail):
        if verbose:
            print("  Either 'POINT_VECTOR' or 'POINTS' need to be present!")
        return False
    # finally
    if verbose:
        print("  ------------")
        print("  ply is valid")
        print("")
    return True


def check_surface(srf, ply_names, verbose=True):
    """
    Check if a given surface dictonary is valid in the sence, that the
    contained data is consistent.
    Checks for correct polyline, surface and volume definitions
    Point duplicates are not checked.

    Parameters
    ----------
    srf : dict
        dictionary contains one surface from the gli file
        with the following information
            "ID" (int or None)
            "NAME" (str)
            "POLYLINES" (list of str or None)
            "EPSILON" (float or None)
            "TYPE" (int or None)
            "MAT_GROUP" (int or None)
            "TIN" (str or None)
    ply_names : list of str
        Names of Polylines in the gli file.
    verbose : bool, optional
        Print information for the executed checks. Default: True

    Returns
    -------
    result : bool
        Validity of the given surface dict.
    """
    if verbose:
        print("  checking surface for validity")
        print("  -----------------------------")
    # check if dict
    if not isinstance(srf, dict):
        if verbose:
            print("  srf is not of type dict")
        return False
    # check for keys in gli dict
    in_srf_keys = set(srf)
    if in_srf_keys == SRF_KEYS:
        if verbose:
            print("  srf keys are valid")
    else:
        if verbose:
            print("  srf keys are not valid!")
            print("  needs: " + " ".join(SRF_KEYS))
            print("  found: " + " ".join(map(str, in_srf_keys)))
            print("  missing: " + " ".join(map(str, SRF_KEYS - in_srf_keys)))
            print("  corrupted: " + " ".join(map(str, in_srf_keys - SRF_KEYS)))
        return False
    # check NAME
    if (
        isinstance(srf["NAME"], STRTYPE)
        and not has_whitespaces(srf["NAME"])
        and len(srf["NAME"]) > 0
    ):
        if verbose:
            print("  srf['NAME'] valid")
            print("  NAME: '" + srf["NAME"] + "'")
    else:
        if verbose:
            print("  srf['NAME'] not valid")
        return False
    # check ID
    if srf["ID"] is None or (isinstance(srf["ID"], int) and srf["ID"] >= 0):
        if verbose:
            print("  srf['ID'] valid")
    else:
        if verbose:
            print("  srf['ID'] not valid")
        return False
    # check POLYLINES
    if srf["POLYLINES"] is None or (
        isinstance(srf["POLYLINES"], list)
        and all(ply in ply_names for ply in srf["POLYLINES"])
    ):
        if verbose:
            print("  srf['POLYLINES'] valid")
    else:
        if verbose:
            print("  srf['POLYLINES'] not valid")
        return False
    # check EPSILON
    if srf["EPSILON"] is None or (
        isinstance(srf["EPSILON"], float) and srf["EPSILON"] >= 0.0
    ):
        if verbose:
            print("  srf['EPSILON'] valid")
    else:
        if verbose:
            print("  srf['EPSILON'] not valid")
        return False
    # check TYPE
    if srf["TYPE"] is None or isinstance(srf["TYPE"], int):
        if verbose:
            print("  srf['TYPE'] valid")
    else:
        if verbose:
            print("  srf['TYPE'] not valid")
        return False
    # check MAT_GROUP
    if srf["MAT_GROUP"] is None or isinstance(srf["MAT_GROUP"], int):
        if verbose:
            print("  srf['MAT_GROUP'] valid")
    else:
        if verbose:
            print("  srf['MAT_GROUP'] not valid")
        return False
    # check TIN
    if srf["TIN"] is None or isinstance(srf["TIN"], STRTYPE):
        if verbose:
            print("  srf['TIN'] valid")
    else:
        if verbose:
            print("  srf['TIN'] not valid")
        return False
    # check if at least POINT_VECTOR or POINTS are given
    if bool(srf["TIN"] is None) == (not bool(srf["POLYLINES"])):
        if verbose:
            print("  Either 'TIN' or 'POLYLINES' need to be present!")
        return False
    # finally
    if verbose:
        print("  ------------")
        print("  srf is valid")
        print("")
    return True


def check_volume(vol, srf_names, verbose=True):
    """
    Check if a given volume dictonary is valid in the sence, that the
    contained data is consistent.

    Parameters
    ----------
    vol : dict
        dictionary contains one surface from the gli file
        with the following information
            "NAME" (str)
            "SURFACES" (list of str)
            "TYPE" (int or None)
            "MAT_GROUP" (int or None)
            "LAYER" (int or None)
    srf_names : int
        Names of Surfaces in the gli file.
    verbose : bool, optional
        Print information for the executed checks. Default: True

    Returns
    -------
    result : bool
        Validity of the given surface dict.
    """
    if verbose:
        print("  checking volume for validity")
        print("  ----------------------------")
    # check if dict
    if not isinstance(vol, dict):
        if verbose:
            print("  vol is not of type dict")
        return False
    # check for keys in gli dict
    in_vol_keys = set(vol)
    if in_vol_keys == VOL_KEYS:
        if verbose:
            print("  vol keys are valid")
    else:
        if verbose:
            print("  vol keys are not valid!")
            print("  needs: " + " ".join(VOL_KEYS))
            print("  found: " + " ".join(map(str, in_vol_keys)))
            print("  missing: " + " ".join(map(str, VOL_KEYS - in_vol_keys)))
            print("  corrupted: " + " ".join(map(str, in_vol_keys - VOL_KEYS)))
        return False
    # check NAME
    if (
        isinstance(vol["NAME"], STRTYPE)
        and not has_whitespaces(vol["NAME"])
        and len(vol["NAME"]) > 0
    ):
        if verbose:
            print("  vol['NAME'] valid")
            print("  NAME: '" + vol["NAME"] + "'")
    else:
        if verbose:
            print("  vol['NAME'] not valid")
        return False
    # check SURFACES
    if (
        isinstance(vol["SURFACES"], list)
        and len(vol["SURFACES"]) > 0
        and all(srf in srf_names for srf in vol["SURFACES"])
    ):
        if verbose:
            print("  vol['SURFACES'] valid")
    else:
        if verbose:
            print("  vol['SURFACES'] not valid")
        return False
    # check TYPE
    if vol["TYPE"] is None or isinstance(vol["TYPE"], int):
        if verbose:
            print(" vol['TYPE'] valid")
    else:
        if verbose:
            print("  vol['TYPE'] not valid")
        return False
    # check MAT_GROUP
    if vol["MAT_GROUP"] is None or isinstance(vol["MAT_GROUP"], int):
        if verbose:
            print("  vol['MAT_GROUP'] valid")
    else:
        if verbose:
            print("  vol['MAT_GROUP'] not valid")
        return False
    # check LAYER
    if vol["LAYER"] is None or isinstance(vol["LAYER"], int):
        if verbose:
            print("  vol['LAYER'] valid")
    else:
        if verbose:
            print("  vol['LAYER'] not valid")
        return False
    # finally
    if verbose:
        print("  ------------")
        print("  vol is valid")
        print("")
    return True


###############################################################################


def check_gli_dict(gli, verbose=True):
    """
    Check if a given gli dictonary is valid in the sence, that the
    contained data is consistent.
    Checks for correct polyline, surface and volume definitions.
    Point duplicates are not checked.

    Parameters
    ----------
    gli : dict
        dictionary contains block from the gli file
        with the following information
            points : ndarray
                Array with all point postions
            point_names : ndarray (of strings)
                Array with all point names
            point_md : ndarray
                Array with all Material-densities at the points
                if point_md should be undefined it takes the value -np.inf
            polylines : list of dict, each containing information about
                "ID" (int or None)
                "NAME" (str)
                "POINTS" (ndarray or None)
                "EPSILON" (float or None)
                "TYPE" (int or None)
                "MAT_GROUP" (int or None)
                "POINT_VECTOR" (str or None)
            surfaces : list of dict, each containing information about
                "ID" (int or None)
                "NAME" (str)
                "POLYLINES" (list of str or None)
                "EPSILON" (float or None)
                "TYPE" (int or None)
                "MAT_GROUP" (int or None)
                "TIN" (str or None)
            volumes : list of dict, each containing information about
                "NAME" (str)
                "SURFACES" (list of str)
                "TYPE" (int or None)
                "MAT_GROUP" (int or None)
                "LAYER" (int or None)
    verbose : bool, optional
        Print information for the executed checks. Default: True

    Returns
    -------
    result : bool
        Validity of the given gli dict.
    """
    if verbose:
        print("")
        print("checking gli for validity")
        print("-------------------------")
    # check if dict
    if not isinstance(gli, dict):
        if verbose:
            print("gli is not of type dict")
        return False
    # check for keys in gli dict
    in_gli_keys = set(gli)
    if in_gli_keys == GLI_KEYS:
        if verbose:
            print("gli keys are valid")
            print("")
    else:
        if verbose:
            print("gli keys are not valid!")
            print("needs: " + " ".join(GLI_KEYS))
            print("found: " + " ".join(map(str, in_gli_keys)))
            print("missing: " + " ".join(map(str, GLI_KEYS - in_gli_keys)))
            print("corrupted: " + " ".join(map(str, in_gli_keys - GLI_KEYS)))
        return False
    # check points
    if gli["points"] is None:
        point_cnt = 0
    # see https://github.com/numpy/numpy/pull/9505 for issubdtype
    elif (
        isinstance(gli["points"], np.ndarray)
        and np.issubdtype(gli["points"].dtype, np.floating)
        and gli["points"].ndim == 2
        and gli["points"].shape[1] == 3
    ):
        point_cnt = gli["points"].shape[0]
        if verbose:
            print("gli['points'] valid")
            print("")
    else:
        if verbose:
            print("gli['points'] not valid")
        return False
    # check points names
    if gli["point_names"] is None:
        if point_cnt > 0:
            if verbose:
                print("gli['point_names'] not valid")
            return False
        else:
            if verbose:
                print("gli['point_names'] valid")
                print("")
    # see https://github.com/numpy/numpy/pull/9505 for issubdtype
    elif (
        isinstance(gli["point_names"], np.ndarray)
        and np.issubdtype(gli["point_names"].dtype, np.object0)
        and gli["point_names"].ndim == 1
        and gli["point_names"].shape[0] == point_cnt
    ):
        names_valid = True
        for name in gli["point_names"]:
            names_valid &= isinstance(name, STRTYPE)
            names_valid &= not has_whitespaces(name)
        if names_valid:
            if verbose:
                print("gli['point_names'] valid")
                print("")
        else:
            if verbose:
                print("gli['point_names'] not valid")
            return False
    else:
        if verbose:
            print("gli['point_names'] not valid")
        return False
    # check point MD
    if gli["point_md"] is None:
        if point_cnt > 0:
            if verbose:
                print("gli['point_md'] not valid")
            return False
        else:
            if verbose:
                print("gli['point_md'] valid")
                print("")
    # see https://github.com/numpy/numpy/pull/9505 for issubdtype
    elif (
        isinstance(gli["point_md"], np.ndarray)
        and np.issubdtype(gli["point_md"].dtype, np.floating)
        and gli["point_md"].ndim == 1
        and gli["point_md"].shape[0] == point_cnt
    ):
        md_valid = True
        for pnt_md in gli["point_md"]:
            md_valid &= pnt_md >= 0.0 or pnt_md == -np.inf
        if md_valid:
            if verbose:
                print("gli['point_md'] valid")
                print("")
        else:
            if verbose:
                print("gli['point_md'] not valid")
            return False
    else:
        if verbose:
            print("gli['point_md'] not valid")
        return False
    # check polylines
    if not isinstance(gli["polylines"], (list, set, tuple)):
        if verbose:
            print("gli['polylines'] not valid")
        return False
    else:
        ply_valid = True
        for ply in gli["polylines"]:
            ply_valid &= check_polyline(ply, point_cnt, verbose)
        if ply_valid:
            ply_names = []
            for ply in gli["polylines"]:
                ply_names.append(ply["NAME"])
            if len(ply_names) != len(set(ply_names)):
                if verbose:
                    print("gli['polylines'] names have duplicates")
                return False
            if verbose:
                print("gli['polylines'] valid")
                print("")
        else:
            if verbose:
                print("gli['polylines'] not valid")
            return False
    # check surfaces
    if not isinstance(gli["surfaces"], (list, set, tuple)):
        if verbose:
            print("gli['surfaces'] not valid")
        return False
    else:
        srf_valid = True
        for srf in gli["surfaces"]:
            srf_valid &= check_surface(srf, ply_names, verbose)
        if srf_valid:
            srf_names = []
            for srf in gli["surfaces"]:
                srf_names.append(srf["NAME"])
            if len(srf_names) != len(set(srf_names)):
                if verbose:
                    print("gli['surfaces'] names have duplicates")
                return False
            if verbose:
                print("gli['surfaces'] valid")
                print("")
        else:
            if verbose:
                print("gli['surfaces'] not valid")
            return False
    # check volumes
    if not isinstance(gli["volumes"], (list, set, tuple)):
        if verbose:
            print("gli['volumes'] not valid")
        return False
    else:
        vol_valid = True
        for vol in gli["volumes"]:
            vol_valid &= check_volume(vol, srf_names, verbose)
        if vol_valid:
            vol_names = []
            for vol in gli["volumes"]:
                vol_names.append(vol["NAME"])
            if len(vol_names) != len(set(vol_names)):
                if verbose:
                    print("gli['volumes'] names have duplicates")
                return False
            if verbose:
                print("gli['volumes'] valid")
                print("")
        else:
            if verbose:
                print("gli['volumes'] not valid")
            return False
    # finally
    if verbose:
        print("------------")
        print("gli is valid")
        print("")
    return True
