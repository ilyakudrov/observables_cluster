import sys
import json
import subprocess
import os
import itertools

sys.path.append(os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "..", "..", "..", "lib", "src", "python"))
from iterate_confs import distribute_jobs

#conf_type = "su2_suzuki"
#conf_type = "gluodynamics"
conf_type = "QCD/140MeV"
#conf_type = "qc2dstag"
theory_type = "su3"

#decomposition_type_arr = ["original"]
decomposition_type_arr = ["abelian"]
#decomposition_type_arr = ["monopoless", "monopole",
#                           "photon", "offdiagonal", "abelian"]

number_of_jobs = 20

calculate_absent = "false"

#additional_parameters_arr = ['/']
#additional_parameters_arr = ['steps_2000/copies=1', 'steps_330/copies=1']
additional_parameters_arr = ['steps_500/copies=1']
#additional_parameters_arr = ['steps_500/copies=3/compensate_1']

smearing_arr = ['HYP1_alpha=1_1_0.5', 'HYP2_alpha=1_1_0.5', 'HYP1_alpha=1_1_0.5_APE_alpha=0.5']
#smearing_arr = ['HYP1_alpha=1_1_0.5']
#smearing_arr = ['HYP1_alpha=1_1_0.5_APE_alpha=0.5']
#smearing_arr = ['unsmeared']

arch = "rrcmpi-a"
# beta_arr = ['beta2.8']
beta_arr = ['/']
mu_arr = ['/']
# mu_arr = ['mu0.05', 'mu0.20', 'mu0.25', 'mu0.30', 'mu0.35', 'mu0.40', 'mu0.45']
#mu_arr = ['mu0.00']
# conf_size_arr = ['40^4']
#conf_size_arr = ['nt4', 'nt6', 'nt8', 'nt10', 'nt12', 'nt14', 'nt16', 'nt18']
#conf_size_arr = ['nt4', 'nt6', 'nt8', 'nt10', 'nt12', 'nt14']
conf_size_arr = ['nt16', 'nt18']
#conf_size_arr = ['nt6']

iter_arrays = [beta_arr, mu_arr, conf_size_arr,
               additional_parameters_arr, decomposition_type_arr, smearing_arr]
for beta, mu, conf_size, additional_parameters, decomposition_type, smearing in itertools.product(*iter_arrays):
    f = open(
        f'/home/clusters/rrcmpi/kudrov/conf/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/parameters_{decomposition_type}.json')
    data = json.load(f)
    conf_format = data['conf_format']
    file_precision = data['file_precision']
    bytes_skip = data['bytes_skip']
    matrix_type = data['matrix_type']
    conf_path_start = data['conf_path_start']
    conf_path_end = data['conf_path_end']
    padding = data['padding']
    conf_name = data['conf_name']
    convert = data['convert']
    L_spat = data['x_size']
    L_time = data['t_size']

    conf_path_start = conf_path_start + \
        f'/{additional_parameters}'

    conf_path_start = f'/home/clusters/rrcmpi/kudrov/smearing/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/{decomposition_type}/{smearing}/{additional_parameters}'
    conf_name = 'smeared_'
    conf_path_end = '/'
    conf_format = 'double'
    padding = 4
    bytes_skip = 0
    convert = 0

    #chains = {'/': [501, 501]}
    #jobs = distribute_jobs(chains, number_of_jobs)
    jobs = distribute_jobs(data['chains'], number_of_jobs)

    for job in jobs:

        log_path = f'/home/clusters/rrcmpi/kudrov/observables_cluster/logs/polyakov_loop/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/'\
            f'{decomposition_type}/{smearing}/{additional_parameters}/{job[0]}'
        conf_path_start1 = f'{conf_path_start}/{job[0]}/{conf_name}'
        try:
            os.makedirs(log_path)
        except:
            pass

        output_path = f'/home/clusters/rrcmpi/kudrov/observables_cluster/result/polyakov_loop/{theory_type}/'\
            f'{conf_type}/{conf_size}/{beta}/{mu}/{decomposition_type}/{smearing}/{additional_parameters}/{job[0]}'

        #-q mem8gb -l nodes=1:ppn=4
        bashCommand = f'qsub -q mem8gb -l nodes=1:ppn=4 -v conf_format={conf_format},'\
            f'bytes_skip={bytes_skip},convert={convert},matrix_type={matrix_type},file_precision={file_precision},'\
            f'conf_path_start={conf_path_start1},conf_path_end={conf_path_end},'\
            f'padding={padding},L_spat={L_spat},L_time={L_time},arch={arch},'\
            f'output_path={output_path},chain={job[0]},conf_start={job[1]},conf_end={job[2]}'\
            f' -o {log_path}/{job[1]:04}-{job[2]:04}.o -e {log_path}/{job[1]:04}-{job[2]:04}.e ../../bash/polyakov_loop/do_polyakov_loop.sh'
        # print(bashCommand)
        process = subprocess.Popen(bashCommand.split())
        output, error = process.communicate()
        #print(output, error)
