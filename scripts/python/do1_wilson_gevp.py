import sys
import json
import subprocess
import os
import itertools

sys.path.append(os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "..", "..", "lib", "src", "python"))
from iterate_confs import distribute_jobs

#conf_type = "su2_suzuki"
conf_type = "gluodynamics"
#conf_type = "QCD/140MeV"
#conf_type = "qc2dstag"
theory_type = "su3"
#wilson_type_array = ['original']
#wilson_type_array = ['monopole', 'abelian', 'photon']
#wilson_type_array = ['monopoless', 'offdiagonal']
wilson_type_array = ['monopole']
#wilson_type_array = ['abelian', 'monopole', 'monopoless', 'offdiagonal', 'photon']
#representation = 'adjoint'
representation = 'fundamental'

#calculate_absent = "true"
calculate_absent = 0
gauge_copies = 100

HYP_enabled = 1
HYP_alpha1 = "1"
HYP_alpha2 = "1"
HYP_alpha3 = "0.5"
APE_alpha = "0.5"
APE_steps = "31"
#HYP_steps_array = ['0', '1']
HYP_steps_array = ['0']
calculation_step_APE = 10
calculation_APE_start = 11
N_dir = 4

number_of_jobs = 500

arch = "rrcmpi-a"

#beta_arr = ['beta2.6', 'beta2.779']
beta_arr = ['beta6.0']
#beta_arr = ['/']
#mu_arr = ['mu0.00', 'mu0.25', 'mu0.30', 'mu0.40']
#mu_arr = ['mu0.00', 'mu0.05', 'mu0.10', 'mu0.15', 'mu0.20', 'mu0.25', 'mu0.30', 'mu0.33', 'mu0.35', 'mu0.37', 'mu0.40', 'mu0.45', 'mu0.50']
mu_arr = ['/']
conf_size_arr = ['32^4']
#conf_size_arr = ['32^3x8', '32^3x16', '32^3x20', '32^3x24', '32^3x28', '32^3x32']
#conf_size_arr = ['32^3x64']
#conf_size_arr = ['nt4', 'nt6', 'nt8', 'nt10', 'nt12', 'nt14', 'nt16', 'nt18', 'nt20']
#conf_size_arr = ['nt4', 'nt6', 'nt8', 'nt10', 'nt12', 'nt14']
#conf_size_arr = ['nt16', 'nt18', 'nt20']
#conf_size_arr = ['nt4']
additional_parameters_arr = ['steps_0/copies=100']
#additional_parameters_arr = ['/']

iter_arrays = [beta_arr, mu_arr, conf_size_arr,
               additional_parameters_arr, wilson_type_array, HYP_steps_array]
for beta, mu, conf_size, additional_parameters, wilson_type, HYP_steps in itertools.product(*iter_arrays):
    f = open(
        f'/home/clusters/rrcmpi/kudrov/conf/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/parameters_{wilson_type}.json')
    data = json.load(f)
    conf_format_wilson = data['conf_format']
    file_precision_wilson = data['file_precision']
    bytes_skip_wilson = data['bytes_skip']
    matrix_type_wilson = data['matrix_type']
    conf_path_start_wilson = data['conf_path_start']
    conf_path_end_wilson = data['conf_path_end']
    padding_wilson = data['padding']
    conf_name_wilson = data['conf_name']
    convert_wilson = data['convert']
    L_spat = data['x_size']
    L_time = data['t_size']
    T_min = 1
    T_max = L_time//2
    #T_max = 4
    #T_max = L_time
    R_min = 1
    R_max = L_spat//2
    #R_max = 4
    if wilson_type != 'original':
        conf_path_start_wilson = conf_path_start_wilson + \
            f'/{additional_parameters}'

    if HYP_enabled == 0:
        smearing_str = f'HYP0_APE_alpha={APE_alpha}'
    else:
        smearing_str = f'HYP{HYP_steps}_alpha={HYP_alpha1}_{HYP_alpha2}_{HYP_alpha3}_APE_alpha={APE_alpha}'

    #chains = {'/': [1, 1000]}
    chains = {'s1': [1, 500]}
    #chains = {'s2': [1, 1424], 's3': [1, 6000], 's4': [1, 6000]}
    #jobs = distribute_jobs(chains, number_of_jobs)
    jobs = distribute_jobs(data['chains'], number_of_jobs)

    for job in jobs:
        # log_path = f'/home/clusters/rrcmpi/kudrov/observables_cluster/logs/smearing/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/'\
        #     f'T_step={T_step}/T_final={T_final}/OR_steps={OR_steps}/{smearing_str}/{job[0]}'
        log_path = f'/home/clusters/rrcmpi/kudrov/observables_cluster/logs/wilson_gevp/{representation}/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/'\
            f'{wilson_type}/{smearing_str}/{additional_parameters}/{job[0]}'
        conf_path_start_wilson1 = f'{conf_path_start_wilson}/{job[0]}/{conf_name_wilson}'
        try:
            os.makedirs(log_path)
        except:
            pass
        path_wilson_loop = f'/home/clusters/rrcmpi/kudrov/observables_cluster/result/wilson_gevp/{representation}/on-axis/{theory_type}/'\
            f'{conf_type}/{conf_size}/{beta}/{mu}/{wilson_type}/{smearing_str}/{additional_parameters}/{job[0]}'
        # qsub -q mem8gb -l nodes=1:ppn=4
        # qsub -q long
        # su3:
        # original: 24^4: 2GB, 28^4: 4GB, 32^4: 8GB, 36^4: 8GB, 40^4: 16GB
        # abelian: 28^4: 2GB, 32^4: 4GB, 36^4: 4GB, 40^4: 8GB
        bashCommand = f'qsub -q mem4gb -l nodes=1:ppn=2 -v convert_wilson={convert_wilson},file_precision_wilson={file_precision_wilson},'\
            f'conf_path_start_wilson={conf_path_start_wilson1},conf_path_end_wilson={conf_path_end_wilson},'\
            f'conf_format_wilson={conf_format_wilson},bytes_skip_wilson={bytes_skip_wilson},representation={representation},'\
            f'padding_wilson={padding_wilson},calculate_absent={calculate_absent},'\
            f'HYP_alpha1={HYP_alpha1},HYP_alpha2={HYP_alpha2},HYP_alpha3={HYP_alpha3},'\
            f'APE_alpha={APE_alpha},HYP_enabled={HYP_enabled},N_dir={N_dir},'\
            f'APE_steps={APE_steps},HYP_steps={HYP_steps},calculation_step_APE={calculation_step_APE},calculation_APE_start={calculation_APE_start},'\
            f'path_wilson={path_wilson_loop},'\
            f'L_spat={L_spat},L_time={L_time},T_min={T_min},T_max={T_max},R_min={R_min},R_max={R_max},gauge_copies={gauge_copies},'\
            f'chain={job[0]},conf_start={job[1]},conf_end={job[2]},arch={arch},matrix_type_wilson={matrix_type_wilson}'\
            f' -o {log_path}/{job[1]:04}-{job[2]:04}.o -e {log_path}/{job[1]:04}-{job[2]:04}.e ../bash/do_wilson_gevp.sh'
        # print(bashCommand)
        process = subprocess.Popen(bashCommand.split())
        output, error = process.communicate()
        # print(output, error)
