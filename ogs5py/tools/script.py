# -*- coding: utf-8 -*-
"""
Script generator for ogs5py.

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
import os
import shutil

from ogs5py.tools.types import STRTYPE, OGS_EXT, MULTI_FILES
from ogs5py.fileclasses.base import BlockFile


def formater(val):
    """
    Format values as string.

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
    Create content line for the script.

    Parameters
    ----------
    cont_line : list of values
        content line from a BlockFile
    """
    return "[" + ", ".join(map(formater, cont_line)) + "]"


def tab(num):
    """
    Get tab indentation.

    Parameters
    ----------
    num : int
        indentation depth
    """
    return num * 4 * " "


def add_block_file(block_file, script, ogs_cls_name="model"):
    """
    Add block-file creation to script.

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
        if block_file.is_block_unique(i):
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
        else:
            print(ogs_cls_name + "." + file_type + ".add_block(", file=script)
            print(tab(1) + "main_key=" + formater(mkey) + ",", file=script)
            line_no = len(cont[0])
            skey = skeys[0]
            # empty first value
            if (
                line_no == 0
                or (line_no == 1 and not cont[0][0])
                or (
                    line_no == 1
                    and len(cont[0][0]) == 1
                    and cont[0][0][0] == ""
                )
            ):
                print(tab(1) + skey + "=[],", file=script)
            # single first value
            elif line_no == 1 and len(cont[0][0]) == 1:
                print(
                    tab(1) + skey + "=" + formater(cont[0][0][0]) + ",",
                    file=script,
                )
            # single first line
            elif line_no == 1:
                print(
                    tab(1) + skey + "=" + get_line(cont[0][0]) + ",",
                    file=script,
                )
            # multiple first lines
            else:
                print(tab(1) + skey + "=[", file=script)
                for cont_k in cont[0]:
                    print(tab(2) + get_line(cont_k) + ",", file=script)
                print(tab(1) + "],", file=script)
            print(")", file=script)
            # additional lines
            for j, skey in enumerate(skeys[1:]):
                j += 1  # get the right content
                print(
                    ogs_cls_name + "." + file_type + ".append_to_block(",
                    file=script,
                )
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
    Add a file to be loaded from a script.

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
    name = load_file.file_name
    file_type = load_file.get_file_type().lower()
    print(
        ogs_cls_name + "." + file_type + ".read_file(" + formater(name) + ")",
        file=script,
    )


def add_list_file(list_file, script, typ, ogs_cls_name="model"):
    """
    Add a listed file to be loaded from a script.

    Parameters
    ----------
    list_file : File
        listed file that should be saved and then loaded from the script
    script : stream
        given opened file for the script
    typ : str
        typ of the list file
    ogs_cls_name : str
        name of the model within the script
    """
    list_file.write_file()
    name = list_file.name
    file_ext = list_file.file_ext
    file_name = name + file_ext
    print(ogs_cls_name + "." + typ + ".add(", file=script)
    print(tab(1) + "name=" + formater(name) + ",", file=script)
    print(tab(1) + "file_ext=" + formater(file_ext) + ",", file=script)
    print(")", file=script)
    print(
        ogs_cls_name + "." + typ + ".read_file(" + formater(file_name) + ")",
        file=script,
    )


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
    Generate a python script for the given model.

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
    load = ", ".join(load)
    # open the script file
    with open(path, "w") as script:
        print("# -*- coding: utf-8 -*-", file=script)
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

        for typ in MULTI_FILES:
            for file in getattr(ogs_class, typ):
                add_list_file(file, script, typ, ogs_cls_name)

        for copy_file in ogs_class.copy_files:
            base = os.path.basename(copy_file)
            shutil.copyfile(copy_file, os.path.join(script_dir, base))
            print(ogs_cls_name + ".add_copy_file(" + base + ")", file=script)

        print(ogs_cls_name + ".write_input()", file=script)
        print(ogs_cls_name + ".run_model()", file=script)
    ogs_class.task_root = original_root
