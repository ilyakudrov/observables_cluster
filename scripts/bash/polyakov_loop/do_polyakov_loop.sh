#!/bin/bash

for((i=${conf_start};i<=${conf_end};i++))
do

if [[ ${conf_path_end} == "/" ]]; then

conf_path_end=""

fi

conf_path="${conf_path_start}`printf %0${padding}d $i`${conf_path_end}"

echo ${conf_path}

if [ -f ${conf_path} ] && [ -s ${conf_path} ] ; then

mkdir -p ${output_path}
output_path1="${output_path}/polyakov_loop_`printf %04d $i`"

parameters="-conf_format ${conf_format} --path_conf $conf_path --file_precision ${file_precision}\
 --bytes_skip ${bytes_skip} --convert ${convert} --path_output ${output_path1}\
 --x_size ${L_spat} --y_size ${L_spat} --z_size ${L_spat} --t_size ${L_time}"

/home/clusters/rrcmpi/kudrov/general_code/apps/polyakov_loop/polyakov_loop_${matrix_type}_${arch} $parameters

fi

done
