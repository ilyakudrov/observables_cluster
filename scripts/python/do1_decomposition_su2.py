import sys
import json
sys.path.append('/home/clusters/rrcmpi/kudrov/scripts/python')
from iterate_confs import *
import subprocess
import os

#conf_size = "24^4"
#conf_size = "40^4"
conf_size = "48^4"
conf_type = "su2_suzuki"
#conf_type = "qc2dstag"
theory_type = "su2"

T_step = 0.0001
T_final = 0.0001
OR_steps = 6

number_of_jobs = 50

arch = "rrcmpi-a"

# for beta in ['/']:
for beta in ['beta2.8']:
    # for beta in ['beta2.5', 'beta2.6']:
    # for beta in ['beta2.4']:
    # for mu in ['mu0.00', 'mu0.05', 'mu0.20', 'mu0.25', 'mu0.30', 'mu0.35', 'mu0.45']:
    # for mu in ['mu0.05', 'mu0.45']:
    for mu in ['/']:

        f = open(
            f'/home/clusters/rrcmpi/kudrov/conf/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/parameters.json')
        data = json.load(f)
        conf_format = data['conf_format']
        bites_skip = data['bites_skip']
        L_spat = data['x_size']
        L_time = data['t_size']
        matrix_type = data['matrix_type']
        conf_path_start = data['conf_path_start']
        conf_path_end = data['conf_path_end']
        padding = data['padding']
        conf_name = data['conf_name']

        #chains = {'/': [1, 2]}
        #chains = {'s0': [201, 250]}
        #jobs = distribute_jobs(chains, number_of_jobs)
        jobs = distribute_jobs(data['chains'], number_of_jobs)

        for job in jobs:

            log_path = f'/home/clusters/rrcmpi/kudrov/observables_cluster/logs/decomposition/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/'\
                f'T_step={T_step}/T_final={T_final}/OR_steps={OR_steps}/{job[0]}'
            conf_path_start1 = f'{conf_path_start}/{job[0]}/{conf_name}'
            try:
                os.makedirs(log_path)
            except:
                pass
            path_conf_monopole = f'/home/clusters/rrcmpi/kudrov/decomposition/confs_decomposed/monopole/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/T_step={T_step}/T_final={T_final}/OR_steps={OR_steps}'
            path_conf_monopoless = f'/home/clusters/rrcmpi/kudrov/decomposition/confs_decomposed/monopoless/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/T_step={T_step}/T_final={T_final}/OR_steps={OR_steps}'
            path_inverse_laplacian = f'/home/clusters/rrcmpi/kudrov/soft/inverse_laplacian/ALPHA{L_spat}x{L_time}_d.LAT'
            # qsub -q mem8gb -l nodes=1:ppn=4
            bashCommand = f'qsub -q long -v conf_path_start={conf_path_start1},conf_path_end={conf_path_end},padding={padding},conf_format={conf_format},bites_skip={bites_skip},'\
                f'T_step={T_step},T_final={T_final},OR_steps={OR_steps},'\
                f'path_conf_monopole={path_conf_monopole},path_conf_monopoless={path_conf_monopoless},path_inverse_laplacian={path_inverse_laplacian},'\
                f'L_spat={L_spat},L_time={L_time},'\
                f'chain={job[0]},conf_start={job[1]},conf_end={job[2]},arch={arch}'\
                f' -o {log_path}/{job[1]:04}-{job[2]:04}.o -e {log_path}/{job[1]:04}-{job[2]:04}.e /home/clusters/rrcmpi/kudrov/observables_cluster/scripts/do_decomposition_su2.sh'
            # print(bashCommand)
            process = subprocess.Popen(bashCommand.split())
            output, error = process.communicate()
            # print(output, error)
