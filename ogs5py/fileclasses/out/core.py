# -*- coding: utf-8 -*-
"""Class for the ogs OUTPUT file."""
from ogs5py.fileclasses.base import BlockFile


class OUT(BlockFile):
    """
    Class for the ogs OUTPUT file.

    Parameters
    ----------
    task_root : str, optional
        Path to the destiny model folder.
        Default: cwd+"ogs5model"
    task_id : str, optional
        Name for the ogs task.
        Default: "model"

    Notes
    -----
    Main-Keywords (#):
        - OUTPUT
        - VERSION

    Sub-Keywords ($) per Main-Keyword:
        - OUTPUT

            - NOD_VALUES
            - PCON_VALUES
            - ELE_VALUES
            - RWPT_VALUES
            - GEO_TYPE
            - TIM_TYPE
            - DAT_TYPE
            - VARIABLESHARING
            - AMPLIFIER
            - PCS_TYPE
            - DIS_TYPE
            - MSH_TYPE
            - MMP_VALUES
            - MFP_VALUES
            - TECPLOT_ZONE_SHARE
            - TECPLOT_ELEMENT_OUTPUT_CELL_CENTERED
            - TECPLOT_ZONES_FOR_MG

        - VERSION

            (content directly related to the main-keyword)

    Standard block:
        :NOD_VALUES: "HEAD"
        :GEO_TYPE: "DOMAIN"
        :DAT_TYPE: "PVD"
        :TIM_TYPE: ["STEPS", 1]

    Keyword documentation:
        https://ogs5-keywords.netlify.com/ogs/wiki/public/doc-auto/by_ext/out

    Reading routines:

        https://github.com/ufz/ogs5/blob/master/FEM/Output.cpp#L194

        https://github.com/ufz/ogs5/blob/master/FEM/rf_out_new.cpp

    See Also
    --------
    add_block
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
            "TECPLOT_ELEMENT_OUTPUT_CELL_CENTERED",
            "TECPLOT_ZONES_FOR_MG",
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
        super(OUT, self).__init__(**OGS_Config)
        self.file_ext = ".out"
