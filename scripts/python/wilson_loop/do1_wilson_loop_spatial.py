import sys
import json
import subprocess
import os
import itertools

sys.path.append(os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "..", "..", "..", "lib", "src", "python"))
from iterate_confs import distribute_jobs

#conf_type = "su2_suzuki"
conf_type = "gluodynamics"
#conf_type = "QCD/140MeV"
#conf_type = "qc2dstag"
theory_type = "su2"
decomposition_type_arr = ["original"]
#decomposition_type_arr = ["monopoless", "monopole", "original", "mag_Landau"]

calculate_absent = 0
#representation="adjoint"
representation="fundamental"
APE_start=1
APE_end=201
APE_step=10
alpha=1
gauge_copies=0

additional_parameters_arr = ['/']
#additional_parameters_arr = ['steps_25/copies=4', 'steps_50/copies=4',
#                             'steps_100/copies=4', 'steps_200/copies=4',
#                             'steps_500/copies=4', 'steps_1000/copies=4', 'steps_2000/copies=4']
#additional_parameters_arr = ['steps_500/copies=3']
#additional_parameters_arr = ['steps_500/copies=3/compensate_1']
# additional_parameters_arr = ['T_step=0.001']
#additional_parameters_arr = ['T_step=0.0001',  'T_step=0.0004',  'T_step=0.0008',  'T_step=0.0015',  'T_step=0.004',  'T_step=0.008',  'T_step=0.0125',  'T_step=0.05',  'T_step=5e-05'
#'T_step=0.0002',  'T_step=0.0005',  'T_step=0.001',   'T_step=0.002',   'T_step=0.006',  'T_step=0.01',   'T_step=0.025',   'T_step=0.1']
#additional_parameters_arr = ['T_step=0.0001', 'T_step=0.0002', 'T_step=0.0004', 'T_step=0.0008',
#                             'T_step=0.001', 'T_step=0.002', 'T_step=0.004', 'T_step=0.008', 'T_step=5e-05']
# additional_parameters_arr = ['steps_500/copies=3/compensate_1', 'steps_1000/copies=3/compensate_1',
#                             'steps_2000/copies=3/compensate_1', 'steps_4000/copies=3/compensate_1']
#additional_parameters_arr = ['steps_1000/copies=3/compensate_1',
#                             'steps_2000/copies=3/compensate_1', 'steps_4000/copies=3/compensate_1']
#additional_parameters_arr = ['steps_330/copies=1', 'steps_2000/copies=1']

axis = 'on-axis'

# smearing_arr = ['HYP0_APE_alpha=0.5',
#                'HYP1_alpha=1_1_0.5_APE_alpha=0.5', 'HYP2_alpha=1_1_0.5_APE_alpha=0.5']
#smearing_arr = ['HYP0_alpha=1_1_0.5_APE_alpha=0.5', 'HYP1_alpha=1_1_0.5_APE_alpha=0.5']
#additional_parameters_arr = ['steps_25/copies=4', 'steps_50/copies=2',
#                             'steps_50/copies=4', 'steps_100/copies=1', 'steps_100/copies=2',
#                             'steps_100/copies=4', 'steps_200/copies=4',
#                             'steps_500/copies=4', 'steps_0/copies=1',
#                             'steps_2/copies=1', 'steps_10/copies=1']
#additional_parameters_arr = ['/']

number_of_jobs = 100

arch = "rrcmpi-a"
beta_arr = ['beta2.779']
#beta_arr = ['/']
mu_arr = ['/']
#mu_arr = ['mu0.05', 'mu0.20', 'mu0.25', 'mu0.30', 'mu0.35', 'mu0.40', 'mu0.45']
#mu_arr = ['mu0.40']
conf_size_arr = ['32^3x8']
#conf_size_arr = ['nt4', 'nt6', 'nt8', 'nt10', 'nt12', 'nt14']

iter_arrays = [beta_arr, mu_arr, conf_size_arr,
               additional_parameters_arr, decomposition_type_arr]
for beta, mu, conf_size, additional_parameters, decomposition_type in itertools.product(*iter_arrays):
    f = open(
        f'/home/clusters/rrcmpi/kudrov/conf/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/parameters_{decomposition_type}.json')
    data = json.load(f)
    conf_format = data['conf_format']
    bytes_skip = data['bytes_skip']
    matrix_type = data['matrix_type']
    conf_path_start = data['conf_path_start']
    conf_path_end = data['conf_path_end']
    padding = data['padding']
    conf_name = data['conf_name']
    convert = data['convert']
    L_spat = data['x_size']
    L_time = data['t_size']
    T_min = 1
    T_max = L_spat // 2
    R_min = 1
    R_max = L_spat // 2

    conf_path_start = conf_path_start + f'/{additional_parameters}'

    chains = {'s0': [1, 1000]}
    #chains = {'s5': [1, 500], 's6': [1, 500]}
    jobs = distribute_jobs(chains, number_of_jobs)
    #jobs = distribute_jobs(data['chains'], number_of_jobs)
    for job in jobs:
        # log_path = f'/home/clusters/rrcmpi/kudrov/observables_cluster/logs/smearing/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/'\
        #     f'T_step={T_step}/T_final={T_final}/OR_steps={OR_steps}/{smearing_str}/{job[0]}'
        log_path = f'/home/clusters/rrcmpi/kudrov/observables_cluster/logs/wilson_loop_spatial/{representation}/{axis}/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/'\
            f'{decomposition_type}/{additional_parameters}/{job[0]}'
        conf_path_start1 = f'{conf_path_start}/{job[0]}/{conf_name}'
        try:
            os.makedirs(log_path)
        except:
            pass
        path_wilson = f'/home/clusters/rrcmpi/kudrov/observables_cluster/result/wilson_loop_spatial/{representation}/{axis}/{theory_type}/'\
            f'{conf_type}/{conf_size}/{beta}/{mu}/{decomposition_type}/{additional_parameters}/alpha_{alpha}/{job[0]}'
        # qsub -q mem8gb -l nodes=1:ppn=4
        # qsub -q long
        # 4gb for 48^4 monopole
        # 8gb for 48^4 su2
        # 8gb for nt6 and bigger
        # 16gb for nt10 and bigger
        bashCommand = f'qsub -q long -v conf_path_start={conf_path_start1},conf_path_end={conf_path_end},'\
            f'conf_format={conf_format},bytes_skip={bytes_skip},path_wilson={path_wilson},convert={convert},'\
            f'padding={padding},calculate_absent={calculate_absent},representation={representation},APE_step={APE_step},'\
            f'APE_start={APE_start},APE_end={APE_end},alpha={alpha},gauge_copies={gauge_copies},'\
            f'L_spat={L_spat},L_time={L_time},T_min={T_min},T_max={T_max},R_min={R_min},R_max={R_max},'\
            f'chain={job[0]},conf_start={job[1]},conf_end={job[2]},arch={arch},matrix_type={matrix_type}'\
            f' -o {log_path}/{job[1]:04}-{job[2]:04}.o -e {log_path}/{job[1]:04}-{job[2]:04}.e ../../bash/wilson_loop/do_wilson_loop_spatial.sh'
        # print(bashCommand)
        process = subprocess.Popen(bashCommand.split())
        output, error = process.communicate()
        # print(output, error)
