#!/bin/bash

for((i=${conf_start};i<=${conf_end};i++))
do

if [[ ${conf_path_end} == "/" ]]; then

conf_path_end=""

fi

conf_path1="${conf_path_start}`printf %0${padding}d $i`${conf_path_end}"

echo ${conf_path1}

if [ -f ${conf_path1} ] && [ -s ${conf_path1} ]; then

mkdir -p ${path_wilson}

if [[ ! -f "${path_wilson}/wilson_loop_`printf %04d $i`" ]] || [ ! $calculate_absent -eq 0 ] ; then

#-conf_format_plaket ${conf_format_plaket1} -conf_path_plaket ${conf_path_plaket1} -bytes_skip_plaket ${bytes_skip_plaket1}\

parameters="-conf_format ${conf_format} -conf_path ${conf_path1} -bytes_skip ${bytes_skip} -convert ${convert}\
    -L_spat ${L_spat} -L_time ${L_time} -representation ${representation} -APE_steps ${APE_steps} -alpha ${alpha}\
    -path_wilson ${path_wilson}/wilson_loop_`printf %04d $i`\
    -T_min ${T_min} -T_max ${T_max} -R_min ${R_min} -R_max ${R_max}"

/home/clusters/rrcmpi/kudrov/general_code/apps/observables/wilson_loops_spatial/wilson_loops_spatial_${matrix_type}_${arch} $parameters

fi
fi

done
