=================
ogs5py Quickstart
=================

.. image:: pics/OGS.png
   :width: 150px
   :align: center

ogs5py is A python-API for the `OpenGeoSys 5 <https://www.opengeosys.org/ogs-5/>`_ scientific modeling package.


Installation
============

The package can be installed via `pip <https://pypi.org/project/gstools/>`_.
On Windows you can install `WinPython <https://winpython.github.io/>`_ to get
Python and pip running.

.. code-block:: none

    pip install ogs5py


Further Information
===================

- General homepage: https://www.opengeosys.org/ogs-5
- OGS5 Repository: https://github.com/ufz/ogs5
- Keyword documentation: https://ogs5-keywords.netlify.com
- OGS5 Benchmarks: https://github.com/ufz/ogs5-benchmarks
- ogs5py Benchmarks: https://github.com/GeoStat-Framework/ogs5py_benchmarks


Pumping Test Example
====================

In the following a simple transient pumping test is simulated on a radial symmetric mesh.
The point output at the observation well is plotted afterwards.

.. code-block:: python

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

.. image:: pics/01_pump_test_drawdown.png
   :width: 400px
   :align: center


OGS5 executable
===============

To obtain an OGS5 executable, ``ogs5py`` brings a download routine :any:`download_ogs`:

.. code-block:: python

    from ogs5py import download_ogs
    download_ogs()

Then a executable is stored in the ogs5py config path and will be called
when a model is run.

You can pass a ``version`` statement to the ``download_ogs`` routine, to
obtain a specific version (5.7, 5.7.1 (win only) and 5.8).
Also "latest" and "stable" are possible.
For OGS 5.7 there are executables for Windows/Linux and MacOS.
For "5.8", "latest" and "stable" there are no MacOS pre-builds.
Have a look at the documentation for all options.

If you have compiled your own OGS5 version, you can add your executable
to the ogs5py config path with :any:`add_exe`:

.. code-block:: python

    from ogs5py import add_exe
    add_exe("path/to/your/ogs/exe")

Otherwise you need to specify the path to the executable within the run command:

.. code-block:: python

    model.run_model(ogs_exe="path/to/ogs")


Requirements
============

- `NumPy >= 1.14.5 <https://www.numpy.org>`_
- `Pandas >= 0.23.2 <https://pandas.pydata.org/>`_
- `meshio >= 4.0.3; <5.0 <https://github.com/nschloe/meshio>`_
- `lxml >= 4.0; <5.0 <https://github.com/lxml/lxml>`_
- `pexpect >= 4.0; <5.0 <https://github.com/pexpect/pexpect>`_
- `vtk >= 8.1 <https://vtk.org/>`_


License
=======

`MIT <https://github.com/GeoStat-Framework/ogs5py/blob/master/LICENSE>`_
