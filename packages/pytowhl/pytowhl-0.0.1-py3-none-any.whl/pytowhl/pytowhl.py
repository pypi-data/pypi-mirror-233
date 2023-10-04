import import_ipynb
import os
from pathlib import Path

from logclshelper import LogClsHelper
from syshelper import SysHelper
from venvhelper import VenvHelper

class PyToWhl(LogClsHelper):

    def __init__(self, 
        pkg_dir = 'src/python/lib',
        pkg_current_version = '0.0.0',
        pkg_venv_dir = '/opt/venv/venv',
        pkg_venv_test_dir = '/opt/venv/venv-test'
    ):
        self.pkg_dir = Path(pkg_dir).absolute().as_posix()
        self.pkg_current_version = pkg_current_version

        self.pkg_name = os.path.basename(self.pkg_dir)
        self.parent_dir = Path(self.pkg_dir).parent.absolute().as_posix()

        self.pkg_venv_dir = Path(pkg_venv_dir).absolute().as_posix()
        self.pkg_venv_test_dir = Path(pkg_venv_test_dir).absolute().as_posix()

    @classmethod
    def run_cmd(cls, cmd):
        return SysHelper.run_cmd(cmd)

    @classmethod
    def get_installed_pkgs(cls):
        return cls.run_cmd('pip freeze').stdout.read().decode().split('\n')[:-1]

    @classmethod
    def install_pkgs(cls, pkgs = []):
        if(any(pkgs)):
            cls.run_cmd(f'pip install {" ".join(pkgs)}')

    @classmethod
    def uninstall_pkgs(cls, pkgs = []):
        if(any(pkgs)):
            cls.run_cmd(f'pip uninstall {" ".join(pkgs)} -y')

    def get_pkg_name(self):
        return self.pkg_name

    def get_pkg_version_to_build(self):
        return self.pkg_current_version

    def get_pkg_venv_dir(self):
        return self.pkg_venv_dir

    def get_pkg_venv_test_dir(self):
        return self.pkg_venv_test_dir
        
    def get_installed_pkgs_from_pkg_venv_dir(self):
        with VenvHelper.activate_context(self.get_pkg_venv_dir()):
            packages = self.get_installed_pkgs()

        return packages

    def uninstall_pkg_from_pkg_venv_test_dir(self):
        self.logger().debug(f'uninstall package {self.get_pkg_name()} from venv {self.get_pkg_venv_test_dir()}')
        
        with VenvHelper.activate_context(self.get_pkg_venv_test_dir()):    
            self.run_cmd(f'pip uninstall {self.get_pkg_name()} -y')

    def generate_requirements_txt_file_from_pkg_venv_dir(self, replace_if_exists = True):
        path = os.path.join(self.parent_dir, 'requirements.txt')
        if(replace_if_exists or (not os.path.exists(path))):
            self.logger().debug(f'generate {path} from venv {self.get_pkg_venv_dir()}')
            
            packages = [pkg.replace('==', '>=') for pkg in self.get_installed_pkgs_from_pkg_venv_dir()]
            
            with open(path, 'w') as fw:
                fw.write('\n'.join(packages))

    def generate_setup_py_lines(self):
        content = [
            'import setuptools',
            '\n',
            'with open("' + os.path.join(self.parent_dir, "requirements.txt") + '") as fr:',
            '\trequirements = fr.read().splitlines()',
            '\n',
            'setuptools.setup(',
            f'name="{self.get_pkg_name()}",',
            f'version="{self.get_pkg_version_to_build()}",',
            f'packages=setuptools.find_packages(),',
            'install_requires=requirements',
            ')',
        ]
        return content

    def generate_setup_py_file(self, replace_if_exists = True):   
        path = os.path.join(self.parent_dir, 'setup.py')
        if(replace_if_exists or (not os.path.exists(path))):
            self.logger().debug(f'generate {path}')
            
            with open(path, 'w') as fw:
                fw.write('\n'.join(self.generate_setup_py_lines()))    

    def generate_readme_md_content(self):
        content = [
            f'#### {self.get_pkg_name()} ####'
        ]
        return content

    def generate_readme_md_file(self, replace_if_exists = False):
        path = os.path.join(self.parent_dir, 'README.md')
        if(replace_if_exists or (not os.path.exists(path))):
            self.logger().debug(f'generate {path}')
            
            with open(path, 'w') as fw:
                fw.write('\n'.join(self.generate_readme_md_content()))   

    def generate_meta_files(self, 
        replace_if_exists_requirements_txt = True,
        replace_if_exists_setup_py = True,
        replace_if_exists_readme_md = False
    ):
        self.generate_requirements_txt_file_from_pkg_venv_dir(replace_if_exists = replace_if_exists_requirements_txt)
        self.generate_setup_py_file(replace_if_exists = replace_if_exists_setup_py)
        self.generate_readme_md_file(replace_if_exists = replace_if_exists_readme_md)

    def get_build_dir_paths(self):
        return [
            os.path.join(self.parent_dir, f'{self.get_pkg_name()}.egg-info'),
            os.path.join(self.parent_dir, 'dist'),
            os.path.join(self.parent_dir, 'build')
        ]
        
    def clear_build_dir_paths(self):
        for path in self.get_build_dir_paths():
            self.logger().debug(f'clear setup output dir {path}')
            
            self.run_cmd(f'rm -rf {path}/*')

    def build_wheel_from_setup_py_file(self):
        self.clear_build_dir_paths()
        
        self.logger().debug('activate temporary venv to run the build')
        with VenvHelper.activate_context(f'venv-pytowhl-{str(id(self))}'):
            self.logger().debug('install build required packages')
            self.run_cmd('pip install wheel build')
            
            self.logger().debug(f'build wheel from setup.py at {self.parent_dir}')
            self.run_cmd(f'python -m build {self.parent_dir}')

    def generate_meta_files_build(self,
        replace_if_exists_requirements_txt = True, 
        replace_if_exists_setup_py = True,
        replace_if_exists_readme_md = False
    ):
        self.generate_meta_files(
            replace_if_exists_requirements_txt = replace_if_exists_requirements_txt,
            replace_if_exists_setup_py = replace_if_exists_setup_py,
            replace_if_exists_readme_md = replace_if_exists_readme_md
        )
        
        self.build_wheel_from_setup_py_file()

    def install_as_editable_pkg_for_venv_test_dir(self):
        self.logger().debug(f'install {self.get_pkg_name()} as editable package for venv {self.get_pkg_venv_test_dir()}')
        VenvHelper.create_venv_if_not_exists(self.get_pkg_venv_test_dir())
        with VenvHelper.activate_context(self.get_pkg_venv_test_dir()):      
            SysUtils.run_cmd(f'pip install -e {self.parent_dir}')









