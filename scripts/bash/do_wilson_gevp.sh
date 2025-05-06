#!/bin/bash

if [ "${matrix_type_wilson}" = "su3_abelian" ] && [ "${representation}" = "adjoint" ] ; then
matrix_type_wilson="su3_angles"
fi

for((i=${conf_start};i<=${conf_end};i++))
do

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

conf_path_wilson1="${conf_path_start_wilson}`printf %0${padding_wilson}d $i`${conf_path_end_wilson}"

if [[ ${gauge_copies} == 0 ]]; then
conf_path_wilson1="${conf_path_wilson1}"
else
conf_path_wilson1="${conf_path_wilson1}_${copy}"
fi

echo ${conf_path_wilson1}

if [ -f ${conf_path_wilson1} ] && [ -s ${conf_path_wilson1} ]; then

mkdir -p ${path_wilson}

if [[ ${gauge_copies} == 0 ]]; then
output_wilson="${path_wilson}/wilson_loop_`printf %04d $i`"
else
output_wilson="${path_wilson}/wilson_loop_`printf %04d $i`_${copy}"
fi

if [[ ! -f "${output_wilson}" ]] || [ ! $calculate_absent -eq 1 ] ; then

parameters="-conf_format_wilson ${conf_format_wilson} -conf_path_wilson ${conf_path_wilson1} -bytes_skip_wilson ${bytes_skip_wilson} -convert_wilson ${convert_wilson}\
    -HYP_alpha1 ${HYP_alpha1} -HYP_alpha2 ${HYP_alpha2} -HYP_alpha3 ${HYP_alpha3} -representation ${representation}\
    -APE_alpha ${APE_alpha} -HYP_enabled ${HYP_enabled} -path_wilson ${output_wilson}\
    -APE_steps ${APE_steps} -HYP_steps ${HYP_steps} -L_spat ${L_spat} -L_time ${L_time}\
    -T_min ${T_min} -T_max ${T_max} -R_min ${R_min} -R_max ${R_max} -calculation_step_APE ${calculation_step_APE}\
    -calculation_APE_start ${calculation_APE_start} -N_dir ${N_dir}"

/home/clusters/rrcmpi/kudrov/general_code/apps/smearing/smearing_wilson_gevp_${matrix_type_wilson}_${arch} $parameters

fi
fi

done
done
