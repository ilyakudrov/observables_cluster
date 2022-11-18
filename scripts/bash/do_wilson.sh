#!/bin/bash

for((i=${conf_start};i<=${conf_end};i++))
do

if [[ ${conf_path_end} == "/" ]]; then

conf_path_end=""

fi

conf_path="${conf_path_start}`printf %0${padding}d $i`${conf_path_end}"

if [ -f ${conf_path} ] && [ -s ${conf_path} ] ; then

mkdir -p ${output_path}
output_path1="${output_path}/wilson_loop_`printf %04d $i`"

parameters="-conf_format ${conf_format} -conf_path $conf_path\
  -bites_skip ${bites_skip} \
  -output_path ${output_path1}\
   -T_min ${T_min} -T_max ${T_max} -R_min ${R_min} -R_max ${R_max} -L_spat ${L_spat} -L_time ${L_time}"

/home/clusters/rrcmpi/kudrov/observables_cluster/code/exe/wilson_${axis}_${matrix_type} $parameters

fi

done
