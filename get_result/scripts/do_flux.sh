#!/bin/bash
conf_type="offd"
smearing="/HYP_APE"
for mu in 0 10 15 25 30 40
do
w=$(($mu/10))
q=$(($mu-$w*10))

for T in 8 10 12
do
for R in 8 10 12 14 16
do
electric_path="/home/clusters/rrcmpi/kudrov/observables/result/flux_tube/${conf_type}${smearing}/mu0.$w$q/T=$T/R=$R/electric_"
magnetic_path="/home/clusters/rrcmpi/kudrov/observables/result/flux_tube/${conf_type}${smearing}/mu0.$w$q/T=$T/R=$R/magnetic_"
output_electric="/home/clusters/rrcmpi/kudrov/observables/get_result/result/flux_tube/${conf_type}${smearing}/mu0.$w$q/electric_T=${T}_R=${R}"
output_magnetic="/home/clusters/rrcmpi/kudrov/observables/get_result/result/flux_tube/${conf_type}${smearing}/mu0.$w$q/magnetic_T=${T}_R=${R}"
output_energy="/home/clusters/rrcmpi/kudrov/observables/get_result/result/flux_tube/${conf_type}${smearing}/mu0.$w$q/energy_T=${T}_R=${R}"
output_action="/home/clusters/rrcmpi/kudrov/observables/get_result/result/flux_tube/${conf_type}${smearing}/mu0.$w$q/action_T=${T}_R=${R}"

if test -f ${conf_path}; then
	/home/clusters/rrcmpi/kudrov/observables/get_result/code/exe/get_aver_flux $electric_path $magnetic_path $R $output_electric $output_magnetic $output_energy $output_action
fi
done
done
done
