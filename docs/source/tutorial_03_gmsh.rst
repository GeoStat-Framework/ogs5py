Tutorial 2: Interaction with pygmsh
===================================

In this example we are generating different meshes with the aid of
`pygmsh <https://github.com/nschloe/pygmsh>`_ and `gmsh <https://gmsh.info>`_

.. code-block:: python

    import numpy as np
    import pygmsh

    from ogs5py import OGS

    with pygmsh.geo.Geometry() as geom:
        poly = geom.add_polygon(
            [
                [+0.0, +0.5],
                [-0.1, +0.1],
                [-0.5, +0.0],
                [-0.1, -0.1],
                [+0.0, -0.5],
                [+0.1, -0.1],
                [+0.5, +0.0],
                [+0.1, +0.1],
            ],
            mesh_size=0.05,
        )

        geom.twist(
            poly,
            translation_axis=[0, 0, 1],
            rotation_axis=[0, 0, 1],
            point_on_axis=[0, 0, 0],
            angle=np.pi / 3,
        )

        mesh = geom.generate_mesh()

    model = OGS()
    # generate example above
    model.msh.import_mesh(mesh, import_dim=3)
    model.msh.show()
    # generate a predefined grid adapter in 2D
    model.msh.generate("grid_adapter2D", in_mat=1, out_mat=0, fill=True)
    model.msh.show(show_material_id=True)
    # generate a predefined grid adapter in 3D
    model.msh.generate("grid_adapter3D", in_mat=1, out_mat=0, fill=True)
    model.msh.show(show_material_id=True)
    # generate a predefined block adapter in 3D
    model.msh.generate("block_adapter3D", xy_dim=5.0, z_dim=1.0, in_res=1)
    model.msh.show(show_element_id=True)

.. image:: pics/03_gen_pygmsh.png
   :width: 400px
   :align: center

.. image:: pics/03_gen_2d_adapater.png
   :width: 400px
   :align: center

.. image:: pics/03_gen_3d_adapater.png
   :width: 400px
   :align: center

.. image:: pics/03_gen_block_adapater.png
   :width: 400px
   :align: center
