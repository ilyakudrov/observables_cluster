import sys
import json
import os
import subprocess
import itertools

sys.path.append(os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "..", "..", "..", "lib", "src", "python"))
from iterate_confs import distribute_jobs

conf_type = "su2_suzuki"
#conf_type = "gluodynamics"
# conf_type = "qc2dstag"
theory_type = "su2"

HYP_enabled = 0
HYP_alpha1 = "1"
HYP_alpha2 = "1"
HYP_alpha3 = "0.5"
APE_alpha = "0.5"
APE_steps = "31"
HYP_steps = 0
calculation_step_APE = 10
calculation_APE_start = 11
N_dir_gevp = 4
copies_required = 1000
mag_steps = 0

#additional_parameters_arr = ['T_step=0.006', 'T_step=0.0125', 'T_step=0.025', 'T_step=0.05', 'T_step=0.1']
# additional_parameters_arr = ['T_step=0.001']
additional_parameters_arr = [f'steps={mag_steps}']

number_of_jobs = 87

arch = "rrcmpi-a"
beta_arr = ['beta2.6']
# beta_arr = ['/']
mu_arr = ['/']
#mu_arr = ['mu0.00', 'mu0.05', 'mu0.20', 'mu0.25', 'mu0.30', 'mu0.35', 'mu0.45']
# mu_arr = ['mu0.15']
conf_size_arr = ['48^4']

iter_arrays = [beta_arr, mu_arr, conf_size_arr,
               additional_parameters_arr]
