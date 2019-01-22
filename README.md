# Welcome to ogs5py

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.2546767.svg)](https://doi.org/10.5281/zenodo.2546767)
[![PyPI version](https://badge.fury.io/py/ogs5py.svg)](https://badge.fury.io/py/ogs5py)
[![Build Status](https://travis-ci.org/GeoStat-Framework/ogs5py.svg?branch=master)](https://travis-ci.org/GeoStat-Framework/ogs5py)
[![Documentation Status](https://readthedocs.org/projects/ogs5py/badge/?version=latest)](https://geostat-framework.readthedocs.io/projects/ogs5py/en/latest/?badge=latest)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

<p align="center">
<img src="https://raw.githubusercontent.com/GeoStat-Framework/ogs5py/master/docs/source/pics/OGS.png" alt="ogs5py-LOGO" width="251px"/>
</p>

## Purpose

ogs5py is A python-API for the [OpenGeoSys 5][ogs5_link] scientific modeling package.


## Installation

You can install the latest version with the following command:

    pip install ogs5py


## Documentation for ogs5py

You can find the documentation under [geostat-framework.readthedocs.io][doc_link].


### Further Information

- General homepage: https://www.opengeosys.org/ogs-5
- OGS5 Repository: https://github.com/ufz/ogs5
- Keyword documentation: https://ogs5-keywords.netlify.com
- OGS5 Benchmarks: https://github.com/ufz/ogs5-benchmarks
- ogs5py Benchmarks: https://github.com/GeoStat-Framework/ogs5py_benchmarks


### Tutorials and Examples

In the following a simple transient pumping test is simulated on a radial symmetric mesh.
The point output at the observation well is plotted afterwards.

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

<p align="center">
<img src="https://raw.githubusercontent.com/GeoStat-Framework/ogs5py/master/docs/source/pics/01_pump_test_drawdown.png" alt="Drawdown" width="600px"/>
</p>


### Reader

It comes along with a set of handy readers for almost all output formats:

* VTK Domain output

    ```python
    from ogs5py.reader import readvtk
    ```

* PVD Domain output

    ```python
    from ogs5py.reader import readpvd
    ```

* TECPLOT point output

    ```python
    from ogs5py.reader import readtec_point
    ```

* TECPLOT polyline output

    ```python
    from ogs5py.reader import readtec_polyline
    ```


### OGS5 executable

The OGS5 executable needs to be in your sys-path under ``ogs[.exe]``.
Otherwise you need to specify the path to the executable within the run command:

```python
model.run_model(ogs_root="path/to/ogs")
```


## Requirements:

- [NumPy >= 1.13.0](https://www.numpy.org)
- [Pandas >= 0.23.0](https://pandas.pydata.org/)
- [whichcraft](https://github.com/pydanny/whichcraft)
- [meshio](https://github.com/nschloe/meshio)
- [lxml](https://github.com/lxml/lxml)
- [vtk](https://vtk.org/)
- [pexpect](https://github.com/pexpect/pexpect)

## Contact

You can contact us via <info@geostat-framework.org>.


## License

[GPL][gpl_link] © 2018-2019 (inspired by Falk Hesse and Miao Jing)

[gpl_link]: https://github.com/GeoStat-Framework/ogs5py/blob/master/LICENSE
[ogs5_link]: https://www.opengeosys.org/ogs-5/
[doc_link]: https://geostat-framework.readthedocs.io/projects/ogs5py/en/latest/
