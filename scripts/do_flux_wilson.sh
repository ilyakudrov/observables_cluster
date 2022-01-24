#!/bin/bash

for((i=${conf_start};i<=${conf_end};i++))
do

if [[ ${conf_path_plaket_end} == "/" ]]; then

conf_path_plaket_end=""

fi

if [[ ${conf_path_wilson_end} == "/" ]]; then

conf_path_wilson_end=""

fi

conf_path_plaket="${conf_path_plaket_start}`printf %0${padding_plaket}d $i`${conf_path_plaket_end}"
conf_path_wilson="${conf_path_wilson_start}`printf %0${padding_wilson}d $i`${conf_path_wilson_end}"

if [ -f ${conf_path_plaket} ] && [ -s ${conf_path_plaket} ] && [ -f ${conf_path_wilson} ] && [ -s ${conf_path_wilson} ] ; then

mkdir -p ${output_path}
output_path_electric="${output_path}/electric_`printf %04d $i`"
output_path_magnetic="${output_path}/magnetic_`printf %04d $i`"

parameters="-conf_format_plaket $conf_format_plaket -conf_format_wilson ${conf_format_wilson} -conf_path_plaket $conf_path_plaket\
 -conf_path_wilson ${conf_path_wilson} -bites_skip_plaket ${bites_skip_plaket} -bites_skip_wilson ${bites_skip_wilson}\
  -matrix_type_plaket ${matrix_type_plaket} -matrix_type_wilson ${matrix_type_wilson} -output_path_electric ${output_path_electric} -output_path_magnetic ${output_path_magnetic}\
   -T_min ${T_min} -T_max ${T_max} -R_min ${R_min} -R_max ${R_max} -L_spat ${L_spat} -L_time ${L_time} -x_trans ${x_trans}"

/home/clusters/rrcmpi/kudrov/observables_cluster/code/exe/flux_wilson_${matrix_type_plaket}_${matrix_type_wilson} $parameters

fi

done
