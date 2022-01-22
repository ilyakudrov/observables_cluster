import sys
import json
sys.path.append('/home/clusters/rrcmpi/kudrov/scripts/python')
from iterate_confs import *
import subprocess
import os

conf_size = "24^4"
#conf_size = "40^4"
conf_type = "su2_suzuki"
matrix_type = "su2"
#conf_type = "qc2dstag"
bites_skip_plaket = 0
bites_skip_wilson = 0

monopole_plaket = '/'
monopole_wilson = 'monopole'

if monopole_plaket == '/':
    monopole1 = matrix_type
else:
    monopole1 = monopole_plaket

if monopole_wilson == '/':
    monopole2 = matrix_type
else:
    monopole2 = monopole_wilson

HYP_alpha1 = "1"
HYP_alpha2 = "1"
HYP_alpha3 = "0.5"
APE_alpha = "0.5"
stout_alpha = "0.15"
APE_steps = "100"
HYP_steps = "0"

R_min = 4
R_max = 12
T_min = 4
T_max = 12

number_of_jobs = 50

smearing = 'smeared'
# smearing = f'HYP{HYP_steps}_alpha={HYP_alpha1}_{HYP_alpha2}_{HYP_alpha3}_APE{APE_steps}_alpha={APE_alpha}'

for beta in ['2.4', '2.5', '2.6']:
    for mu in [""]:
        f = open(
            f'/home/clusters/rrcmpi/kudrov/conf/{matrix_type}{conf_type}/{conf_size}/beta{beta}/{mu}/{monopole_plaket}/parameters.json')
        data_plaket = json.load(f)

        conf_format_plaket = data_plaket['conf_format']
        bites_skip_plaket = data_plaket['bites_skip']
        matrix_type_plaket = data_plaket['matrix_type']
        L_spat = data_plaket['x_size']
        L_time = data_plaket['t_size']
        conf_path_plaket_start = data_plaket['conf_path_start']
        conf_path_plaket_end = data_plaket['conf_path_end']
        padding_plaket = data_plaket['padding']

        f = open(
            f'/home/clusters/rrcmpi/kudrov/conf/{matrix_type}/{conf_type}/{conf_size}/beta{beta}/{mu}/{monopole_wilson}/parameters.json')
        data_wilson = json.load(f)
        conf_format_wilson = data_wilson['conf_format']
        bites_skip_wilson = data_wilson['bites_skip']
        matrix_type_wilson = data_wilson['matrix_type']
        conf_path_wilson_start = data_wilson['conf_path_start']
        conf_path_wilson_end = data_wilson['conf_path_end']
        padding_wilson = data_wilson['padding']

        if smearing == 'smeared':
            conf_format_wilson = 'double'
            bites_skip_wilson = '0'
            conf_path_wilson_start = f'/home/clusters/rrcmpi/kudrov/smearing_cluster/confs_smeared/{matrix_type}/'\
                f'{conf_type}/{conf_size}/beta{beta}/{mu}/HYP{HYP_steps}_alpha={HYP_alpha1}_{HYP_alpha2}_{HYP_alpha3}_APE{APE_steps}_alpha={APE_alpha}/conf_'
            conf_path_wilson_end = '""'
            padding_wilson = 4

        jobs = distribute_jobs(data_plaket['chains'], number_of_jobs)

        for job in jobs:

            log_path = f'/home/clusters/rrcmpi/kudrov/observables_cluster/logs/flux_tube_wilson/{matrix_type}/{conf_type}/{conf_size}/beta{beta}/mu{mu}/{monopole1}-{monopole2}/{job[0]}'
            try:
                os.makedirs(log_path)
            except:
                pass

            output_path = f'/home/clusters/rrcmpi/kudrov/observables_cluster/result/flux_tube_wilson/{matrix_type}/{conf_type}/{conf_size}/beta{beta}/mu{mu}/{monopole1}-{monopole2}/{job[0]}'

            bashCommand = f'qsub -q long -v conf_format_plaket={conf_format_plaket},conf_format_wilson={conf_format_wilson},bites_skip_plaket={bites_skip_plaket},'\
                f'bites_skip_wilson={bites_skip_wilson},matrix_type_plaket={matrix_type_plaket},matrix_type_wilson={matrix_type_wilson},'\
                f'conf_path_plaket_start={conf_path_plaket_start},conf_path_plaket_end={conf_path_plaket_end},conf_path_wilson_start={conf_path_wilson_start},conf_path_wilson_end={conf_path_wilson_end},'\
                f'padding_plaket={padding_plaket},padding_wilson={padding_wilson},L_spat={L_spat},L_time={L_time},chain={job[0]},conf_start={job[1]},conf_end={job[2]}'\
                f' -o {log_path}/{job[1]:04}-{job[2]:04}.o -e {log_path}/{job[1]:04}-{job[2]:04}.e /home/clusters/rrcmpi/kudrov/observables_cluster/scripts/do_flux_wilson.sh'
            # print(bashCommand)
            process = subprocess.Popen(bashCommand.split())
            output, error = process.communicate()
            #print(output, error)
