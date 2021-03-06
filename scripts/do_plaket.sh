#!/bin/bash

for((i=${conf_start};i<=${conf_end};i++))
do

if [[ ${conf_path_end} == "/" ]]; then

conf_path_end=""

fi

conf_path="${conf_path_start}`printf %0${padding}d $i`${conf_path_end}"

if [ -f ${conf_path} ] && [ -s ${conf_path} ] ; then

mkdir -p ${output_path}
output_path1="${output_path}/plaket_`printf %04d $i`"

parameters="-conf_format ${conf_format} -conf_path $conf_path\
  -bites_skip ${bites_skip} \
  -output_path ${output_path1}\
  -L_spat ${L_spat} -L_time ${L_time}"

/home/clusters/rrcmpi/kudrov/observables_cluster/code/exe/plaket_${matrix_type}_${arch} $parameters

fi

done
