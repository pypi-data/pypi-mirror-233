# -*- coding: utf-8 -*-
# @Time    : 2023/1/12 12:03
# @Author  : Quanfa
# @Desc    :

from .path_tool import MyPath
from .matlab import save_mat, load_mat
import torch as saver
import sys


def save(object, path, name, suffix):
    if suffix == 'Figure':
        object.savefig(path)
    if suffix == 'mat':
        save_mat(object, path, name)
    else:
        saver.save(object, path)
    print('save ', name, ' at ', path)


class ScriptFileSaver:
    def __init__(self, script_file, locals, version: int = None):
        """
        A combination of database and saver in framework.

        :param root_path: local path
        :param date_mark:
        :param version:
        :param author:
        """
        self.locals = locals
        # region calculate version
        script_path = MyPath.from_file(script_file)
        relative_path = script_path.relative_to('myscripts').get_parent()
        script_name = MyPath.from_file(script_file).get_name()[:-3]
        root_path = script_path.my_root()
        local_path = root_path.cat('mylocal')
        save_path_parent = local_path.cat(relative_path).cat(script_name)
        save_path_parent.ensure()
        if version is None:
            version = 1
        # endregion
        self.local_path = save_path_parent.cat('s' + str(version))
        self.version = version
        self.local_path.ensure()
        self.root_path = root_path

        # region append project path to system
        # sys.path.append(root_path.cat('myclasses'))
        # sys.path.append(root_path.cat('myscripts'))
        if not root_path in sys.path:
            sys.path.append(root_path)
        # endregion

    def path_of(self, file_name='auto_save_result', suffix='sus'):
        """

        :param file_name:
        :return:
        """
        if suffix == '':
            path = self.local_path.cat(file_name)
        else:
            path = self.local_path.cat(file_name + '.' + suffix)

        return path

    def save(self, name, object=None, suffix=None, path=None):
        """
        保存变量，任意类型的python对象
        :param name: 保存的名字
        :param object: 如果没给定，就自动从内存中搜索
        :param suffix: sus, sci util saved; mat, matlab
        :return:
        """
        if object is None:
            object = self.locals[name]
        if suffix is None:
            suffix = str(type(object)).split("'")[1].split('.')[-1]
        if path is None:
            path = self.path_of(name, suffix)
        else:
            path = MyPath(path)

        save(object, path, name, suffix)
        return path

    def load(self, name=None, suffix=None, object_sample=None, path=None):
        """
        load from specified version.
        :param name:
        :return:
        """
        if path is None:
            if suffix is None:
                path = self.local_path.get_files(mark=name, list_r=True)[0]
                suffix = path.split('.')[-1]
            else:
                path = self.path_of(name, suffix)
        print('load ', suffix, ' from ', path)
        if object_sample is not None:
            return object_sample.load(path)
        if suffix == 'mat':
            return load_mat(path)
        else:
            return saver.load(path)
