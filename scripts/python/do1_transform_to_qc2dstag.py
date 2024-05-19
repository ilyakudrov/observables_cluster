import sys
import json
import subprocess
import os
import itertools

sys.path.append(os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "..", "..", "lib", "src", "python"))
from iterate_confs import distribute_jobs

conf_type = "qc2dstag"
theory_type = "su2"
decomposition_type_array = ['monopoless', 'monopole']

calculate_absent = 0
gauge_copies = 0

number_of_jobs = 10
arch = "rrcmpi"

#beta_arr = ['beta6.1']
beta_arr = ['/']
#mu_arr = ['mu0.00', 'mu0.20', 'mu0.30', 'mu0.35', 'mu0.40', 'mu0.45']
mu_arr = ['mu0.00', 'mu0.05', 'mu0.15']
# mu_arr = ['/']
conf_size_arr = ['40^4']
additional_parameters_arr = ['steps_0/copies=20']
#additional_parameters_arr = ['/']
conf_name_new = 'decomposition_type_'

iter_arrays = [beta_arr, mu_arr, conf_size_arr,
               additional_parameters_arr, decomposition_type_array]
for beta, mu, conf_size, additional_parameters, decomposition_type in itertools.product(*iter_arrays):
    f = open(
        f'/home/clusters/rrcmpi/kudrov/conf/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/parameters_{decomposition_type}.json')
    data = json.load(f)
    conf_format = data['conf_format']
    bytes_skip = data['bytes_skip']
    matrix_type = data['matrix_type']
    conf_path_start = data['conf_path_start']
    conf_path_end = data['conf_path_end']
    padding = data['padding']
    conf_name = data['conf_name']
    convert = data['convert']
    L_spat = data['x_size']
    L_time = data['t_size']

    #chains = {'/': [501, 501]}
    #chains = {'s5': [1, 450], 's6': [1, 450]}
    #jobs = distribute_jobs(chains, number_of_jobs)
    jobs = distribute_jobs(data['chains'], number_of_jobs)

    for job in jobs:
        log_path = f'/home/clusters/rrcmpi/kudrov/observables_cluster/logs/transform_to_qc2dstag/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/'\
            f'{decomposition_type}/{additional_parameters}/{job[0]}'
        try:
            os.makedirs(log_path)
        except:
            pass
        # qsub -q mem8gb -l nodes=1:ppn=4
        # qsub -q long
        bashCommand = f'qsub -q long -l nodes=1:ppn=8 -v convert={convert},'\
            f'conf_path_start={conf_path_start},conf_path_end={conf_path_end},'\
            f'conf_format={conf_format},bytes_skip={bytes_skip},conf_name={conf_name},'\
            f'padding={padding},calculate_absent={calculate_absent},'\
            f'L_spat={L_spat},L_time={L_time},gauge_copies={gauge_copies},'\
            f'chain={job[0]},conf_start={job[1]},conf_end={job[2]},arch={arch},matrix_type={matrix_type}'\
            f' -o {log_path}/{job[1]:04}-{job[2]:04}.o -e {log_path}/{job[1]:04}-{job[2]:04}.e ../bash/do_transform_to_qc2dstag.sh'
        # print(bashCommand)
        process = subprocess.Popen(bashCommand.split())
        output, error = process.communicate()
        # print(output, error)
