# -*- coding: utf-8 -*-
"""
This is the unittest for ogs5py.
"""
import os
import unittest
import numpy as np
from ogs5py import OGS, download_ogs, MSH, GLI, hull_deform


class TestOGS(unittest.TestCase):
    def setUp(self):
        self.ogs_path = os.getcwd()
        self.ogs_exe = download_ogs(path=self.ogs_path)

    def test_pump(self):
        self.model = OGS(task_root=os.path.join(self.ogs_path, "pump_test"))
        self.model.output_dir = "out"
        # generate a radial mesh
        self.model.msh.generate("radial", dim=2, rad=range(51))
        # generate a radial outer boundary
        self.model.gli.generate("radial", dim=2, rad_out=50.0)
        self.model.gli.add_points([0.0, 0.0, 0.0], "pwell")
        self.model.gli.add_points([1.0, 0.0, 0.0], "owell")

        self.model.bc.add_block(  # boundary condition
            PCS_TYPE="GROUNDWATER_FLOW",
            PRIMARY_VARIABLE="HEAD",
            GEO_TYPE=["POLYLINE", "boundary"],
            DIS_TYPE=["CONSTANT", 0.0],
        )
        self.model.st.add_block(  # source term
            PCS_TYPE="GROUNDWATER_FLOW",
            PRIMARY_VARIABLE="HEAD",
            GEO_TYPE=["POINT", "pwell"],
            DIS_TYPE=["CONSTANT_NEUMANN", -1.0e-04],
        )
        self.model.ic.add_block(  # initial condition
            PCS_TYPE="GROUNDWATER_FLOW",
            PRIMARY_VARIABLE="HEAD",
            GEO_TYPE="DOMAIN",
            DIS_TYPE=["CONSTANT", 0.0],
        )
        self.model.mmp.add_block(  # medium properties
            GEOMETRY_DIMENSION=2,
            STORAGE=[1, 1.0e-04],
            PERMEABILITY_TENSOR=["ISOTROPIC", 1.0e-4],
            POROSITY=0.2,
        )
        self.model.num.add_block(  # numerical solver
            PCS_TYPE="GROUNDWATER_FLOW",
            LINEAR_SOLVER=[2, 5, 1.0e-14, 1000, 1.0, 100, 4],
        )
        self.model.out.add_block(  # point observation
            PCS_TYPE="GROUNDWATER_FLOW",
            NOD_VALUES="HEAD",
            GEO_TYPE=["POINT", "owell"],
            DAT_TYPE="TECPLOT",
            TIM_TYPE=["STEPS", 1],
        )
        self.model.pcs.add_block(  # set the process type
            PCS_TYPE="GROUNDWATER_FLOW", NUM_TYPE="NEW"
        )
        self.model.tim.add_block(  # set the timesteps
            PCS_TYPE="GROUNDWATER_FLOW",
            TIME_START=0,
            TIME_END=600,
            TIME_STEPS=[[10, 30], [5, 60]],
        )
        self.model.write_input()
        self.success = self.model.run_model(ogs_exe=self.ogs_exe)
        self.assertTrue(self.success)
        self.point = self.model.readtec_point(pcs="GROUNDWATER_FLOW")
        self.time = self.point["owell"]["TIME"]
        self.head = self.point["owell"]["HEAD"]
        self.assertTrue(len(self.time) == len(self.head) == 16)
        self.assertAlmostEqual(self.head[-1], -0.55744648, places=3)
        self.pnt = self.model.output_files(
            pcs="GROUNDWATER_FLOW", typ="TEC_POINT"
        )
        self.ply = self.model.output_files(
            pcs="GROUNDWATER_FLOW", typ="TEC_POLYLINE"
        )
        self.vtk = self.model.output_files(pcs="GROUNDWATER_FLOW", typ="VTK")
        self.pvd = self.model.output_files(pcs="GROUNDWATER_FLOW", typ="PVD")
        self.assertTrue(len(self.ply) == len(self.vtk) == len(self.pvd) == 0)
        self.assertTrue(len(self.pnt) == 1)

        self.model.gen_script(os.path.join(self.ogs_path, "script"))
        self.model.load_model(self.model.task_root)
        self.model.task_root = "new_root"
        self.model.task_id = "new_id"
        self.model.reset()

    def test_mesh(self):
        self.msh = MSH()
        self.gli = GLI()
        self.msh2 = MSH()
        self.msh2.generate(generator="radial", dim=3, rad=[0, 1])

        self.msh.generate(generator="rectangular", dim=2)
        self.msh.generate(generator="rectangular", dim=3)
        self.msh.generate(generator="radial", dim=2)
        self.msh.generate(generator="radial", dim=2, rad=range(1, 11))
        self.msh.generate(generator="radial", dim=3)
        self.msh.generate(generator="radial", dim=3, rad=range(1, 11))
        self.msh.combine_mesh(self.msh2)
        self.msh.transform(
            hull_deform,
            niv_top=0,
            niv_bot=-1,
            func_top=lambda x, y: np.cos(np.sqrt(x ** 2 + y ** 2)) + 1,
        )
        self.gli.generate(generator="rectangular", dim=2)
        self.gli.generate(generator="rectangular", dim=3)
        self.gli.generate(generator="radial", dim=2)
        self.gli.generate(generator="radial", dim=2, rad_in=1)
        self.gli.generate(generator="radial", dim=3)
        self.gli.generate(generator="radial", dim=3, rad_in=1)

        self.msh.swap_axis()
        self.msh.swap_axis(axis1=0, axis2=2)
        self.msh.rotate(0.1)
        self.msh.shift((1, 1, 1))
        self.msh.export_mesh("test.vtk")
        self.msh.import_mesh("test.vtk")
        self.gli.swap_axis()
        self.gli.swap_axis(axis1=0, axis2=2)
        self.gli.rotate(0.1)
        self.gli.shift((1, 1, 1))

        self.cen = self.msh.centroids_flat
        self.mat = self.msh.MATERIAL_ID_flat
        self.vol = self.msh.volumes_flat
        self.nod = self.msh.node_centroids_flat
        self.msh.center

        self.assertTrue(
            len(self.cen) == len(self.mat) == len(self.vol) == len(self.nod)
        )


if __name__ == "__main__":
    unittest.main()
