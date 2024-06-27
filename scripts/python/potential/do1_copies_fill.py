import subprocess
import itertools
import os

conf_type = 'gluodynamics'
#conf_type = "su2_suzuki"
#conf_type = 'QCD/140MeV'
#conf_type = "qc2dstag"
theory_type = 'su3'
decomposition_type_arr = ['monopole']
representation = 'fundamental'
operator_type = 'wilson_loop'
gauge_copies = 20
axis = 'on-axis'
smearing = 'smearing'
smearing_param_arr = ['HYP0_alpha=1_1_0.5_APE_alpha=0.6']
additional_parameters_arr = ['steps_0/copies=20']
#additional_parameters_arr = ['/']
beta_arr = ['beta6.0']
# beta_arr = ['/']
mu_arr = ['/']
#mu_arr = ['mu0.05', 'mu0.20', 'mu0.25', 'mu0.30', 'mu0.35', 'mu0.40', 'mu0.45']
#mu_arr = ['mu0.35', 'mu0.40']
#conf_size_arr = ['16^4', '24^4', '32^4']
conf_size_arr = ['16^4']
#conf_size_arr = ['nt4', 'nt6', 'nt8', 'nt10', 'nt12', 'nt14', 'nt16', 'nt18', 'nt20']
iter_arrays = [beta_arr, mu_arr, conf_size_arr,
               additional_parameters_arr, decomposition_type_arr, smearing_param_arr]
for beta, mu, conf_size, additional_parameters, decomposition_type, smearing_param in itertools.product(*iter_arrays):
    log_path = f'/home/clusters/rrcmpi/kudrov/observables_cluster/logs/potential_fill_copies/{representation}/{axis}/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/'\
            f'{decomposition_type}/{smearing}/{additional_parameters}'
    try:
        os.makedirs(log_path)
    except:
        pass
    base_path = '/home/clusters/rrcmpi/kudrov/observables_cluster/result'
    path_output_base = '/home/clusters/rrcmpi/kudrov/observables/data'
    path_params = f'{smearing}/{operator_type}/{representation}/{axis}'\
                    f'/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/{decomposition_type}'\
                    f'/{smearing_param}/{additional_parameters}'
    parameters = f'--base_path {base_path} --path_output_base {path_output_base} --path_params {path_params} --copies {gauge_copies}'
    command_qsub = f'qsub -q long -v'
    command_parameters = f'parameters={parameters}'
    command_script = f'-o {log_path}/{decomposition_type}.o -e {log_path}/{decomposition_type}.e ../../bash/potential/do_copies_fill.sh'
    command = command_qsub.split() + [command_parameters] + command_script.split()
    process = subprocess.Popen(command)
    output, error = process.communicate()
