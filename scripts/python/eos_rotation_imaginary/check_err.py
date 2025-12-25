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

script_name = 'average_distribution'
#for additional_dir in ['nt4p_im1_global_vm48', 'nt4p_im2_global_vm48', 'nt4p_re2_global_vm48']:
for additional_dir in ['']:
    base_path = f"/home/clusters/rrcmpi/kudrov/observables_cluster/logs/eos_energy_average/{script_name}/{additional_dir}"
    lattice_dirs = get_dir_names(base_path)
    for lattice_size in lattice_dirs:
        boundary_dirs = get_dir_names(f'{base_path}/{lattice_size}')
        for boundary in boundary_dirs:
            velocity_dirs = get_dir_names(f'{base_path}/{lattice_size}/{boundary}')
            for velocity in velocity_dirs:
                beta_dirs = get_dir_names(f'{base_path}/{lattice_size}/{boundary}/{velocity}')
                for beta in beta_dirs:
                    log_path = f'{base_path}/{lattice_size}/{boundary}/{velocity}/{beta}/energy_average.e'
                    if not os.path.isfile(log_path) or os.stat(log_path).st_size != 0:
                        #print(lattice_size, boundary, velocity, beta)
                        print(log_path)
