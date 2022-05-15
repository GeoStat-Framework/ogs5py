# Changelog

All notable changes to **ogs5py** will be documented in this file.


## [1.2.0] - 2020-05-15

### Enhancements
* move to a `pyproject.toml` based installation: [d5ea756](https://github.com/GeoStat-Framework/ogs5py/commit/d5ea756629f3aaad6f4f8e197926f932677a6658)
* move from `develop`/`master` branches to a single `main` branch
* use GitHub Actions for CI: [b6811ce](https://github.com/GeoStat-Framework/ogs5py/commit/b6811ce3c39fa0eea849aac146384032cda10a37)
* use f-strings where possible [#11](https://github.com/GeoStat-Framework/ogs5py/pull/11)
* simplified documentation [#11](https://github.com/GeoStat-Framework/ogs5py/pull/11)
* added changelog to documentation [#11](https://github.com/GeoStat-Framework/ogs5py/pull/11)
* added citation file and paper reference [#11](https://github.com/GeoStat-Framework/ogs5py/pull/11)
* use Python 3 style classes [#11](https://github.com/GeoStat-Framework/ogs5py/pull/11)

### Changes
* `downlaod_ogs` only supports version "5.7", "5.7.1" and "5.8" since the CI for OGS5 was shut down: [8b1cc91](https://github.com/GeoStat-Framework/ogs5py/commit/8b1cc91e5e88ac65288bc30b9c44fda781b70710)

### Bugfixes
* make `downlaod_ogs` work again [8b1cc91](https://github.com/GeoStat-Framework/ogs5py/commit/8b1cc91e5e88ac65288bc30b9c44fda781b70710)
* documentation fix in `GLI.add_polyline` [#7](https://github.com/GeoStat-Framework/ogs5py/issues/7)
* require `pygmsh<7` for now [#11](https://github.com/GeoStat-Framework/ogs5py/pull/11)


## [1.1.1] - 2020-04-02

### Bugfixes
* check if `__version__` is present (only if installed)


## [1.1.0] - 2020-03-22

### Bugfixes
* meshio 4 was not compatible
* fixed integer type in exporting meshes with element/material IDs
* better check for OGS5 success on Windows

### Changes
* drop py2.7 support


## [1.0.5] - 2019-11-18

### Bugfixes
* ``MSH.set_material_id``: better handling of non-int single values: [f34d2e5](https://github.com/GeoStat-Framework/ogs5py/commit/f34d2e510e7bb340abc19150270b956c407d7ff6)
* ``MSH.show``: better handling of material IDs: [26b4610](https://github.com/GeoStat-Framework/ogs5py/commit/26b46108a14f4fe95e0b7424bb51e4482c75eae9)
* ``GLI.add_polyline``: Adding polyline by point-names was not possible: [17dd199](https://github.com/GeoStat-Framework/ogs5py/commit/17dd19944f49666f00d09fe2d21e88345439cf4d)

### Additions
* better integration of pygmsh: [570afd9](https://github.com/GeoStat-Framework/ogs5py/commit/570afd9d415c9fa402788c82f4864b7e6ddbf5d9)
* new functions ``specialrange`` and ``generate_time``: [e5f3aba](https://github.com/GeoStat-Framework/ogs5py/commit/e5f3aba542c41116e0fe0415e0eea6e689a7ccee)
* updated examples


## [1.0.4] - 2019-09-10

### Bugfixes
* ogs5py was not usable offline: [0f98c32](https://github.com/GeoStat-Framework/ogs5py/commit/0f98c32213d02b4b46455a5392b3c1c6fc021228)
* ``add_exe`` was not recognizing operation system: [89b07e5](https://github.com/GeoStat-Framework/ogs5py/commit/89b07e51df4b4f31b8c42c56e4ad24063c57f845)

### Additions
* new sub-keywords for OUT (added to OGS5 in Aug 19) when using TECPLOT (TECPLOT_ELEMENT_OUTPUT_CELL_CENTERED, TECPLOT_ZONES_FOR_MG): [ebcb22a](https://github.com/GeoStat-Framework/ogs5py/commit/ebcb22acb9afff83cc4593425d5dcde1bf97b9dc)

### Changes
* RFR Class was refactored to allow multiple variables: [3c1c445](https://github.com/GeoStat-Framework/ogs5py/commit/3c1c44533a9640ac1f2c173c321a029141f7aa2b)


## [1.0.3] - 2019-08-23

### Bugfixes
* ``MSH.show`` TempFile was not working on Windows: [c0d0960](https://github.com/GeoStat-Framework/ogs5py/commit/c0d0960b02c73237120030d6b1b23082dea085bc)


## [1.0.2] - 2019-08-22

### Bugfixes
* Don't fix QT_API for MAYAVI and use vtk for export: [33398ad](https://github.com/GeoStat-Framework/ogs5py/commit/33398adb4f3e1750e037434b8096c8eae7f0f419)
* ``PopenSpawn`` has no close attribute on Windows: [12f05d6](https://github.com/GeoStat-Framework/ogs5py/commit/12f05d6bcc5b5992f0d6aeb6feee09a4ca2f11b9)


## [1.0.1] - 2019-08-22

### Bugfixes
* ``download_ogs(version="latest" build="PETSC")`` was not working: [552503b](https://github.com/GeoStat-Framework/ogs5py/commit/552503b030634465aa324ebf3401fed8805c856b)


## [1.0.0] - 2019-08-22

### Bugfixes
* ``GLI.add_polyline`` now allows integer coordinates for points: [bf5d684](https://github.com/GeoStat-Framework/ogs5py/commit/bf5d684a2c01f2b6eb4e13098cfc77711c05d35d)
* ``MSH.centroids`` are now calculated as center of mass instead of center of element nodes: [b0708a6](https://github.com/GeoStat-Framework/ogs5py/commit/b0708a69bd290d613d663385193a3a9ff69ee625)
* ``MSH.show`` was not working: [6a0489b](https://github.com/GeoStat-Framework/ogs5py/commit/6a0489bc1675b909946e1a870459fc7f7ddf7629)
* ``OGS.run_model`` has now a better check for OGS success: [143d0ab](https://github.com/GeoStat-Framework/ogs5py/commit/143d0ab56e63f9e5cc1688bc621788ad42be67e9)
* ``GMSH`` interface was updated to new meshio-API: [d3e0594](https://github.com/GeoStat-Framework/ogs5py/commit/d3e05941a7a76a6d6fdf53a148af7b196fede66a)
* ``RFR`` file was not written: [41e55f3](https://github.com/GeoStat-Framework/ogs5py/commit/41e55f3d585afe6f8cdb9b94317d5166dc51b2e1)
* ``BC`` new sub-key TIME_INTERVAL was missing: [94ec5c5](https://github.com/GeoStat-Framework/ogs5py/commit/94ec5c500de8877dc462df6ef86af5ae0187625f)

### Additions
* ``download_ogs`` downloads a system dependent OGS5 executable: [ede32e4](https://github.com/GeoStat-Framework/ogs5py/commit/ede32e411785b51cdd0983a924c3c7ea117ab026)
* ``add_exe`` add a self compiled OGS5 executable: [ede32e4](https://github.com/GeoStat-Framework/ogs5py/commit/ede32e411785b51cdd0983a924c3c7ea117ab026)
* ``MSH.import_mesh`` now allows the import of material_id and element_id if given as cell_data in the external mesh: [00a77fa](https://github.com/GeoStat-Framework/ogs5py/commit/00a77fae9d492eb16872443e9be4262d4515da27)
* ``MSH.export_mesh`` now automatically exports material_id (already the case before) and element_id.
  Also you can now export additional ``point_data`` and ``field_data``: [00a77fa](https://github.com/GeoStat-Framework/ogs5py/commit/00a77fae9d492eb16872443e9be4262d4515da27)
* New method ``MSH.set_material_id`` to set the material IDs for specific elements: [4b11c6a](https://github.com/GeoStat-Framework/ogs5py/commit/4b11c6a70164565a8ab0b58d56b084b27ea781f1)
* ``MSH.show`` now can show additional cell_data: [ffd7604](https://github.com/GeoStat-Framework/ogs5py/commit/ffd76045e0591a00fd51c937ba62c4d5945c3fed)
* New routine ``show_vtk`` to show vtk output with mayavi: [f640c19](https://github.com/GeoStat-Framework/ogs5py/commit/f640c1977d7b9a869c56f61186613c8b9c9ef345)
* New method ``OGS.output_files`` to get a list of output files: [2f5f102](https://github.com/GeoStat-Framework/ogs5py/commit/2f5f10237c1b54d21b0b6a01598680e889dc7bf6)
* New attribute ``file_name`` for files: [632c2e7](https://github.com/GeoStat-Framework/ogs5py/commit/632c2e7b1ab33ec3b55bd8be6fbbe1f67d5c5651)
* BlockFile: new method ``append_to_block``: [efc9aac](https://github.com/GeoStat-Framework/ogs5py/commit/efc9aac16293960f199440d5df3ff924f8d593ff)
* ``OGS.gen_script`` now allowes multiple subkeys: [2cd344b](https://github.com/GeoStat-Framework/ogs5py/commit/2cd344b3ad6b6e1d7fcfd9e560854e5fe102b604)

### Changes
* ``MSH.export_mesh`` argument ``add_data_by_id`` renamed to ``cell_data_by_id``: [00a77fa](https://github.com/GeoStat-Framework/ogs5py/commit/00a77fae9d492eb16872443e9be4262d4515da27)
* ``OGS.run_model`` argument ``ogs_root`` renamed to ``ogs_exe``: [6fcdb61](https://github.com/GeoStat-Framework/ogs5py/commit/6fcdb617b4f61e738240830d637a0718732a66ad)
* Files that can occure multiple times (mpd, rfr, ...) are better handled now: [4a9c9d2](https://github.com/GeoStat-Framework/ogs5py/commit/4a9c9d2a2209e49b336bdb59fd51f3362be44c8f)
* ``ogs5py`` is now licensed under the MIT license: [ae96c0e](https://github.com/GeoStat-Framework/ogs5py/commit/ae96c0e7a5889632e9c34d0fc4577df587da3164)
* Extra named files now get their name by keyword ``name``: [632c2e7](https://github.com/GeoStat-Framework/ogs5py/commit/632c2e7b1ab33ec3b55bd8be6fbbe1f67d5c5651)


## [0.6.5] - 2019-07-05

### Bugfixes
* gli.add_polyline: Adding polyline by given point IDs was not possible: [3ec23af](https://github.com/GeoStat-Framework/ogs5py/commit/3ec23af77456200a128e8f9435be074375cb251d)

### Additions
* New swap_axis routine in msh and gli: You can now easily swap axis of a mesh. If you have generated a 2D mesh in x-y you can get a x-z cross-section by swapping the y and z axis: [3ec23af](https://github.com/GeoStat-Framework/ogs5py/commit/3ec23af77456200a128e8f9435be074375cb251d)


## [0.6.4] - 2019-05-16

### Bugfixes
* generator bugfix: more decimals to combine meshes: [51211a6](https://github.com/GeoStat-Framework/ogs5py/commit/51211a654c91432db0a46a5f269acfeed34c0076)
* Adopt new meshio container style: [b08260b](https://github.com/GeoStat-Framework/ogs5py/commit/b08260be821a09068a618c5e3b3804b7f0dcca38) [167fb2c](https://github.com/GeoStat-Framework/ogs5py/commit/167fb2c8e231ac4ab6a561a3b19345f2038065b0)
* Better checking for the ogs executable: [bffa41a](https://github.com/GeoStat-Framework/ogs5py/commit/bffa41a72d5283279428982ad82f07d16f1d9171) [6c3895f](https://github.com/GeoStat-Framework/ogs5py/commit/6c3895f25aa9c6b5316d31a0ea0cdc7eb289a839)
* Suppressing VTK Errors: [cfa4671](https://github.com/GeoStat-Framework/ogs5py/commit/cfa4671f93c54508db87aec181f9c8f0b892d61a)
* DOC updates: [9131e0c](https://github.com/GeoStat-Framework/ogs5py/commit/9131e0cf9e0e1f2a8d65ceaf0907fdbe4fa089bf) [7a27d8f](https://github.com/GeoStat-Framework/ogs5py/commit/7a27d8f9210362bd8516591a7aaa7d7d4004b7e9) [fc4314c](https://github.com/GeoStat-Framework/ogs5py/commit/fc4314cf5a4e055561bd8a4c805de06b6608082b)

### Additions
* New routine to zip data by IDs: [9accf6e](https://github.com/GeoStat-Framework/ogs5py/commit/9accf6e84b4cf25c485073c946728cc35d0c09ae)
* reading routines in the OGS Class: [592bc50](https://github.com/GeoStat-Framework/ogs5py/commit/592bc507ff10e9a8dbff5a49c510fa8acffe62a0)
* New `del_block` routine in Blockfiles: [8d15a90](https://github.com/GeoStat-Framework/ogs5py/commit/8d15a900103b72c2845129f5345ea8250be41384)


## [0.6.3] - 2019-03-21

### Bugfixes
* The used method os.makedirs has no keyword argument 'exist_ok' in python 2.7, so we prevent using it.
  See: [40fea36](https://github.com/GeoStat-Framework/ogs5py/commit/40fea361f55cb3fdbe6e420ffb419f359d7ee2ea)


## [0.6.2] - 2019-03-21

### Bugfixes
* The vtk reading routine could not read multiple scalar cell data.
  See: [568e7be](https://github.com/GeoStat-Framework/ogs5py/commit/568e7be105df6b60eb68b533940eaeba769e3a1b)


## [0.6.1] - 2019-01-22

### Bugfixes
* The BlockFile reading routine was cutting of the given keys.
  See: [d82fd30](https://github.com/GeoStat-Framework/ogs5py/commit/d82fd30f5400bf4d9cb9ea137b2ef4e9dc7b11a6)


## [0.6.0] - 2019-01-22

First release of ogs5py.


[Unreleased]: https://github.com/GeoStat-Framework/ogs5py/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/GeoStat-Framework/ogs5py/compare/v1.1.1...v1.2.0
[1.1.1]: https://github.com/GeoStat-Framework/ogs5py/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/GeoStat-Framework/ogs5py/compare/v1.0.5...v1.1.0
[1.0.5]: https://github.com/GeoStat-Framework/ogs5py/compare/v1.0.4...v1.0.5
[1.0.4]: https://github.com/GeoStat-Framework/ogs5py/compare/v1.0.3...v1.0.4
[1.0.3]: https://github.com/GeoStat-Framework/ogs5py/compare/v1.0.2...v1.0.3
[1.0.2]: https://github.com/GeoStat-Framework/ogs5py/compare/v1.0.1...v1.0.2
[1.0.1]: https://github.com/GeoStat-Framework/ogs5py/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/GeoStat-Framework/ogs5py/compare/v0.6.5...v1.0.0
[0.6.5]: https://github.com/GeoStat-Framework/ogs5py/compare/v0.6.4...v0.6.5
[0.6.4]: https://github.com/GeoStat-Framework/ogs5py/compare/v0.6.3...v0.6.4
[0.6.3]: https://github.com/GeoStat-Framework/ogs5py/compare/v0.6.2...v0.6.3
[0.6.2]: https://github.com/GeoStat-Framework/ogs5py/compare/v0.6.1...v0.6.2
[0.6.1]: https://github.com/GeoStat-Framework/ogs5py/compare/v0.6.0...v0.6.1
[0.6.0]: https://github.com/GeoStat-Framework/ogs5py/releases/tag/v0.6.0
