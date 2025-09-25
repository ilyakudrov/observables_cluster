#!/bin/bash

for((i=${conf_start};i<=${conf_end};i++))
do

if [[ ${conf_path_end_plaket} == "/" ]]; then
conf_path_end_plaket=""
fi

if [[ ${conf_path_end_wilson} == "/" ]]; then
conf_path_end_wilson=""
fi

if [[ ${gauge_copies} == 0 ]]; then
ending_copy=1
else
ending_copy=${gauge_copies}
fi

for((copy=0;copy<${ending_copy};copy++))
do

conf_path_plaket="${conf_path_start_plaket}`printf %0${padding_plaket}d $i`${conf_path_end_plaket}"
conf_path_wilson="${conf_path_start_wilson}`printf %0${padding_wilson}d $i`${conf_path_end_wilson}"

if [[ ${gauge_copies} == 0 ]]; then
conf_path_plaket="${conf_path_plaket}"
conf_path_wilson="${conf_path_wilson}"
else
conf_path_plaket="${conf_path_plaket}_${copy}"
conf_path_wilson="${conf_path_wilson}_${copy}"
fi

echo ${conf_path_plaket}
echo ${conf_path_wilson}

if [ -f ${conf_path_plaket} ] && [ -s ${conf_path_plaket} ] && [ -f ${conf_path_wilson} ] && [ -s ${conf_path_wilson} ] ; then

mkdir -p "${output_path}/longitudinal"
mkdir -p "${output_path}/transversal"

if [[ ${gauge_copies} == 0 ]]; then
output_path_electric_long="${output_path}/longitudinal/electric_`printf %04d $i`"
output_path_magnetic_long="${output_path}/longitudinal/magnetic_`printf %04d $i`"
output_path_electric_trans="${output_path}/transversal/electric_`printf %04d $i`"
output_path_magnetic_trans="${output_path}/transversal/magnetic_`printf %04d $i`"
else
output_path_electric_long="${output_path}/longitudinal/electric_`printf %04d $i`_${copy}"
output_path_magnetic_long="${output_path}/longitudinal/magnetic_`printf %04d $i`_${copy}"
output_path_electric_trans="${output_path}/transversal/electric_`printf %04d $i`_${copy}"
output_path_magnetic_trans="${output_path}/transversal/magnetic_`printf %04d $i`_${copy}"
fi

if [[ ! -f "${output_path_electric_long}" ]] || [[ ! -f "${output_path_magnetic_long}" ]] || [[ ! -f "${output_path_electric_trans}" ]] || [[ ! -f "${output_path_magnetic_trans}" ]] || [ ! $calculate_absent -eq 1 ] ; then

parameters="--conf_format_plaket $conf_format_plaket --conf_format_wilson ${conf_format_wilson} --conf_path_plaket $conf_path_plaket\
   --conf_path_wilson ${conf_path_wilson} --bytes_skip_plaket ${bytes_skip_plaket} --bytes_skip_wilson ${bytes_skip_wilson} --file_precision_wilson ${file_precision_wilson} --file_precision_plaket ${file_precision_plaket}\
   --matrix_type_plaket ${matrix_type_plaket} --matrix_type_wilson ${matrix_type_wilson} --output_path_electric_long ${output_path_electric_long} --output_path_magnetic_long ${output_path_magnetic_long}\
   --output_path_electric_trans ${output_path_electric_trans} --output_path_magnetic_trans ${output_path_magnetic_trans} --convert_plaket ${convert_plaket} --convert_wilson ${convert_wilson}
   --T_min ${T_min} --T_max ${T_max} --R_min ${R_min} --R_max ${R_max} --L_spat ${L_spat} --L_time ${L_time}"

/home/clusters/rrcmpi/kudrov/general_code/apps/observables/flux_tube/flux_tube_wilson_${matrix_type_plaket}_${matrix_type_wilson}_${arch} $parameters

fi
fi

done
done
