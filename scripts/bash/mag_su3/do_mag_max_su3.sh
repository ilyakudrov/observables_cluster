#!/bin/bash

for((i=${conf_start};i<=${conf_end};i++))
do

if [[ ${conf_path_end} == "/" ]]; then

conf_path_end=""

fi

path_conf="${conf_path_start}`printf %0${padding}d $i`${conf_path_end}"
echo ${path_conf}

if [ -f ${path_conf} ] && [ -s ${path_conf} ] ; then

mkdir -p ${conf_path_output}
mkdir -p ${functional_path_output}

path_functional_output="${functional_path_output}/functional"

seed=$(date +%s)

/home/clusters/rrcmpi/kudrov/SU3_MA_gauge_GPU/src/gaugefixing/apps/MAGaugeFixingSU3_maximization_4D_DP_N${L_spat}T${L_time}  --ftype ILDG --fbasename ${conf_path_start} \
 --fending ${conf_path_end} --reinterpret DOUBLE --fnumberformat ${padding} -m 1 --fstartnumber ${i} --sasteps 5 --samin 2.5 --samax 0.5\
 --output_SA_functional ${path_functional_output} --gaugecopies 1 --output_conf "${conf_path_output}/conf.SP_" --output_ending "" --seed ${seed} --microupdates 6 --precision 1e-12

fi

done
