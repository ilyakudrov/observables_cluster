import sys
import json
sys.path.append('/home/clusters/rrcmpi/kudrov/scripts/python')
from iterate_confs import *
import subprocess
import os

L_spat = 64
L_time = 4
#conf_size = "nt16_gov"
conf_size = "nt4"
#conf_size = "16^4"
#conf_size = "48^4"
#conf_type = "su2_suzuki"
# conf_type = "gluodynamics"
conf_type = "QCD/140MeV"
#conf_type = "qc2dstag"
theory_type = "su3"

calculate_absent = "false"

#additional_parameters = 'T_step=0.001/T_final=0.5/OR_steps=4'
# additional_parameters = '/'
additional_parameters = 'steps_2000/copies=1'

number_of_jobs = 100

for beta in ['/']:
    # for beta in ['beta2.8']:
    # for beta in ['beta6.1']:
    # for beta in ['beta2.4']:
    # for mu in ['mu0.00', 'mu0.05', 'mu0.20', 'mu0.25', 'mu0.30', 'mu0.35', 'mu0.45']:
    # for mu in ['mu0.05', 'mu0.45']:
    for mu in ['/']:
        f = open(
            f'/home/clusters/rrcmpi/kudrov/conf/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/parameters.json')
        data = json.load(f)
        conf_format = data['conf_format']
        bytes_skip = data['bytes_skip']
        matrix_type = data['matrix_type']
        conf_path_start = data['conf_path_start']
        conf_path_end = data['conf_path_end']
        padding = data['padding']
        conf_name = data['conf_name']

        conf_path_start = f'/home/clusters/rrcmpi/kudrov/mag_su3/conf_gaugefixed/{conf_type}/{conf_size}/{additional_parameters}'
        padding = 4
        conf_name = 'conf.SP_gaugefixed_'

        #chains = {'/': [601, 601]}
        #chains = {'s0': [201, 250]}
        #jobs = distribute_jobs(chains, number_of_jobs)
        jobs = distribute_jobs(data['chains'], number_of_jobs)

        for job in jobs:
            log_path = f'/home/clusters/rrcmpi/kudrov/observables_cluster/logs/mag_su3/maximization/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/'\
                f'{additional_parameters}/{job[0]}'
            try:
                os.makedirs(log_path)
            except:
                pass
            conf_path_output = f'/home/clusters/rrcmpi/kudrov/mag_su3/conf_maximized/{theory_type}/'\
                f'{conf_type}/{conf_size}/{beta}/{mu}/{additional_parameters}/{job[0]}'
            functional_path_output = f'/home/clusters/rrcmpi/kudrov/mag_su3/maximization/{theory_type}/'\
                f'{conf_type}/{conf_size}/{beta}/{mu}/{additional_parameters}/{job[0]}'

            bashCommand = f'qsub -q kepler -l nodes=1:ppn=8 -v conf_path_start={conf_path_start},conf_path_end={conf_path_end},'\
                f'conf_format={conf_format},bytes_skip={bytes_skip},'\
                f'padding={padding},calculate_absent={calculate_absent},conf_path_output={conf_path_output},'\
                f'L_spat={L_spat},L_time={L_time},'\
                f'chain={job[0]},conf_start={job[1]},conf_end={job[2]}'\
                f' -o {log_path}/{job[1]:04}-{job[2]:04}.o -e {log_path}/{job[1]:04}-{job[2]:04}.e /home/clusters/rrcmpi/kudrov/observables_cluster/scripts/do_mag_max_su3.sh'
            # print(bashCommand)
            process = subprocess.Popen(bashCommand.split())
            output, error = process.communicate()
            # print(output, error)
