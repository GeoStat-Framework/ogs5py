# Changelog

All notable changes to **ogs5py** will be documented in this file.


## [Unreleased]

### Bugfixes
* ``GLI.add_polyline`` now allows integer coordinates for points: https://github.com/GeoStat-Framework/ogs5py/commit/bf5d684a2c01f2b6eb4e13098cfc77711c05d35d
* ``MSH.centroids`` are now calculated as center of mass instead of center of element nodes: https://github.com/GeoStat-Framework/ogs5py/commit/b0708a69bd290d613d663385193a3a9ff69ee625
* ``MSH.show`` was not working: https://github.com/GeoStat-Framework/ogs5py/commit/6a0489bc1675b909946e1a870459fc7f7ddf7629
* ``OGS.run_model`` has now a better check for OGS success: https://github.com/GeoStat-Framework/ogs5py/commit/143d0ab56e63f9e5cc1688bc621788ad42be67e9
* ``GMSH`` interface was updated to new meshio-API: https://github.com/GeoStat-Framework/ogs5py/commit/d3e05941a7a76a6d6fdf53a148af7b196fede66a

### Additions
* ``download_ogs`` downloads a system dependent OGS5 executable: https://github.com/GeoStat-Framework/ogs5py/commit/ede32e411785b51cdd0983a924c3c7ea117ab026
* ``MSH.import_mesh`` now allows the import of material_id and element_id if given as cell_data in the external mesh: https://github.com/GeoStat-Framework/ogs5py/commit/00a77fae9d492eb16872443e9be4262d4515da27
* ``MSH.export_mesh`` now automatically exports material_id (already the case before) and element_id.
  Also you can now export additional ``point_data`` and ``field_data``: https://github.com/GeoStat-Framework/ogs5py/commit/00a77fae9d492eb16872443e9be4262d4515da27
* New method ``MSH.set_material_id`` to set the material IDs for specific elements: https://github.com/GeoStat-Framework/ogs5py/commit/4b11c6a70164565a8ab0b58d56b084b27ea781f1

### Changes
* ``MSH.export_mesh`` argument ``add_data_by_id`` renamed to ``cell_data_by_id``: https://github.com/GeoStat-Framework/ogs5py/commit/00a77fae9d492eb16872443e9be4262d4515da27
* ``ogs5py`` is now licensed under the MIT license

## [0.6.5] - 2019-07-05

### Bugfixes
* gli.add_polyline: Adding polyline by given point IDs was not possible: https://github.com/GeoStat-Framework/ogs5py/commit/3ec23af77456200a128e8f9435be074375cb251d

### Additions
* New swap_axis routine in msh and gli: You can now easily swap axis of a mesh. If you have generated a 2D mesh in x-y you can get a x-z cross-section by swapping the y and z axis: https://github.com/GeoStat-Framework/ogs5py/commit/3ec23af77456200a128e8f9435be074375cb251d


## [0.6.4] - 2019-05-16

### Bugfixes
* generator bugfix: more decimals to combine meshes: https://github.com/GeoStat-Framework/ogs5py/commit/51211a654c91432db0a46a5f269acfeed34c0076
* Adopt new meshio container style: https://github.com/GeoStat-Framework/ogs5py/commit/b08260be821a09068a618c5e3b3804b7f0dcca38 https://github.com/GeoStat-Framework/ogs5py/commit/167fb2c8e231ac4ab6a561a3b19345f2038065b0
* Better checking for the ogs executable: https://github.com/GeoStat-Framework/ogs5py/commit/bffa41a72d5283279428982ad82f07d16f1d9171 https://github.com/GeoStat-Framework/ogs5py/commit/6c3895f25aa9c6b5316d31a0ea0cdc7eb289a839
* Suppressing VTK Errors: https://github.com/GeoStat-Framework/ogs5py/commit/cfa4671f93c54508db87aec181f9c8f0b892d61a
* DOC updates: https://github.com/GeoStat-Framework/ogs5py/commit/9131e0cf9e0e1f2a8d65ceaf0907fdbe4fa089bf https://github.com/GeoStat-Framework/ogs5py/commit/7a27d8f9210362bd8516591a7aaa7d7d4004b7e9 https://github.com/GeoStat-Framework/ogs5py/commit/fc4314cf5a4e055561bd8a4c805de06b6608082b

### Additions
* New routine to zip data by IDs: https://github.com/GeoStat-Framework/ogs5py/commit/9accf6e84b4cf25c485073c946728cc35d0c09ae
* reading routines in the OGS Class: https://github.com/GeoStat-Framework/ogs5py/commit/592bc507ff10e9a8dbff5a49c510fa8acffe62a0
* New `del_block` routine in Blockfiles: https://github.com/GeoStat-Framework/ogs5py/commit/8d15a900103b72c2845129f5345ea8250be41384


## [0.6.3] - 2019-03-21

### Bugfixes
* The used method os.makedirs has no keyword argument 'exist_ok' in python 2.7, so we prevent using it.
  See: https://github.com/GeoStat-Framework/ogs5py/commit/40fea361f55cb3fdbe6e420ffb419f359d7ee2ea


## [0.6.2] - 2019-03-21

### Bugfixes
* The vtk reading routine could not read multiple scalar cell data.
  See: https://github.com/GeoStat-Framework/ogs5py/commit/568e7be105df6b60eb68b533940eaeba769e3a1b


## [0.6.1] - 2019-01-22

### Bugfixes
* The BlockFile reading routine was cutting of the given keys.
  See: https://github.com/GeoStat-Framework/ogs5py/commit/d82fd30f5400bf4d9cb9ea137b2ef4e9dc7b11a6### Added


## [0.6.0] - 2019-01-22

First release of ogs5py.


[Unreleased]: https://github.com/GeoStat-Framework/ogs5py/compare/v0.6.5...HEAD
[0.6.5]: https://github.com/GeoStat-Framework/ogs5py/compare/v0.6.4...v0.6.5
[0.6.4]: https://github.com/GeoStat-Framework/ogs5py/compare/v0.6.3...v0.6.4
[0.6.3]: https://github.com/GeoStat-Framework/ogs5py/compare/v0.6.2...v0.6.3
[0.6.2]: https://github.com/GeoStat-Framework/ogs5py/compare/v0.6.1...v0.6.2
[0.6.1]: https://github.com/GeoStat-Framework/ogs5py/compare/v0.6.0...v0.6.1
[0.6.0]: https://github.com/GeoStat-Framework/ogs5py/releases/tag/v0.6.0
