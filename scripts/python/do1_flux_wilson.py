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
bites_skip_smeared = 4

HYP_alpha1 = "1"
HYP_alpha2 = "1"
HYP_alpha3 = "0.5"
APE_alpha = "0.5"
stout_alpha = "0.15"
APE_steps = "100"
HYP_steps = "0"

number_of_jobs = 100

calculate_absent = 'false'

monopole = "/"
smearing = f'HYP{HYP_steps}_alpha={HYP_alpha1}_{HYP_alpha2}_{HYP_alpha3}_APE{APE_steps}_alpha={APE_alpha}'

for mu in ["0.00"]:
	#f = open(f'/home/clusters/rrcmpi/kudrov/conf/{conf_type}/{conf_size}/mu{mu}/parameters.json')
	#data = json.load(f)

	if conf_type == "su2_suzuki":
		matrix_type="su2"
		conf_format="double_fortran"
		bites_skip = 8
		smeared_format="double"
		matrix_type_smeared = 'su2'
		chains = {'/': [1, 100]}
		L_spat=24
		L_time=24

		if monopole == "monopoless":
			smeared_format="double"
			matrix_type_smeared = 'su2'
			conf_format = "double_fortran"
			bites_skip = 8
			matrix_type = 'su2'
		elif monopole == "monopole":
			smeared_format="double"
			#smeared_format="float_fortran"
			bites_skip_smeared = 8
			matrix_type_smeared = 'abelian'
			conf_format = "double_fortran"
			bites_skip = 8
			matrix_type = 'su2'
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

	for job in jobs:

		log_path = f'/home/clusters/rrcmpi/kudrov/observables_cluster/logs/flux_tube_wilson/{monopole}/{conf_type}/{conf_size}/mu{mu}/{job[0]}'
		try:
			os.makedirs(log_path)
		except:
			pass

		bashCommand = f'qsub -q long -v conf_format={conf_format},smeared_format={smeared_format},bites_skip={bites_skip},'\
			f'bites_skip_smeared={bites_skip_smeared},matrix_type={matrix_type},matrix_type_smeared={matrix_type_smeared},'\
			f'smearing={smearing},L_spat={L_spat},L_time={L_time},chain={job[0]},conf_start={job[1]},conf_end={job[2]},'\
			f'calculate_absent={calculate_absent},monopole={monopole},conf_type={conf_type},mu={mu},conf_size={conf_size}'\
			f' -o {log_path}/{job[1]:04}-{job[2]:04}.o -e {log_path}/{job[1]:04}-{job[2]:04}.e /home/clusters/rrcmpi/kudrov/observables_cluster/scripts/do_flux_wilson.sh'
		#print(bashCommand)
		process = subprocess.Popen(bashCommand.split())
		output, error = process.communicate()
		#print(output, error)
