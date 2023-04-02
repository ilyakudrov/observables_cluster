#!/bin/bash

for((i=${conf_start};i<=${conf_end};i++))
do

if [[ ${conf_path_end} == "/" ]]; then

conf_path_end=""

fi

path_conf="${conf_path_start}`printf %0${padding}d $i`${conf_path_end}"

echo conf_path_start ${conf_path_start}
echo conf_path_end ${conf_path_end}
echo path_conf ${path_conf}

if [ -f ${path_conf} ] && [ -s ${path_conf} ] ; then

mkdir -p "${path_functional_output}"

path_functional="${path_functional_output}/functional_`printf %04d $i`"

parameters="-conf_format ${conf_format} -path_conf $path_conf -conf_format ${conf_format} -bytes_skip ${bytes_skip} \
    -path_functional_output ${path_functional} \
    -x_size ${L_spat} -y_size ${L_spat} -z_size ${L_spat} -t_size ${L_time}"


/home/clusters/rrcmpi/kudrov/general_code/apps/mag_su2/mag_functional_${arch} $parameters

fi

done
