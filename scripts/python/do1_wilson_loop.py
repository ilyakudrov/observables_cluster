import sys
import json
import subprocess
import os

sys.path.append(os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "..", "..", "lib", "src", "python"))
from iterate_confs import distribute_jobs

L_spat = 32
time_sizes = [32]
#conf_size = "nt20_gov"
#conf_size = "40^4"
conf_size = "32^4"
#conf_type = "su2_suzuki"
conf_type = "gluodynamics"
#conf_type = "QCD/140MeV"
#conf_type = "qc2dstag"
theory_type = "su3"
#decomposition_type_array = ["original"]
decomposition_type_array = ["abelian"]
#decomposition_type_array = ["monopoless", "monopole", "photon", "offdiagonal", "original", "abelian"]
#decomposition_type_array = ["monopole", "photon"]
#decomposition_type_array = ["monopole", "monopoless", "offdiagonal", "photon"]

calculate_absent = "false"

compensate = 1
# additional_parameters = 'T_step=0.001/T_final=0.5/OR_steps=4'
#additional_parameters = '/'
additional_parameters = 'steps_500/copies=3'
#additional_parameters = f'steps_500/copies=3/compensate_{compensate}'
#additional_parameters = f'T_step=0.0001'

axis = 'on-axis'

# smearing_arr = ['HYP0_APE_alpha=0.5',
#                'HYP1_alpha=1_1_0.5_APE_alpha=0.5', 'HYP2_alpha=1_1_0.5_APE_alpha=0.5']
#smearing_arr = ['HYP0_alpha=1_1_0.5_APE_alpha=0.5', 'HYP1_alpha=1_1_0.5_APE_alpha=0.5']
smearing_arr = ['HYP0_alpha=1_1_0.5_APE_alpha=0.5']
#smearing_arr = ['unsmeared']

number_of_jobs = 200

arch = "rrcmpi-a"

for T in time_sizes:
    L_time = T
    #conf_size = f"nt{T}"
    #conf_size = f"nt{T}_gov"
    conf_size = f"{T}^4"
    T_min = 1
    T_max = T // 2
    R_min = 1
    R_max = L_spat // 2
    for smearing in smearing_arr:
        for decomposition_type in decomposition_type_array:
            for beta in ['beta6.2']:
            #for beta in ['/']:
                # for beta in ['beta2.8']:
                # for beta in ['beta6.3']:
                # for beta in ['beta2.4']:
                #for mu in ['mu0.00', 'mu0.05', 'mu0.20', 'mu0.25', 'mu0.30', 'mu0.35', 'mu0.45']:
                #for mu in ['mu0.45']:
                for mu in ['/']:
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

                    #conf_path_start = conf_path_start + f'/{additional_parameters}'
                    
                    conf_path_start = f'/home/clusters/rrcmpi/kudrov/smearing/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/{decomposition_type}/{smearing}/{additional_parameters}'
                    conf_name = 'smeared_'
                    conf_path_end = '/'
                    conf_format = 'double'
                    padding = 4
                    bytes_skip = 0
                    convert = 0

                    #chains = {'/': [1, 200]}
                    #chains = {'s0': [201, 250]}
                    #jobs = distribute_jobs(chains, number_of_jobs)
                    jobs = distribute_jobs(data['chains'], number_of_jobs)
                    for job in jobs:
                        # log_path = f'/home/clusters/rrcmpi/kudrov/observables_cluster/logs/smearing/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/'\
                        #     f'T_step={T_step}/T_final={T_final}/OR_steps={OR_steps}/{smearing_str}/{job[0]}'
                        log_path = f'/home/clusters/rrcmpi/kudrov/observables_cluster/logs/wilson_loop/{axis}/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/'\
                            f'{decomposition_type}/{smearing}/{additional_parameters}/{job[0]}'
                        conf_path_start1 = f'{conf_path_start}/{job[0]}/{conf_name}'
                        try:
                            os.makedirs(log_path)
                        except:
                            pass
                        path_wilson = f'/home/clusters/rrcmpi/kudrov/observables_cluster/result/wilson_loop/{axis}/{theory_type}/'\
                            f'{conf_type}/{conf_size}/{beta}/{mu}/{decomposition_type}/{smearing}/{additional_parameters}/{job[0]}'
                        # qsub -q mem8gb -l nodes=1:ppn=4
                        # qsub -q long
                        # 4gb for 48^4 monopole
                        # 8gb for 48^4 su2
                        # 8gb for nt6 and bigger
                        # 16gb for nt10 and bigger
                        bashCommand = f'qsub -q mem4gb -l nodes=1:ppn=2 -v conf_path_start={conf_path_start1},conf_path_end={conf_path_end},'\
                            f'conf_format={conf_format},bytes_skip={bytes_skip},path_wilson={path_wilson},convert={convert},'\
                            f'padding={padding},calculate_absent={calculate_absent},'\
                            f'L_spat={L_spat},L_time={L_time},T_min={T_min},T_max={T_max},R_min={R_min},R_max={R_max},'\
                            f'chain={job[0]},conf_start={job[1]},conf_end={job[2]},arch={arch},matrix_type={matrix_type}'\
                            f' -o {log_path}/{job[1]:04}-{job[2]:04}.o -e {log_path}/{job[1]:04}-{job[2]:04}.e ../bash/do_wilson_loop.sh'
                        # print(bashCommand)
                        process = subprocess.Popen(bashCommand.split())
                        output, error = process.communicate()
                        # print(output, error)
