import subprocess
import os
from contextlib import contextmanager
from pathlib import Path 
from logclshelper import LogClsHelper
from syshelper import SysHelper

class VenvHelper(LogClsHelper):
  
    @classmethod
    def run_cmd(cls, cmd):
        return SysHelper.run_cmd(cmd)
        
    @classmethod
    def get_venv_paths(cls):
        paths = cls.run_cmd('find / -name "*activate" -type f').stdout.read().decode().split('\n')[:-1]
        venv_paths = [path.split('/bin/activate')[0] for path in paths if '/bin/activate' in path]
        return venv_paths

    @classmethod
    def remove_venv_paths_from_path(cls, venv_paths = None):

        if(venv_paths is None):
            venv_paths = self.get_venv_paths()
        
        paths = os.environ['PATH'].split(':')
        cls.logger().debug(f'remove venv paths {venv_paths} from $PATH {paths}')
        
        venv_path_bins = {os.path.join(venv_path, 'bin') for venv_path in venv_paths}
        paths_without_venv_path_bins = [path for path in paths if path not in venv_path_bins]
        os.environ['PATH'] =  ':'.join(paths_without_venv_path_bins)
        cls.logger().debug(f'$PATH {paths_without_venv_path_bins}')

    @classmethod
    def create_venv_if_not_exists(cls, venv_dir):
        if(not os.path.isdir(venv_dir)):
            cls.logger().debug(f'create venv {venv_dir}')
            cls.run_cmd(f'python -m venv {venv_dir}')
        else:
            cls.logger().debug(f'venv {venv_dir} already exists')
            
    @classmethod
    def remove_venv_from_path(cls, venv_dir):
        cls.remove_venv_paths_from_path([venv_dir])

    @classmethod
    def activate_venv(cls, venv_dir):
        cls.logger().debug(f'activate venv {venv_dir}')

        os.environ['VIRTUAL_ENV'] = venv_dir
        cls.remove_venv_from_path(venv_dir)
        os.environ['PATH'] =  venv_dir + '/bin:' + os.environ['PATH']

    @classmethod
    def deactivate_venv(cls, venv_dir):
        cls.logger().debug(f'deactivate venv {venv_dir}')

        cls.remove_venv_from_path(venv_dir)
        os.environ['VIRTUAL_ENV'] = ''

    @classmethod
    def remove_venv_dir(cls, venv_dir):
        cls.logger().debug(f'remove venv dir {venv_dir}')
        cls.run_cmd(f'rm -rf {venv_dir}')

    @classmethod
    @contextmanager
    def activate_context(cls, venv_dir):      
        should_remove = False
        try:
            cls.logger().debug(f'$PATH before context {os.environ["PATH"].split(":")}')
            if(not os.path.isdir(venv_dir)):
                cls.create_venv_if_not_exists(venv_dir)
                should_remove = True
                cls.logger().debug(f'venv {venv_dir} just created, it will be deleted at the end of context')
            
            cls.activate_venv(venv_dir)
            cls.logger().debug(f'$PATH during context {os.environ["PATH"].split(":")}')
            yield
        finally:
            cls.deactivate_venv(venv_dir)
            if(should_remove):
                cls.remove_venv_dir(venv_dir)
            cls.logger().debug(f'$PATH after context {os.environ["PATH"].split(":")}')











