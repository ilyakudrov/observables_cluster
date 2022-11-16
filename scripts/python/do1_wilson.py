import sys
import json
sys.path.append(os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "..", "..", "lib", "src", "python"))
from iterate_confs import distribute_jobs
import subprocess
import os


conf_size = "nt18_gov"
conf_size = "48^4"
# conf_type = "su2_suzuki"
conf_type = "QCD/140MeV"
#conf_type = "qc2dstag"
theory_type = "su3"

axis = 'on-axis'

R_min = 1
R_max = 14
T_min = 1
T_max = 32

number_of_jobs = 100

smearing = 'smeared'
diagonal = False

for monopole in ['monopoless', 'monopole', '/']:
    # for monopole in ['monopoless']:
    # for beta in ['/']:
    for beta in ['beta2.8']:
        # for beta in ['beta2.4', 'beta2.5', 'beta2.6']:
        # for beta in ['beta2.4']:
        # for mu in ['mu0.00', 'mu0.05', 'mu0.20', 'mu0.25', 'mu0.30', 'mu0.35', 'mu0.45']:
        # for mu in ['mu0.25']:
        for mu in ['/']:

            # f = open(
            #    f'/home/clusters/rrcmpi/kudrov/smearing_cluster/smearing_parameters/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/{monopole}/smearing_wilson.json')
            #data_smearing = json.load(f)
            #HYP_alpha1 = data_smearing['HYP_alpha1']
            #HYP_alpha2 = data_smearing['HYP_alpha2']
            #HYP_alpha3 = data_smearing['HYP_alpha3']
            #APE_alpha = data_smearing['APE_alpha']
            #APE = data_smearing['APE']
            #HYP = data_smearing['HYP']
            #APE_steps = data_smearing['APE_steps']
            #HYP_steps = data_smearing['HYP_steps']

            #HYP_alpha1 = "1"
            #HYP_alpha2 = "1"
            #HYP_alpha3 = "0.5"
            HYP_alpha1 = "0.75"
            HYP_alpha2 = "0.6"
            HYP_alpha3 = "0.3"
            APE_alpha = "0.5"
            stout_alpha = "0.15"
            APE_steps = "400"
            HYP_steps = "1"

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

            if smearing == 'smeared':
                conf_format = 'double'
                bites_skip = '0'
                conf_path_start = f'/home/clusters/rrcmpi/kudrov/smearing_cluster/confs_smeared/{theory_type}/'\
                    f'{conf_type}/{conf_size}/{beta}/{mu}/{monopole}/HYP{HYP_steps}_alpha={HYP_alpha1}_{HYP_alpha2}_{HYP_alpha3}_APE{APE_steps}_alpha={APE_alpha}'
                conf_path_end = '/'
                padding = 4
                conf_name = 'conf_'
                smearing = f'HYP{HYP_steps}_alpha={HYP_alpha1}_{HYP_alpha2}_{HYP_alpha3}_APE{APE_steps}_alpha={APE_alpha}'

            if diagonal:
                matrix_type = 'abelian'
                conf_format = conf_format + '_convert_abelian'
                if monopole == 'monopoless':
                    monopole1 = 'photon'
                elif monopole == '/':
                    monopole1 = 'abelian'
                else:
                    print('can not do diagonal for monopole')
            else:
                monopole1 = monopole

            #chains = {'/': [1, 1]}
            #jobs = distribute_jobs(chains, number_of_jobs)
            jobs = distribute_jobs(data['chains'], number_of_jobs)

            for job in jobs:

                log_path = f'/home/clusters/rrcmpi/kudrov/observables_cluster/logs/wilson_loop/{axis}/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/{monopole1}/{smearing}/{job[0]}'
                conf_path_start1 = f'{conf_path_start}/{job[0]}/{conf_name}'
                try:
                    os.makedirs(log_path)
                except:
                    pass

                output_path = f'/home/clusters/rrcmpi/kudrov/observables_cluster/result/wilson_loop/{axis}/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/{monopole1}/{smearing}/{job[0]}'

                # qsub -q mem8gb -l nodes=1:ppn=4
                bashCommand = f'qsub -q mem8gb -l nodes=1:ppn=4 -v axis={axis},conf_format={conf_format},'\
                    f'bites_skip={bites_skip},matrix_type={matrix_type},'\
                    f'conf_path_start={conf_path_start1},conf_path_end={conf_path_end},'\
                    f'padding={padding},R_min={R_min},R_max={R_max},T_min={T_min},T_max={T_max},L_spat={L_spat},L_time={L_time},'\
                    f'output_path={output_path},chain={job[0]},conf_start={job[1]},conf_end={job[2]}'\
                    f' -o {log_path}/{job[1]:04}-{job[2]:04}.o -e {log_path}/{job[1]:04}-{job[2]:04}.e ../bash/do_wilson.sh'
                # print(bashCommand)
                process = subprocess.Popen(bashCommand.split())
                output, error = process.communicate()
                #print(output, error)
