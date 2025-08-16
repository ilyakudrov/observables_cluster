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

arch="rrcmpi-a"
number_of_jobs = 100

#smearing_arr = ['HYP0_alpha=1_1_0.5_APE_alpha=0.5', 'HYP1_alpha=1_1_0.5_APE_alpha=0.5',
#                'HYP2_alpha=1_1_0.5_APE_alpha=0.5', 'HYP3_alpha=1_1_0.5_APE_alpha=0.5']
smearing_arr = ['HYP0_APE_alpha=0.5']
decomposition_type_plaket_arr = ["original", "monopole", "monopoless", "abelian"]
decomposition_type_wilson_arr = ["original", "monopole", "monopoless", "abelian"]
beta_arr = ['/']
#beta_arr = ['beta6.2']
#mu_arr = ['mu0.00', 'mu0.20', 'mu0.30', 'mu0.35', 'mu0.40', 'mu0.45']
#mu_arr = ['/']
mu_arr = ['mu0.00', 'mu0.20']
conf_size_arr = ['40^4']
additional_parameters_arr = ['/']

iter_arrays = [beta_arr, mu_arr, conf_size_arr,
               decomposition_type_plaket_arr,
               decomposition_type_wilson_arr, smearing_arr, additional_parameters_arr]
for beta, mu, conf_size, decomposition_type_plaket, decomposition_type_wilson, smearing, additional_parameters in itertools.product(*iter_arrays):

    f = open(
        f'/home/clusters/rrcmpi/kudrov/conf/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/parameters_{decomposition_type_plaket}.json')
    data_plaket = json.load(f)
    conf_format_plaket = data_plaket['conf_format']
    file_precision_plaket = data_plaket['file_precision']
    bytes_skip_plaket = data_plaket['bytes_skip']
    matrix_type_plaket = data_plaket['matrix_type']
    conf_path_start_plaket = data_plaket['conf_path_start']
    conf_path_end_plaket = data_plaket['conf_path_end']
    padding_plaket = data_plaket['padding']
    conf_name_plaket = data_plaket['conf_name']
    convert_plaket = data_plaket['convert']
    L_spat = data_plaket['x_size']
    L_time = data_plaket['t_size']

    R_min = 4
    R_max = L_spat / 2
    #R_max = 6
    T_min = 4
    T_max = L_time / 2
    #T_max = 6

    f = open(
        f'/home/clusters/rrcmpi/kudrov/conf/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/parameters_{decomposition_type_wilson}.json')
    data_wilson = json.load(f)
    conf_format_wilson = data_wilson['conf_format']
    file_precision_wilson = data_wilson['file_precision']
    bytes_skip_wilson = data_wilson['bytes_skip']
    matrix_type_wilson = data_wilson['matrix_type']
    conf_path_start_wilson = data_wilson['conf_path_start']
    conf_path_end_wilson = data_wilson['conf_path_end']
    padding_wilson = data_wilson['padding']
    conf_name_wilson = data_wilson['conf_name']
    convert_wilson = data_wilson['convert']

    conf_path_start_wilson = f'/home/clusters/rrcmpi/kudrov/smearing/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/{decomposition_type_wilson}/{smearing}/{additional_parameters}'
    conf_name_wilson = 'smeared_'
    conf_path_end_wilson = '/'
    conf_format_wilson = 'double'
    padding_wilson = 4
    bytes_skip_wilson = 0
    convert_wilson = 0

    #chains = {'/': [201, 201]}
    #jobs = distribute_jobs(chains, number_of_jobs)
    jobs = distribute_jobs(data_plaket['chains'], number_of_jobs)

    for job in jobs:

        log_path = f'/home/clusters/rrcmpi/kudrov/observables_cluster/logs/flux_tube_wilson/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/'\
            f'/{decomposition_type_plaket}-{decomposition_type_wilson}/{smearing}/{job[0]}'
        conf_path_start_plaket1 = f'{conf_path_start_plaket}/{job[0]}/{conf_name_plaket}'
        conf_path_start_wilson1 = f'{conf_path_start_wilson}/{job[0]}/{conf_name_wilson}'
        try:
            os.makedirs(log_path)
        except:
            pass

        output_path = f'/home/clusters/rrcmpi/kudrov/observables_cluster/result/flux_tube_wilson/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/{decomposition_type_plaket}-{decomposition_type_wilson}'\
            f'/{smearing}/{job[0]}'
        #-q mem8gb -l nodes=1:ppn=4
        bashCommand = f'qsub -q mem4gb -l nodes=1:ppn=2 -v conf_format_plaket={conf_format_plaket},conf_format_wilson={conf_format_wilson},bytes_skip_plaket={bytes_skip_plaket},'\
            f'bytes_skip_wilson={bytes_skip_wilson},matrix_type_plaket={matrix_type_plaket},matrix_type_wilson={matrix_type_wilson},file_precision_wilson={file_precision_wilson},file_precision_plaket={file_precision_plaket},'\
            f'conf_path_start_plaket={conf_path_start_plaket1},conf_path_end_plaket={conf_path_end_plaket},conf_path_start_wilson={conf_path_start_wilson1},conf_path_end_wilson={conf_path_end_wilson},'\
            f'padding_plaket={padding_plaket},padding_wilson={padding_wilson},convert_plaket={convert_plaket},convert_wilson={convert_wilson},'\
            f'R_min={R_min},R_max={R_max},T_min={T_min},T_max={T_max},x_trans={x_trans},L_spat={L_spat},L_time={L_time},'\
            f'output_path={output_path},chain={job[0]},conf_start={job[1]},conf_end={job[2]},arch={arch}'\
            f' -o {log_path}/{job[1]:04}-{job[2]:04}.o -e {log_path}/{job[1]:04}-{job[2]:04}.e ../bash/do_flux_wilson.sh'
        # print(bashCommand)
        process = subprocess.Popen(bashCommand.split())
        output, error = process.communicate()
        #print(output, error)
