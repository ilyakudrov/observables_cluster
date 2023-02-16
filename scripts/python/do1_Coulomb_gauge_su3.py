import sys
import json
import itertools
sys.path.append(os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "..", "..", "lib", "src", "python"))
from iterate_confs import distribute_jobs
import subprocess
import os

conf_type = "QCD/140MeV"
theory_type = "su3"

number_of_jobs = 1

beta_arr = ['/']
# beta_arr = ['beta2.5', 'beta2.6']
mu_arr = ['/']
# mu_arr = ['mu0.00', 'mu0.05', 'mu0.20', 'mu0.25', 'mu0.30', 'mu0.35', 'mu0.45']
conf_size_arr = ['nt16']

iter_arrays = [beta_arr, mu_arr, conf_size_arr]
for beta, mu, conf_size in itertools.product(*iter_arrays):

    f = open(
        f'/home/clusters/rrcmpi/kudrov/conf/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/parameters.json')
    data = json.load(f)
    conf_format = data['conf_format']
    bytes_skip = data['bytes_skip']
    L_spat = data['x_size']
    L_time = data['t_size']
    matrix_type = data['matrix_type']
    conf_path_start = data['conf_path_start']
    conf_path_end = data['conf_path_end']
    padding = data['padding']
    conf_name = data['conf_name']

    if conf_format == 'ildg':
        conf_format = 'ILDG'
    elif conf_format == 'double_qc2dstag':
        conf_format = 'QCDSTAG'

    chains = {'/': [661, 661]}
    # chains = {'s0': [201, 250]}
    jobs = distribute_jobs(chains, number_of_jobs)
    #jobs = distribute_jobs(data['chains'], number_of_jobs)

    for job in jobs:

        log_path = f'/home/clusters/rrcmpi/kudrov/observables_cluster/logs/Coulomb_gauge_su3/{conf_type}/{conf_size}/{beta}/{mu}/'\
            f'{job[0]}'
        try:
            os.makedirs(log_path)
        except:
            pass
        output_conf_path = f'/home/clusters/rrcmpi/kudrov/Coulomb_su3/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}'
        # qsub -q mem8gb -l nodes=1:ppn=4
        bashCommand = f'qsub -q kepler -l nodes=1:ppn=8 -v conf_path_start={conf_path_start}/{conf_name},conf_path_end={conf_path_end},padding={padding},conf_format={conf_format},bytes_skip={bytes_skip},'\
            f'output_conf_path={output_conf_path},'\
            f'L_spat={L_spat},L_time={L_time},chain={job[0]},conf_start={job[1]},conf_end={job[2]}'\
            f' -o {log_path}/{job[1]:04}-{job[2]:04}.o -e {log_path}/{job[1]:04}-{job[2]:04}.e ../bash/do_Coulomb_gauge_su3.sh'
        # print(bashCommand)
        process = subprocess.Popen(bashCommand.split())
        output, error = process.communicate()
        # print(output, error)
