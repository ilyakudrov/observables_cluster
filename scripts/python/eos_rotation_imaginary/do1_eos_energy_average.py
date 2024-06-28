import itertools
import sys
import subprocess
import os

def get_dir_names(path: str) -> list[str]:
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

lattice_size_arr = ['5x30x121sq', '6x36x145sq', '7x42x169sq']
#lattice_size_arr = ['5x30x121sq', '6x36x145sq']
boundary_arr=["OBCb_cV"]
base_path="/home/clusters/rrcmpi/kudrov/eos_high_precision/result/logs"
bin_test = False
iter_arrays = [lattice_size_arr, boundary_arr]
for lattice_size, boundary in itertools.product(*iter_arrays):
    velocity_dirs = get_dir_names(f'{base_path}/{lattice_size}/{boundary}')
    for velocity in velocity_dirs:
        beta_dirs = get_dir_names(f'{base_path}/{lattice_size}/{boundary}/{velocity}')
        for beta in beta_dirs:
            log_path = f'/home/clusters/rrcmpi/kudrov/observables_cluster/logs/eos_energy_average/{lattice_size}/{boundary}/{velocity}/{beta}'
            try:
                os.makedirs(log_path)
            except:
                pass
            parameters=f'--base_path {base_path} --lattice_size {lattice_size} --velocity {velocity} --boundary {boundary} --beta {beta}'
            if bin_test:
                parameters += '--bin_test'
            command_qsub = f'qsub -q mem16gb -l nodes=1:ppn=8 -v'
            command_parameters = f'parameters={parameters}'
            command_script = f'-o {log_path}/energy_average.o -e {log_path}/energy_average.e ../../bash/eos_rotation_imaginary/do_eos_energy_average.sh'
            command = command_qsub.split() + [command_parameters] + command_script.split()
            #print(command)
            process = subprocess.Popen(command)
            output, error = process.communicate()
