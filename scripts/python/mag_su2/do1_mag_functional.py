import sys
import json
import os
sys.path.append(os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "..", "..", "..", "lib", "src", "python"))
from iterate_confs import distribute_jobs
import subprocess

#conf_size = "36^4"
conf_size = "nt4"
#conf_type = "gluodynamics"
#conf_type = "su2_suzuki"
#conf_type = "qc2dstag"
conf_type = "QCD/140MeV"
theory_type = "su3"

arch = "rrcmpi"

#additional_parameters = 'T_step=0.01'
additional_parameters = '/'

number_of_jobs = 100

for beta in ['/']:
# for beta in ['beta6.3']:
# for beta in ['beta2.5', 'beta2.6']:
#for beta in ['beta2.6']:
    for mu in ['mu0.00', 'mu0.05', 'mu0.20', 'mu0.25', 'mu0.30', 'mu0.35', 'mu0.45']:
    # for mu in ['mu0.05', 'mu0.45']:
    #for mu in ['/']:

        f = open(
            f'/home/clusters/rrcmpi/kudrov/conf/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/parameters_mag.json')
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

        conf_path_start = conf_path_start + f'/{additional_parameters}'

        #chains = {'/': [1, 50]}
        #chains = {'s0': [201, 250]}
        #jobs = distribute_jobs(chains, number_of_jobs)
        jobs = distribute_jobs(data['chains'], number_of_jobs)

        for job in jobs:

            log_path = f'/home/clusters/rrcmpi/kudrov/observables_cluster/logs/mag/functional/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/'\
                f'{additional_parameters}/{job[0]}'
            conf_path_start1 = f'{conf_path_start}/{job[0]}/{conf_name}'
            try:
                os.makedirs(log_path)
            except:
                pass
            path_functional_output = f'/home/clusters/rrcmpi/kudrov/observables_cluster/result/mag/functional/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/{additional_parameters}/{job[0]}'
            # for nt8 and bigger
            # qsub -q mem4gb -l nodes=1:ppn=2
            bashCommand = f'qsub -q long -v conf_path_start={conf_path_start1},conf_path_end={conf_path_end},padding={padding},conf_format={conf_format},bytes_skip={bytes_skip},'\
                f'path_functional_output={path_functional_output},arch={arch},theory_type={theory_type},'\
                f'L_spat={L_spat},L_time={L_time},chain={job[0]},conf_start={job[1]},conf_end={job[2]}'\
                f' -o {log_path}/{job[1]:04}-{job[2]:04}.o -e {log_path}/{job[1]:04}-{job[2]:04}.e ../../bash/mag_su2/do_mag_functional.sh'
            # print(bashCommand)
            process = subprocess.Popen(bashCommand.split())
            output, error = process.communicate()
            # print(output, error)
