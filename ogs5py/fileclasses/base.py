#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
History
-------
Written,  SM, Mar 2018
"""
from __future__ import print_function, division
import os
import shutil
import itertools
import numpy as np

# current working directory
CWD = os.getcwd()
# indentation of subkeywords
SUB_IND = "  "
# indentation of content
CON_IND = "   "
# Top Comment for OGSpy
TOP_COM = "|-----------Written with ogs5py-----------|"


class OGSfile(object):
    """
    OGS Base class to derive all file formats.
    """

    MKEYS = []
    SKEYS = []

    STD = {}

    def __init__(self, task_root=CWD+"/ogs5model", task_id="model"):
        '''
        Initialize an OGS file.

        Parameters
        ----------
        task_root : string, optional
            Path to the destiny folder. Default is the current working dir
        task_id : string, optional
            Name for the ogs task. Default: "ogs"
        '''
#        self._add_doc()

        self.task_root = task_root
        self.task_id = task_id
        self.top_com = TOP_COM
        # placeholder for later derived classes for each file-type
        self.f_type = ".std"
        # list of main keywords indicated by "#"
        self.mainkw = []
        # list of subkeywords sorted by main keywords indicated by "$"
        # if no subkeyword is needed for content "" is set as subkeyword
        # for example with #POINTS in the *.gli file
        self.subkw = []
        # content of each subkeyword, each list is a line
        self.cont = []

        # if an existing file should be copied
        self.copy_file = None
        self.copy_path = None

    @classmethod
    def _get_clsname(cls):
        return cls.__name__

    def get_file_type(self):
        """Get the OGS file class name"""
        return self._get_clsname()

    def _add_doc(self):
        out = ""
        tab = "    "
        for i, mkw in enumerate(self.MKEYS):
            out += min(i, 1)*tab+"- "+mkw+"\n"
            for skw in self.SKEYS[i]:
                if skw:
                    out += 2*tab+"- "+skw+"\n"
                else:
                    out += 2*tab+"- no sub keyword\n"
        self.__doc__.format(out)

    @property
    def is_empty(self):
        """state if the OGS file is empty"""
        # check if the list of main keywords is empty
        return not bool(self.mainkw)

    def get_block_no(self):
        """Get the number of blocks in the file."""
        return len(self.mainkw)

    def reset(self):
        '''
        Delete every content.
        '''
        self.del_main_keyword(del_all=True)
        self._update_in()

    def update_block(self, index=None, main_key=None, **block):
        '''
        Update a Block from the actual file.

        Parameters
        ----------
        index : int or None, optional
            Positional index of the block of interest. As default, the last
            one is used. Default: None
        main_key : string, optional
            Main keyword of the block that should be updated (see: ``MKEYS``)
            This shouldn't be done.
            Default: None
        **block : keyword dict
            here the dict-keywords are the ogs-subkeywords and the value is
            the content that should be added with this ogs-subkeyword
            If a block should contain content directly connected to a main
            keyword, use this main keyword as input-keyword and the content as
            value: ``SUBKEY=content``
        '''
        # get the block
        upd_block = self.get_block(index, as_dict=True)
        # change the main key if wanted
        if main_key is not None:
            upd_block["main_key"] = main_key
        # update the block
        upd_block.update(block)
        # remove the old one
        self.del_main_keyword(main_index=index, del_all=False)
        # set the updated one
        self.add_block(index=index, **upd_block)

    def get_block(self, index=None, as_dict=True):
        '''
        Get a Block from the actual file.

        Parameters
        ----------
        index : int or None, optional
            Positional index of the block of interest. As default, the last
            one is returned. Default: None
        as_dict : bool, optional
            Here you can state of you want the output as a dictionary, which
            can be used as key-word-arguments for `add_block`. If False,
            you get the main-key, a list of sub-keys and a list of content.
            Default: True
        '''
        # set the main keyword index
        if index is None:
            index = len(self.mainkw) - 1

        if -len(self.mainkw) <= index < len(self.mainkw):
            main_key = self.mainkw[index]
            sub_key = self.subkw[index]
            cont = self.cont[index]
        else:
            print("ogs5py " + self.get_file_type() +
                  ": get_block index out of bounds - "+str(index))
            if as_dict:
                return {}
            return None, [], []

        if as_dict:
            out = {"main_key": main_key}
            for sub, con in zip(sub_key, cont):
                out[sub] = con
            return out

        return main_key, sub_key, cont

    def add_block(self, index=None, main_key=None, **block):
        '''
        Add a new Block to the actual file.

        Keywords are the sub keywords of the actual file type:

        #MAIN_KEY
         $SUBKEY1
          content1 ...
         $SUBKEY2
          content2 ...

        which looks like the following:

        ``FILE.add_block(SUBKEY1=content1, SUBKEY2=content2)``

        Parameters
        ----------
        index : int or None, optional
            Positional index, where to insert the given Block.
            As default, it will be added at the end. Default: None.
        main_key : string, optional
            Main keyword of the block that should be added (see: ``MKEYS``)
            Default: the first main keyword of the file-type
        **block : keyword dict
            here the dict-keywords are the ogs-subkeywords and the value is
            the content that should be added with this ogs-subkeyword
            If a block should contain content directly connected to a main
            keyword, use this main keyword as input-keyword and the content as
            value: ``SUBKEY=content``
        '''
        if main_key is None:
            # workaround for main keywords with directly connected content
            main_block = set(block) & set(self.MKEYS)
            if main_block:
                for mkw in self.MKEYS:
                    if mkw not in main_block:
                        continue
                    self.add_main_keyword(mkw, main_index=index)
                    self.add_multi_content(block[mkw], main_index=index)
                return
            # for regular block take the first main keyword
            if self.MKEYS:
                main_key = self.MKEYS[0]
            else:
                return
        else:
            # format the main_key
            main_key = str(main_key)

        # if KEY is unknown do nothing
        if main_key not in self.MKEYS:
            print("ogs5py " + self.get_file_type() +
                  ": add_block - unknown main key '"+main_key+"'")
            return

        # get the index of the main keyword
        mindex = self.MKEYS.index(main_key)
        # set the standard input if None is given
        if not block:
            block = self.STD

        # format the dictonary to use upper-case keys
        # block = format_dict(block)
        if block:
            self.add_main_keyword(main_key, main_index=index)
        # iterate over sub keywords to prevent order
        # since the kwargs dict doesn't prevent the order of the input
        # this can lead to errors, if the keywords are not added in the right
        # order (for example MMP with PERMEABILITY_TENSOR and _DISTRIBUTION)
        for skw in self.SKEYS[mindex]:
            if skw not in block:
                continue
            if skw:  # needed? "" can't be a keyword
                self.add_sub_keyword(skw, main_index=index)
                self.add_multi_content(block[skw], main_index=index)

    def add_main_keyword(self, key, main_index=None):
        '''
        Add a new main keyword (#key) to the actual file

        Parameters
        ----------
        key : string
            key name
        main_index : int, optional
            position, where the new main keyword should be added between the
            existing ones. As default, it is placed at the end.
        '''
        if main_index is None:
            main_index = len(self.mainkw)
        self.mainkw.insert(main_index, key)
        self.subkw.insert(main_index, [])
        self.cont.insert(main_index, [])

    def add_sub_keyword(self, key, main_index=None, sub_index=None):
        '''
        Add a new sub keyword ($key) to the actual file

        Parameters
        ----------
        key : string
            key name
        main_index : int, optional
            index of the corresponding main keyword where the
            sub keyword should be added. As default, the last main keyword
            is taken.
        sub_index : int, optional
            position, where the new sub keyword should be added between the
            existing ones. As default, it is placed at the end.

        Notes
        -----
        There needs to be at least one main keyword, otherwise the subkeyword
        is not added.
        '''
        if main_index is None:
            main_index = len(self.mainkw) - 1
            if main_index == -1:
                # if no main key index is given, a subkey can't be added
                print("ogs5py " + self.get_file_type() +
                      ": Before adding a subkey, add a main keyword")
                return
        if sub_index is None:
            sub_index = len(self.subkw[main_index])
        self.subkw[main_index].insert(sub_index, key)
        self.cont[main_index].insert(sub_index, [])

    def add_content(self, content, main_index=None,
                    sub_index=None, line_index=None):
        '''
        Add single-line content to the actual file

        Parameters
        ----------
        content : list
            list containing one line of content given as a list of single
            statements
        main_index : int, optional
            index of the corresponding main keyword where the
            sub keyword should be added. As default, the last main keyword
            is taken.
        sub_index : int, optional
            index of the corresponding sub keyword where the
            content should be added. As default, the last sub keyword
            is taken.
        line_index : int, optional
            position, where the new line of content should be added between the
            existing ones. As default, it is placed at the end.

        Notes
        -----
        There needs to be at least one main keyword, otherwise the content
        is not added.

        If no sub keyword is present, a blank one ("") will be added
        and the content is then directly connected to the actual main keyword.
        '''
        # set the main keyword index
        if main_index is None:
            main_index = len(self.mainkw) - 1
            if main_index == -1:
                # if no main key index is given, content can't be added
                print("ogs5py " + self.get_file_type() +
                      ": Before adding content, add a main keyword")
                return
        # set the sub keyword index
        if sub_index is None:
            sub_index = len(self.subkw[main_index]) - 1
            if sub_index == -1:
                # if the content is directly related to the main keyword
                # add "" as a subkey
                self.add_sub_keyword("", main_index)
                sub_index = 0
        # get the position
        if line_index is None:
            line_index = len(self.cont[main_index][sub_index])
        # assure that content is a list of strings
        content = list(np.array(content, dtype=str).reshape(-1))
        # if the content is given as string with whitespaces, split it
        content = list(itertools.chain(*[con.split() for con in content]))
        # add the content (if sth was given (no blank lines))
        if content:
            self.cont[main_index][sub_index].insert(line_index, content)

    def add_multi_content(self, content, main_index=None, sub_index=None):
        '''
        Add multiple content to the actual file

        Parameters
        ----------
        content : list
            list containing lines of content, each given as a list of single
            statements
        main_index : int, optional
            index of the corresponding main keyword where the
            sub keyword should be added. As default, the last main keyword
            is taken.
        sub_index : int, optional
            index of the corresponding sub keyword where the
            content should be added. As default, the last sub keyword
            is taken.

        Notes
        -----
        There needs to be at least one main keyword, otherwise the content
        is not added.

        The content will be added at the end of the actual subkeyword.

        If no sub keyword is present, a blank one ("") will be added
        and the content is then directly connected to the actual main keyword.
        '''
        # we need a list of lists, where each row is a line
        # and a line can contain multiple contents
        content = np.array(content, ndmin=2, dtype=object)
        for con in content:
            self.add_content(con, main_index, sub_index)

    def del_main_keyword(self, main_index=None, del_all=False):
        '''
        Delete a main keyword (#key) by its position

        Parameters
        ----------
        main_index : int, optional
            position, which main keyword should be deleted. Default: -1
        del_all: bool, optional
            State, if all main keywords shall be deleted. Default: False
        '''
        # set the main keyword index
        if main_index is None:
            main_index = len(self.mainkw) - 1
        if del_all:
            self.mainkw = []
            self.subkw = []
            self.cont = []
        elif -len(self.mainkw) <= main_index < len(self.mainkw):
            del self.mainkw[main_index]
            del self.subkw[main_index]
            del self.cont[main_index]

    def del_sub_keyword(self, main_index=-1, sub_index=-1, del_all=False):
        '''
        Delete a sub keyword ($key) by its position

        Parameters
        ----------
        main_index : int, optional
            index of the corresponding main keyword where the
            sub keyword should be deleted. As default, the last main keyword
            is taken.
        pos : int, optional
            position, which sub keyword should be deleted. Default: -1
        del_all: bool, optional
            State, if all sub keywords shall be deleted. Default: False
        '''
        if -len(self.mainkw) <= main_index < len(self.mainkw):
            if del_all:
                self.subkw[main_index] = []
                self.cont[main_index] = []
            elif (-len(self.subkw[main_index]) <= sub_index <
                  len(self.subkw[main_index])):
                del self.subkw[main_index][sub_index]
                del self.cont[main_index][sub_index]

    def del_content(self, main_index=-1,
                    sub_index=-1, line_index=-1, del_all=False):
        '''
        Delete content by its position

        Parameters
        ----------
        main_index : int, optional
            index of the corresponding main keyword where the
            sub keyword should be deleted. As default, the last main keyword
            is taken.
        sub_index : int, optional
            index of the corresponding sub keyword where the
            content should be deleted. As default, the last sub keyword
            is taken.
        line_index : int, optional
            position of the content line, that should be deleted. Default: -1
        del_all: bool, optional
            State, if all content shall be deleted. Default: False
        '''
        if -len(self.mainkw) <= main_index < len(self.mainkw):
            if (-len(self.subkw[main_index]) <= sub_index <
                    len(self.subkw[main_index])):
                if del_all:
                    if self.subkw[main_index][sub_index]:
                        self.cont[main_index][sub_index] = []
                    else:
                        # if the content was directly related to the mainkw
                        self.del_sub_keyword(main_index, sub_index)
                elif (-len(self.cont[main_index][sub_index]) <= line_index <
                      len(self.cont[main_index][sub_index])):
                    del self.cont[main_index][sub_index][line_index]
                    # if no content is left and it was directly related to main
                    if not self.cont[main_index][sub_index]:
                        if not self.subkw[main_index][sub_index]:
                            self.del_sub_keyword(main_index, sub_index)

    def add_copy_link(self, path, symlink=False):
        '''
        Instead of writing a file, you can give a path to an existing file,
        that will be copied/linked to the target folder.

        Parameters
        ----------
        path : str
            path to the existing file that should be copied
        symlink : bool, optional
            on UNIX systems it is possible to use a symbolic link to save
            time if the file is big. Default: False
        '''
        if os.path.isfile(path):
            path = os.path.abspath(path)
            self.copy_file = "link" if symlink else "copy"
            self.copy_path = path
        else:
            print("ogs5py " + self.get_file_type() +
                  ": Given copy-path is not a readable file: "+path)

    def del_copy_link(self):
        '''
        Remove a former given link to an external file.
        '''
        self.copy_file = None
        self.copy_path = None

    def read_file(self, path, encoding=None, verbose=False):
        '''
        Read an existing OGS input file

        Parameters
        ----------
        path : str
            path to the existing file that should be read
        encoding : str or None, optional
            encoding of the given file. If ``None`` is given, the system
            standard is used. Default: ``None``
        verbose : bool, optional
            Print information of the reading process. Default: False
        '''
        # in python3 open was replaced with io.open
        # so we can use encoding key word in python2
        from io import open

        self.reset()

        with open(path, "r", encoding=encoding) as fin:
            # serach first main keyword
            mkw = search_mkw(fin)
            # if no main keyword is found, the file is corrupted
            if not mkw:
                if verbose:
                    print("ogs5py " + self.get_file_type() +
                          ": Given path is not a readable ogs-file: "+path)
                return
            subkw_found = False
            stop_found = mkw == "STOP"
            # if the STOP keyword is found first, the file is corrupted
            if stop_found:
                if verbose:
                    print("ogs5py " + self.get_file_type() +
                          ": ogs-file is empty: "+path)
                return
            # add the found keyword
            self.add_main_keyword(mkw)
            for line in fin:
                # remove comments
                sline = uncomment(line)
                # skip blank lines and comments
                if not sline:
                    continue
                if not is_key(sline) and not subkw_found:
                    # handle exceptional case when content is present
                    # without subkey (like #POINTS in .gli)
                    self.add_sub_keyword("")
                    subkw_found = True
                    self.add_content(sline)
                # check if given line is a key
                elif is_mkey(sline):
                    # if STOP is found, stop the reading
                    if get_key(sline) == "STOP":
                        stop_found = True
                        self._update_in()
                        return
                    self.add_main_keyword(get_key(sline))
                    subkw_found = False
                elif is_skey(sline):
                    self.add_sub_keyword(get_key(sline))
                    subkw_found = True
                else:
                    self.add_content(sline)

        # check if stop was found
        if not stop_found:
            if verbose:
                print("ogs5py " + self.get_file_type() +
                      ": Given ogs-file doesn't have a #STOP: "+path)
            self.reset()

    def save(self, path, **kwargs):
        '''
        Save the actual OGS input file in the given path.
        Its path is given by "task_root+task_id+f_type".

        Parameters
        ----------
        path : str
            path to where to file should be saved
        update : bool, optional
            state if the content should be updated before saving. Default: True
        '''
        if "update" in kwargs:
            update = bool(kwargs["update"])
        else:
            update = True
        # update the content
        if update:
            self._update_out()
        # bug in OGS5 ... mpd files need Windows line-ending
        if ((not self.is_empty and
             self.mainkw[0] == "MEDIUM_PROPERTIES_DISTRIBUTED")):
            lend = "\r\n"
        else:
            lend = "\n"

        # open the file
        with open(path, "w") as fout:
            # print top comment
            if self.top_com:
                print(self.top_com, end=lend, file=fout)
            # iterate over the main keywords
            for i, mkw in enumerate(self.mainkw):
                print("#"+mkw, end=lend, file=fout)
                # iterate over the subkeywords
                for j, skw in enumerate(self.subkw[i]):
                    # check if skw is not "" (as in the exception-case)
                    if skw:
                        print(SUB_IND+"$"+skw, end=lend, file=fout)
                    # iterate over the content
                    for con in self.cont[i][j]:
                        # bug in OGS5 ... mpd files need tab as separator
                        # and no initial indentation
                        if ((mkw == "MEDIUM_PROPERTIES_DISTRIBUTED" and
                             skw == "DATA")):
                            print(*con,
                                  # sep="\t", end=lend, file=fout)
                                  sep=" ", end="\n", file=fout)
                        else:
                            print(CON_IND, *con,
                                  sep=" ", end=lend, file=fout)
            # write the final STOP keyword
            print("#STOP", end="", file=fout)

    def write_file(self):
        '''
        Write the actual OGS input file to the given folder.
        Its path is given by "task_root+task_id+f_type".
        '''
        # update the content
        self._update_out()
        # create the file path
        if not os.path.exists(self.task_root):
            os.makedirs(self.task_root)
        f_path = os.path.join(self.task_root, self.task_id+self.f_type)
        # check if we can copy the file or if we need to write it from data
        if self.copy_file is None:
            # if no content is present skip this file
            if not self.is_empty:
                self.save(f_path)
        # copy a given file if wanted
        elif self.copy_file == "copy":
            shutil.copyfile(self.copy_path, f_path)
        else:
            os.symlink(self.copy_path, f_path)

    def _update_in(self):
        '''
        An update routine to set the file data in the right format after input.
        '''
        pass

    def _update_out(self):
        '''
        An update routine to set the file data in the right format for output.
        '''
        pass

    def __repr__(self):
        """
        Return a formatted representation of the file.

        Info
        ----
        Type : str
        """
        out = ""
        for i, mkw in enumerate(self.mainkw):
            out += "#"+mkw+"\n"
            # iterate over the subkeywords
            for j, skw in enumerate(self.subkw[i]):
                # check if skw is not "" (as in the exception-case)
                if skw:
                    out += SUB_IND+"$"+skw+"\n"
                # iterate over the content
                for con in self.cont[i][j][:3]:
                    out += CON_IND+" ".join(con)+"\n"
                if len(self.cont[i][j]) > 3:
                    out += CON_IND+" ...\n"
        if self.mainkw:
            out += "#STOP"
        return out

    def __str__(self):
        """
        Return a formatted representation of the file.

        Info
        ----
        Type : str
        """
        return self.__repr__()


def search_mkw(fin):
    '''
    Search for the first main keyword in a given file-stream.

    Parameters
    ----------
    fin : stream
        given opened file
    '''
    mkw = ""
    for line in fin:
        # remove comments
        sline = uncomment(line)
        if not sline:
            continue
        if is_mkey(sline):
            mkw = get_key(sline)
            break
    return mkw


def uncomment(line):
    '''
    Remove OGS comments from a given line of an OGS file.
    Comments are indicated by ";". The line is then splitted by whitespaces.

    Parameters
    ----------
    line : str
        given line
    '''
    return line.split(";")[0].split()


def is_key(sline):
    '''
    Check if the given splitted line is an OGS key

    Parameters
    ----------
    sline : list of str
        given splitted line
    '''
    return sline[0][0] in ["$", "#"]


def is_mkey(sline):
    '''
    Check if the given splitted line is a main key

    Parameters
    ----------
    sline : list of str
        given splitted line
    '''
    return sline[0][0] == "#"


def is_skey(sline):
    '''
    Check if the given splitted line is a sub key

    Parameters
    ----------
    sline : list of str
        given splitted line
    '''
    return sline[0][0] == "$"


def get_key(sline):
    '''
    Get the key of a splitted line if there is any. Else return ""

    Parameters
    ----------
    sline : list of str
        given splitted line
    '''
    return sline[0][1:] if is_key(sline) else ""


def format_dict(dict_in):
    '''
    format the dictionary to use upper-case keys

    Parameters
    ----------
    dict_in : dict
        input dictionary
    '''
    dict_out = {}
    for key in dict_in:
        new_key = str(key).upper()
        if new_key != key and new_key in dict_in:
            print("Your given OGS-keywords are not unique: "+new_key)
            print("  --> DATA WILL BE LOST")
        dict_out[new_key] = dict_in[key]
    return dict_out
