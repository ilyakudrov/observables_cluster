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
wilson_type_array = ['monopole']
#wilson_type_array = ['abelian']
#wilson_type_array = ['monopoless', 'monopole', 'abelian', 'photon', 'offdiagonal']
#wilson_type_array = ['monopoless', 'offdiagonal']
#wilson_type_array = ['abelian']
#wilson_type_array = ['mag', 'mag_Landau']
#wilson_type_array = ['offdiagonal']
#wilson_type_array = ["photon", "offdiagonal"]
plaket_type = 'original'

#calculate_absent = "true"
calculate_absent = 0
gauge_copies = 20

APE_enabled = 1
HYP_enabled = 1
#HYP_alpha1 = "0.75"
#HYP_alpha2 = "0.6"
#HYP_alpha3 = "0.3"
HYP_alpha1 = "1"
HYP_alpha2 = "1"
HYP_alpha3 = "0.5"
APE_alpha = "0.6"
APE_steps = "151"
#HYP_steps_array = ['1', '3']
HYP_steps_array = ['0']
calculation_step_APE = 10
calculation_APE_start = 1
calculation_step_HYP = 1
calculation_HYP_start = 1

wilson_enabled = 1
flux_enabled = 0
polyakov_correlator_enabled = 0
polyakov_correlator_type = 'singlet'
# polyakov_correlator_type = 'color_average'
save_conf = 0

number_of_jobs = 600

arch = "rrcmpi-a"

#beta_arr = ['beta2.6', 'beta2.779']
beta_arr = ['beta6.0']
#beta_arr = ['/']
#mu_arr = ['mu0.00', 'mu0.20', 'mu0.30', 'mu0.35', 'mu0.40', 'mu0.45']
#mu_arr = ['mu0.15']
mu_arr = ['/']
#conf_size_arr = ['40^4']
#conf_size_arr = ['32^3x8', '32^3x16', '32^3x20', '32^3x24', '32^3x28', '32^3x32']
conf_size_arr = ['16^4', '32^4']
#conf_size_arr = ['32^3x64']
#conf_size_arr = ['nt4', 'nt6', 'nt8', 'nt10', 'nt12', 'nt14', 'nt16', 'nt18', 'nt20']
#conf_size_arr = ['nt4', 'nt6', 'nt8', 'nt10', 'nt12', 'nt14']
#conf_size_arr = ['nt16', 'nt18', 'nt20']
#conf_size_arr = ['nt20']
#additional_parameters_arr = ['T_step=0.001']
#additional_parameters_arr = ['T_step=0.0001', 'T_step=0.0002', 'T_step=0.0004' 'T_step=0.0005',
#				'T_step=0.0008', 'T_step=0.001', 'T_step=0.0015', 'T_step=0.002',
#				'T_step=0.004', 'T_step=0.006', 'T_step=0.008', 'T_step=0.01', 'T_step=0.0125',
#				'T_step=0.025', 'T_step=0.05', 'T_step=0.1', 'T_step=5e-05']
#additional_parameters_arr = ['T_step=0.0001', 'T_step=0.006', 'T_step=0.001', 'T_step=0.0125',
#				'T_step=0.025', 'T_step=0.05', 'T_step=0.1']
#additional_parameters_arr = ['T_step=0.0001', 'T_step=0.0006', 'T_step=0.001', 'T_step=0.00125',
#                               'T_step=0.0025', 'T_step=0.00375', 'T_step=0.00625', 'T_step=0.01']
#additional_parameters_arr = ['T_step=0.0001', 'T_step=0.0004', 'T_step=0.0008', 'T_step=0.0015', 'T_step=0.004',
#				'T_step=0.008', 'T_step=0.0125', 'T_step=0.05', 'T_step=5e-05',
#				'T_step=0.0002', 'T_step=0.0005', 'T_step=0.001', 'T_step=0.002',
#				'T_step=0.006', 'T_step=0.01', 'T_step=0.025', 'T_step=0.1']
additional_parameters_arr = ['steps_0/copies=20']
#additional_parameters_arr = ['steps_0/copies=20', 'steps_100/copies=20/0.01', 'steps_4000/copies=20/0.01']
#additional_parameters_arr = ['steps_25/copies=4', 'steps_100/copies=2', 'steps_100/copies=1',
#                             'steps_50/copies=4', 'steps_50/copies=2',
#                             'steps_100/copies=4', 'steps_200/copies=4',
#                             'steps_500/copies=4', 'steps_0/copies=1',
#                             'steps_2/copies=1', 'steps_10/copies=1',
#                             'steps_1000/copies=4', 'steps_2000/copies=4']
#additional_parameters_arr = ['/']

