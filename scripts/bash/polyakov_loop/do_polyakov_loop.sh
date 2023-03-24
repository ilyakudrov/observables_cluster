#!/bin/bash

for((i=${conf_start};i<=${conf_end};i++))
do

if [[ ${conf_path_end} == "/" ]]; then

conf_path_end=""

fi

conf_path="${conf_path_start}`printf %0${padding}d $i`${conf_path_end}"

echo ${conf_path1}

if [ -f ${conf_path} ] && [ -s ${conf_path} ] ; then

mkdir -p ${output_path}
output_path1="${output_path}/polyakov_loop_`printf %04d $i`"

parameters="-conf_format ${conf_format} -conf_path $conf_path\
 -bytes_skip ${bytes_skip} -output_path ${output_path1} -L_spat ${L_spat} -L_time ${L_time}"

/home/clusters/rrcmpi/kudrov/general_code/apps/polyakov_loop/polyakov_loop_${matrix_type}_${arch} $parameters

fi

done
