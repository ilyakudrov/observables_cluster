#!/bin/bash

for((i=${conf_start};i<=${conf_end};i++))
do

if [[ ${conf_path_end} == "/" ]]; then

conf_path_end=""

fi

path_conf="${conf_path_start}`printf %0${padding}d $i`${conf_path_end}"
echo ${path_conf}

if [ -f ${path_conf} ] && [ -s ${path_conf} ] ; then

mkdir -p "${output_path}/clusters_unwrapped"
mkdir -p "${output_path}/clusters_wrapped"
mkdir -p "${output_path}/windings"
mkdir -p "${output_path}/monopoles"

path_output_clusters_unwrapped="${output_path}/clusters_unwrapped/clusters_unwrapped_`printf %04d $i`"
path_output_clusters_wrapped="${output_path}/clusters_wrapped/clusters_wrapped_`printf %04d $i`"
path_output_windings="${output_path}/windings/windings_`printf %04d $i`"
path_output_monopoles="${output_path}/monopoles/monopoles_`printf %04d $i`"

parameters="-conf_format ${conf_format} -path_conf $path_conf -conf_format ${conf_format} -bytes_skip ${bytes_skip} \
    -path_output_clusters_unwrapped ${path_output_clusters_unwrapped} -path_output_windings ${path_output_windings} -path_output_monopoles ${path_output_monopoles} \
    -path_output_clusters_wrapped ${path_output_clusters_wrapped} -x_size ${L_spat} -y_size ${L_spat} -z_size ${L_spat} -t_size ${L_time}"


/home/clusters/rrcmpi/kudrov/general_code/apps/monopoles_su3/monopoles_su3_${arch} $parameters

fi

done
