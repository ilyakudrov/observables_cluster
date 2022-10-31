import sys
import json
sys.path.append('/home/clusters/rrcmpi/kudrov/scripts/python')
from iterate_confs import *
import subprocess
import os

L_spat = 16
L_time = 16
conf_size = "16^4"
conf_type = "gluodynamics"
theory_type = "su3"

arch = "rrcmpi"

additional_parameters = 'DP_steps_500/copies=3'
parallel = 0


number_of_jobs = 500

# for beta in ['/']:
for beta in ['beta6.0']:
    # for beta in ['beta2.5', 'beta2.6']:
    # for beta in ['beta2.4']:
    # for mu in ['mu0.00', 'mu0.05', 'mu0.20', 'mu0.25', 'mu0.30', 'mu0.35', 'mu0.45']:
    # for mu in ['mu0.05', 'mu0.45']:
    for mu in ['/']:

        f = open(
            f'/home/clusters/rrcmpi/kudrov/conf/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/parameters.json')
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

        #conf_format = "double_qc2dstag"
        #bites_skip = 0
        #matrix_type = 'su3'
        #conf_path_start = f'/home/clusters/rrcmpi/kudrov/Landau_su3/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/{additional_parameters}'
        #conf_path_end = "/"
        #padding = 4
        #conf_name = "conf_Landau_gaugefixed_"

        #chains = {'/': [1, 500]}
        #chains = {'s0': [201, 250]}
        #jobs = distribute_jobs(chains, number_of_jobs)
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
            bashCommand = f'qsub -q long -v conf_path_start={conf_path_start1},conf_path_end={conf_path_end},padding={padding},conf_format={conf_format},bytes_skip={bytes_skip},'\
                f'path_conf_monopole={path_conf_monopole},path_conf_monopoless={path_conf_monopoless},path_inverse_laplacian={path_inverse_laplacian},'\
                f'L_spat={L_spat},L_time={L_time},parallel={parallel}'\
                f'chain={job[0]},conf_start={job[1]},conf_end={job[2]},arch={arch}'\
                f' -o {log_path}/{job[1]:04}-{job[2]:04}.o -e {log_path}/{job[1]:04}-{job[2]:04}.e /home/clusters/rrcmpi/kudrov/observables_cluster/scripts/do_decomposition_su3.sh'
            # print(bashCommand)
            process = subprocess.Popen(bashCommand.split())
            output, error = process.communicate()
            # print(output, error)
