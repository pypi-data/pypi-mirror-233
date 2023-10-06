import compileall
import os
import runpy

from shutil import copy as scopy
from os import remove
from .FileSys.path_tool import MyPath

def copy(src, dst):
    pdst = os.path.dirname(dst)
    if not os.path.exists(pdst):  # 如果路径不存在
        os.makedirs(pdst)
    scopy(src, dst)

def delete_gap_dir(dir):
        if os.path.isdir(dir):
            for d in os.listdir(dir):
                delete_gap_dir(os.path.join(dir, d))
            if not os.listdir(dir):
                os.rmdir(dir)

def compile_to(
        src: MyPath=r'package',
        dst: MyPath=r'release_folder',
        py_version='36', name='EasyPro',
        version=None,
        delete=False,
        upload=True,
):
    if version is None:
        from datetime import datetime
        version = py_version+'.'+datetime.now().strftime("%Y.%m.%d.%H.%M")
    version = version.replace('.0','.')


    release_folder = dst.cat('release_'+name)
    pakage_copy = release_folder.cat(name)

    # region clear
    for root, dirs, files in os.walk(src):
        for file in files:
            if '.pyc' in file:
                path = MyPath(root).cat(file)
                remove(path)

    for root, dirs, files in os.walk(pakage_copy):
        for file in files:
            path = MyPath(root).cat(file)
            remove(path)

    delete_gap_dir(pakage_copy)
    # endregion

    for root, dirs, files in os.walk(src):
        for file in files:
            src_path = MyPath(root).cat(file)
            dst_path = src_path.replace(src, pakage_copy)
            if '.py' in file and not'.pyc' in file:
                dst_path = dst_path.replace('/__pycache__', '').replace('.cpython-' + py_version, '')
                copy(src_path, dst_path)
                continue

    # generate setup
    ds = pakage_copy.split('/')
    dst_path = MyPath('').cat(*ds[:-1])

    f = dst_path.cat('setup.py')
    f.ensure()
    f = open(f, 'w')
    f.write(
        """# -*- coding:utf-8 -*-
import sys
sys.argv.append('sdist')
from distutils.core import setup
from setuptools import find_packages

setup(name=\'""" + name + """\',
            version=\'""" + version + """\',
            packages=find_packages(),  
            description='A python lib for xxxxx',
            long_description='',
            author='Quanfa',
            package_data={
            '': ['*.py'],
            },
            author_email='quanfa@tju.edu.cn',
            url='http://www.xxxxx.com/',
            license='MIT',
            )

            """
    )
    f.close()
    if True:
        f = dst_path.cat('compile.py')
        f.ensure()
        f = open(f, 'w')
        f.write(
            """# -*- coding:utf-8 -*-
from os.path import abspath
path = abspath(__file__).replace('\\\\', '/')
mask = 'T20'
paths = path.split('/')
root_path = ''
for c in paths:
    root_path += c
    if mask in c:
        break
    root_path += '/'
import sys

sys.path.append(root_path)
from distutils.core import setup
from setuptools import find_packages
import os
sys.argv.append('sdist')
dst_path = \'"""+dst_path+ """\'
os.chdir(dst_path)
import runpy
runpy.run_path(r\'"""+dst_path.cat('setup.py')+"""\')
                    """
        )
        f.close()

        runpy.run_path(dst_path.cat('compile.py'))

        release_name = name + '-' + version + '.tar.gz'
        rp = dst.cat(release_name)
        copy(dst_path.cat('dist', release_name), rp)

    if delete:
        for root, dirs, files in os.walk(release_folder):
            for file in files:
                path = os.path.join(root, file)
                remove(path)

        try:
            delete_gap_dir(release_folder)
        except:
            pass


    if upload:
        mycmd = f"python -m twine upload  -u quanfa -p Py@70539 {rp}"
        s = os.system(mycmd)
        print(s)


def compile_(
        src: MyPath=r'package',
        dst: MyPath=r'release_folder',
        py_version='36', name='EasyPro',
        version=None,
        delete=False,
):
    if version is None:
        from datetime import datetime
        version = py_version+'.'+datetime.now().strftime("%Y.%m.%d.%H.%M")
    version = version.replace('.0','.')

    release_folder = dst.cat('release_'+name)
    pakage_copy = release_folder.cat(name)

    for root, dirs, files in os.walk(src):
        for file in files:
            if '.pyc' in file:
                path = MyPath(root).cat(file)
                remove(path)

    for root, dirs, files in os.walk(pakage_copy):
        for file in files:
            path = MyPath(root).cat(file)
            remove(path)
    def delete_gap_dir(dir):
        if os.path.isdir(dir):
            for d in os.listdir(dir):
                delete_gap_dir(os.path.join(dir, d))
            if not os.listdir(dir):
                os.rmdir(dir)

    delete_gap_dir(pakage_copy)

    compileall.compile_dir(src)

    for root, dirs, files in os.walk(src):
        for file in files:
            src_path = MyPath(root).cat(file)
            dst_path = src_path.replace(src, pakage_copy)
            if '.pyc' in file:
                if '__init__' in file:
                    continue
                dst_path = dst_path.replace('/__pycache__', '').replace('.cpython-' + py_version, '')
                copy(src_path, dst_path)
                continue
            if '__init__.py' in file:
                copy(src_path, dst_path)

    # generate setup
    ds = pakage_copy.split('/')
    dst_path = MyPath('').cat(*ds[:-1])

    f = dst_path.cat('setup.py')
    f.ensure()
    f = open(f, 'w')
    f.write(
        """# -*- coding:utf-8 -*-
import sys
sys.argv.append('sdist')
from distutils.core import setup
from setuptools import find_packages

setup(name=\'""" + name + """\',
            version=\'""" + version + """\',
            packages=find_packages(),  
            description='A python lib for xxxxx',
            long_description='',
            author='Quanfa',
            package_data={
            '': ['*.pyc'],
            },
            author_email='quanfa@tju.edu.cn',
            url='http://www.xxxxx.com/',
            license='MIT',
            )

            """
    )
    f.close()
    if True:
        f = dst_path.cat('compile.py')
        f.ensure()
        f = open(f, 'w')
        f.write(
            """# -*- coding:utf-8 -*-
from os.path import abspath
path = abspath(__file__).replace('\\\\', '/')
mask = 'T20'
paths = path.split('/')
root_path = ''
for c in paths:
    root_path += c
    if mask in c:
        break
    root_path += '/'
import sys

sys.path.append(root_path)
from distutils.core import setup
from setuptools import find_packages
import os
sys.argv.append('sdist')
dst_path = \'"""+dst_path+ """\'
os.chdir(dst_path)
import runpy
runpy.run_path(r\'"""+dst_path.cat('setup.py')+"""\')
                    """
        )
        f.close()

        runpy.run_path(dst_path.cat('compile.py'))

        release_name = name + '-' + version + '.tar.gz'

        release_tar = dst.cat(release_name)

        copy(dst_path.cat('dist', release_name), release_tar)

    if delete:
        for root, dirs, files in os.walk(release_folder):
            for file in files:
                path = os.path.join(root, file)
                remove(path)

        try:
            delete_gap_dir(release_folder)
        except:
            pass


