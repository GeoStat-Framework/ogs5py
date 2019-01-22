# -*- coding: utf-8 -*-
"""
Class for the ogs NUMERICS file.
"""

from __future__ import absolute_import, division, print_function
from ogs5py.fileclasses.base import BlockFile


class NUM(BlockFile):
    """
    Class for the ogs NUMERICS file.

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
        - NUMERICS

    Sub-Keywords ($) per Main-Keyword:
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

    Standard block:
        :PCS_TYPE: "GROUNDWATER_FLOW"
        :LINEAR_SOLVER: [2, 5, 1.0e-14, 1000, 1.0, 100, 4]

    Keyword documentation:
        https://ogs5-keywords.netlify.com/ogs/wiki/public/doc-auto/by_ext/num

    Reading routines:
        https://github.com/ufz/ogs5/blob/master/FEM/rf_num_new.cpp#L346

    See Also
    --------
    add_block
    """

    MKEYS = ["NUMERICS"]
    # sorted
    SKEYS = [
        [
            "PCS_TYPE",
            "RENUMBER",
            "PLASTICITY_TOLERANCE",
            "NON_LINEAR_ITERATION",
            "NON_LINEAR_SOLVER",
            "LINEAR_SOLVER",
            "OVERALL_COUPLING",
            "COUPLING_ITERATIONS",
            "COUPLING_CONTROL",
            "COUPLED_PROCESS",
            "EXTERNAL_SOLVER_OPTION",
            "ELE_GAUSS_POINTS",
            "ELE_MASS_LUMPING",
            "ELE_UPWINDING",
            "ELE_SUPG",
            "GRAVITY_PROFILE",
            "DYNAMIC_DAMPING",
            "LOCAL_PICARD1",
            "NON_LINEAR_UPDATE_VELOCITY",
            "FEM_FCT",
            "NEWTON_DAMPING",
            "ADDITIONAL_NEWTON_TOLERANCES",
            "REACTION_SCALING",  # really?
            "METHOD",  # really?
            #        "TIME_STEPS",
        ]
    ]

    STD = {
        "PCS_TYPE": "GROUNDWATER_FLOW",
        "LINEAR_SOLVER": [2, 5, 1.0e-14, 1000, 1.0, 100, 4],
    }

    def __init__(self, **OGS_Config):
        super(NUM, self).__init__(**OGS_Config)
        self.file_ext = ".num"
