# -*- coding: utf-8 -*-
"""
script creation for ogs5py

.. currentmodule:: ogs5py.tools.script

Generator
^^^^^^^^^

.. autosummary::
   gen_script

Helpers
^^^^^^^

.. autosummary::
   formater
   get_line
   tab
   add_block_file
   add_load_file
   add_list_file

----
"""
from __future__ import division, print_function, absolute_import
import os
import shutil

from ogs5py.tools.types import STRTYPE, OGS_EXT
from ogs5py.fileclasses.base import BlockFile


def formater(val):
    """
    format values as string

    Parameters
    ----------
    val : value
        input value to be formatted
    """
    if isinstance(val, STRTYPE):
        # add quotes to strings
        return "'" + val + "'"
    return str(val)


def get_line(cont_line):
    """
    create content line for the script

    Parameters
    ----------
    cont_line : list of values
        content line from a BlockFile
    """
    return "[" + ", ".join(map(formater, cont_line)) + "]"


def tab(num):
    """
    tab indentation

    Parameters
    ----------
    num : int
        indentation depth
    """
    return num * 4 * " "


def add_block_file(block_file, script, ogs_cls_name="model"):
    """
    add block-file creation to script

    Parameters
    ----------
    block_file : BlockFile
        BlockFile class to be added to the script
    script : stream
        given opened file for the script
    ogs_cls_name : str
        name of the model within the script
    """
    block_no = block_file.get_block_no()
    file_type = block_file.get_file_type().lower()
    for i in range(block_no):
        mkey, skeys, cont = block_file.get_block(index=i, as_dict=False)
        print(ogs_cls_name + "." + file_type + ".add_block(", file=script)
        if "" not in skeys:
            print(tab(1) + "main_key=" + formater(mkey) + ",", file=script)
        for j, skey in enumerate(skeys):
            if skey == "":
                skey = mkey
            line_no = len(cont[j])
            # empty value
            if (
                line_no == 0
                or (line_no == 1 and not cont[j][0])
                or (
                    line_no == 1
                    and len(cont[j][0]) == 1
                    and cont[j][0][0] == ""
                )
            ):
                print(tab(1) + skey + "=[],", file=script)
            # single value
            elif line_no == 1 and len(cont[j][0]) == 1:
                print(
                    tab(1) + skey + "=" + formater(cont[j][0][0]) + ",",
                    file=script,
                )
            # single line
            elif line_no == 1:
                print(
                    tab(1) + skey + "=" + get_line(cont[j][0]) + ",",
                    file=script,
                )
            # multiple lines
            else:
                print(tab(1) + skey + "=[", file=script)
                for cont_k in cont[j]:
                    print(tab(2) + get_line(cont_k) + ",", file=script)
                print(tab(1) + "],", file=script)
        print(")", file=script)


def add_load_file(load_file, script, ogs_cls_name="model"):
    """
    add a file to be loaded from a script

    Parameters
    ----------
    load_file : OGSFile
        file that should be saved and then loaded from the script
    script : stream
        given opened file for the script
    ogs_cls_name : str
        name of the model within the script
    """
    if load_file.is_empty:
        return
    load_file.write_file()
    name = load_file.task_id + load_file.file_ext
    file_type = load_file.get_file_type().lower()
    print(
        ogs_cls_name + "." + file_type + ".read_file(" + formater(name) + ")",
        file=script,
    )


def add_list_file(list_file, script, base, cls_name, ogs_cls_name="model"):
    """
    add a listed file to be loaded from a script

    Parameters
    ----------
    list_file : File
        listed file that should be saved and then loaded from the script
    script : stream
        given opened file for the script
    base : str
        Base class of the listed file (MPD, GLIext, RFR, ...)
    cls_name : str
        name of the class in the script
    ogs_cls_name : str
        name of the model within the script
    """
    if base == "MPD":
        add = "add_mpd"
    elif base == "GLIext":
        add = "add_gli_ext"
    elif base == "RFR":
        add = "add_rfr"
    elif base == "GEMinit":
        add = "add_gem_init"
    else:  # ASC as default case
        base = "ASC"
        add = "add_asc"

    list_file.write_file()
    file_name = list_file.file_name
    file_ext = list_file.file_ext
    name = file_name + file_ext
    print(cls_name + " = " + base + "(", file=script)
    print(tab(1) + "file_name=" + formater(file_name) + ",", file=script)
    print(tab(1) + "file_ext=" + formater(file_ext) + ",", file=script)
    print(")", file=script)
    print(cls_name + ".read_file(" + formater(name) + ")", file=script)
    print(ogs_cls_name + "." + add + "(" + cls_name + ")", file=script)


