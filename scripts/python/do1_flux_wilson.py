import sys
import json
sys.path.append('/home/clusters/rrcmpi/kudrov/scripts/python')
from iterate_confs import *
import subprocess
import os

#conf_size = "24^4"
conf_size = "40^4"
#conf_size = "32^4"
#conf_type = "su2_suzuki"
conf_type = "qc2dstag"
theory_type = "su2"
bites_skip_plaket = 0
bites_skip_wilson = 0

monopole_plaket = '/'
monopole_wilson = '/'

if monopole_plaket == '/':
    monopole1 = theory_type
else:
    monopole1 = monopole_plaket

if monopole_wilson == '/':
    monopole2 = theory_type
else:
    monopole2 = monopole_wilson

#HYP_alpha1 = "1"
#HYP_alpha2 = "1"
#HYP_alpha3 = "0.5"
#APE_alpha = "0.5"
#stout_alpha = "0.15"
#APE_steps = "40"
#HYP_steps = "0"

R_min = 4
R_max = 16
T_min = 4
T_max = 16
x_trans = 0

number_of_jobs = 100

smearing = 'smeared'

for beta in ['/']:\
#for beta in ['beta2.4', 'beta2.5', 'beta2.6']:
#for beta in ['beta2.4']:
    for mu in ['mu0.20']:
    #for mu in ['mu0.30']:
    #for mu in ['']:

        f = open(
                f'/home/clusters/rrcmpi/kudrov/smearing_cluster/smearing_parameters/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/{monopole_wilson}/smearing_flux.json')
        data_smearing = json.load(f)
        HYP_alpha1 = data_smearing['HYP_alpha1']
        HYP_alpha2 = data_smearing['HYP_alpha2']
        HYP_alpha3 = data_smearing['HYP_alpha3']
        APE_alpha = data_smearing['APE_alpha']
        APE = data_smearing['APE']
        HYP = data_smearing['HYP']
        APE_steps = data_smearing['APE_steps']
        HYP_steps = data_smearing['HYP_steps']

        #HYP_alpha1 = "1"
        #HYP_alpha2 = "1"
        #HYP_alpha3 = "0.5"
        #HYP_alpha1 = "0.75"
        #HYP_alpha2 = "0.6"
        #HYP_alpha3 = "0.3"
        #APE_alpha = "0.5"
        #stout_alpha = "0.15"
        #APE_steps = "200"
        #HYP_steps = "1"

        f = open(
            f'/home/clusters/rrcmpi/kudrov/conf/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/{monopole_plaket}/parameters.json')
        data_plaket = json.load(f)

        conf_format_plaket = data_plaket['conf_format']
        bites_skip_plaket = data_plaket['bites_skip']
        matrix_type_plaket = data_plaket['matrix_type']
        L_spat = data_plaket['x_size']
        L_time = data_plaket['t_size']
        conf_path_plaket_start = data_plaket['conf_path_start']
        conf_path_plaket_end = data_plaket['conf_path_end']
        padding_plaket = data_plaket['padding']
        conf_name_plaket = data_plaket['conf_name']

        f = open(
            f'/home/clusters/rrcmpi/kudrov/conf/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/{monopole_wilson}/parameters.json')
        data_wilson = json.load(f)
        conf_format_wilson = data_wilson['conf_format']
        bites_skip_wilson = data_wilson['bites_skip']
        matrix_type_wilson = data_wilson['matrix_type']
        conf_path_wilson_start = data_wilson['conf_path_start']
        conf_path_wilson_end = data_wilson['conf_path_end']
        padding_wilson = data_wilson['padding']
        conf_name_wilson = data_wilson['conf_name']

        if smearing == 'smeared':
            conf_format_wilson = 'double'
            bites_skip_wilson = '0'
            conf_path_wilson_start = f'/home/clusters/rrcmpi/kudrov/smearing_cluster/confs_smeared/{theory_type}/'\
                f'{conf_type}/{conf_size}/{beta}/{mu}/{monopole_wilson}/HYP{HYP_steps}_alpha={HYP_alpha1}_{HYP_alpha2}_{HYP_alpha3}_APE{APE_steps}_alpha={APE_alpha}'
            conf_path_wilson_end = '/'
            padding_wilson = 4
            conf_name_wilson = 'conf_'

        #chains = {'/': [201, 201]}
        #jobs = distribute_jobs(chains, number_of_jobs)
        jobs = distribute_jobs(data_plaket['chains'], number_of_jobs)

        for job in jobs:

            log_path = f'/home/clusters/rrcmpi/kudrov/observables_cluster/logs/flux_tube_wilson/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/{monopole1}-{monopole2}'\
                f'/HYP{HYP_steps}_alpha={HYP_alpha1}_{HYP_alpha2}_{HYP_alpha3}_APE{APE_steps}_alpha={APE_alpha}/{job[0]}'
            conf_path_plaket_start1 = f'{conf_path_plaket_start}/{job[0]}/{conf_name_plaket}'
            conf_path_wilson_start1 = f'{conf_path_wilson_start}/{job[0]}/{conf_name_wilson}'
            try:
                os.makedirs(log_path)
            except:
                pass

            output_path = f'/home/clusters/rrcmpi/kudrov/observables_cluster/result/flux_tube_wilson/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/{monopole1}-{monopole2}'\
                f'/HYP{HYP_steps}_alpha={HYP_alpha1}_{HYP_alpha2}_{HYP_alpha3}_APE{APE_steps}_alpha={APE_alpha}/{job[0]}'

            bashCommand = f'qsub -q long -v conf_format_plaket={conf_format_plaket},conf_format_wilson={conf_format_wilson},bites_skip_plaket={bites_skip_plaket},'\
                f'bites_skip_wilson={bites_skip_wilson},matrix_type_plaket={matrix_type_plaket},matrix_type_wilson={matrix_type_wilson},'\
                f'conf_path_plaket_start={conf_path_plaket_start1},conf_path_plaket_end={conf_path_plaket_end},conf_path_wilson_start={conf_path_wilson_start1},conf_path_wilson_end={conf_path_wilson_end},'\
                f'padding_plaket={padding_plaket},padding_wilson={padding_wilson},R_min={R_min},R_max={R_max},T_min={T_min},T_max={T_max},x_trans={x_trans},L_spat={L_spat},L_time={L_time},'\
		f'output_path={output_path},chain={job[0]},conf_start={job[1]},conf_end={job[2]}'\
                f' -o {log_path}/{job[1]:04}-{job[2]:04}.o -e {log_path}/{job[1]:04}-{job[2]:04}.e /home/clusters/rrcmpi/kudrov/observables_cluster/scripts/do_flux_wilson.sh'
            #print(bashCommand)
            process = subprocess.Popen(bashCommand.split())
            output, error = process.communicate()
            #print(output, error)
