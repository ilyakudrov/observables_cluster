import sys
import json
import subprocess
import os
import itertools

sys.path.append(os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "..", "..", "..", "lib", "src", "python"))
from iterate_confs import distribute_jobs

#conf_type = "su2_suzuki"
conf_type = "qc2dstag"
#conf_type = "gluodynamics"
theory_type = "su2"

#steps_arr = [0.00125, 0.0025, 0.00375, 0.00625, 0.01]
#steps_arr = [0.006, 0.0125, 0.025, 0.05, 0.1]
steps_arr = [0.001]
T_init = 2.5
T_final = 0.1
OR_steps = 4
thermalization_steps = 50
tolerance_maximal = 1e-8
tolerance_average = 1e-12
tolerance_digits = 7
gauge_copies = 5

#is_new_trial = 1
#is_final = 0
#is_compare = 1
#is_compare_spins = 1
#is_functional_save = 1
#fixation_type = 'new'

is_new_trial = 0
is_final = 1
is_compare = 0
is_compare_spins = 0
is_functional_save = 0
fixation_type = 'final'

number_of_jobs = 400

arch = "rrcmpi"

conf_size_arr = ['40^4']
beta_arr = ['/']
#beta_arr = ['beta2.441']
mu_arr = ['mu0.15']
#mu_arr = ['mu0.45']
#mu_arr = ['/']

iter_arrays = [beta_arr, mu_arr, conf_size_arr, steps_arr]
for beta, mu, conf_size, T_step in itertools.product(*iter_arrays):
    f = open(
        f'/home/clusters/rrcmpi/kudrov/conf/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/parameters_original.json')
    data = json.load(f)
    conf_format = data['conf_format']
    bytes_skip = data['bytes_skip']
    L_spat = data['x_size']
    L_time = data['t_size']
    matrix_type = data['matrix_type']
    conf_path_start = data['conf_path_start']
    conf_path_end = data['conf_path_end']
    padding = data['padding']
    conf_name = data['conf_name']

    #chains = {'/': [201, 201]}
    #chains = {'s0': [201, 201]}
    #jobs = distribute_jobs(chains, number_of_jobs)
    jobs = distribute_jobs(data['chains'], number_of_jobs)
    for job in jobs:
        log_path = f'/home/clusters/rrcmpi/kudrov/observables_cluster/logs/mag/{fixation_type}/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/'\
            f'T_step={T_step}/{job[0]}'
        conf_path_start1 = f'{conf_path_start}/{job[0]}/{conf_name}'
        try:
            os.makedirs(log_path)
        except:
            pass
        output_path_functional = f'/home/clusters/rrcmpi/kudrov/observables_cluster/result/mag/functional/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/'\
            f'T_step={T_step}/{job[0]}'
        output_path_conf_spin = f'/home/clusters/rrcmpi/kudrov/mag/spins/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/T_step={T_step}/{job[0]}'
        output_path_confs_gaugefixed = f'/home/clusters/rrcmpi/kudrov/mag/conf_mag/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/T_step={T_step}/{job[0]}'
        # qsub -q mem8gb -l nodes=1:ppn=4
        bashCommand = f'qsub -q long -v conf_path_start={conf_path_start1},conf_path_end={conf_path_end},padding={padding},matrix_type={matrix_type},conf_format={conf_format},bytes_skip={bytes_skip},'\
            f'T_step={T_step},T_init={T_init},T_final={T_final},OR_steps={OR_steps},thermalization_steps={thermalization_steps},'\
            f'output_path_functional={output_path_functional},output_path_conf_spin={output_path_conf_spin},output_path_confs_gaugefixed={output_path_confs_gaugefixed},'\
            f'tolerance_maximal={tolerance_maximal},tolerance_average={tolerance_average},tolerance_digits={tolerance_digits},gauge_copies={gauge_copies},is_new_trial={is_new_trial},'\
            f'is_final={is_final},is_compare={is_compare},is_compare_spins={is_compare_spins},is_functional_save={is_functional_save},L_spat={L_spat},L_time={L_time},'\
            f'chain={job[0]},conf_start={job[1]},conf_end={job[2]},arch={arch}'\
            f' -o {log_path}/{job[1]:04}-{job[2]:04}.o -e {log_path}/{job[1]:04}-{job[2]:04}.e ../../bash/mag_su2/do_mag_su2.sh'
        # print(bashCommand)
        process = subprocess.Popen(bashCommand.split())
        output, error = process.communicate()
        # print(output, error)
