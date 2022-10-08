import sys
import json
sys.path.append('/home/clusters/rrcmpi/kudrov/scripts/python')
from iterate_confs import *
import subprocess
import os

L_spat = 48
L_time = 48
#conf_size = "36^4"
conf_size = "48^4"
#conf_type = "gluodynamics"
conf_type = "su2_suzuki"
theory_type = "su2"

arch = "rrcmpi-a"

additional_parameters = 'T_step=0.0005/T_final=0.5/OR_steps=4'


number_of_jobs = 50

# for beta in ['/']:
# for beta in ['beta6.3']:
# for beta in ['beta2.5', 'beta2.6']:
for beta in ['beta2.7']:
    # for mu in ['mu0.00', 'mu0.05', 'mu0.20', 'mu0.25', 'mu0.30', 'mu0.35', 'mu0.45']:
    # for mu in ['mu0.05', 'mu0.45']:
    for mu in ['/']:

        f = open(
            f'/home/clusters/rrcmpi/kudrov/conf/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/parameters.json')
        data = json.load(f)

        conf_format = "double"
        bytes_skip = 0
        matrix_type = 'su2'
        conf_path_start = f'/home/clusters/rrcmpi/kudrov/mag/conf_mag/su2/{conf_type}/{conf_size}/{beta}/{additional_parameters}'
        conf_path_end = "/"
        padding = 4
        conf_name = "conf_"

        chains = {'/': [1, 50]}
        #chains = {'s0': [201, 250]}
        jobs = distribute_jobs(chains, number_of_jobs)
        #jobs = distribute_jobs(data['chains'], number_of_jobs)

        for job in jobs:

            log_path = f'/home/clusters/rrcmpi/kudrov/observables_cluster/logs/monopoles_su2/{conf_type}/{conf_size}/{beta}/{mu}/'\
                f'{additional_parameters}/{job[0]}'
            conf_path_start1 = f'{conf_path_start}/{job[0]}/{conf_name}'
            try:
                os.makedirs(log_path)
            except:
                pass
            output_path = f'/home/clusters/rrcmpi/kudrov/observables_cluster/result/monopoles_su2/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/{additional_parameters}'
            # for nt8 and bigger
            # qsub -q mem4gb -l nodes=1:ppn=2
            bashCommand = f'qsub -q long -v conf_path_start={conf_path_start1},conf_path_end={conf_path_end},padding={padding},conf_format={conf_format},bytes_skip={bytes_skip},'\
                f'output_path={output_path},arch={arch},'\
                f'L_spat={L_spat},L_time={L_time},chain={job[0]},conf_start={job[1]},conf_end={job[2]}'\
                f' -o {log_path}/{job[1]:04}-{job[2]:04}.o -e {log_path}/{job[1]:04}-{job[2]:04}.e /home/clusters/rrcmpi/kudrov/observables_cluster/scripts/do_monopoles_su2.sh'
            # print(bashCommand)
            process = subprocess.Popen(bashCommand.split())
            output, error = process.communicate()
            # print(output, error)
