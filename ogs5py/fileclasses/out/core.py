"""
Class for the ogs OUTPUT file.
"""

from __future__ import absolute_import, division, print_function
from ogs5py.fileclasses.base import OGSfile


class OUT(OGSfile):
    """
    Class for the ogs OUTPUT file.

    Keywords for a block
    --------------------
    - OUTPUT
        - AMPLIFIER
        - DAT_TYPE
        - DIS_TYPE
        - ELE_VALUES
        - GEO_TYPE
        - MFP_VALUES
        - MMP_VALUES
        - MSH_TYPE
        - NOD_VALUES
        - PCON_VALUES
        - PCS_TYPE
        - RWPT_VALUES
        - TECPLOT_ZONE_SHARE
        - TIM_TYPE
        - VARIABLESHARING

    Standard block
    --------------
    :NOD_VALUES: "HEAD"
    :GEO_TYPE: "DOMAIN"
    :DAT_TYPE: "PVD"
    :TIM_TYPE: ["STEPS", 1]

    Info
    ----
    See: ``add_block``

    https://ogs5-keywords.netlify.com/ogs/wiki/public/doc-auto/by_ext/out

    https://github.com/ufz/ogs5/blob/master/FEM/Output.cpp#L194

    https://github.com/ufz/ogs5/blob/master/FEM/rf_out_new.cpp
    """

    MKEYS = ["OUTPUT", "VERSION"]
    # sorted
    SKEYS = [
        [
            "NOD_VALUES",
            "PCON_VALUES",
            "ELE_VALUES",
            "RWPT_VALUES",
            "GEO_TYPE",
            "TIM_TYPE",
            "DAT_TYPE",
            "VARIABLESHARING",
            "AMPLIFIER",
            "PCS_TYPE",
            "DIS_TYPE",
            "MSH_TYPE",
            "MMP_VALUES",
            "MFP_VALUES",
            "TECPLOT_ZONE_SHARE",
        ],
        [""],  # content directly related to main key "VERSION"
    ]

    STD = {
        "NOD_VALUES": "HEAD",
        "GEO_TYPE": "DOMAIN",
        "DAT_TYPE": "PVD",
        "TIM_TYPE": ["STEPS", 1],
    }

    def __init__(self, **OGS_Config):
        """
        Input
        -----

        OGS_Config dictonary

        """
        super(OUT, self).__init__(**OGS_Config)
        self.file_ext = ".out"
