[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Welcome to ogs5py
=================

Purpose
-------
ogs5py is A python-API for the OpenGeoSys 5 scientific modeling package.


Installation
------------
You can install the latest version with the following command:

    pip install https://github.com/GeoStat-Framework/ogs5py/archive/master.zip


Contents
--------
With ogs5py you can setup, control and start an OGS5 model within python.

It comes along with a set of handy readers for almost all output formats:

* VTK Domain output

        ogs5py.reader.readvtk

* PVD Domain output

        ogs5py.reader.readpvd

* TECPLOT point output

        ogs5py.reader.readtec_point

* TECPLOT polyline output

        ogs5py.reader.readtec_polyline


Example
-------

In the following a simple transient pumping test is simulated on a radial symmetric mesh. The point output at the observation well is plotted afterwards.

```python
from ogs5py import OGS
from ogs5py.reader import readtec_point
from matplotlib import pyplot as plt

model = OGS(task_root="pump_test", task_id="model")

# generate a radial mesh
model.msh.generate("radial", dim=2, rad=range(51))
# generate a radial outer boundary
model.gli.generate("radial", dim=2, rad_out=50.)
model.gli.add_points([0., 0., 0.], "pwell")
model.gli.add_points([1., 0., 0.], "owell")

model.bc.add_block(  # boundary condition
    PCS_TYPE='GROUNDWATER_FLOW',
    PRIMARY_VARIABLE='HEAD',
    GEO_TYPE=['POLYLINE', "boundary"],
    DIS_TYPE=['CONSTANT', 0.0],
)
model.st.add_block(  # source term
    PCS_TYPE='GROUNDWATER_FLOW',
    PRIMARY_VARIABLE='HEAD',
    GEO_TYPE=['POINT', "pwell"],
    DIS_TYPE=['CONSTANT_NEUMANN', -1.0e-04],
)
model.ic.add_block(  # initial condition
    PCS_TYPE='GROUNDWATER_FLOW',
    PRIMARY_VARIABLE='HEAD',
    GEO_TYPE='DOMAIN',
    DIS_TYPE=['CONSTANT', 0.0],
)
model.mmp.add_block(  # medium properties
    GEOMETRY_DIMENSION=2,
    STORAGE=[1, 1.0e-04],
    PERMEABILITY_TENSOR=['ISOTROPIC', 1.0e-4],
    POROSITY=0.2,
)
model.num.add_block(  # numerical solver
    PCS_TYPE='GROUNDWATER_FLOW',
    LINEAR_SOLVER=[2, 5, 1.0e-14, 1000, 1.0, 100, 4],
)
model.out.add_block(  # domain output
    PCS_TYPE='GROUNDWATER_FLOW',
    NOD_VALUES='HEAD',
    GEO_TYPE='DOMAIN',
    DAT_TYPE='PVD',
    TIM_TYPE=['STEPS', 1],
)
model.out.add_block(  # point observation
    PCS_TYPE='GROUNDWATER_FLOW',
    NOD_VALUES='HEAD',
    GEO_TYPE=['POINT', "owell"],
    DAT_TYPE='TECPLOT',
    TIM_TYPE=['STEPS', 1],
)
model.pcs.add_block(  # set the process type
    PCS_TYPE='GROUNDWATER_FLOW',
    NUM_TYPE='NEW',
)
model.tim.add_block(  # set the timesteps
    PCS_TYPE='GROUNDWATER_FLOW',
    TIME_START=0,
    TIME_END=600,
    TIME_STEPS=[
        [10, 30],
        [5, 60],
    ],
)
model.write_input()
success = model.run_model()

point = readtec_point(
    task_root="pump_test",
    task_id="model",
    pcs='GROUNDWATER_FLOW',
)
time = point['owell']["TIME"]
head = point['owell']["HEAD"]

plt.plot(time, head)
plt.show()
```

Requirements
------------
The ogs5 executable needs to be in your sys-path. Otherwise you need to specify the path to the executable within the run command:

    ogs.run_model(ogs_root="path/to/ogs")

Created April 2018, Copyright Sebastian Mueller 2018

(inspired by Falk Hesse and Miao Jing)
