#!/bin/bash

for((i=${conf_start};i<=${conf_end};i++))
do

if [[ ${conf_path_end_plaket} == "/" ]]; then

conf_path_end_plaket=""

fi

if [[ ${conf_path_end_wilson} == "/" ]]; then

conf_path_end_wilson=""

fi

conf_path_plaket="${conf_path_start_plaket}`printf %0${padding_plaket}d $i`${conf_path_end_plaket}"
conf_path_wilson="${conf_path_start_wilson}`printf %0${padding_wilson}d $i`${conf_path_end_wilson}"

echo ${conf_path_plaket}
echo ${conf_path_wilson}

if [ -f ${conf_path_plaket} ] && [ -s ${conf_path_plaket} ] && [ -f ${conf_path_wilson} ] && [ -s ${conf_path_wilson} ] ; then

mkdir -p "${output_path}/longitudinal"
mkdir -p "${output_path}/transversal"
output_path_electric_long="${output_path}/longitudinal/electric_`printf %04d $i`"
# output_path_magnetic_long="${output_path}/longitudinal/magnetic_`printf %04d $i`"
output_path_electric_trans="${output_path}/transversal/electric_`printf %04d $i`"
# output_path_magnetic_trans="${output_path}/transversal/magnetic_`printf %04d $i`"

parameters="-conf_format_plaket $conf_format_plaket -conf_format_wilson ${conf_format_wilson} -conf_path_plaket $conf_path_plaket\
   -conf_path_wilson ${conf_path_wilson} -bytes_skip_plaket ${bytes_skip_plaket} -bytes_skip_wilson ${bytes_skip_wilson}\
   -matrix_type_plaket ${matrix_type_plaket} -matrix_type_wilson ${matrix_type_wilson} -output_path_electric_long ${output_path_electric_long}\
   -output_path_electric_trans ${output_path_electric_trans} -convert_plaket ${convert_plaket} -convert_wilson ${convert_wilson}\
   -T_min ${T_min} -T_max ${T_max} -R_min ${R_min} -R_max ${R_max} -d_ouside ${d_ouside} -L_spat ${L_spat} -L_time ${L_time} -x_trans ${x_trans}"

/home/clusters/rrcmpi/kudrov/general_code/apps/observables/flux_tube/flux_tube_schwinger_${matrix_type_plaket}_${matrix_type_wilson}_${arch} $parameters

fi

done
