import sys
import json
import os
import subprocess
import itertools

sys.path.append(os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "..", "..", "..", "lib", "src", "python"))
from iterate_confs import distribute_jobs

L_spat = 64
L_time = 14
#conf_size = "36^4"
conf_size = "nt4"
#conf_type = "gluodynamics"
conf_type = "QCD/140MeV"
theory_type = "su3"

arch = "rrcmpi-a"

number_of_jobs = 100

beta_arr = ['beta2.8']
#mu_arr = ['mu0.00', 'mu0.05', 'mu0.20', 'mu0.25', 'mu0.30', 'mu0.35', 'mu0.45']
mu_arr = ['/']
additional_parameters_arr = ['steps_500/copies=1']
conf_size_arr = ['36^4']

number_of_jobs = 50

iter_arrays = [beta_arr, mu_arr, conf_size_arr, additional_parameters_arr]
for beta, mu, conf_size, additional_parameters in itertools.product(*iter_arrays):

    f = open(
        f'/home/clusters/rrcmpi/kudrov/conf/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/parameters_mag.json')
    data = json.load(f)
    conf_format = data['conf_format']
    bytes_skip = data['bytes_skip']
    matrix_type = data['matrix_type']
    conf_path_start = data['conf_path_start']
    conf_path_end = data['conf_path_end']
    padding = data['padding']
    conf_name = data['conf_name']
    L_spat = data['x_size']
    L_time = data['t_size']

    conf_path_start = conf_path_start + f'/{additional_parameters}'

    #chains = {'/': [1, 500]}
    #chains = {'s0': [201, 250]}
    #jobs = distribute_jobs(chains, number_of_jobs)
    jobs = distribute_jobs(data['chains'], number_of_jobs)

    for job in jobs:

        log_path = f'/home/clusters/rrcmpi/kudrov/observables_cluster/logs/monopoles_su3/{conf_type}/{conf_size}/{beta}/{mu}/'\
            f'{additional_parameters}/{job[0]}'
        conf_path_start1 = f'{conf_path_start}/{job[0]}/{conf_name}'
        try:
            os.makedirs(log_path)
        except:
            pass
        output_path = f'/home/clusters/rrcmpi/kudrov/observables_cluster/result/monopoles_su3/{conf_type}/{conf_size}/{beta}/{mu}/{additional_parameters}'
        # for nt8 and bigger
        # qsub -q mem4gb -l nodes=1:ppn=2
        bashCommand = f'qsub -q mem4gb -l nodes=1:ppn=2 -v conf_path_start={conf_path_start1},conf_path_end={conf_path_end},padding={padding},conf_format={conf_format},bytes_skip={bytes_skip},'\
            f'output_path={output_path},arch={arch},'\
            f'L_spat={L_spat},L_time={L_time},chain={job[0]},conf_start={job[1]},conf_end={job[2]}'\
            f' -o {log_path}/{job[1]:04}-{job[2]:04}.o -e {log_path}/{job[1]:04}-{job[2]:04}.e ../../bash/monopoles/do_monopoles_su3.sh'
        # print(bashCommand)
        process = subprocess.Popen(bashCommand.split())
        output, error = process.communicate()
        # print(output, error)
