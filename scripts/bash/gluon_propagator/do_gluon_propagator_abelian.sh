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

mkdir -p ${output_path_abelian}
mkdir -p ${output_path_monopole}
mkdir -p ${output_path_photon}

if [[ ${gauge_copies} == 0 ]]; then
output_abelian="${output_path_abelian}/gluon_propagator_`printf %04d $i`"
output_monopole="${output_path_monopole}/gluon_propagator_`printf %04d $i`"
output_photon="${output_path_photon}/gluon_propagator_`printf %04d $i`"
else
output_abelian="${output_path_abelian}/gluon_propagator_`printf %04d $i`_${copy}"
output_monopole="${output_path_monopole}/gluon_propagator_`printf %04d $i`_${copy}"
output_photon="${output_path_photon}/gluon_propagator_`printf %04d $i`_${copy}"
fi

if [[ ! -f "${output_abelian}" ]] || [[ ! -f "${output_monopole}" ]] || [[ ! -f "${output_photon}" ]] || [ ! $calculate_absent -eq 1 ] ; then

parameters="--conf_format ${conf_format} --conf_path ${conf_path1} --bytes_skip ${bytes_skip} --convert ${convert} --file_precision ${file_precision}\
    --output_path ${output_abelian} --output_path ${output_monopole} --output_path ${output_photon} --L_spat ${L_spat} --L_time ${L_time} --beta ${beta}"

/home/clusters/rrcmpi/kudrov/general_code/apps/observables/gluon_propagator/gluon_propagator_abelian_${arch} $parameters

fi
fi

done
done
