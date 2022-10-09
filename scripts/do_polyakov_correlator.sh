#!/bin/bash

for((i=${conf_start};i<=${conf_end};i++))
do


if [[ ${conf_path_end} == "/" ]]; then

conf_path_end=""

fi

conf_path1="${conf_path_start}`printf %0${padding}d $i`${conf_path_end}"

echo ${conf_path1}

if [ -f ${conf_path1} ] && [ -s ${conf_path1} ] ; then

mkdir -p ${path_wilson}
mkdir -p ${path_output_correlator}

#if [ ! -f "${path_wilson}/wilson_loop_`printf %04d $i`" ] || [  ! ${calculate_absent} ] ; then


parameters="-conf_format ${conf_format} -conf_path ${conf_path1} -bytes_skip ${bytes_skip}\
    -x_size ${L_spat} -y_size ${L_spat} -z_size ${L_spat} -t_size ${L_time} -D_max ${D_max}\
    -path_output_correlator ${path_output_correlator}/correlator_`printf %04d $i`\"

/home/clusters/rrcmpi/kudrov/general_code/apps/polyakov_loop_correlator/polyakov_loop_correlator_${matrix_type}_${arch} $parameters

#fi
fi

done
