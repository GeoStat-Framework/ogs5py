# -*- coding: utf-8 -*-
"""
This is the unittest for ogs5py.
"""
from __future__ import division, absolute_import, print_function

import os
import unittest
from ogs5py import OGS, download_ogs
from ogs5py.ogs import OGS_NAME


class TestOGS(unittest.TestCase):
    def setUp(self):
        self.ogs_path = os.getcwd()
        self.ogs_name = OGS_NAME
        self.ogs_root = os.path.join(self.ogs_path, self.ogs_name)
        download_ogs(path=self.ogs_path, name=self.ogs_name)

    def test_pump(self):
        self.model = OGS(task_root=os.path.join(self.ogs_path, "pump_test"))
        # generate a radial mesh
        self.model.msh.generate("radial", dim=2, rad=range(51))
        # generate a radial outer boundary
        self.model.gli.generate("radial", dim=2, rad_out=50.)
        self.model.gli.add_points([0., 0., 0.], "pwell")
        self.model.gli.add_points([1., 0., 0.], "owell")

        self.model.bc.add_block(  # boundary condition
            PCS_TYPE='GROUNDWATER_FLOW',
            PRIMARY_VARIABLE='HEAD',
            GEO_TYPE=['POLYLINE', "boundary"],
            DIS_TYPE=['CONSTANT', 0.0],
        )
        self.model.st.add_block(  # source term
            PCS_TYPE='GROUNDWATER_FLOW',
            PRIMARY_VARIABLE='HEAD',
            GEO_TYPE=['POINT', "pwell"],
            DIS_TYPE=['CONSTANT_NEUMANN', -1.0e-04],
        )
        self.model.ic.add_block(  # initial condition
            PCS_TYPE='GROUNDWATER_FLOW',
            PRIMARY_VARIABLE='HEAD',
            GEO_TYPE='DOMAIN',
            DIS_TYPE=['CONSTANT', 0.0],
        )
        self.model.mmp.add_block(  # medium properties
            GEOMETRY_DIMENSION=2,
            STORAGE=[1, 1.0e-04],
            PERMEABILITY_TENSOR=['ISOTROPIC', 1.0e-4],
            POROSITY=0.2,
        )
        self.model.num.add_block(  # numerical solver
            PCS_TYPE='GROUNDWATER_FLOW',
            LINEAR_SOLVER=[2, 5, 1.0e-14, 1000, 1.0, 100, 4],
        )
        self.model.out.add_block(  # point observation
            PCS_TYPE='GROUNDWATER_FLOW',
            NOD_VALUES='HEAD',
            GEO_TYPE=['POINT', "owell"],
            DAT_TYPE='TECPLOT',
            TIM_TYPE=['STEPS', 1],
        )
        self.model.pcs.add_block(  # set the process type
            PCS_TYPE='GROUNDWATER_FLOW',
            NUM_TYPE='NEW',
        )
        self.model.tim.add_block(  # set the timesteps
            PCS_TYPE='GROUNDWATER_FLOW',
            TIME_START=0,
            TIME_END=600,
            TIME_STEPS=[
                [10, 30],
                [5, 60],
            ],
        )
        self.model.write_input()
        self.success = self.model.run_model(ogs_root=self.ogs_root)
        self.assertTrue(self.success)
        self.point = self.model.readtec_point(pcs='GROUNDWATER_FLOW')
        self.time = self.point['owell']["TIME"]
        self.head = self.point['owell']["HEAD"]
        self.assertTrue(len(self.time) == len(self.head) == 16)
        self.assertAlmostEqual(self.head[-1], -0.55744648, places=3)

        self.model.gen_script(os.path.join(self.ogs_path, "script"))
        self.model.load_model(self.model.task_root)


if __name__ == "__main__":
    unittest.main()
