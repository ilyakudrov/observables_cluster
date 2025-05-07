import sys
import json
import subprocess
import os
import itertools

sys.path.append(os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "..", "..", "lib", "src", "python"))
from iterate_confs import distribute_jobs

#conf_type = "su2_suzuki"
conf_type = "gluodynamics"
#conf_type = "QCD/140MeV"
#conf_type = "qc2dstag"
theory_type = "su2"
decomposition_type_array = ['original']

calculate_absent = 0
gauge_copies = 0

beta = 2.701

number_of_jobs = 1000

arch = "rrcmpi-a"

#beta_arr = ['beta2.6', 'beta2.779']
beta_arr = ['beta6.0']
beta_num = 2.701
#beta_arr = ['/']
#mu_arr = ['mu0.15']
#mu_arr = ['mu0.00', 'mu0.05', 'mu0.10', 'mu0.15', 'mu0.20', 'mu0.25', 'mu0.30', 'mu0.33', 'mu0.35', 'mu0.37', 'mu0.40', 'mu0.45', 'mu0.50']
mu_arr = ['/']
conf_size_arr = ['24^4']
#conf_size_arr = ['32^3x8', '32^3x16', '32^3x20', '32^3x24', '32^3x28', '32^3x32']
#conf_size_arr = ['32^3x64']
#conf_size_arr = ['nt4', 'nt6', 'nt8', 'nt10', 'nt12', 'nt14', 'nt16', 'nt18', 'nt20']
# additional_parameters_arr = ['steps_100/copies=100']
additional_parameters_arr = ['/']

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
    if decomposition_type != 'original':
        conf_path_start = conf_path_start + \
            f'/{additional_parameters}'

    # chains = {'/': [1, 1000]}
    #chains = {'s1': [2, 2]}
    #chains = {'s2': [1, 1424], 's3': [1, 6000], 's4': [1, 6000]}
    # jobs = distribute_jobs(chains, number_of_jobs)
    jobs = distribute_jobs(data['chains'], number_of_jobs)

    for job in jobs:
        log_path = f'/home/clusters/rrcmpi/kudrov/observables_cluster/logs/gluon_propagator/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/'\
            f'{decomposition_type}/{additional_parameters}/{job[0]}'
        conf_path_start1 = f'{conf_path_start}/{job[0]}/{conf_name}'
        try:
            os.makedirs(log_path)
        except:
            pass
        output_path = f'/home/clusters/rrcmpi/kudrov/observables_cluster/result/gluon_propagator/on-axis/{theory_type}/'\
            f'{conf_type}/{conf_size}/{beta}/{mu}/{decomposition_type}/{additional_parameters}/{job[0]}'
        # qsub -q mem8gb -l nodes=1:ppn=4
        # qsub -q long
        # su3:
        # original: 24^4: 2GB, 28^4: 4GB, 32^4: 8GB, 36^4: 8GB, 40^4: 16GB
        # abelian: 28^4: 2GB, 32^4: 4GB, 36^4: 4GB, 40^4: 8GB
        bashCommand = f'qsub -q long -v convert={convert},'\
            f'conf_path_start={conf_path_start1},conf_path_end={conf_path_end},'\
            f'conf_format={conf_format},bytes_skip={bytes_skip},beta={beta_num},'\
            f'padding={padding},calculate_absent={calculate_absent},'\
            f'output_path={output_path},L_spat={L_spat},L_time={L_time},gauge_copies={gauge_copies},'\
            f'chain={job[0]},conf_start={job[1]},conf_end={job[2]},arch={arch},matrix_type={matrix_type}'\
            f' -o {log_path}/{job[1]:04}-{job[2]:04}.o -e {log_path}/{job[1]:04}-{job[2]:04}.e ../bash/do_gluon_propagator.sh'
        # print(bashCommand)
        process = subprocess.Popen(bashCommand.split())
        output, error = process.communicate()
        # print(output, error)
