import sys
import json
sys.path.append('/home/clusters/rrcmpi/kudrov/scripts/python')
from iterate_confs import *
import subprocess
import os

L_spat = 64
L_time = 16
conf_size = "nt16_gov"
#conf_size = "nt20_gov"
#conf_size = "40^4"
# conf_size = "48^4"
# conf_type = "su2_suzuki"
#conf_type = "gluodynamics"
conf_type = "QCD/140MeV"
#conf_type = "qc2dstag"
theory_type = "su3"
# matrix_type_array = ["monopoless", "monopole"]
matrix_type_array = ["original"]

calculate_absent = "false"

# additional_parameters = 'T_step=0.001/T_final=0.5/OR_steps=4'
additional_parameters = '/'
#additional_parameters = 'DP_steps_500/copies=3'

T_min = 1
T_max = 14
R_min = 1
R_max = 32

number_of_jobs = 100

arch = "rrcmpi-a"

for matrix_type in matrix_type_array:
    for beta in ['/']:
        # for beta in ['beta2.8']:
        # for beta in ['beta6.3']:
        # for beta in ['beta2.4']:
        # for mu in ['mu0.00', 'mu0.05', 'mu0.20', 'mu0.25', 'mu0.30', 'mu0.35', 'mu0.45']:
        # for mu in ['mu0.05', 'mu0.45']:
        for mu in ['/']:
            if matrix_type == 'original':
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
                #conf_path_start = f'/home/clusters/rrcmpi/kudrov/Coulomb_su3/su3/QCD/140MeV/{conf_size}'
                #conf_name = 'conf_Coulomb_gaugefixed_'
            else:
                conf_format = 'double'
                bytes_skip = 0
                padding = 4
                if matrix_type == 'monopoless':
                    if theory_type == 'su2':
                        matrix_type = 'su2'
                    elif theory_type == 'su3':
                        matrix_type = 'su3'
                    else:
                        print('wrong theory type')
                elif matrix_type == 'monopole':
                    if theory_type == 'su2':
                        matrix_type = 'abelian'
                    elif theory_type == 'su3':
                        matrix_type = 'su3_abelian'
                    else:
                        print('wrong theory type')
                conf_path_start = f'/home/clusters/rrcmpi/kudrov/decomposition/confs_decomposed/'\
                    f'{matrix_type}/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/{additional_parameters}'
                conf_path_end = '/'
                conf_name = f'conf_{matrix_type}_'

            # chains = {'/': [1, 50]}
            #chains = {'s0': [201, 250]}
            # jobs = distribute_jobs(chains, number_of_jobs)
            jobs = distribute_jobs(data['chains'], number_of_jobs)
            for job in jobs:
                # log_path = f'/home/clusters/rrcmpi/kudrov/observables_cluster/logs/smearing/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/'\
                #     f'T_step={T_step}/T_final={T_final}/OR_steps={OR_steps}/{smearing_str}/{job[0]}'
                log_path = f'/home/clusters/rrcmpi/kudrov/observables_cluster/logs/wilson_loops/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/'\
                    f'{matrix_type}/{additional_parameters}/{job[0]}'
                conf_path_start1 = f'{conf_path_start}/{job[0]}/{conf_name}'
                try:
                    os.makedirs(log_path)
                except:
                    pass
                path_wilson = f'/home/clusters/rrcmpi/kudrov/observables_cluster/result/smearing/wilson_loop/{theory_type}/'\
                    f'{conf_type}/{conf_size}/{beta}/{mu}/{matrix_type}/{additional_parameters}/{job[0]}'
                # qsub -q mem8gb -l nodes=1:ppn=4
                # qsub -q long
                # 4gb for 48^4 monopole
                # 8gb for 48^4 su2
                # 8gb for nt6 and bigger
                # 16gb for nt10 and bigger
                bashCommand = f'qsub -q mem8gb -l nodes=1:ppn=4 -v conf_path_start={conf_path_start1},conf_path_end={conf_path_end},'\
                    f'conf_format={conf_format},bytes_skip={bytes_skip},path_wilson={path_wilson},'\
                    f'padding={padding},calculate_absent={calculate_absent},'\
                    f'L_spat={L_spat},L_time={L_time},T_min={T_min},T_max={T_max},R_min={R_min},R_max={R_max},'\
                    f'chain={job[0]},conf_start={job[1]},conf_end={job[2]},arch={arch},matrix_type={matrix_type}'\
                    f' -o {log_path}/{job[1]:04}-{job[2]:04}.o -e {log_path}/{job[1]:04}-{job[2]:04}.e /home/clusters/rrcmpi/kudrov/observables_cluster/scripts/do_wilson_loop.sh'
                # print(bashCommand)
                process = subprocess.Popen(bashCommand.split())
                output, error = process.communicate()
                # print(output, error)
