import os
from pathlib import Path
import json

from logclshelper import LogClsHelper
from syshelper import SysHelper

class IPyToPy(LogClsHelper):

    def __init__(self, 
        nb_dir_path = 'src/notebook', 
        py_dir_path = 'src/python',
        suffix_nb_only = ' #nb#',
        prefix_py_only = '#py# '
    ):
        self.nb_dir_path = nb_dir_path
        self.py_dir_path = py_dir_path

        self.suffix_nb_only = suffix_nb_only
        self.prefix_py_only = prefix_py_only

    def format_nb_json(self, nb_json):
        for cell in nb_json['cells']:
            if('outputs' in cell):
                cell['outputs'] = []
                
    def format_nb_file(self, nb_path):
        self.__class__.logger().debug(f'format {nb_path}')
        
        nb_json = json.load(open(nb_path))
        self.format_nb_json(nb_json)
        
        with open(nb_path, "w") as outfile:
            json.dump(nb_json, outfile)

    def yield_nb_file_paths(self):
        return SysHelper.yield_filtered_paths(
            parent_dir = self.nb_dir_path,
            lambda_filter_path = lambda path : path.endswith('.ipynb') and ('.ipynb_checkpoints/' not in path),
            accept_dirs = False
        )
        
    def format_nb_files(self):
        for nb_path in self.yield_nb_file_paths():
            self.format_nb_file(nb_path)

    def get_py_path_from_nb_path(self, nb_path):
        return nb_path.replace(self.nb_dir_path, self.py_dir_path).replace('.ipynb', '.py')

    def yield_py_lines_from_nb_cell_code_source(self, nb_cell_code_source):
        last_stripped_line = ''
        for line in nb_cell_code_source:
            stripped_line = line.strip()
                
            if(not stripped_line.endswith(self.suffix_nb_only)): 
                if(stripped_line or last_stripped_line):
                    if(stripped_line.startswith(self.prefix_py_only)):
                        line = line.replace(self.prefix_py_only, '')
                    yield line
                    last_stripped_line = stripped_line

    def yield_py_lines_from_nb_cell_markdown_source(self, nb_cell_markdown_source):
        for line in nb_cell_markdown_source:
            if line.strip():
                yield('#' + line)

    def yield_py_lines_from_nb_cell(self, nb_cell):
        if nb_cell['cell_type'] == 'code':
            return self.yield_py_lines_from_nb_cell_code_source(nb_cell['source'])

        elif nb_cell['cell_type'] == 'markdown':
            return self.yield_py_lines_from_nb_cell_markdown_source(nb_cell['source'])

    def yield_py_lines_from_nb_json(self, nb_json):
        for nb_cell in nb_json['cells']:
            for line in self.yield_py_lines_from_nb_cell(nb_cell):
                yield line
            yield '\n\n'
            
    def convert_nb_file_to_py_file(self, nb_path):
        nb_json = json.load(open(nb_path))
        py_path = self.get_py_path_from_nb_path(nb_path)

        self.__class__.logger().debug(f'convert {nb_path} to {py_path}')
        
        py_dir_path = os.path.dirname(py_path)
        Path(py_dir_path).mkdir(parents = True, exist_ok = True)
        
        with open(py_path, 'w+') as py_file:
            for line in self.yield_py_lines_from_nb_json(nb_json):
                py_file.write(line)
                
    def convert_nb_files_to_py_files(self):
        for nb_file_path in self.yield_nb_file_paths():
            self.convert_nb_file_to_py_file(nb_file_path)

    def format_convert_nb_files_to_py_files(self):
        self.format_nb_files()
        self.convert_nb_files_to_py_files()

    def is_path_nb_dir(self, path):
        nb_files = SysHelper.yield_filtered_paths(
            parent_dir = path,
            accept_dirs = False, 
            max_depth = 0,
            lambda_filter_path = lambda path : path.endswith('.ipynb')
        )

        nb_files_not_empty = next(nb_files, None) is not None
        return nb_files_not_empty
        
    def yield_nb_dir_paths(self):
        return SysHelper.yield_filtered_paths(
            parent_dir = self.nb_dir_path,
            lambda_filter_path = lambda path : self.is_path_nb_dir(path) and ('.ipynb_checkpoints/' not in path),
            accept_files = False
        )

    def yield_py_dir_paths(self):
        for nb_dir_path in self.yield_nb_dir_paths():
            py_dir_path = self.get_py_path_from_nb_path(nb_dir_path)
            yield py_dir_path

    def clear_py_dir_paths(self):
        for path in self.yield_py_dir_paths():
            self.__class__.logger().debug(f'clear python dir {path}')
            SysHelper.run_cmd(f'rm -rf {path}/*.py')

    def clear_py_dir_paths_format_convert_nb_files_to_py_files(self):
        self.clear_py_dir_paths()
        self.format_convert_nb_files_to_py_files()