def gen_script(
    ogs_class,
    script_dir=os.path.join(os.getcwd(), "ogs_script"),
    script_name="model.py",
    ogs_cls_name="model",
    task_root=None,
    task_id=None,
    output_dir=None,
    separate_files=None,
):
    """
    Generate a python script for the given model

    Parameters
    ----------
    ogs_class : OGS
        model class to be converted to a script
    script_dir : str
        target directory for the script
    script_name : str
        name for the script file (including .py ending)
    ogs_cls_name : str
        name of the model in the script
    task_root : str
        used task_root in the script
    task_id : str
        used task_id in the script
    output_dir : str
        used output_dir in the script
    separate_files : list of str or None
        list of files, that should be written to separate files and
        then loaded from the script

    Notes
    -----
    This will only create BlockFiles from the script. GLI and MSH files
    as well as every listed or line-wise file will be stored separately.
    """
    if separate_files is None:
        separate_files = []
    if task_root is None:
        task_root = ogs_class.task_root
    if task_id is None:
        task_id = ogs_class.task_id
    if not os.path.exists(script_dir):
        os.makedirs(script_dir)
    path = os.path.join(script_dir, script_name)
    # temporarily overwrite the task_root
    original_root = ogs_class.task_root
    ogs_class.task_root = script_dir
    # set the imported classes
    load = ["OGS"]
    if ogs_class.mpd:
        load.append("MPD")
    if ogs_class.gli_ext:
        load.append("GLIext")
    if ogs_class.rfr:
        load.append("RFR")
    if ogs_class.gem_init:
        load.append("GEMinit")
    if ogs_class.asc:
        load.append("ASC")
    load = ", ".join(load)
    # open the script file
    with open(path, "w") as script:
        print("# -*- coding: utf-8 -*-", file=script)
        # print("from __future__ import division, print_function", file=script)
        print("from ogs5py import " + load, file=script)
        print("", file=script)
        print(ogs_cls_name + " = OGS(", file=script)
        print(tab(1) + "task_root=" + formater(task_root) + ",", file=script)
        print(tab(1) + "task_id=" + formater(task_id) + ",", file=script)
        if output_dir is not None:
            print(
                tab(1) + "output_dir=" + formater(output_dir) + ",",
                file=script,
            )
        print(")", file=script)

        for ext in OGS_EXT:
            ogs_file = getattr(ogs_class, ext[1:])
            if (
                not isinstance(ogs_file, BlockFile)
                or ext[1:] in separate_files
            ):
                add_load_file(ogs_file, script, ogs_cls_name)
            else:
                add_block_file(ogs_file, script, ogs_cls_name)

        add_load_file(ogs_class.pqcdat, script, ogs_cls_name)

        for mpd_file in ogs_class.mpd:
            add_list_file(mpd_file, script, "MPD", "mpd_file", ogs_cls_name)

        for gli_ext_file in ogs_class.gli_ext:
            add_list_file(
                gli_ext_file, script, "GLIext", "gli_ext_file", ogs_cls_name
            )

        for rfr_file in ogs_class.rfr:
            add_list_file(rfr_file, script, "RFR", "rfr_file", ogs_cls_name)

        for gem_init_file in ogs_class.gem_init:
            add_list_file(
                gem_init_file, script, "GEMinit", "gem_init_file", ogs_cls_name
            )

        for asc_file in ogs_class.asc:
            add_list_file(asc_file, script, "ASC", "asc_file", ogs_cls_name)

        for copy_file in ogs_class.copy_files:
            base = os.path.basename(copy_file)
            shutil.copyfile(copy_file, os.path.join(script_dir, base))
            print(ogs_cls_name + ".add_copy_file(" + base + ")", file=script)

        print(ogs_cls_name + ".write_input()", file=script)
        print(ogs_cls_name + ".run_model()", file=script)
    ogs_class.task_root = original_root
