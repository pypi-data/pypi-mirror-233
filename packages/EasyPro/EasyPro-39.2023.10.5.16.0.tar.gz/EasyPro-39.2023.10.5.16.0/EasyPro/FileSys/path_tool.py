# -*- coding: utf-8 -*-
# @Time    : 2023/1/22 12:46
# @Author  : Quanfa
"""
path tool
# MyPath
    basic string format representing a path
"""
import os
from os.path import dirname, abspath


def get_files(directory: str, mark='.') -> dict:
    files = {}
    for filename in os.listdir(directory):
        if mark in filename:
            files[filename] = directory + "/" + filename
    return files


class MyPath(str):
    """
    basic class for the path of files (have . at the end) and directories.
    """

    def __new__(cls, path):
        path = str(path)
        if path == '':
            return str.__new__(cls, path)
        path = path.replace('\\', '/')
        if path[-1] == '/':
            path = path[: -1]
        return str.__new__(cls, path)

    def get_level(self, level_start, level_end=None):
        cs = self.split('/')

        if level_end is None:
            return cs[level_start]

        r = ''
        for c in cs[level_start: level_end]:
            r += '/' + c

        return r

    def cat(self, *value):
        result = self
        for other in value:
            if other == '':
                continue
            if other[0] == '/':
                other = MyPath(other[1:])
            else:
                other = MyPath(other)
            if result == '':
                result = other
            else:
                result = result + '/' + other
        result = MyPath(result)
        return result

    def is_file(self):
        name = self.get_name()
        if '.' in name:
            return True
        return False

    def get_name(self):
        return self.split('/')[-1]

    def suffix_of(self):
        if self.is_file():
            return self.split('.')[-1]
        return ''

    def get_parent(self):
        """parent of the file or directory"""
        return MyPath(dirname(self))

    # region existence
    def ensure(self):
        """make sure that the path exist."""
        path = self
        # if path is directory
        if self.is_file():
            path.get_parent().ensure()
            f = open(path, 'a')
            f.close()
        else:
            if not os.path.exists(path):
                os.makedirs(path)

    def exist(self) -> bool:
        return os.path.exists(self)

    # endregion
    @staticmethod
    def from_file(file=__file__):
        return MyPath(abspath(file))

    @staticmethod
    def get_root(file, mask='T20'):
        """ get root using file in .../T20*"""
        path = MyPath.from_file(file)
        return path.my_root(mask)

    def my_root(self, mask='T20'):
        paths = self.split('/')
        path = ''
        for c in paths:
            path += c
            if mask in c:
                break
            path += '/'
        return MyPath(path)
    
    def relative_to(self, mask='T20'):
        path = self.split(mask)[1]
        return MyPath(path)

    def extend_to_sys(self):
        import sys
        sys.path.append(self)

    def get_files(self, mark='.', list_r=False):
        """
        :param mark: file mark, if mark in filename.
        :param list_r: if trans to list
        :return: dict or list
        """
        directory = self
        files = {}
        for filename in os.listdir(directory):
            if mark in filename:
                files[filename] = directory.cat(filename)
        if list_r:
            return list(files.values())
        return files


