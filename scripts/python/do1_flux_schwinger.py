import sys
import json
import itertools
import subprocess
import os
sys.path.append(os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "..", "..", "lib", "src", "python"))
from iterate_confs import distribute_jobs

#conf_type = "su2_suzuki"
conf_type = "qc2dstag"
#conf_type = "gluodynamics"
theory_type = "su2"

x_trans = 0
d_ouside = 10
d_max = 15
HYP_alpha1 = "1"
HYP_alpha2 = "1"
HYP_alpha3 = "0.5"
APE_alpha = "0.5"
APE_steps = "121"
HYP_steps = "1"

arch = "rrcmpi-a"
number_of_jobs = 200


#smearing_arr = ['original']
decomposition_type_plaket_arr = ["original"]
decomposition_type_wilson_arr = ["original"]
beta_arr = ['/']
#beta_arr = ['beta2.5']
#mu_arr = ['mu0.00', 'mu0.20', 'mu0.30', 'mu0.35', 'mu0.40', 'mu0.45']
#mu_arr = ['/']
#mu_arr = ['mu0.00', 'mu0.30', 'mu0.35', 'mu0.40', 'mu0.45']
mu_arr = ['mu0.00']
conf_size_arr = ['40^4']
additional_parameters_arr = ['/']

iter_arrays = [beta_arr, mu_arr, conf_size_arr,
               decomposition_type_plaket_arr,
               decomposition_type_wilson_arr, additional_parameters_arr]
for beta, mu, conf_size, decomposition_type_plaket, decomposition_type_wilson, additional_parameters in itertools.product(*iter_arrays):
    f = open(
        f'/home/clusters/rrcmpi/kudrov/conf/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/parameters_{decomposition_type_plaket}.json')
    data = json.load(f)
    conf_format_plaket = data['conf_format']
    file_precision_plaket = data['file_precision']
    bytes_skip_plaket = data['bytes_skip']
    matrix_type_plaket = data['matrix_type']
    conf_path_start_plaket = data['conf_path_start']
    conf_path_end_plaket = data['conf_path_end']
    padding_plaket = data['padding']
    conf_name_plaket = data['conf_name']
    convert_plaket = data['convert']
    L_spat = data['x_size']
    L_time = data['t_size']

    R_min = 4
    R_max = L_spat / 2
    #R_max = 16
    T_min = 4
    T_max = L_time / 2
    #T_max = 10

    f = open(
        f'/home/clusters/rrcmpi/kudrov/conf/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/parameters_{decomposition_type_wilson}.json')
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

    if HYP_steps == 0:
        smearing_str = f'HYP0_APE_alpha={APE_alpha}'
    else:
        smearing_str = f'HYP{HYP_steps}_alpha={HYP_alpha1}_{HYP_alpha2}_{HYP_alpha3}_APE_alpha={APE_alpha}'

    #chains = {'/': [201, 201]}
    #jobs = distribute_jobs(chains, number_of_jobs)
    jobs = distribute_jobs(data['chains'], number_of_jobs)

    for job in jobs:

        log_path = f'/home/clusters/rrcmpi/kudrov/observables_cluster/logs/flux_tube_schwinger/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/'\
            f'/{decomposition_type_plaket}/{smearing_str}/{job[0]}'
        conf_path_start_plaket1 = f'{conf_path_start_plaket}/{job[0]}/{conf_name_plaket}'
        conf_path_start_wilson1 = f'{conf_path_start_wilson}/{job[0]}/{conf_name_wilson}'
        try:
            os.makedirs(log_path)
        except:
            pass

        output_path = f'/home/clusters/rrcmpi/kudrov/observables_cluster/result/flux_tube_schwinger/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/{decomposition_type_plaket}'\
            f'/{smearing_str}/{job[0]}'
        # -q mem8gb -l nodes=1:ppn=4
        bashCommand = f'qsub -q mem8gb -l nodes=1:ppn=4 -v conf_format_plaket={conf_format_plaket},conf_format_wilson={conf_format_wilson},bytes_skip_plaket={bytes_skip_plaket},'\
            f'bytes_skip_wilson={bytes_skip_wilson},matrix_type_plaket={matrix_type_plaket},matrix_type_wilson={matrix_type_wilson},file_precision_wilson={file_precision_wilson},file_precision_plaket={file_precision_plaket},'\
            f'conf_path_start_plaket={conf_path_start_plaket1},conf_path_end_plaket={conf_path_end_plaket},conf_path_start_wilson={conf_path_start_wilson1},conf_path_end_wilson={conf_path_end_wilson},'\
            f'padding_plaket={padding_plaket},padding_wilson={padding_wilson},convert_plaket={convert_plaket},convert_wilson={convert_wilson},'\
            f'HYP_alpha1={HYP_alpha1},HYP_alpha2={HYP_alpha2},HYP_alpha3={HYP_alpha3},APE_alpha={APE_alpha},APE_steps={APE_steps},HYP_steps={HYP_steps},'\
            f'R_min={R_min},R_max={R_max},T_min={T_min},T_max={T_max},x_trans={x_trans},d_ouside={d_ouside},d_max={d_max},L_spat={L_spat},L_time={L_time},'\
            f'output_path={output_path},chain={job[0]},conf_start={job[1]},conf_end={job[2]},arch={arch}'\
            f' -o {log_path}/{job[1]:04}-{job[2]:04}.o -e {log_path}/{job[1]:04}-{job[2]:04}.e ../bash/do_flux_schwinger.sh'
        # print(bashCommand)
        process = subprocess.Popen(bashCommand.split())
        output, error = process.communicate()
        #print(output, error)
