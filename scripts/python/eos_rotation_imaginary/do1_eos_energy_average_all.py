import itertools
import sys
import subprocess
import os
import pandas as pd

def get_dir_names(path: str) -> list[str]:
    """Get names of subdirectories in path.

    Args:
        path: path where to find subdirectories

    Returns: list of names of the subdirectories
    """
    directories = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        directories.extend(dirnames)
        break
    return directories

def queue_job(df, spec_additional_path, bin_test):
    df = df.reset_index()
    df['lattice_dir'] = df['lattice_dir'].apply(lambda x: x[:x.rfind('/')])
    base_paths = ' '.join(df['lattice_dir'])
    lattice_sizes = ' '.join(df['lattice_size'])
    velocities = ' '.join(df['velocity'])
    boundaries = ' '.join(df['boundary'])
    betas = ' '.join(df['beta'])
    start = df.loc[df.index[0], 'lattice_size'] + '_' + df.loc[df.index[0], 'boundary'] + '_' + df.loc[df.index[0], 'velocity'] + '_' + df.loc[df.index[0], 'beta']
    end = df.loc[df.index[-1], 'lattice_size'] + '_' + df.loc[df.index[-1], 'boundary'] + '_' + df.loc[df.index[-1], 'velocity'] + '_' + df.loc[df.index[-1], 'beta']
    log_path = f'/home/clusters/rrcmpi/kudrov/observables_cluster/logs/eos_energy_average/common_distribution'
    try:
        os.makedirs(log_path)
    except:
        pass
    add_parameters = f'--spec_additional_path {spec_additional_path}'
    if bin_test:
        add_parameters += '--bin_test'
    command_qsub = f'qsub -q mem8gb -l nodes=1:ppn=4 -v'
    command_parameters = f'base_paths={base_paths},lattice_sizes={lattice_sizes},boundaries={boundaries},velocities={velocities},betas={betas},add_parameters={add_parameters}'
    command_script = f'-o {log_path}/{start}-{end}.o -e {log_path}/{start}-{end}.e ../../bash/eos_rotation_imaginary/do_eos_energy_average_all.sh'
    command = command_qsub.split() + [command_parameters] + command_script.split()
    print(command)
    process = subprocess.Popen(command)
    output, error = process.communicate()


job_number = 1000
data_summary_path = '/home/clusters/rrcmpi/kudrov/observables/result/eos_rotation_imaginary/data_summary.csv'
df_data = pd.read_csv(data_summary_path, dtype=str)
df_data['beta1'] = pd.to_numeric(df_data['beta'], errors='coerce')
df_data = df_data[~df_data['beta1'].isnull()]
df_data = df_data.drop(labels='beta1', axis=1)
df_data = df_data[df_data['observation_number'] != '0']
data_size = len(df_data.index)
bin_size = (data_size + job_number - 1) // job_number
bins = [i//bin_size for i in range(data_size)]
df_data['bins'] = bins
spec_additional_path = '/home/clusters/rrcmpi/kudrov/observables/data/eos_rotation_imaginary'
bin_test = False
df_data.groupby('bins').apply(queue_job, spec_additional_path, bin_test)
