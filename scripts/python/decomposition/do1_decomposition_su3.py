import sys
import json
import subprocess
import os
import itertools

sys.path.append(os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "..", "..", "..", "lib", "src", "python"))
from iterate_confs import distribute_jobs

#conf_type = "gluodynamics"
conf_type = "QCD/140MeV"
theory_type = "su3"

compensate = 1
parallel = 1
#additional_parameters_arr = ['steps_25/copies=4', 'steps_50/copies=4', 
#                             'steps_100/copies=4', 'steps_200/copies=4', 
#                             'steps_1000/copies=4', 'steps_2000/copies=4']
additional_parameters_arr = ['steps_500/copies=1']

number_of_jobs = 400

arch = "rrcmpi-a"
beta_arr = ['/']
#beta_arr = ['beta6.3']
mu_arr = ['/']
#mu_arr = ['mu0.00', 'mu0.05', 'mu0.20', 'mu0.25', 'mu0.30', 'mu0.35', 'mu0.45']
#conf_size_arr = ['nt4', 'nt6', 'nt8', 'nt10', 'nt12', 'nt14']
conf_size_arr = ['nt16', 'nt18', 'nt20']
#conf_size_arr = ['36^4']

iter_arrays = [beta_arr, mu_arr, conf_size_arr,
               additional_parameters_arr]
for beta, mu, conf_size, additional_parameters in itertools.product(*iter_arrays):
    f = open(
        f'/home/clusters/rrcmpi/kudrov/conf/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/parameters_mag_Landau.json')
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

    #conf_format = "double_qc2dstag"
    #bites_skip = 0
    #matrix_type = 'su3'
    #conf_path_start = f'/home/clusters/rrcmpi/kudrov/Landau_su3/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/{additional_parameters}'
    #conf_path_end = "/"
    #padding = 4
    #conf_name = "conf_Landau_gaugefixed_"

    # chains = {'/': [1, 200]}
    #chains = {'s0': [201, 250]}
    # jobs = distribute_jobs(chains, number_of_jobs)
    jobs = distribute_jobs(data['chains'], number_of_jobs)

    for job in jobs:

        log_path = f'/home/clusters/rrcmpi/kudrov/observables_cluster/logs/decomposition_su3/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/'\
            f'{additional_parameters}/{job[0]}'
        conf_path_start1 = f'{conf_path_start}/{job[0]}/{conf_name}'
        try:
            os.makedirs(log_path)
        except:
            pass
        path_conf_monopole = f'/home/clusters/rrcmpi/kudrov/decomposition/confs_decomposed/monopole/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/{additional_parameters}'
        path_conf_monopoless = f'/home/clusters/rrcmpi/kudrov/decomposition/confs_decomposed/monopoless/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/{additional_parameters}'
        path_inverse_laplacian = f'/home/clusters/rrcmpi/kudrov/soft/inverse_laplacian/ALPHA{L_spat}x{L_time}_d.LAT'
        # qsub -q mem8gb -l nodes=1:ppn=4
        bashCommand = f'qsub -q mem16gb -l nodes=1:ppn=8 -v conf_path_start={conf_path_start1},conf_path_end={conf_path_end},padding={padding},conf_format={conf_format},bytes_skip={bytes_skip},'\
            f'path_conf_monopole={path_conf_monopole},path_conf_monopoless={path_conf_monopoless},path_inverse_laplacian={path_inverse_laplacian},'\
            f'L_spat={L_spat},L_time={L_time},parallel={parallel},compensate={compensate},'\
            f'chain={job[0]},conf_start={job[1]},conf_end={job[2]},arch={arch}'\
            f' -o {log_path}/{job[1]:04}-{job[2]:04}.o -e {log_path}/{job[1]:04}-{job[2]:04}.e ../../bash/decomposition/do_decomposition_su3.sh'
        # print(bashCommand)
        process = subprocess.Popen(bashCommand.split())
        output, error = process.communicate()
        # print(output, error)
