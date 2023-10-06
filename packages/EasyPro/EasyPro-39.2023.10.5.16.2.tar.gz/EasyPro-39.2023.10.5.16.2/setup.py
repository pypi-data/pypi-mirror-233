# -*- coding:utf-8 -*-
import sys
sys.argv.append('sdist')
from distutils.core import setup
from setuptools import find_packages

setup(name='EasyPro',
            version='39.2023.10.5.16.2',
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

            