for beta, mu, conf_size, additional_parameters in itertools.product(*iter_arrays):
    f = open(
        f'/home/clusters/rrcmpi/kudrov/conf/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/parameters_original.json')
    data = json.load(f)
    conf_format = data['conf_format']
    file_precision = data['file_precision']
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
    T_max = L_time//2
    R_min = 1
    R_max = L_spat//2

    if HYP_enabled == 0 or HYP_steps == 0:
        smearing_str = f'HYP0_APE_alpha={APE_alpha}'
    else:
        smearing_str = f'HYP{HYP_steps}_alpha={HYP_alpha1}_{HYP_alpha2}_{HYP_alpha3}_APE_alpha={APE_alpha}'

    #chains = {'/': [1, 10]}
    #chains = {'s0': [201, 201]}
    #jobs = distribute_jobs(chains, number_of_jobs)
    jobs = distribute_jobs(data['chains'], number_of_jobs)

    for job in jobs:
        log_path = f'/home/clusters/rrcmpi/kudrov/observables_cluster/logs/mag_functional_dependence/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/'\
            f'{additional_parameters}/{job[0]}'
        conf_path_start1 = f'{conf_path_start}/{job[0]}/{conf_name}'
        try:
            os.makedirs(log_path)
        except:
            pass
        path_functional = f'/home/clusters/rrcmpi/kudrov/observables_cluster/result/mag_functional_dependence/functional/'\
            f'{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/{additional_parameters}/{job[0]}'
        path_wilson_loops_abelian = f'/home/clusters/rrcmpi/kudrov/observables_cluster/result/mag_functional_dependence/wilson_gevp/'\
            f'{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/{additional_parameters}/abelian/{job[0]}'
        path_wilson_loops_monopole = f'/home/clusters/rrcmpi/kudrov/observables_cluster/result/mag_functional_dependence/wilson_gevp/'\
            f'{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/{additional_parameters}/monopole/{job[0]}'
        path_clusters_unwrapped_abelian = f'/home/clusters/rrcmpi/kudrov/observables_cluster/result/mag_functional_dependence/monpoles/'\
            f'{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/{additional_parameters}/abelian/clusters_unwrapped/{job[0]}'
        path_clusters_unwrapped_monopole = f'/home/clusters/rrcmpi/kudrov/observables_cluster/result/mag_functional_dependence/monpoles/'\
            f'{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/{additional_parameters}/monopole/clusters_unwrapped/{job[0]}'
        path_clusters_unwrapped_monopoless = f'/home/clusters/rrcmpi/kudrov/observables_cluster/result/mag_functional_dependence/monpoles/'\
            f'{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/{additional_parameters}/monopoless/clusters_unwrapped/{job[0]}'
        path_clusters_wrapped_abelian = f'/home/clusters/rrcmpi/kudrov/observables_cluster/result/mag_functional_dependence/monpoles/'\
            f'{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/{additional_parameters}/abelian/clusters_wrapped/{job[0]}'
        path_clusters_wrapped_monopole = f'/home/clusters/rrcmpi/kudrov/observables_cluster/result/mag_functional_dependence/monpoles/'\
            f'{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/{additional_parameters}/monopole/clusters_wrapped/{job[0]}'
        path_clusters_wrapped_monopoless = f'/home/clusters/rrcmpi/kudrov/observables_cluster/result/mag_functional_dependence/monpoles/'\
            f'{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/{additional_parameters}/monopoless/clusters_wrapped/{job[0]}'
        path_windings_abelian = f'/home/clusters/rrcmpi/kudrov/observables_cluster/result/mag_functional_dependence/monpoles/'\
            f'{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/{additional_parameters}/abelian/windings/{job[0]}'
        path_windings_monopole = f'/home/clusters/rrcmpi/kudrov/observables_cluster/result/mag_functional_dependence/monpoles/'\
            f'{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/{additional_parameters}/monopole/windings/{job[0]}'
        path_windings_monopoless = f'/home/clusters/rrcmpi/kudrov/observables_cluster/result/mag_functional_dependence/monpoles/'\
            f'{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/{additional_parameters}/monopoless/windings/{job[0]}'

        path_inverse_laplacian = f'/home/clusters/rrcmpi/kudrov/inverse_laplacian/inverse_laplacian_{L_spat}x{L_time}'
        # qsub -q mem8gb -l nodes=1:ppn=4
        bashCommand = f'qsub -q mem16gb -l nodes=1:ppn=8 -v conf_path_start={conf_path_start1},conf_path_end={conf_path_end},padding={padding},conf_format={conf_format},bytes_skip={bytes_skip},'\
            f'path_inverse_laplacian={path_inverse_laplacian},N_dir_gevp={N_dir_gevp},HYP_alpha1={HYP_alpha1},HYP_alpha2={HYP_alpha2},HYP_alpha3={HYP_alpha3},copies_required={copies_required},'\
            f'path_functional={path_functional},path_wilson_loops_abelian={path_wilson_loops_abelian},path_wilson_loops_monopole={path_wilson_loops_monopole},'\
            f'path_clusters_unwrapped_abelian={path_clusters_unwrapped_abelian},path_clusters_unwrapped_monopole={path_clusters_unwrapped_monopole},path_clusters_unwrapped_monopoless={path_clusters_unwrapped_monopoless},'\
            f'path_clusters_wrapped_abelian={path_clusters_wrapped_abelian},path_clusters_wrapped_monopole={path_clusters_wrapped_monopole},path_clusters_wrapped_monopoless={path_clusters_wrapped_monopoless},'\
            f'path_windings_abelian={path_windings_abelian},path_windings_monopole={path_windings_monopole},path_windings_monopoless={path_windings_monopoless},'\
            f'file_precision={file_precision},L_spat={L_spat},L_time={L_time},APE_alpha={APE_alpha},HYP_enabled={HYP_enabled},mag_steps={mag_steps},'\
            f'APE_steps={APE_steps},HYP_steps={HYP_steps},calculation_step_APE={calculation_step_APE},calculation_APE_start={calculation_APE_start},'\
            f'chain={job[0]},conf_start={job[1]},conf_end={job[2]},arch={arch}'\
            f' -o {log_path}/{job[1]:04}-{job[2]:04}.o -e {log_path}/{job[1]:04}-{job[2]:04}.e ../../bash/decomposition/do_functional_dependence_su2.sh'
        # print(bashCommand)
        process = subprocess.Popen(bashCommand.split())
        output, error = process.communicate()
        # print(output, error)
