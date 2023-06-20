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
#wilson_type_array = ["monopoless", "photon",
#                     "offdiagonal", "monopole", "abelian"]
#wilson_type_array = ['original']
wilson_type_array = ['abelian']
#wilson_type_array = ['monopoless']
#wilson_type_array = ["", "offdiagonal"]
plaket_type = 'original'

calculate_absent = "false"

APE_enabled = 1
HYP_enabled = 1
#HYP_alpha1 = "0.75"
#HYP_alpha2 = "0.6"
#HYP_alpha3 = "0.3"
HYP_alpha1 = "1"
HYP_alpha2 = "1"
HYP_alpha3 = "0.5"
APE_alpha = "0.5"
APE_steps = "200"
HYP_steps_array = ['0']
calculation_step_APE = 100
calculation_APE_start = 700

wilson_enabled = 0
flux_enabled = 0
save_conf = 1

number_of_jobs = 100

arch = "rrcmpi-a"

beta_arr = ['beta6.3']
#beta_arr = ['/']
#mu_arr = ['mu0.00', 'mu0.20', 'mu0.30', 'mu0.35', 'mu0.40', 'mu0.45']
#mu_arr = ['mu0.40']
mu_arr = ['/']
conf_size_arr = ['36^4']
#conf_size_arr = ['nt4', 'nt6', 'nt8', 'nt10', 'nt12', 'nt14']
#conf_size_arr = ['nt16', 'nt18']
#additional_parameters_arr = ['steps_25/copies=4']
#additional_parameters_arr = ['T_step=0.0002']
#additional_parameters_arr = ['steps_2000/copies=1', 'steps_330/copies=1']
#additional_parameters_arr = ['steps_25/copies=4']
additional_parameters_arr = ['steps_25/copies=4', 'steps_50/copies=4', 
                             'steps_100/copies=4', 'steps_200/copies=4', 
                             'steps_500/copies=4', 'steps_1000/copies=4', 'steps_2000/copies=4']
#additional_parameters_arr = ['/']

iter_arrays = [beta_arr, mu_arr, conf_size_arr,
               additional_parameters_arr, wilson_type_array, HYP_steps_array]
