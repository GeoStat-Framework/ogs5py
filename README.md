# Welcome to ogs5py

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.2546767.svg)](https://doi.org/10.5281/zenodo.2546767)
[![PyPI version](https://badge.fury.io/py/ogs5py.svg)](https://badge.fury.io/py/ogs5py)
[![Build Status](https://travis-ci.com/GeoStat-Framework/ogs5py.svg?branch=master)](https://travis-ci.org/GeoStat-Framework/ogs5py)
[![Coverage Status](https://coveralls.io/repos/github/GeoStat-Framework/ogs5py/badge.svg?branch=master)](https://coveralls.io/github/GeoStat-Framework/ogs5py?branch=master)
[![Documentation Status](https://readthedocs.org/projects/ogs5py/badge/?version=stable)](https://geostat-framework.readthedocs.io/projects/ogs5py/en/stable/?badge=stable)
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
For more details on this example, see: [Tutorial 1][tut1_link]

```python
from ogs5py import OGS, specialrange, generate_time
from matplotlib import pyplot as plt

# discretization and parameters
time = specialrange(0, 3600, 50, typ="cub")
rad = specialrange(0, 1000, 100, typ="cub")
obs = rad[21]
angles = 32
storage = 1e-3
transmissivity = 1e-4
rate = -1e-3
# model setup
model = OGS(task_root="pump_test", task_id="model")
# generate a radial mesh and geometry ("boundary" polyline)
model.msh.generate("radial", dim=2, rad=rad, angles=angles)
model.gli.generate("radial", dim=2, rad_out=rad[-1], angles=angles)
model.gli.add_points([0.0, 0.0, 0.0], "pwell")
model.gli.add_points([obs, 0.0, 0.0], "owell")
model.bc.add_block(  # boundary condition
    PCS_TYPE="GROUNDWATER_FLOW",
    PRIMARY_VARIABLE="HEAD",
    GEO_TYPE=["POLYLINE", "boundary"],
    DIS_TYPE=["CONSTANT", 0.0],
)
model.st.add_block(  # source term
    PCS_TYPE="GROUNDWATER_FLOW",
    PRIMARY_VARIABLE="HEAD",
    GEO_TYPE=["POINT", "pwell"],
    DIS_TYPE=["CONSTANT_NEUMANN", rate],
)
model.ic.add_block(  # initial condition
    PCS_TYPE="GROUNDWATER_FLOW",
    PRIMARY_VARIABLE="HEAD",
    GEO_TYPE="DOMAIN",
    DIS_TYPE=["CONSTANT", 0.0],
)
model.mmp.add_block(  # medium properties
    GEOMETRY_DIMENSION=2,
    STORAGE=[1, storage],
    PERMEABILITY_TENSOR=["ISOTROPIC", transmissivity],
)
model.num.add_block(  # numerical solver
    PCS_TYPE="GROUNDWATER_FLOW",
    LINEAR_SOLVER=[2, 5, 1e-14, 1000, 1.0, 100, 4],
)
model.out.add_block(  # point observation
    PCS_TYPE="GROUNDWATER_FLOW",
    NOD_VALUES="HEAD",
    GEO_TYPE=["POINT", "owell"],
    DAT_TYPE="TECPLOT",
)
model.pcs.add_block(  # set the process type
    PCS_TYPE="GROUNDWATER_FLOW", NUM_TYPE="NEW"
)
model.tim.add_block(  # set the timesteps
    PCS_TYPE="GROUNDWATER_FLOW",
    **generate_time(time)
)
model.write_input()
model.run_model()
```

<p align="center">
<img src="https://raw.githubusercontent.com/GeoStat-Framework/ogs5py/master/docs/source/pics/01_pump_test_drawdown.png" alt="Drawdown" width="600px"/>
</p>


### OGS5 executable

To obtain an OGS5 executable, ``ogs5py`` brings a download routine:

```python
from ogs5py import download_ogs
download_ogs()
```

Then a executable is stored in the ogs5py config path and will be called
when a model is run.

You can pass a ``version`` statement to the ``download_ogs`` routine, to
obtain a specific version (5.7, 5.7.1 (win only) and 5.8).
Also "latest" and "stable" are possible.
For OGS 5.7 there are executables for Windows/Linux and MacOS.
For "5.8", "latest" and "stable" there are no MacOS pre-builds.
Have a look at the documentation for all options.

If you have compiled your own OGS5 version, you can add your executable
to the ogs5py config path with:

```python
from ogs5py import add_exe
add_exe("path/to/your/ogs/exe")
```

Otherwise you need to specify the path to the executable within the run command:

```python
model.run_model(ogs_exe="path/to/ogs")
```


## Requirements:

- [NumPy >= 1.14.5](https://www.numpy.org)
- [Pandas >= 0.23.2](https://pandas.pydata.org/)
- [meshio >= 4.0.3; <5.0](https://github.com/nschloe/meshio)
- [lxml >= 4.0; <5.0](https://github.com/lxml/lxml)
- [pexpect >= 4.0; <5.0](https://github.com/pexpect/pexpect)
- [vtk >= 8.1](https://vtk.org/)

## Contact

You can contact us via <info@geostat-framework.org>.


## License

[MIT][gpl_link] © 2018-2020 (inspired by Falk Hesse and Miao Jing)

This project is based on [OGSPY][ogspy_link].

[ogspy_link]: https://github.com/fhesze/OGSPY
[gpl_link]: https://github.com/GeoStat-Framework/ogs5py/blob/master/LICENSE
[ogs5_link]: https://www.opengeosys.org/ogs-5/
[doc_link]: https://ogs5py.readthedocs.io/
[tut1_link]: https://geostat-framework.readthedocs.io/projects/ogs5py/en/stable/tutorial_01_pump.html
