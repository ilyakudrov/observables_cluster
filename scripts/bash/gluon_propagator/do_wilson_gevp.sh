#!/bin/bash

if [ "${matrix_type}" = "su3_abelian" ] && [ "${representation}" = "adjoint" ] ; then
matrix_type="su3_angles"
fi

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

echo ${conf_path1}

if [ -f ${conf_path1} ] && [ -s ${conf_path1} ]; then

mkdir -p ${output_path}

if [[ ${gauge_copies} == 0 ]]; then
output="${output_path}/gluon_propagator_`printf %04d $i`"
else
output="${output_path}/gluon_propagator_`printf %04d $i`_${copy}"
fi

if [[ ! -f "${output}" ]] || [ ! $calculate_absent -eq 1 ] ; then

parameters="-conf_format ${conf_format} -conf_path ${conf_path1} -bytes_skip ${bytes_skip} -convert ${convert}\
    -output_path ${output} -L_spat ${L_spat} -L_time ${L_time} -beta ${beta}"

/home/clusters/rrcmpi/kudrov/general_code/apps/observables/gluon_propagator_${matrix_type}_${arch} $parameters

fi
fi

done
done
