#!/bin/bash
conf_type="qc2dstag"
smearing="/HYP_APE"
for mu in 5 #10 15 25 30 40
do
w=$(($mu/10))
q=$(($mu-$w*10))

path_wilson="/home/clusters/rrcmpi/kudrov/observables/result/wilson_loop/${conf_type}${smearing}/mu0.$w$q/wilson_loop_"
path_sizes="/home/clusters/rrcmpi/kudrov/observables/result/wilson_loop/${conf_type}${smearing}/mu0.$w$q/sizes_"
path_output="/home/clusters/rrcmpi/kudrov/observables/get_result/result/wilson_loop/${conf_type}${smearing}/wilson_loops_mu0.$w$q"

if test -f ${conf_path}; then
	/home/clusters/rrcmpi/kudrov/observables/get_result/code/exe/get_aver_wilson $path_wilson $path_sizes $path_output
fi
done