for beta, mu, conf_size, additional_parameters, wilson_type, HYP_steps in itertools.product(*iter_arrays):
    if True:
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
        R_max = L_spat

        #print("path start", conf_path_start_wilson)

        if wilson_type != 'original':
        	conf_path_start_wilson = conf_path_start_wilson + \
            		f'/{additional_parameters}'
        #conf_path_start_wilson = f'/home/clusters/rrcmpi/kudrov/Coulomb_su3/su3/QCD/140MeV/{conf_size}'
        #conf_name_wilson = 'conf_Coulomb_gaugefixed_'
    else:
        conf_format_wilson = 'double'
        bytes_skip_wilson = 0
        padding_wilson = 4
        #conf_format_wilson = 'double_vitaly'
        #bytes_skip_wilson = 4
        #padding_wilson = 5
        if wilson_type == 'monopoless':
            if theory_type == 'su2':
                matrix_type_wilson = 'su2'
            elif theory_type == 'su3':
                matrix_type_wilson = 'su3'
            else:
                print('wrong theory type')
        elif wilson_type == 'monopole':
            if theory_type == 'su2':
                matrix_type_wilson = 'abelian'
            elif theory_type == 'su3':
                matrix_type_wilson = 'su3_abelian'
            else:
                print('wrong theory type')
        conf_path_start_wilson = f'/home/clusters/rrcmpi/kudrov/decomposition/confs_decomposed/'\
            f'{wilson_type}/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/{additional_parameters}'
        conf_path_end_wilson = '/'
        conf_name_wilson = f'conf_{wilson_type}_'

        #conf_path_start_wilson = '/net/pool-01/vborn/Copy_from_lustre/SU3/su3mag/MAG_U1_decomp_mod'
        #conf_path_end_wilson = '.LAT'
        #conf_name_wilson = f'CON_MON_MAG_'

        #conf_path_start_wilson = '/net/pool-01/vborn/Copy_from_lustre/SU3/su3mag/L16_OFFD-mod'
        #conf_path_end_wilson = '.lat'
        #conf_name_wilson = f'MLS_conf.'

        #conf_path_start_wilson = '/net/pool-01/vborn/Copy_from_lustre/SU3/su3mag/MAG_U1_decomp'
        #conf_path_end_wilson = '.LAT'
        #conf_name_wilson = f'CON_MON_MAG_'

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

    #chains = {'/': [1, 2]}
    #chains = {'s0': [201, 201]}
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
        path_conf_wilson_loop = f'/home/clusters/rrcmpi/kudrov/observables_cluster/result/smearing/wilson_loop/{theory_type}/'\
            f'{conf_type}/{conf_size}/{beta}/{mu}/{wilson_type}/{smearing_str}/{additional_parameters}/{job[0]}'
        path_conf_flux_tube = f'/home/clusters/rrcmpi/kudrov/observables_cluster/result/smearing/flux_tube/{theory_type}/'\
            f'{conf_type}/{conf_size}/{beta}/{mu}/{wilson_type}_{plaket_type}/{smearing_str}/{additional_parameters}/{job[0]}'
        conf_path_output = f'/home/clusters/rrcmpi/kudrov/smearing/{theory_type}/'\
            f'{conf_type}/{conf_size}/{beta}/{mu}/{wilson_type}/{smearing_str}/{additional_parameters}/{job[0]}'
        # qsub -q mem8gb -l nodes=1:ppn=4
        # qsub -q long
        # 4gb for su3 gluo 36^4
        # 4gb for 48^4 monopole
        # 8gb for 48^4 su2
        # 8gb for nt6 and bigger
        # 16gb for nt10 and bigger
        bashCommand = f'qsub -q mem8gb -l nodes=1:ppn=4 -v conf_path_start_plaket={conf_path_start_plaket1},conf_path_end_plaket={conf_path_end_plaket},'\
            f'conf_format_plaket={conf_format_plaket},bytes_skip_plaket={bytes_skip_plaket},convert_wilson={convert_wilson},'\
            f'conf_path_start_wilson={conf_path_start_wilson1},conf_path_end_wilson={conf_path_end_wilson},'\
            f'conf_format_wilson={conf_format_wilson},bytes_skip_wilson={bytes_skip_wilson},convert_plaket={convert_plaket},'\
            f'padding_wilson={padding_wilson},padding_plaket={padding_plaket},calculate_absent={calculate_absent},save_conf={save_conf},conf_path_output={conf_path_output},'\
            f'HYP_alpha1={HYP_alpha1},HYP_alpha2={HYP_alpha2},HYP_alpha3={HYP_alpha3},'\
            f'APE_alpha={APE_alpha},APE_enabled={APE_enabled},HYP_enabled={HYP_enabled},'\
            f'APE_steps={APE_steps},HYP_steps={HYP_steps},calculation_step_APE={calculation_step_APE},calculation_APE_start={calculation_APE_start},'\
            f'path_wilson={path_conf_wilson_loop},path_flux={path_conf_flux_tube},wilson_enabled={wilson_enabled},flux_enabled={flux_enabled},'\
            f'L_spat={L_spat},L_time={L_time},T_min={T_min},T_max={T_max},R_min={R_min},R_max={R_max},'\
            f'chain={job[0]},conf_start={job[1]},conf_end={job[2]},arch={arch},matrix_type_plaket={matrix_type_plaket},matrix_type_wilson={matrix_type_wilson}'\
            f' -o {log_path}/{job[1]:04}-{job[2]:04}.o -e {log_path}/{job[1]:04}-{job[2]:04}.e ../bash/do_smearing.sh'
        # print(bashCommand)
        process = subprocess.Popen(bashCommand.split())
        output, error = process.communicate()
        # print(output, error)
