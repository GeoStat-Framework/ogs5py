"""
Class for the ogs FLUID PROPERTY file.
"""

from __future__ import absolute_import, division, print_function
from ogs5py.fileclasses.base import OGSfile


class MFP(OGSfile):
    """
    Class for the ogs FLUID PROPERTY file.

    Keywords for a block
    --------------------
    - FLUID_PROPERTIES
        - COMPONENTS
        - COMPRESSIBILITY
        - DAT_TYPE
        - DECAY
        - DENSITY
        - DIFFUSION
        - DRHO_DT_UNSATURATED
        - EOS_TYPE
        - FLUID_NAME
        - FLUID_TYPE
        - GRAVITY
        - HEAT_CONDUCTIVITY
        - ISOTHERM
        - JTC
        - NON_GRAVITY
        - PHASE_DIFFUSION
        - SPECIFIC_HEAT_CAPACITY
        - SPECIFIC_HEAT_SOURCE
        - TEMPERATURE
        - VISCOSITY

    Standard block
    --------------
    :FLUID_TYPE: "LIQUID"
    :DENSITY: [[1, 1.0e+03]]
    :VISCOSITY: [[1, 1.0e-03]]

    Info
    ----
    See: ``add_block``

    https://ogs5-keywords.netlify.com/ogs/wiki/public/doc-auto/by_ext/mfp

    https://github.com/ufz/ogs5/blob/master/FEM/rf_mfp_new.cpp#L140
    """

    MKEYS = ["FLUID_PROPERTIES"]
    # sorted
    SKEYS = [
        [
            "FLUID_TYPE",
            "COMPONENTS",
            "FLUID_NAME",
            "EOS_TYPE",
            "COMPRESSIBILITY",
            "JTC",
            "DAT_TYPE",
            "NON_GRAVITY",
            "DRHO_DT_UNSATURATED",
            "DENSITY",
            "TEMPERATURE",
            "VISCOSITY",
            "SPECIFIC_HEAT_CAPACITY",
            "HEAT_CONDUCTIVITY",
            "PHASE_DIFFUSION",
            "DIFFUSION",
            "DECAY",
            "ISOTHERM",
            "GRAVITY",
            "SPECIFIC_HEAT_SOURCE",
        ]
    ]

    STD = {
        "FLUID_TYPE": "LIQUID",
        "DENSITY": [1, 1.0e03],
        "VISCOSITY": [1, 1.0e-03],
    }

    def __init__(self, **OGS_Config):
        """
        Input
        -----

        OGS_Config dictonary

        """
        super(MFP, self).__init__(**OGS_Config)
        self.file_ext = ".mfp"
