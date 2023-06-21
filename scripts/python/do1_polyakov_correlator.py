import sys
import json
import itertools
import subprocess
import os

sys.path.append(os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "..", "..", "lib", "src", "python"))
from iterate_confs import distribute_jobs

#conf_type = "su2_suzuki"
conf_type = "gluodynamics"
#conf_type = "QCD/140MeV"
#conf_type = "qc2dstag"
#conf_size = "40^4"
# conf_size = "48^4"
theory_type = "su3"

decomposition_type_arr = ["original"]
#decomposition_type_arr = ["abelian"]
#decomposition_type_arr = ["monopoless", "monopole", "photon", "offdiagonal", "abelian"]

calculate_absent = "false"

#additional_parameters_arr = ['steps_25/copies=4', 'steps_50/copies=4',
#                             'steps_100/copies=4', 'steps_200/copies=4',
#                             'steps_1000/copies=4', 'steps_2000/copies=4']
#additional_parameters_arr = ['steps_500/copies=3']
#additional_parameters_arr = ['steps_500/copies=3/compensate_1']
#additional_parameters_arr = ['T_step=0.0002']
#additional_parameters_arr = ['T_step=0.0001', 'T_step=0.0002', 'T_step=0.0004', 'T_step=0.0008', 'T_step=0.0016', 'T_step=0.0032']
# additional_parameters_arr = ['T_step=0.0001', 'T_step=0.0002', 'T_step=0.0004', 'T_step=0.0008',
#                             'T_step=0.001', 'T_step=0.002', 'T_step=0.004', 'T_step=0.008', 'T_step=5e-05']
# additional_parameters_arr = ['steps_500/copies=3/compensate_1', 'steps_1000/copies=3/compensate_1',
#                             'steps_2000/copies=3/compensate_1', 'steps_4000/copies=3/compensate_1']
#additional_parameters_arr = ['steps_1000/copies=3/compensate_1',
#                             'steps_2000/copies=3/compensate_1', 'steps_4000/copies=3/compensate_1']
#additional_parameters_arr = ['steps_330/copies=1', 'steps_2000/copies=1']
additional_parameters_arr = ['/']

#correlator_type = 'color_average'
correlator_type = 'singlet'

D_max = 32

# smearing_arr = ['HYP0_APE_alpha=0.5',
#                'HYP1_alpha=1_1_0.5_APE_alpha=0.5', 'HYP2_alpha=1_1_0.5_APE_alpha=0.5']
# smearing_arr = ['HYP0_alpha=1_1_0.5_APE_alpha=0.5', 'HYP1_alpha=1_1_0.5_APE_alpha=0.5']
#smearing_arr = ['HYP1_alpha=1_1_0.5_APE_alpha=0.5']
smearing_arr = ['unsmeared']

number_of_jobs = 200

arch = "rrcmpi-a"
# beta_arr = ['beta6.2']
beta_arr = ['/']
mu_arr = ['/']
#mu_arr = ['mu0.05', 'mu0.20', 'mu0.25', 'mu0.30', 'mu0.35', 'mu0.40', 'mu0.45']
#mu_arr = ['mu0.00']
# conf_size_arr = ['32^3x64']
conf_size_arr = ['nt4', 'nt6', 'nt8', 'nt10', 'nt12', 'nt14']

arch = "rrcmpi-a"

iter_arrays = [beta_arr, mu_arr, conf_size_arr,
               additional_parameters_arr, decomposition_type_arr, smearing_arr]
for beta, mu, conf_size, additional_parameters, decomposition_type, smearing in itertools.product(*iter_arrays):
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


    conf_path_start = f'/home/clusters/rrcmpi/kudrov/smearing/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/{decomposition_type}/{smearing}/{additional_parameters}'
    conf_name = 'smeared_'
    conf_path_end = '/'
    conf_format = 'double'
    padding = 4
    bytes_skip = 0
    convert = 0

    #chains = {'/': [601, 601]}
    #chains = {'s0': [201, 250]}
    #jobs = distribute_jobs(chains, number_of_jobs)
    jobs = distribute_jobs(data['chains'], number_of_jobs)
    for job in jobs:
        log_path = f'/home/clusters/rrcmpi/kudrov/observables_cluster/logs/polyakov_loop_correlator/{correlator_type}/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/'\
            f'{smearing}/{additional_parameters}/{job[0]}'
        conf_path_start1 = f'{conf_path_start}/{job[0]}/{conf_name}'
        try:
            os.makedirs(log_path)
        except:
            pass
        path_output_correlator = f'/home/clusters/rrcmpi/kudrov/observables_cluster/result/polyakov_loop_correlator/{correlator_type}/{theory_type}/'\
            f'{conf_type}/{conf_size}/{beta}/{mu}/{smearing}/{additional_parameters}/{job[0]}'
        # qsub -q mem8gb -l nodes=1:ppn=4
        # qsub -q long
        # 4gb since nt8
        # 8gb since nt16
        bashCommand = f'qsub -q mem4gb -l nodes=1:ppn=2 -v conf_path_start={conf_path_start1},conf_path_end={conf_path_end},'\
            f'conf_format={conf_format},bytes_skip={bytes_skip},path_output_correlator={path_output_correlator},'\
            f'padding={padding},calculate_absent={calculate_absent},correlator_type={correlator_type},'\
            f'L_spat={L_spat},L_time={L_time},D_max={D_max},matrix_type={matrix_type},'\
            f'chain={job[0]},conf_start={job[1]},conf_end={job[2]},arch={arch},'\
            f' -o {log_path}/{job[1]:04}-{job[2]:04}.o -e {log_path}/{job[1]:04}-{job[2]:04}.e ../bash/do_polyakov_correlator.sh'
        # print(bashCommand)
        process = subprocess.Popen(bashCommand.split())
        output, error = process.communicate()
        # print(output, error)
