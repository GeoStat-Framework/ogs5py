# -*- coding: utf-8 -*-
import numpy as np
from ogs5py import OGS, MPD, by_id
from gstools import SRF, Gaussian

# covariance model for conductivity field
cov_model = Gaussian(dim=3, var=2, len_scale=10, anis=[1, 0.2])
srf = SRF(model=cov_model, mean=-9, seed=1000)
# ogs base class
model = OGS(task_root="test_het_3D", task_id="model", output_dir="out")
# generate a radial 3D mesh and conductivity field
model.gli.generate("radial", dim=3, angles=64, rad_out=100, z_size=-10)
model.gli.add_polyline("pwell", [[0, 0, 0], [0, 0, -10]])
model.msh.generate(
    "radial", dim=3, angles=64, rad=np.arange(101), z_arr=-np.arange(11),
)
cond = np.exp(srf.mesh(model.msh))
mpd = MPD(model.task_id)
mpd.add_block(
    MSH_TYPE="GROUNDWATER_FLOW",
    MMP_TYPE="PERMEABILITY",
    DIS_TYPE="ELEMENT",
    DATA=by_id(cond),
)
model.add_mpd(mpd)
for srf in model.gli.SURFACE_NAMES:  # set boundary condition
    model.bc.add_block(
        PCS_TYPE="GROUNDWATER_FLOW",
        PRIMARY_VARIABLE="HEAD",
        GEO_TYPE=["SURFACE", srf],
        DIS_TYPE=["CONSTANT", 0.0],
    )
model.st.add_block(  # set pumping condition at the pumpingwell
    PCS_TYPE="GROUNDWATER_FLOW",
    PRIMARY_VARIABLE="HEAD",
    GEO_TYPE=["POLYLINE", "pwell"],
    DIS_TYPE=["CONSTANT_NEUMANN", -1.0e-3],
)
model.ic.add_block(  # set the initial condition
    PCS_TYPE="GROUNDWATER_FLOW",
    PRIMARY_VARIABLE="HEAD",
    GEO_TYPE="DOMAIN",
    DIS_TYPE=["CONSTANT", 0.0],
)
model.mmp.add_block(  # permeability, storage and porosity
    GEOMETRY_DIMENSION=3,
    STORAGE=[1, 1.0e-4],
    PERMEABILITY_DISTRIBUTION=model.task_id + ".mpd",
    POROSITY=0.2,
)
model.num.add_block(  # numerical solver
    PCS_TYPE='GROUNDWATER_FLOW',
    LINEAR_SOLVER=[2, 5, 1.0e-14, 1000, 1.0, 100, 4],
)
model.out.add_block(  # set the outputformat
    PCS_TYPE="GROUNDWATER_FLOW",
    NOD_VALUES="HEAD",
    GEO_TYPE="DOMAIN",
    DAT_TYPE="PVD",
)
model.pcs.add_block(  # set the process type
    PCS_TYPE="GROUNDWATER_FLOW", NUM_TYPE="NEW", TIM_TYPE="STEADY"
)
model.write_input()
success = model.run_model()
