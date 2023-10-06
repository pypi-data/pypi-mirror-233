# -*- coding: utf-8 -*-
# @Time    : 2023/8/31 11:22
# @Author  : Quanfa
import sys
from .FileSys.project import create_project_at

args = sys.argv[1:]

command = args[0]
print(args)
if command == 'create':
    try:
        project_path = args[1]
        project_name = args[2]
    except:
        print('create [project path] [project name]')

    create_project_at(project_path, project_name)