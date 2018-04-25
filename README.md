
ogs5py: A python-API for the OpenGeoSys 5 scientific modeling package
=====================================================================

Contents
--------
With ogs5py you can setup, control and start an OGS5 model within python.

It comes along with a set of handy readers for almost all output formats:

* VTK Domain output

        ogs5py.read.readvtk

* PVD Domain output

        ogs5py.read.readpvd

* TECPLOT point output

        ogs5py.read.readtec_point

* TECPLOT polyline output

        ogs5py.read.readtec_polyline


Example
-------
    import os
    import numpy as np
    from ogs5py import OGS
    from ogs5py.reader import readpvd
    # get the current working directory
    CWD = os.getcwd()
    # ------------------------ogs configuration---------------------------------- #
    pwell = "w00"
    dim_no = 2
    dire = os.path.dirname(CWD+"/test-ogs/")
    pcs_type_flow = 'GROUNDWATER_FLOW'
    var_name_flow = 'HEAD'
    t_id = 'pt'
    # ------------------------time configuration--------------------------------- #
    time_start = 0
    time_steps = np.array([10, 5, 4, 3, 2, 1, 4])
    step_size = np.array([30, 60, 300, 600, 900, 1800, 3600])
    time_end = np.sum(time_steps*step_size)
    # ------------------------generate ogs base class---------------------------- #
    ogs = OGS(task_root=dire+"/",
              task_id=t_id,
              output_dir=dire+"/"+pwell+"/")
    # ------------------------generate mesh + gli-------------------------------- #
    # generate a radial mesh
    ogs.msh.generate("radial", dim=dim_no, rad=np.arange(51))
    # generate a radial boundary geometry
    ogs.gli.generate("radial", dim=dim_no, rad_out=50.)
    # add the pumping well
    ogs.gli.add_points([0., 0., 0.], pwell)
    # --------------generate different ogs input classes------------------------- #
    # set boundary condition
    for ply in ogs.gli.POLYLINE_NAMES:
        ogs.bc.add_block(PCS_TYPE=pcs_type_flow,
                         PRIMARY_VARIABLE=var_name_flow,
                         GEO_TYPE=[['POLYLINE', ply]],
                         DIS_TYPE=[['CONSTANT', 0.0]])
    # set pumping condition at the pumpingwell
    ogs.st.add_block(PCS_TYPE=pcs_type_flow,
                     PRIMARY_VARIABLE=var_name_flow,
                     GEO_TYPE=[['POINT', pwell]],
                     DIS_TYPE=[['CONSTANT_NEUMANN', -1.0e-04]])
    # set the initial condition
    ogs.ic.add_block(PCS_TYPE=pcs_type_flow,
                     PRIMARY_VARIABLE=var_name_flow,
                     GEO_TYPE='DOMAIN',
                     DIS_TYPE=[['CONSTANT', 0.0]])
    # set the fluid properties
    ogs.mfp.add_block(FLUID_TYPE='LIQUID',
                      DENSITY=[[1, 1.0e+03]],
                      VISCOSITY=[[1, 1.0e-03]])
    # permeability, storage and porosity
    ogs.mmp.add_block(GEOMETRY_DIMENSION=dim_no,
                      STORAGE=[[1, 1.0e-04]],
                      PERMEABILITY_TENSOR=[['ISOTROPIC', 1.0e-4]],
                      POROSITY='0.2')
    # set the parameters for the solver
    ogs.num.add_block(PCS_TYPE=pcs_type_flow,
                      LINEAR_SOLVER=[[2, 5, 1.0e-06, 1000, 1.0, 1, 4]],
                      ELE_GAUSS_POINTS=3)
    # set the outputformat for the whole domain (just for checking)
    ogs.out.add_block(NOD_VALUES=var_name_flow,
                      GEO_TYPE='DOMAIN',
                      DAT_TYPE='PVD',
                      TIM_TYPE=[['STEPS', 1]])
    # set the process type
    ogs.pcs.add_block(PCS_TYPE=pcs_type_flow,
                      NUM_TYPE='NEW')
    # set the timesteps
    ogs.tim.add_block(PCS_TYPE=pcs_type_flow,
                      TIME_START=time_start,
                      TIME_END=time_end,
                      TIME_STEPS=zip(time_steps, step_size))
    # --------------run OGS simulation------------------------------------------- #
    print("write files")
    ogs.write_input()
    print("run model")
    ogs.run_model()
    print("load output")
    out = readpvd(task_root=dire+"/"+pwell+"/",
                  task_id=t_id,
                  pcs=None)
    print(out.keys())

Installation
------------
Just download the code an run the following command from the
source code directory:

    pip install -U .
    
Requirements
------------
The ogs5 executable needs to be in your sys-path. Otherwise you need to specify the path to the executable within the run command:

    ogs.run_model(ogs_root="path/to/ogs")

Created April 2018, Copyright Sebastian Mueller 2018
