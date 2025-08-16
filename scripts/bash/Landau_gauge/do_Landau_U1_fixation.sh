#!/bin/bash

for((i=${conf_start};i<=${conf_end};i++))
do

if [[ ${conf_path_end} == "/" ]]; then

conf_path_end=""

fi

path_conf="${conf_path_start}`printf %0${padding}d $i`${conf_path_end}"

if [ -f ${path_conf} ] && [ -s ${path_conf} ] ; then

mkdir -p ${output_path_confs_gaugefixed}
mkdir -p ${output_path_functional}

path_conf_output="${output_path_confs_gaugefixed}/conf_`printf %04d $i`"
path_functional_output="${output_path_functional}/functional_`printf %04d $i`"

parameters="--conf_format ${conf_format} --path_conf $path_conf --bytes_skip ${bytes_skip} --file_precision ${file_precision}\
    --path_conf_output ${path_conf_output} --path_functional_output ${path_functional_output}\
    --x_size ${L_spat} --y_size ${L_spat} --z_size ${L_spat} --t_size ${L_time}"

/home/clusters/rrcmpi/kudrov/general_code/apps/Landau_U1/Landau_U1_fixation_${arch} $parameters

fi

done
