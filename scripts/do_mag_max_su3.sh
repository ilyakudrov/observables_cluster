#!/bin/bash

for((i=${conf_start};i<=${conf_end};i++))
do

if [[ ${conf_path_end} == "/" ]]; then

conf_path_end=""

fi

path_conf="${conf_path_start}`printf %0${padding}d $i`${conf_path_end}"

if [ -f ${path_conf} ] && [ -s ${path_conf} ] ; then

mkdir -p ${conf_path_output}
mkdir -p ${output_path_conf_spin}
mkdir -p ${output_path_functional}

path_functional_output="${output_path_functional}/functional_`printf %04d $i`"

/home/clusters/rrcmpi/kudrov/SU3_MA_gauge_GPU/src/gaugefixing/apps/MAGaugeFixingSU3_maximization_4D_DP_N${space_size}T${time_size}  --ftype QCDSTAG --fbasename ${conf_path_start} \
 --fending ${conf_path_end} --reinterpret DOUBLE --fnumberformat ${padding} -m 1 --fstartnumber ${conf_start} --sasteps ${sasteps} --samin ${temperature_min} --samax ${temperature_max}\
 --output_SA_functional ${output_SA_functional} --gaugecopies ${gaugecopies} --output_conf "${conf_path_output}_" --output_ending "" --seed ${seed} --microupdates 6

fi

done
