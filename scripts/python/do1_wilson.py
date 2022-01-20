import sys
import json
sys.path.append('/home/clusters/rrcmpi/kudrov/scripts/python')
from iterate_confs import *
import subprocess
import os

conf_size = "24^4"
#conf_size = "40^4"
conf_type = "su2_suzuki"
#conf_type = "qc2dstag"
bites_skip = 4

number_of_jobs = 50
axis = 'on-axis'

calculate_absent = 'false'

monopole = "/"
#smearing = f'HYP{HYP_steps}_alpha={HYP_alpha1}_{HYP_alpha2}_{HYP_alpha3}_APE{APE_steps}_alpha={APE_alpha}'

for mu in ["0.00"]:
	for beta in [4, 5, 6]:
		#f = open(f'/home/clusters/rrcmpi/kudrov/conf/{conf_type}/{conf_size}/mu{mu}/parameters.json')
		#data = json.load(f)

		if conf_type == "su2_suzuki":
			matrix_type="su2"
			conf_format="double_fortran"
			bites_skip = 8
			chains = {'/': [1, 100]}
			L_spat=24
			L_time=24
			T_min=1
			#T_max=2
			T_max=12
			R_min="0.9"
			#R_max="2.1"
			R_max="12.1"

			if monopole == "monopoless":
				conf_format = "double_fortran"
				bites_skip = 8
				matrix_type = 'su2'
			elif monopole == "monopole":
				conf_format = "float_fortran"
				bites_skip = 8
				matrix_type = 'abelian'
		elif conf_type == "qc2dstag":
			matrix_type="su2"
			conf_format="double_qc2dstag"
			smeared_format="double"
			chains = {'/': [201, 1000]}
			L_spat=40
			L_time=40

			if monopole == "monopoless":
				smeared_format="double"
				bites_skip_smeared = 4
				matrix_type_smeared = 'su2'
				conf_format = "double_qc2dstag"
				bites_skip = 4
				matrix_type = 'su2'
			elif monopole == "monopole":
				smeared_format="double_fortran"
				bites_skip_smeared = 4
				matrix_type_smeared = 'abelian'
				conf_format = "double_qc2dstag"
				bites_skip = 4
				matrix_type = 'su2'

		jobs = distribute_jobs(chains, number_of_jobs)
		#print('beta old', beta)
		#beta = beta.replace('.', 'p')
		#print('beta new', beta)

		for job in jobs:
			log_path = f'/home/clusters/rrcmpi/kudrov/observables_cluster/logs/wilson_loop/{axis}/{monopole}/{conf_type}/{conf_size}/beta2.{beta}/mu{mu}/{job[0]}'
			try:
				os.makedirs(log_path)
			except:
				pass

			bashCommand = f'qsub -q long -v conf_format={conf_format},bites_skip={bites_skip},matrix_type={matrix_type},axis={axis},beta={beta},'\
				f'L_spat={L_spat},L_time={L_time},T_min={T_min},T_max={T_max},R_min={R_min},R_max={R_max},chain={job[0]},conf1={job[1]},conf2={job[2]},'\
				f'calculate_absent={calculate_absent},monopole={monopole},conf_type={conf_type},mu={mu},conf_size={conf_size}'\
				f' -o {log_path}/{job[1]:04}-{job[2]:04}.o -e {log_path}/{job[1]:04}-{job[2]:04}.e /home/clusters/rrcmpi/kudrov/observables_cluster/scripts/do_wilson.sh'
			#print(bashCommand)
			process = subprocess.Popen(bashCommand.split())
			output, error = process.communicate()
			#print(output, error)
