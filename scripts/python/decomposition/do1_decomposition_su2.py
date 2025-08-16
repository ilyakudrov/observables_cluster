import sys
import json
import os
import subprocess
import itertools

sys.path.append(os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "..", "..", "..", "lib", "src", "python"))
from iterate_confs import distribute_jobs

#conf_type = "su2_suzuki"
#conf_type = "gluodynamics"
conf_type = "qc2dstag"
theory_type = "su2"

#additional_parameters_arr = ['T_step=0.006', 'T_step=0.0125', 'T_step=0.025', 'T_step=0.05', 'T_step=0.1']
additional_parameters_arr = ['T_step=0.001']

number_of_jobs = 600

arch = "rrcmpi"
#beta_arr = ['beta2.478']
beta_arr = ['/']
#mu_arr = ['/']
#mu_arr = ['mu0.00', 'mu0.05', 'mu0.20', 'mu0.25', 'mu0.30', 'mu0.35', 'mu0.45']
mu_arr = ['mu0.15']
conf_size_arr = ['40^4']

iter_arrays = [beta_arr, mu_arr, conf_size_arr,
               additional_parameters_arr]
for beta, mu, conf_size, additional_parameters in itertools.product(*iter_arrays):
    f = open(
        f'/home/clusters/rrcmpi/kudrov/conf/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/parameters_mag.json')
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

    conf_path_start = conf_path_start + f'/{additional_parameters}'

    #conf_format = 'double'
    #bytes_skip = 0
    #matrix_type = 'su2'
    #conf_path_start = f'/home/clusters/rrcmpi/kudrov/mag/conf_mag/su2/{conf_type}/{conf_size}/{beta}/{mu}/{additional_parameters}'
    #conf_path_end = '/'
    #padding = 4
    #conf_name = 'conf_'

    #chains = {'/': [1, 5]}
    #chains = {'s0': [201, 201]}
    #jobs = distribute_jobs(chains, number_of_jobs)
    jobs = distribute_jobs(data['chains'], number_of_jobs)

    for job in jobs:

        log_path = f'/home/clusters/rrcmpi/kudrov/observables_cluster/logs/decomposition/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/'\
            f'{additional_parameters}/{job[0]}'
        conf_path_start1 = f'{conf_path_start}/{job[0]}/{conf_name}'
        try:
            os.makedirs(log_path)
        except:
            pass
        path_conf_monopole = f'/home/clusters/rrcmpi/kudrov/decomposition/confs_decomposed/monopole/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/{additional_parameters}/{job[0]}'
        path_conf_monopoless = f'/home/clusters/rrcmpi/kudrov/decomposition/confs_decomposed/monopoless/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/{additional_parameters}/{job[0]}'
        path_inverse_laplacian = f'/home/clusters/rrcmpi/kudrov/soft/inverse_laplacian/inverse_laplacian_{L_spat}x{L_time}'
        # qsub -q mem8gb -l nodes=1:ppn=4
        bashCommand = f'qsub -q long -v conf_path_start={conf_path_start1},conf_path_end={conf_path_end},padding={padding},conf_format={conf_format},bytes_skip={bytes_skip},'\
            f'path_conf_monopole={path_conf_monopole},path_conf_monopoless={path_conf_monopoless},path_inverse_laplacian={path_inverse_laplacian},'\
            f'file_precision={file_precision},L_spat={L_spat},L_time={L_time},'\
            f'chain={job[0]},conf_start={job[1]},conf_end={job[2]},arch={arch}'\
            f' -o {log_path}/{job[1]:04}-{job[2]:04}.o -e {log_path}/{job[1]:04}-{job[2]:04}.e ../../bash/decomposition/do_decomposition_su2.sh'
        # print(bashCommand)
        process = subprocess.Popen(bashCommand.split())
        output, error = process.communicate()
        # print(output, error)
