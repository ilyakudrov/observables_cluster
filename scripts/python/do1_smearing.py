import sys
import json
sys.path.append('/home/clusters/rrcmpi/kudrov/scripts/python')
from iterate_confs import *
import subprocess
import os

L_spat = 48
L_time = 48
conf_size = "48^4"
#conf_size = "40^4"
#conf_size = "48^4"
conf_type = "su2_suzuki"
#conf_type = "qc2dstag"
theory_type = "su2"
wilson_type = "original"
plaket_type = 'original'

T_step = 0.0001
T_final = 0.5
OR_steps = 4

APE_enabled = 1
HYP_enabled = 1
HYP_alpha1 = "0.75"
HYP_alpha2 = "0.6"
HYP_alpha3 = "0.3"
APE_alpha = "0.5"
APE_steps = "10"
HYP_steps = "1"
calculation_step_APE = 2
calculation_APE_start = 6

wilson_enabled = 1
flux_enabled = 0

T_min = 1
T_max = 24
R_min = 1
R_max = 24

number_of_jobs = 1

arch = "rrcmpi-a"

# for beta in ['/']:
for beta in ['beta2.8']:
    # for beta in ['beta2.5', 'beta2.6']:
    # for beta in ['beta2.4']:
    # for mu in ['mu0.00', 'mu0.05', 'mu0.20', 'mu0.25', 'mu0.30', 'mu0.35', 'mu0.45']:
    # for mu in ['mu0.05', 'mu0.45']:
    for mu in ['/']:

        if wilson_type == 'original':
            f = open(
                f'/home/clusters/rrcmpi/kudrov/conf/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/parameters.json')
            data = json.load(f)
            conf_format_wilson = data['conf_format']
            bytes_skip_wilson = data['bytes_skip']
            matrix_type_wilson = data['matrix_type']
            conf_path_start_wilson = data['conf_path_start']
            conf_path_end_wilson = data['conf_path_end']
            padding_wilson = data['padding']
            conf_name_wilson = data['conf_name']
        else:
            conf_format_wilson = 'double'
            bytes_skip_wilson = 0
            if wilson_type == 'monopoless':
                matrix_type_wilson = 'su2'
            elif wilson_type == 'monopole':
                matrix_type_wilson = 'abelian'
            conf_path_start_wilson = f'/home/clusters/rrcmpi/kudrov/decomposition/confs_decomposed/'\
                f'{wilson_type}/su2/{conf_type}/{conf_size}/{beta}/{mu}/T_step={T_step}/T_final={T_final}/OR_steps={OR_steps}'
            conf_path_end_wilson = '/'
            padding_wilson = 4
            conf_name_wilson = f'conf_{wilson_type}_'

        if plaket_type == 'original':
            f = open(
                f'/home/clusters/rrcmpi/kudrov/conf/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/parameters.json')
            data = json.load(f)
            conf_format_plaket = data['conf_format']
            bytes_skip_plaket = data['bytes_skip']
            matrix_type_plaket = data['matrix_type']
            conf_path_start_plaket = data['conf_path_start']
            conf_path_end_plaket = data['conf_path_end']
            padding_plaket = data['padding']
            conf_name_plaket = data['conf_name']
        else:
            conf_format_plaket = 'double'
            bytes_skip_plaket = 0
            if plaket_type == 'monopoless':
                matrix_type_plaket = 'su2'
            elif plaket_type == 'monopole':
                matrix_type_plaket = 'abelian'
            conf_path_start_plaket = f'/home/clusters/rrcmpi/kudrov/decomposition/confs_decomposed/'\
                f'{wilson_type}/su2/{conf_type}/{conf_size}/{beta}/{mu}/T_step={T_step}/T_final={T_final}/OR_steps={OR_steps}'
            conf_path_end_plaket = '/'
            padding_plaket = 4
            conf_name_plaket = f'conf_{plaket_type}_'

        if HYP_enabled == '0':
            smearing_str = f'HYP0_APE_alpha={APE_alpha}'
        else:
            smearing_str = f'HYP{HYP_steps}_alpha={HYP_alpha1}_{HYP_alpha2}_{HYP_alpha3}_APE_alpha={APE_alpha}'

        chains = {'/': [1, 1]}
        #chains = {'s0': [201, 250]}
        jobs = distribute_jobs(chains, number_of_jobs)
        #jobs = distribute_jobs(data['chains'], number_of_jobs)

        for job in jobs:

            log_path = f'/home/clusters/rrcmpi/kudrov/observables_cluster/logs/smearing/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/'\
                f'T_step={T_step}/T_final={T_final}/OR_steps={OR_steps}/{smearing_str}/{job[0]}'
            conf_path_start_wilson1 = f'{conf_path_start_wilson}/{job[0]}/{conf_name_wilson}'
            conf_path_start_plaket1 = f'{conf_path_start_plaket}/{job[0]}/{conf_name_plaket}'
            try:
                os.makedirs(log_path)
            except:
                pass
            path_conf_wilson_loop = f'/home/clusters/rrcmpi/kudrov/observables_cluster/result/smearing/wilson_loop/{theory_type}/'\
                f'{conf_type}/{conf_size}/{beta}/{mu}/{wilson_type}/{matrix_type_wilson}/{smearing_str}/{job[0]}'
            path_conf_flux_tube = f'/home/clusters/rrcmpi/kudrov/observables_cluster/result/smearing/flux_tube/{theory_type}/'\
                f'{conf_type}/{conf_size}/{beta}/{mu}/{matrix_type_wilson}_{matrix_type_plaket}/{smearing_str}/{job[0]}'
            # qsub -q mem8gb -l nodes=1:ppn=4
            # qsub -q long
            bashCommand = f'qsub -q mem8gb -l nodes=1:ppn=4 -v conf_path_start_plaket={conf_path_start_plaket1},conf_path_end_plaket={conf_path_end_plaket},'\
                f'conf_format_plaket={conf_format_plaket},bytes_skip_plaket={bytes_skip_plaket},'\
                f'conf_path_start_wilson={conf_path_start_wilson1},conf_path_end_wilson={conf_path_end_wilson},'\
                f'conf_format_wilson={conf_format_wilson},bytes_skip_wilson={bytes_skip_wilson},'\
                f'T_step={T_step},T_final={T_final},OR_steps={OR_steps},padding={padding_wilson},'\
                f'HYP_alpha1={HYP_alpha1},HYP_alpha2={HYP_alpha2},HYP_alpha3={HYP_alpha3},'\
                f'APE_alpha={APE_alpha},APE_enabled={APE_enabled},HYP_enabled={HYP_enabled},'\
                f'APE_steps={APE_steps},HYP_steps={HYP_steps},calculation_step_APE={calculation_step_APE},calculation_APE_start={calculation_APE_start},'\
                f'path_wilson={path_conf_wilson_loop},path_flux={path_conf_flux_tube},wilson_enabled={wilson_enabled},flux_enabled={flux_enabled},'\
                f'L_spat={L_spat},L_time={L_time},T_min={T_min},T_max={T_max},R_min={R_min},R_max={R_max},'\
                f'chain={job[0]},conf_start={job[1]},conf_end={job[2]},arch={arch},matrix_type_plaket={matrix_type_plaket},matrix_type_wilson={matrix_type_wilson}'\
                f' -o {log_path}/{job[1]:04}-{job[2]:04}.o -e {log_path}/{job[1]:04}-{job[2]:04}.e /home/clusters/rrcmpi/kudrov/observables_cluster/scripts/do_smearing.sh'
            #print(bashCommand)
            process = subprocess.Popen(bashCommand.split())
            output, error = process.communicate()
            # print(output, error)