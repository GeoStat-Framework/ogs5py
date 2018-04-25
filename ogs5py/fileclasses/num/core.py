'''
Class for the ogs NUMERICS file.
'''

from __future__ import absolute_import, division, print_function
from ogs5py.fileclasses.base import OGSfile


class NUM(OGSfile):
    """
    Class for the ogs NUMERICS file.

    Keywords for a block
    --------------------
    - NUMERICS
        - COUPLED_PROCESS
        - COUPLING_CONTROL
        - COUPLING_ITERATIONS
        - DYNAMIC_DAMPING
        - ELE_GAUSS_POINTS
        - ELE_MASS_LUMPING
        - ELE_SUPG
        - ELE_UPWINDING
        - EXTERNAL_SOLVER_OPTION
        - FEM_FCT
        - GRAVITY_PROFILE
        - LINEAR_SOLVER
        - LOCAL_PICARD
        - NON_LINEAR_ITERATION
        - NON_LINEAR_SOLVER
        - NON_LINEAR_UPDATE_VELOCITY
        - OVERALL_COUPLING
        - PCS_TYPE
        - PLASTICITY_TOLERANCE
        - RENUMBER
        - TIME_STEPS

    Standard block
    --------------
    :PCS_TYPE: "GROUNDWATER_FLOW"
    :LINEAR_SOLVER: [[2, 5, 1.0e-06, 1000, 1.0, 1, 4]]
    :ELE_GAUSS_POINTS: 3

    Info
    ----
    See: ``add_block``
    """

    MKEYS = ["NUMERICS"]
    SKEYS = [["COUPLED_PROCESS",
              "COUPLING_CONTROL",
              "COUPLING_ITERATIONS",
              "DYNAMIC_DAMPING",
              "ELE_GAUSS_POINTS",
              "ELE_MASS_LUMPING",
              "ELE_SUPG",
              "ELE_UPWINDING",
              "EXTERNAL_SOLVER_OPTION",
              "FEM_FCT",
              "GRAVITY_PROFILE",
              "LINEAR_SOLVER",
              "LOCAL_PICARD",
              "NON_LINEAR_ITERATION",
              "NON_LINEAR_SOLVER",
              "NON_LINEAR_UPDATE_VELOCITY",
              "OVERALL_COUPLING",
              "PCS_TYPE",
              "PLASTICITY_TOLERANCE",
              "RENUMBER",
              "TIME_STEPS"]]

    STD = {"PCS_TYPE": "GROUNDWATER_FLOW",
           "LINEAR_SOLVER": [[2, 5, 1.0e-06, 1000, 1.0, 1, 4]],
           "ELE_GAUSS_POINTS": 3}

    def __init__(self, **OGS_Config):
        '''
        Input
        -----

        OGS_Config dictonary

        '''
        super(NUM, self).__init__(**OGS_Config)
        self.f_type = '.num'
