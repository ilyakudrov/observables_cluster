import itertools
import sys
import subprocess
import os

def get_dir_names(path):
    """Get names of subdirectories in path.

    Args:
        path: path where to find subdirectories

    Returns: list of names of the subdirectories
    """
    directories = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        directories.extend(dirnames)
        break
    return directories

def get_error_files(path: str):
    """Get names of files with error log in directory path.

    Args:
        path: path of logs

    Returns: list of file names
    """
    files = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        files.extend(filenames)
        break
    return list(f for f in files if f.endswith('.e'))

base_path = "/home/clusters/rrcmpi/kudrov/observables_cluster/logs/eos_energy_average/common_average_polyakov"
lattice_dirs = get_dir_names(base_path)
file_list = get_error_files(base_path)
for file in file_list:
    if os.stat(f'{base_path}/{file}').st_size != 0:
        #print(lattice_size, boundary, velocity, beta)
        print(file)
