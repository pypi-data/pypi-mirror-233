# -*- coding: utf-8 -*-
# @Time    : 2023/8/31 13:03
# @Author  : Quanfa
from .path_tool import MyPath
def create_project_at(folder=r'D:\Task\a1_Ongoing', name='test'):
    """
    create project and at folder. init then.
    """

    # date, version
    from datetime import datetime
    date = datetime.now().strftime("%Y%m%d")
    project_name = 'T' + date + '_' + name

    init_project(MyPath(folder + '/' + project_name))
    print(folder + '/' + project_name)


# def hang_up_project_(folder=r'D:\Task', name=''):
#     pass


def init_project(root_path: MyPath):
    """
    init project framework in pycharm style
    """
    # init local, myclass, script
    class_path = root_path.cat('/myclasses')
    script_path = root_path.cat('/myscripts')
    report_path = root_path.cat('/myreport')
    local_path = root_path.cat('/mylocal')

    local_path.ensure()
    class_path.ensure()
    script_path.ensure()
    report_path.ensure()

    # init readme.md
    read_file = report_path.cat('/readme.md')
    read_file.ensure()

    # init git.ignore
    git_ignore = root_path.cat('/.gitignore')
    f = open(git_ignore, 'w')
    f.write('.idea\nmylocal\n')

    # set each path

    f = open(script_path + '/__init__.py', 'w')
    f.write(
        """
from EasyPro.FileSys import ScriptFileSaver
sfs = ScriptFileSaver(__file__, locals())

# region src_path
root_path = sfs.root_path
scripts_path = root_path.cat('myscripts')
local_path = root_path.cat('mylocal')
# endregion

if __name__ == '__main__':
    from EasyPro.FileSys.project import create_script
    create_script(scripts_path, name='test')
        """
    )


# def get_date_time():
#     return datetime.now().strftime("d%Y%m%ds%H%M")


# def get_date():
#     return get_date_time()[:9]


# def get_time():
#     return get_date_time()[9:]


def create_script(scripts_path: MyPath, name='test'):
    """
    create script for running or test.

    :param root_path: project path
    :param name: script name
    :return:
    """
    # region script path
    script_dir_path = scripts_path  # script dir

    file_names = script_dir_path.get_files('.py')
    index_files = list(file_names.keys())
    index = len(index_files)

    # build path
    script_path = script_dir_path.cat('s'+str(index)+'_'+ name + '.py')
    script_path: MyPath
    if script_path.exist():
        print('script in this name has already existed in your scripts:',script_path,'Try to use git if you want to edit your script to a new branch.')
        return False
    # endregion

    # write
    f = open(script_path, 'w')
    f.write(
        """# -*- coding: utf-8 -*-
from EasyPro.FileSys import ScriptFileSaver
sfs = ScriptFileSaver(__file__, locals())

if __name__ == '__main__':
    print('Running has finished')
 """
    )
    print('create script at', script_path)

