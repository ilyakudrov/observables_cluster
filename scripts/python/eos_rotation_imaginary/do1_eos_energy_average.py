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

#lattice_size_arr = ['5x30x121sq', '6x36x145sq', '7x42x169sq']
#lattice_size_arr = ['30x30x121sq', '36x36x145sq', '42x42x169sq', '5x30x121sq', '6x36x145sq', '7x42x169sq']
#lattice_size_arr = ['30x30x121sq']
lattice_size_arr = ['7x42x169sq']
#lattice_size_arr = ['5x30x81sq']
#lattice_size_arr = ['5x30x181sq']
#lattice_size_arr = ['42x42x169sq', '7x42x169sq']
#lattice_size_arr = ['24x24x97sq', '4x24x97sq']
#lattice_size_arr = ['30x30x121sq', '5x30x121sq']
#lattice_size_arr = ['30x30x81sq', '5x30x181sq', '5x30x81sq']
#boundary_arr = ["OBCb_cV", "PBC_cV"]
#boundary_arr = ["PBC_cV"]
boundary_arr = ["OBCb_cV"]
#base_path = "/home/clusters/rrcmpi/kudrov/eos_high_precision/result/logs"
#base_path = '/lustre/rrcmpi/roenko/gluo_rotation_omp/results_hydra/EoS-Sym/logs'
#base_path = '/lustre/rrcmpi/roenko/gluo_rotation_omp/results_hydra/EoS-Sym-ext/logs'
#base_path = '/lustre/rrcmpi/roenko/gluo_rotation_omp/results/EoS-Sym/logs'
#base_path = '/home/clusters/rrcmpi/kudrov/eos_high_precision/results/EoS-Sym/logs'
base_path = '/lustre/rrcmpi/roenko/sychev_hydra/gluo_rotation/eos_run3_p2/nt7o_extra_set2/logs'
spec_additional_path = '/home/clusters/rrcmpi/kudrov/observables/data/eos_rotation_imaginary'
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
            result_path = f"/home/clusters/rrcmpi/kudrov/observables/result/eos_rotation_imaginary/{lattice_size}/{boundary}/{velocity}/{beta}"
            parameters = f'--base_path {base_path} --lattice_size {lattice_size} --velocity {velocity} --boundary {boundary} --beta {beta} --result_path {result_path} --spec_additional_path {spec_additional_path}'
            if bin_test:
                parameters += '--bin_test'
            command_qsub = f'qsub -q mem16gb -l nodes=1:ppn=8 -v'
            command_parameters = f'parameters={parameters}'
            command_script = f'-o {log_path}/energy_average.o -e {log_path}/energy_average.e ../../bash/eos_rotation_imaginary/do_eos_energy_average.sh'
            command = command_qsub.split() + [command_parameters] + command_script.split()
            #print(command)
            process = subprocess.Popen(command)
            output, error = process.communicate()