iter_arrays = [beta_arr, mu_arr, conf_size_arr,
               additional_parameters_arr, wilson_type_array, HYP_steps_array]
for beta, mu, conf_size, additional_parameters, wilson_type, HYP_steps in itertools.product(*iter_arrays):
    f = open(
        f'/home/clusters/rrcmpi/kudrov/conf/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/parameters_{wilson_type}.json')
    data = json.load(f)
    conf_format_wilson = data['conf_format']
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
    T_max = L_time
    R_min = 1
    R_max = L_spat // 2
    polyakov_correlator_D = L_spat/2-1
    if wilson_type != 'original':
        conf_path_start_wilson = conf_path_start_wilson + \
            f'/{additional_parameters}'

    if plaket_type == 'original':
        f = open(
            f'/home/clusters/rrcmpi/kudrov/conf/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/parameters_{plaket_type}.json')
        data = json.load(f)
        conf_format_plaket = data['conf_format']
        bytes_skip_plaket = data['bytes_skip']
        matrix_type_plaket = data['matrix_type']
        conf_path_start_plaket = data['conf_path_start']
        conf_path_end_plaket = data['conf_path_end']
        padding_plaket = data['padding']
        conf_name_plaket = data['conf_name']
        convert_plaket = data['convert']
    else:
        conf_format_plaket = 'double'
        bytes_skip_plaket = 0
        if plaket_type == 'monopoless':
            if theory_type == 'su2':
                matrix_type_plaket = 'su2'
            elif theory_type == 'su3':
                matrix_type_wilson = 'su3'
            else:
                print('wrong theory type')
        elif plaket_type == 'monopole':
            if theory_type == 'su2':
                matrix_type_plaket = 'abelian'
            elif theory_type == 'su3':
                matrix_type_wilson = 'su3_abelian'
            else:
                print('wrong theory type')
        conf_path_start_plaket = f'/home/clusters/rrcmpi/kudrov/decomposition/confs_decomposed/'\
            f'{wilson_type}/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/{additional_parameters}'
        conf_path_end_plaket = '/'
        padding_plaket = 4
        conf_name_plaket = f'conf_{plaket_type}_'

    if HYP_enabled == 0:
        smearing_str = f'HYP0_APE_alpha={APE_alpha}'
    else:
        smearing_str = f'HYP{HYP_steps}_alpha={HYP_alpha1}_{HYP_alpha2}_{HYP_alpha3}_APE_alpha={APE_alpha}'

    if APE_enabled == 0:
        smearing_str = f'HYP{HYP_steps}_alpha={HYP_alpha1}_{HYP_alpha2}_{HYP_alpha3}'

    #chains = {'/': [1001, 1001]}
    #chains = {'s5': [1, 450], 's6': [1, 450]}
    #jobs = distribute_jobs(chains, number_of_jobs)
    jobs = distribute_jobs(data['chains'], number_of_jobs)

    for job in jobs:

        # log_path = f'/home/clusters/rrcmpi/kudrov/observables_cluster/logs/smearing/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/'\
        #     f'T_step={T_step}/T_final={T_final}/OR_steps={OR_steps}/{smearing_str}/{job[0]}'
        log_path = f'/home/clusters/rrcmpi/kudrov/observables_cluster/logs/smearing/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/'\
            f'{wilson_type}_{plaket_type}/{smearing_str}/{additional_parameters}/{job[0]}'
        conf_path_start_wilson1 = f'{conf_path_start_wilson}/{job[0]}/{conf_name_wilson}'
        conf_path_start_plaket1 = f'{conf_path_start_plaket}/{job[0]}/{conf_name_plaket}'
        try:
            os.makedirs(log_path)
        except:
            pass
        path_wilson_loop = f'/home/clusters/rrcmpi/kudrov/observables_cluster/result/smearing/wilson_loop/fundamental/on-axis/{theory_type}/'\
            f'{conf_type}/{conf_size}/{beta}/{mu}/{wilson_type}/{smearing_str}/{additional_parameters}/{job[0]}'
        path_flux_tube = f'/home/clusters/rrcmpi/kudrov/observables_cluster/result/smearing/flux_tube/{theory_type}/'\
            f'{conf_type}/{conf_size}/{beta}/{mu}/{wilson_type}_{plaket_type}/{smearing_str}/{additional_parameters}/{job[0]}'
        path_polyakov_correlator = f'/home/clusters/rrcmpi/kudrov/observables_cluster/result/smearing/polyakov_correlator/{theory_type}/'\
            f'{conf_type}/{conf_size}/{beta}/{mu}/{wilson_type}_{plaket_type}/{smearing_str}/{additional_parameters}/{polyakov_correlator_type}/{job[0]}'
        conf_path_output = f'/home/clusters/rrcmpi/kudrov/smearing/{theory_type}/'\
            f'{conf_type}/{conf_size}/{beta}/{mu}/{wilson_type}/{smearing_str}/{additional_parameters}/{job[0]}'
        # qsub -q mem8gb -l nodes=1:ppn=4
        # qsub -q long
        # 4gb for su3 gluo 36^4
        # 4gb for 48^4 monopole
        # 8gb for 48^4 su2
        # 8gb for nt6 and bigger
        # 16gb for nt10 and bigger
        bashCommand = f'qsub -q mem16gb -l nodes=1:ppn=8 -v conf_path_start_plaket={conf_path_start_plaket1},conf_path_end_plaket={conf_path_end_plaket},'\
            f'conf_format_plaket={conf_format_plaket},bytes_skip_plaket={bytes_skip_plaket},convert_wilson={convert_wilson},'\
            f'conf_path_start_wilson={conf_path_start_wilson1},conf_path_end_wilson={conf_path_end_wilson},'\
            f'conf_format_wilson={conf_format_wilson},bytes_skip_wilson={bytes_skip_wilson},convert_plaket={convert_plaket},'\
            f'padding_wilson={padding_wilson},padding_plaket={padding_plaket},calculate_absent={calculate_absent},save_conf={save_conf},conf_path_output={conf_path_output},'\
            f'HYP_alpha1={HYP_alpha1},HYP_alpha2={HYP_alpha2},HYP_alpha3={HYP_alpha3},'\
            f'APE_alpha={APE_alpha},APE_enabled={APE_enabled},HYP_enabled={HYP_enabled},'\
            f'APE_steps={APE_steps},HYP_steps={HYP_steps},calculation_step_APE={calculation_step_APE},calculation_APE_start={calculation_APE_start},'\
            f'calculation_step_HYP={calculation_step_HYP},calculation_HYP_start={calculation_HYP_start},polyakov_correlator_D={polyakov_correlator_D},'\
            f'path_wilson={path_wilson_loop},path_flux={path_flux_tube},path_polyakov_correlator={path_polyakov_correlator},polyakov_correlator_type={polyakov_correlator_type},'\
            f'wilson_enabled={wilson_enabled},flux_enabled={flux_enabled},polyakov_correlator_enabled={polyakov_correlator_enabled},'\
            f'L_spat={L_spat},L_time={L_time},T_min={T_min},T_max={T_max},R_min={R_min},R_max={R_max},gauge_copies={gauge_copies},'\
            f'chain={job[0]},conf_start={job[1]},conf_end={job[2]},arch={arch},matrix_type_plaket={matrix_type_plaket},matrix_type_wilson={matrix_type_wilson}'\
            f' -o {log_path}/{job[1]:04}-{job[2]:04}.o -e {log_path}/{job[1]:04}-{job[2]:04}.e ../bash/do_smearing.sh'
        # print(bashCommand)
        process = subprocess.Popen(bashCommand.split())
        output, error = process.communicate()
        # print(output, error)
