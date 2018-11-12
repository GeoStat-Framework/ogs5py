"""
Class for the ogs MEDIUM_PROPERTIES file.
"""

from __future__ import absolute_import, division, print_function
from ogs5py.fileclasses.base import OGSfile


class MMP(OGSfile):
    """
    Class for the ogs MEDIUM_PROPERTIES file.

    Keywords for a block
    --------------------
    - MEDIUM_PROPERTIES
        - CAPILLARY_PRESSURE
        - CHANNEL
        - COMPOUND_DEPENDENT_DT
        - CONDUCTIVITY_MODEL
        - CONVERSION_FACTOR
        - DATA
        - DIFFUSION
        - DIS_TYPE
        - ELEMENT_VOLUME_MULTIPLYER
        - EVAPORATION
        - FLOWLINEARITY
        - GEOMETRY_AREA
        - GEOMETRY_DIMENSION
        - GEOMETRY_INCLINATION
        - GEO_TYPE
        - HEAT_DISPERSION
        - HEAT_TRANSFER
        - INTERPHASE_FRICTION
        - MASS_DISPERSION
        - MMP_TYPE
        - MSH_TYPE
        - NAME
        - ORGANIC_CARBON
        - PARTICLE_DIAMETER
        - PCS_TYPE
        - PERMEABILITY_FUNCTION_DEFORMATION
        - PERMEABILITY_FUNCTION_EFFSTRESS
        - PERMEABILITY_FUNCTION_POROSITY
        - PERMEABILITY_FUNCTION_PRESSURE
        - PERMEABILITY_FUNCTION_STRAIN
        - PERMEABILITY_FUNCTION_STRESS
        - PERMEABILITY_FUNCTION_VELOCITY
        - PERMEABILITY_SATURATION
        - PERMEABILITY_TENSOR
        - PERMEABILITY_DISTRIBUTION
        - POROSITY
        - POROSITY_DISTRIBUTION
        - RILL
        - SPECIFIC_STORAGE
        - STORAGE
        - STORAGE_FUNCTION_EFFSTRESS
        - SURFACE_FRICTION
        - TORTUOSITY
        - TRANSFER_COEFFICIENT
        - UNCONFINED
        - VOL_BIO
        - VOL_MAT
        - WIDTH

    Standard block
    --------------
    :GEOMETRY_DIMENSION: 2,
    :STORAGE: [[1, 1.0e-4]],
    :PERMEABILITY_TENSOR: [["ISOTROPIC", 1.0e-4]],
    :POROSITY: [[1, 0.2]]

    Info
    ----
    See: ``add_block``

    https://svn.ufz.de/ogs/wiki/public/doc-auto/by_ext/mmp

    https://github.com/ufz/ogs5/blob/master/FEM/rf_mmp_new.cpp#L281
    """

    MKEYS = ["MEDIUM_PROPERTIES"]
    # sorted
    SKEYS = [
        [
            "PCS_TYPE",
            "NAME",
            "GEO_TYPE",
            "GEOMETRY_DIMENSION",
            "GEOMETRY_INCLINATION",
            "GEOMETRY_AREA",
            "POROSITY",
            "VOL_MAT",
            "VOL_BIO",
            "TORTUOSITY",
            "FLOWLINEARITY",
            "ORGANIC_CARBON",
            "STORAGE",
            "CONDUCTIVITY_MODEL",
            "UNCONFINED",
            "PERMEABILITY_TENSOR",
            "PERMEABILITY_FUNCTION_DEFORMATION",
            "PERMEABILITY_FUNCTION_STRAIN",
            "PERMEABILITY_FUNCTION_PRESSURE",
            "PERMEABILITY_SATURATION",
            "PERMEABILITY_FUNCTION_STRESS",
            "PERMEABILITY_FUNCTION_EFFSTRESS",
            "PERMEABILITY_FUNCTION_VELOCITY",
            "PERMEABILITY_FUNCTION_POROSITY",
            "CAPILLARY_PRESSURE",
            "TRANSFER_COEFFICIENT",
            "SPECIFIC_STORAGE",
            "STORAGE_FUNCTION_EFFSTRESS",
            "MASS_DISPERSION",
            "COMPOUND_DEPENDENT_DT",
            "HEAT_DISPERSION",
            "DIFFUSION",
            "EVAPORATION",
            "SURFACE_FRICTION",
            "WIDTH",
            "RILL",
            "CHANNEL",
            "PERMEABILITY_DISTRIBUTION",
            "POROSITY_DISTRIBUTION",
            "HEAT_TRANSFER",
            "PARTICLE_DIAMETER",
            "INTERPHASE_FRICTION",
            "ELEMENT_VOLUME_MULTIPLYER",
        ]
    ]

    STD = {
        "GEOMETRY_DIMENSION": 2,
        "STORAGE": [1, 1.0e-4],
        "PERMEABILITY_TENSOR": ["ISOTROPIC", 1.0e-4],
        "POROSITY": [1, 0.2],
    }

    def __init__(self, **OGS_Config):
        """
        Input
        -----

        OGS_Config dictonary

        """
        super(MMP, self).__init__(**OGS_Config)
        self.file_ext = ".mmp"
