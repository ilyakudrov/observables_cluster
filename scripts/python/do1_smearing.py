import sys
import json
sys.path.append(os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "..", "..", "lib", "src", "python"))
from iterate_confs import distribute_jobs
import subprocess
import os

L_spat = 16
L_time = 16
#conf_size = "nt16_gov"
#conf_size = "nt8"
conf_size = "16^4"
#conf_size = "48^4"
#conf_type = "su2_suzuki"
conf_type = "gluodynamics"
#conf_type = "QCD/140MeV"
#conf_type = "qc2dstag"
theory_type = "su3"
#wilson_type_array = ["monopoless", "monopole"]
wilson_type_array = ['monopole']
plaket_type = 'original'

calculate_absent = "false"

#additional_parameters = 'T_step=0.001/T_final=0.5/OR_steps=4'
additional_parameters = '/'
#additional_parameters = 'DP_steps_500/copies=3'

APE_enabled = 1
HYP_enabled = 1
#HYP_alpha1 = "0.75"
#HYP_alpha2 = "0.6"
#HYP_alpha3 = "0.3"
HYP_alpha1 = "1"
HYP_alpha2 = "1"
HYP_alpha3 = "0.5"
APE_alpha = "0.5"
APE_steps = "500"
HYP_steps_array = ['0', '1']
calculation_step_APE = 100
calculation_APE_start = 300

wilson_enabled = 1
flux_enabled = 0
save_conf = 0

T_min = 1
T_max = 8
R_min = 1
R_max = 8

number_of_jobs = 100

arch = "rrcmpi"

for wilson_type in wilson_type_array:
    for HYP_steps in HYP_steps_array:
        # for beta in ['/']:
        # for beta in ['beta2.8']:
        for beta in ['beta6.1']:
            # for beta in ['beta2.4']:
            # for mu in ['mu0.00', 'mu0.05', 'mu0.20', 'mu0.25', 'mu0.30', 'mu0.35', 'mu0.45']:
            # for mu in ['mu0.05', 'mu0.45']:
            for mu in ['/']:

                if wilson_type == 'original':
                    f = open(
                        f'/home/clusters/rrcmpi/kudrov/conf/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/parameters.json')
                    data = json.load(f)
                    conf_format_wilson = data['conf_format']
                    bytes_skip_wilson = data['bytes_skip']
                    matrix_type_wilson = data['matrix_type']
                    conf_path_start_wilson = data['conf_path_start']
                    conf_path_end_wilson = data['conf_path_end']
                    padding_wilson = data['padding']
                    conf_name_wilson = data['conf_name']

                    #conf_path_start_wilson = f'/home/clusters/rrcmpi/kudrov/Coulomb_su3/su3/QCD/140MeV/{conf_size}'
                    #conf_name_wilson = 'conf_Coulomb_gaugefixed_'
                else:
                    #conf_format_wilson = 'double'
                    #bytes_skip_wilson = 0
                    #padding_wilson = 4
                    conf_format_wilson = 'double_vitaly'
                    bytes_skip_wilson = 4
                    padding_wilson = 5
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
                    # conf_path_start_wilson = f'/home/clusters/rrcmpi/kudrov/decomposition/confs_decomposed/'\
                    #    f'{wilson_type}/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/{additional_parameters}'
                    #conf_path_end_wilson = '/'
                    #conf_name_wilson = f'conf_{wilson_type}_'

                    #conf_path_start_wilson = '/net/pool-01/vborn/Copy_from_lustre/SU3/su3mag/MAG_U1_decomp_mod'
                    #conf_path_end_wilson = '.LAT'
                    #conf_name_wilson = f'CON_MON_MAG_'

                    #conf_path_start_wilson = '/net/pool-01/vborn/Copy_from_lustre/SU3/su3mag/L16_OFFD-mod'
                    #conf_path_end_wilson = '.lat'
                    #conf_name_wilson = f'MLS_conf.'

                    conf_path_start_wilson = '/net/pool-01/vborn/Copy_from_lustre/SU3/su3mag/MAG_U1_decomp'
                    conf_path_end_wilson = '.LAT'
                    conf_name_wilson = f'CON_MON_MAG_'

                if plaket_type == 'original':
                    f = open(
                        f'/home/clusters/rrcmpi/kudrov/conf/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/parameters.json')
                    data = json.load(f)
                    conf_format_plaket = data['conf_format']
                    bytes_skip_plaket = data['bytes_skip']
                    matrix_type_plaket = data['matrix_type']
                    conf_path_start_plaket = data['conf_path_start']
                    conf_path_end_plaket = data['conf_path_end']
                    padding_plaket = data['padding']
                    conf_name_plaket = data['conf_name']
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

                #chains = {'/': [601, 601]}
                #chains = {'s0': [201, 250]}
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
                        f'{conf_type}/{conf_size}/{beta}/{mu}/{smearing_str}/{additional_parameters}/{job[0]}'
                    # qsub -q mem8gb -l nodes=1:ppn=4
                    # qsub -q long
                    # 4gb for 48^4 monopole
                    # 8gb for 48^4 su2
                    # 8gb for nt6 and bigger
                    # 16gb for nt10 and bigger
                    bashCommand = f'qsub -q long -v conf_path_start_plaket={conf_path_start_plaket1},conf_path_end_plaket={conf_path_end_plaket},'\
                        f'conf_format_plaket={conf_format_plaket},bytes_skip_plaket={bytes_skip_plaket},'\
                        f'conf_path_start_wilson={conf_path_start_wilson1},conf_path_end_wilson={conf_path_end_wilson},'\
                        f'conf_format_wilson={conf_format_wilson},bytes_skip_wilson={bytes_skip_wilson},'\
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
