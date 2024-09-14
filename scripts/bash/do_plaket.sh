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

if [[ ${gauge_copies} == 0 ]]; then
conf_path_end1="${conf_path_end}_${copy}"
else
conf_path_end1="${conf_path_end}"
fi

conf_path="${conf_path_start}`printf %0${padding}d $i`${conf_path_end1}"

echo "conf_path" ${conf_path}

if [ -f ${conf_path} ] && [ -s ${conf_path} ] ; then

if [[ ${gauge_copies} == 0 ]]; then
output_path_plaket="${output_path}/plaket_`printf %04d $i`"
else
output_path_plaket="${output_path}/plaket_`printf %04d $i`_${copy}"
fi

echo "output_path_plaket" ${output_path_plaket}

if [[ ! ${output_path_plaket} ]] || [ ! $calculate_absent -eq 1 ] ; then

echo output_path ${output_path}
mkdir -p ${output_path}
output_path1=${output_path_plaket}

parameters="-conf_format ${conf_format} -conf_path $conf_path\
  -bytes_skip ${bytes_skip} -convert ${convert} -path ${output_path1}\
  -L_spat ${L_spat} -L_time ${L_time}"

/home/clusters/rrcmpi/kudrov/general_code/apps/observables/plaket/plaket_${matrix_type}_${arch} $parameters

fi
fi

done
done
