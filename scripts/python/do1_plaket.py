import sys
import json
sys.path.append('/home/clusters/rrcmpi/kudrov/scripts/python')
from iterate_confs import *
import subprocess
import os

#conf_size = "24^4"
#conf_size = "40^4"
#conf_size = "48^4"
conf_size = "28^4"
#conf_type = "su2_suzuki"
conf_type = "gluodynamics"
#conf_type = "qc2dstag"
#theory_type = "su2"
theory_type = "su3"

number_of_jobs = 100
arch="rrcmpi"

for monopole in ['/']:
    # for monopole in ['monopoless']:
    # for beta in ['/']:
    for beta in ['beta6.1']:
        # for beta in ['beta2.4', 'beta2.5', 'beta2.6']:
        # for beta in ['beta2.4']:
        # for mu in ['mu0.00', 'mu0.05', 'mu0.20', 'mu0.25', 'mu0.30', 'mu0.35', 'mu0.45']:
        # for mu in ['mu0.25']:
        for mu in ['/']:

            f = open(
                f'/home/clusters/rrcmpi/kudrov/conf/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/{monopole}/parameters.json')
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

            #chains = {'/': [1, 1]}
            #jobs = distribute_jobs(chains, number_of_jobs)
            jobs = distribute_jobs(data['chains'], number_of_jobs)

            for job in jobs:

                log_path = f'/home/clusters/rrcmpi/kudrov/observables_cluster/logs/plaket/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/{monopole}/{job[0]}'
                conf_path_start1 = f'{conf_path_start}/{job[0]}/{conf_name}'
                try:
                    os.makedirs(log_path)
                except:
                    pass

                output_path = f'/home/clusters/rrcmpi/kudrov/observables_cluster/result/plaket/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/{monopole}/{job[0]}'

                # qsub -q mem8gb -l nodes=1:ppn=4
                bashCommand = f'qsub -q long -v conf_format={conf_format},'\
                    f'bites_skip={bites_skip},matrix_type={matrix_type},arch={arch},'\
                    f'conf_path_start={conf_path_start1},conf_path_end={conf_path_end},'\
                    f'padding={padding},L_spat={L_spat},L_time={L_time},'\
                    f'output_path={output_path},chain={job[0]},conf_start={job[1]},conf_end={job[2]}'\
                    f' -o {log_path}/{job[1]:04}-{job[2]:04}.o -e {log_path}/{job[1]:04}-{job[2]:04}.e /home/clusters/rrcmpi/kudrov/observables_cluster/scripts/do_plaket.sh'
                # print(bashCommand)
                process = subprocess.Popen(bashCommand.split())
                output, error = process.communicate()
                #print(output, error)
