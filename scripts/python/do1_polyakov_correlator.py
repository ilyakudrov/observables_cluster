import sys
import json
sys.path.append('/home/clusters/rrcmpi/kudrov/scripts/python')
from iterate_confs import *
import subprocess
import os

L_spat = 64
L_time = 4
conf_size = "nt4"
#conf_size = "40^4"
# conf_size = "48^4"
# conf_type = "su2_suzuki"
#conf_type = "gluodynamics"
conf_type = "QCD/140MeV"
#conf_type = "qc2dstag"
theory_type = "su3"

calculate_absent = "false"

#additional_parameters = 'T_step=0.0005/T_final=0.5/OR_steps=4'
additional_parameters = '/'
#additional_parameters = 'DP_steps_500/copies=3'

smearing = 'HYP1_alpha=1_1_0.5'
D_max = 6

number_of_jobs = 50

arch = "rrcmpi-a"

for beta in ['/']:
    # for beta in ['beta2.8']:
    # for beta in ['beta6.3']:
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

        conf_format = 'double'
        conf_path_start = f'/home/clusters/rrcmpi/kudrov/smearing/{theory_type}/{conf_type}/{conf_size}/{smearing}'
        conf_name = 'smeared_'

        # chains = {'/': [1, 50]}
        #chains = {'s0': [201, 250]}
        # jobs = distribute_jobs(chains, number_of_jobs)
        jobs = distribute_jobs(data['chains'], number_of_jobs)
        for job in jobs:
            log_path = f'/home/clusters/rrcmpi/kudrov/observables_cluster/logs/polyakov_loop_correlator/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/'\
                f'{smearing}/{additional_parameters}/{job[0]}'
            conf_path_start1 = f'{conf_path_start}/{job[0]}/{conf_name}'
            try:
                os.makedirs(log_path)
            except:
                pass
            path_output_correlator = f'/home/clusters/rrcmpi/kudrov/observables_cluster/result/polyakov_loop_correlator/{theory_type}/'\
                f'{conf_type}/{conf_size}/{beta}/{mu}/{smearing}/{additional_parameters}/{job[0]}'
            # qsub -q mem8gb -l nodes=1:ppn=4
            # qsub -q long
            # 4gb for 48^4 monopole
            # 8gb for 48^4 su2
            # 8gb for nt6 and bigger
            # 16gb for nt10 and bigger
            bashCommand = f'qsub -q long -v conf_path_start={conf_path_start1},conf_path_end={conf_path_end},'\
                f'conf_format={conf_format},bytes_skip={bytes_skip},path_output_correlator={path_output_correlator},'\
                f'padding={padding},calculate_absent={calculate_absent},'\
                f'L_spat={L_spat},L_time={L_time},D_max={D_max},matrix_type={matrix_type}'\
                f'chain={job[0]},conf_start={job[1]},conf_end={job[2]},arch={arch},'\
                f' -o {log_path}/{job[1]:04}-{job[2]:04}.o -e {log_path}/{job[1]:04}-{job[2]:04}.e /home/clusters/rrcmpi/kudrov/observables_cluster/scripts/do_polyakov_correlator.sh'
            # print(bashCommand)
            process = subprocess.Popen(bashCommand.split())
            output, error = process.communicate()
            # print(output, error)
