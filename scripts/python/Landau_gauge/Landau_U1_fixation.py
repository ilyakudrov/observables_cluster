import sys
import json
import subprocess
import os
import itertools

sys.path.append(os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "..", "..", "..", "lib", "src", "python"))
from iterate_confs import distribute_jobs

#conf_type = "su2_suzuki"
conf_type = "gluodynamics"
# conf_type = "qc2dstag"
theory_type = "su2"

number_of_jobs = 500

arch = "rrcmpi-a"

# additional_parameters_arr = ['/']
additional_parameters_arr = ['T_step=0.001']

beta_arr = ['beta2.478']

# beta_arr = ['/']
mu_arr = ['/']
# mu_arr = ['mu0.05', 'mu0.20', 'mu0.25', 'mu0.30', 'mu0.35', 'mu0.40', 'mu0.45']
# mu_arr = ['mu0.00']
conf_size_arr = ['32^3x8']
# conf_size_arr = ['nt4', 'nt6', 'nt8', 'nt10', 'nt12', 'nt14']

iter_arrays = [beta_arr, mu_arr, conf_size_arr,
               additional_parameters_arr]
for beta, mu, conf_size, additional_parameters in itertools.product(*iter_arrays):
    f = open(
        f'/home/clusters/rrcmpi/kudrov/conf/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/parameters_mag.json')
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

    conf_path_start = conf_path_start + f'/{additional_parameters}'

    #chains = {'/': [1, 1]}
    # chains = {'s0': [201, 201]}
    #jobs = distribute_jobs(chains, number_of_jobs)
    jobs = distribute_jobs(data['chains'], number_of_jobs)

    for job in jobs:
        log_path = f'/home/clusters/rrcmpi/kudrov/observables_cluster/logs/Landau_U1/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/'\
            f'{additional_parameters}/{job[0]}'
        conf_path_start1 = f'{conf_path_start}/{job[0]}/{conf_name}'
        try:
            os.makedirs(log_path)
        except:
            pass
        output_path_functional = f'/home/clusters/rrcmpi/kudrov/observables_cluster/result/Landau_U1/functional/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/'\
            f'{additional_parameters}/{job[0]}'
        output_path_confs_gaugefixed = f'/home/clusters/rrcmpi/kudrov/Landau_U1/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/{additional_parameters}/{job[0]}'
        # qsub -q mem8gb -l nodes=1:ppn=4
        bashCommand = f'qsub -q long -v conf_path_start={conf_path_start1},conf_path_end={conf_path_end},padding={padding},matrix_type={matrix_type},conf_format={conf_format},bytes_skip={bytes_skip},'\
            f'output_path_functional={output_path_functional},output_path_confs_gaugefixed={output_path_confs_gaugefixed},'\
            f'L_spat={L_spat},L_time={L_time},'\
            f'chain={job[0]},conf_start={job[1]},conf_end={job[2]},arch={arch}'\
            f' -o {log_path}/{job[1]:04}-{job[2]:04}.o -e {log_path}/{job[1]:04}-{job[2]:04}.e ../../bash/Landau_gauge/do_Landau_U1_fixation.sh'
        # print(bashCommand)
        process = subprocess.Popen(bashCommand.split())
        output, error = process.communicate()
        # print(output, error)
