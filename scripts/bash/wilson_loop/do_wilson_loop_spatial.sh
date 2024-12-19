#!/bin/bash

for((i=${conf_start};i<=${conf_end};i++))
do

if [[ ${conf_path_end} == "/" ]]; then

conf_path_end=""

fi

if [[ ${gauge_copies} == 0 ]]; then
ending_copy=1
else
ending_copy=${gauge_copies}
fi

for((copy=0;copy<${ending_copy};copy++))
do

conf_path1="${conf_path_start}`printf %0${padding}d $i`${conf_path_end}"

if [[ ${gauge_copies} == 0 ]]; then
conf_path1="${conf_path1}"
else
conf_path1="${conf_path1}_${copy}"
fi

if [ -f ${conf_path1} ] && [ -s ${conf_path1} ]; then

mkdir -p ${path_wilson}

if [[ ${gauge_copies} == 0 ]]; then
output_path="${path_wilson}/wilson_loop_`printf %04d $i`"
else
output_path="${path_wilson}/wilson_loop_`printf %04d $i`_${copy}"
fi

if [[ ! -f ${output_path} ]] || [ ! $calculate_absent -eq 0 ] ; then

parameters="-conf_format ${conf_format} -conf_path ${conf_path1} -bytes_skip ${bytes_skip} -convert ${convert}\
    -L_spat ${L_spat} -L_time ${L_time} -representation ${representation} -APE_start ${APE_start} -APE_end ${APE_end} -APE_step ${APE_step} -alpha ${alpha}\
    -path_wilson ${path_wilson}/wilson_loop_`printf %04d $i`\
    -T_min ${T_min} -T_max ${T_max} -R_min ${R_min} -R_max ${R_max}"

/home/clusters/rrcmpi/kudrov/general_code/apps/observables/wilson_loops_spatial/wilson_loops_spatial_${matrix_type}_${arch} $parameters

fi
fi

done
done
