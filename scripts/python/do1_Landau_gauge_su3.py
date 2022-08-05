import sys
import json
sys.path.append('/home/clusters/rrcmpi/kudrov/scripts/python')
from iterate_confs import *
import subprocess
import os

L_spat1 = 32
L_time1 = 32
conf_size = "32^4"
conf_type = "gluodynamics"
theory_type = "su3"

DP_steps = 500
copies = 3

number_of_jobs = 50

# for beta in ['/']:
for beta in ['beta6.1']:
    # for beta in ['beta2.5', 'beta2.6']:
    # for beta in ['beta2.4']:
    # for mu in ['mu0.00', 'mu0.05', 'mu0.20', 'mu0.25', 'mu0.30', 'mu0.35', 'mu0.45']:
    # for mu in ['mu0.05', 'mu0.45']:
    for mu in ['/']:

        # f = open(
        #     f'/home/clusters/rrcmpi/kudrov/conf/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/parameters.json')
        # data = json.load(f)
        # conf_format = data['conf_format']
        # bites_skip = data['bites_skip']
        # L_spat = data['x_size']
        # L_time = data['t_size']
        # matrix_type = data['matrix_type']
        # conf_path_start = data['conf_path_start']
        # conf_path_end = data['conf_path_end']
        # padding = data['padding']
        # conf_name = data['conf_name']

        conf_format = "QCDSTAG"
        bites_skip = 0
        L_spat = L_spat1
        L_time = L_time1
        matrix_type = 'su3'
        conf_path_start = f'/home/clusters/rrcmpi/kudrov/mag_su3/conf_gaugefixed/{conf_type}/{conf_size}/DP_steps_{DP_steps}/copies={copies}/CONFDP_gaugefixed_'
        conf_path_end = "/"
        padding = 4
        conf_name = ""

        chains = {'/': [1, 500]}
        #chains = {'s0': [201, 250]}
        jobs = distribute_jobs(chains, number_of_jobs)
        #jobs = distribute_jobs(data['chains'], number_of_jobs)

        for job in jobs:

            log_path = f'/home/clusters/rrcmpi/kudrov/observables_cluster/logs/Landau_gauge_su3/{conf_type}/{conf_size}/{beta}/{mu}/'\
                f'DP_steps_{DP_steps}/copies={copies}/{job[0]}'
            try:
                os.makedirs(log_path)
            except:
                pass
            output_conf_path = f'/home/clusters/rrcmpi/kudrov/Landau_su3/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/DP_steps_{DP_steps}/copies={copies}'
            # qsub -q mem8gb -l nodes=1:ppn=4
            bashCommand = f'qsub -q kepler -l nodes=1:ppn=8 -v conf_path_start={conf_path_start},conf_path_end={conf_path_end},padding={padding},conf_format={conf_format},bites_skip={bites_skip},'\
                f'DP_steps={DP_steps},copies={copies},output_conf_path={output_conf_path},'\
                f'L_spat={L_spat},L_time={L_time},chain={job[0]},conf_start={job[1]},conf_end={job[2]}'\
                f' -o {log_path}/{job[1]:04}-{job[2]:04}.o -e {log_path}/{job[1]:04}-{job[2]:04}.e /home/clusters/rrcmpi/kudrov/observables_cluster/scripts/do_Landau_gauge_su3.sh'
            # print(bashCommand)
            process = subprocess.Popen(bashCommand.split())
            output, error = process.communicate()
            # print(output, error)
