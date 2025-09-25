import sys
import json
import os
import subprocess
import itertools

sys.path.append(os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "..", "..", "..", "lib", "src", "python"))
from iterate_confs import distribute_jobs

#conf_type = "su2_suzuki"
conf_type = "gluodynamics"
#conf_type = "QCD/140MeV"
#conf_type = "qc2dstag"
theory_type = "su3"

calculate_absent = 0

copies = 20
T_min = 0.001

tolerance = '1e-15'
#doSA = 0
save_each = 0
save_best = 1

number_of_jobs = 160

beta_arr = ['beta6.1']
#beta_arr = ['/']
#mu_arr = ['mu0.00', 'mu0.05', 'mu0.20', 'mu0.25', 'mu0.30', 'mu0.35', 'mu0.45']
mu_arr = ['/']
#conf_size_arr = ['nt16', 'nt18', 'nt20']
conf_size_arr = ['36^4']
#steps_arr = [25, 50, 100, 200, 500, 1000, 2000]
steps_arr = [100]
#steps_arr = [62, 125, 250]
#steps_arr = [0, 2, 10]

iter_arrays = [beta_arr, mu_arr, conf_size_arr, steps_arr]
for beta, mu, conf_size, steps in itertools.product(*iter_arrays):
    additional_parameters = f'steps_{steps}/copies={copies}'
    f = open(
        f'/home/clusters/rrcmpi/kudrov/conf/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/parameters_original.json')
    data = json.load(f)
    conf_format = data['conf_format']
    bytes_skip = data['bytes_skip']
    matrix_type = data['matrix_type']
    conf_path_start = data['conf_path_start']
    conf_path_end = data['conf_path_end']
    padding = data['padding']
    conf_name = data['conf_name']
    L_spat = data['x_size']
    L_time = data['t_size']

    if steps == 0:
        doSA = 0
    else:
        doSA = 1

    #conf_path_start = f'/home/clusters/rrcmpi/kudrov/mag_su3/conf_gaugefixed/{conf_type}/{conf_size}/{additional_parameters}'
    #padding = 4
    #conf_name = 'CONFDP_gaugefixed_'

    #conf_path_start = f'/home/clusters/rrcmpi/kudrov/mag_su3/conf_gaugefixed/{conf_type}/{conf_size}/{additional_parameters}'
    #padding = 4
    #conf_name = 'conf.SP_gaugefixed_'
    #conf_path_end = '.ildg'

    #chains = {'/': [1, 1]}
    #chains = {'/': [1001, 1001]}
    #chains = {'s2': [1, 2000]}
    #chains = {'s1': [1, 500]}
    #jobs = distribute_jobs(chains, number_of_jobs)
    jobs = distribute_jobs(data['chains'], number_of_jobs)

    for job in jobs:
        log_path = f'/home/clusters/rrcmpi/kudrov/observables_cluster/logs/mag_su3/conf_gaugefixed/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/'\
            f'{additional_parameters}/{job[0]}'
        try:
            os.makedirs(log_path)
        except:
            pass
        conf_path_output = f'/home/clusters/rrcmpi/kudrov/mag_su3/conf_gaugefixed/'\
            f'{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/{additional_parameters}/{job[0]}'
        functional_path_output = f'/home/clusters/rrcmpi/kudrov/observables_cluster/result/mag/functional/'\
            f'{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/{additional_parameters}/{job[0]}'

        conf_path_start1 = f'{conf_path_start}/{job[0]}/{conf_name}'

        bashCommand = f'qsub -q kepler -l nodes=1:ppn=8 -v conf_path_start={conf_path_start1},conf_path_end={conf_path_end},'\
            f'conf_format={conf_format},bytes_skip={bytes_skip},tolerance={tolerance},conf_path_output={conf_path_output},'\
            f'padding={padding},calculate_absent={calculate_absent},functional_path_output={functional_path_output},'\
            f'L_spat={L_spat},L_time={L_time},steps={steps},T_min={T_min},copies={copies},doSA={doSA},save_each={save_each},save_best={save_best},'\
            f'chain={job[0]},conf_start={job[1]},conf_end={job[2]}'\
            f' -o {log_path}/{job[1]:04}-{job[2]:04}.o -e {log_path}/{job[1]:04}-{job[2]:04}.e ../../bash/mag_su3/do_mag_su3.sh'
        # print(bashCommand)
        process = subprocess.Popen(bashCommand.split())
        output, error = process.communicate()
        # print(output, error)
