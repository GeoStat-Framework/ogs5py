"""
Class for the ogs SOURCE_TERM file.
"""

from __future__ import absolute_import, division, print_function
from ogs5py.fileclasses.base import OGSfile


class ST(OGSfile):
    """
    Class for the ogs SOURCE_TERM file.

    Keywords for a block
    --------------------
    - SOURCE_TERM
        - AIR_BREAKING
        - CHANNEL
        - COMP_NAME
        - CONSTRAINED
        - DISTRIBUTE_VOLUME_FLUX
        - DIS_TYPE
        - EXPLICIT_SURFACE_WATER_PRESSURE
        - FCT_TYPE
        - GEO_TYPE
        - MSH_TYPE
        - NEGLECT_SURFACE_WATER_PRESSURE
        - NODE_AVERAGING
        - PCS_TYPE
        - PRIMARY_VARIABLE
        - TIME_INTERPOLATION
        - TIM_TYPE

    Standard block
    --------------
    :PCS_TYPE: "GROUNDWATER_FLOW"
    :PRIMARY_VARIABLE: "HEAD"
    :GEO_TYPE: [["POINT", "WELL"]]
    :DIS_TYPE: [["CONSTANT_NEUMANN", -1.0e-03]]

    Info
    ----
    See: ``add_block``

    https://svn.ufz.de/ogs/wiki/public/doc-auto/by_ext/st

    https://github.com/ufz/ogs5/blob/master/FEM/rf_st_new.cpp#L221
    """

    MKEYS = ["SOURCE_TERM"]
    # sorted
    SKEYS = [
        [
            "PCS_TYPE",
            "PRIMARY_VARIABLE",
            "COMP_NAME",
            "GEO_TYPE",
            "DIS_TYPE",
            "NODE_AVERAGING",
            "DISTRIBUTE_VOLUME_FLUX",
            "NEGLECT_SURFACE_WATER_PRESSURE",
            "EXPLICIT_SURFACE_WATER_PRESSURE",
            "CHANNEL",
            "AIR_BREAKING",
            "TIM_TYPE",
            "TIME_INTERPOLATION",
            "FCT_TYPE",
            "MSH_TYPE",
            "CONSTRAINED",
        ]
    ]

    STD = {
        "PCS_TYPE": "GROUNDWATER_FLOW",
        "PRIMARY_VARIABLE": "HEAD",
        "GEO_TYPE": [["POINT", "WELL"]],
        "DIS_TYPE": [["CONSTANT_NEUMANN", -1.0e-03]],
    }

    def __init__(self, **OGS_Config):
        """
        Input
        -----

        OGS_Config dictonary

        """
        super(ST, self).__init__(**OGS_Config)
        self.file_ext = ".st"
