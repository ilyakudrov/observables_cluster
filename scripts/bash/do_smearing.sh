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
starting_copy=0
else
starting_copy=1
fi

for((copy=${starting_copy};copy<=${gauge_copies};copy++))
do

conf_path_plaket1="${conf_path_start_plaket}`printf %0${padding_plaket}d $i`${conf_path_end_plaket}"
conf_path_wilson1="${conf_path_start_wilson}`printf %0${padding_wilson}d $i`${conf_path_end_wilson}"

if [[ ${copy} == 0 ]]; then
conf_path_plaket1="${conf_path_plaket1}"
conf_path_wilson1="${conf_path_wilson1}"
else
conf_path_plaket1="${conf_path_plaket1}_${copy}"
conf_path_wilson1="${conf_path_wilson1}_${copy}"
fi

echo ${conf_path_plaket1}
echo ${conf_path_wilson1}

if [ -f ${conf_path_wilson1} ] && [ -s ${conf_path_wilson1} ]; then

if [[ -f ${conf_path_plaket1} ]] && [[ -s ${conf_path_plaket1} ]] || [[ ! ${flux_enabled} == 1 ]]; then

if [ ${wilson_enabled} -eq 1 ] ; then
mkdir -p ${path_wilson}
fi

if [ ${flux_enabled} -eq 1 ] ; then
mkdir -p ${path_flux}
fi

if [ ${polyakov_correlator_enabled} -eq 1 ] ; then
mkdir -p ${path_polyakov_correlator}
fi

if [ ${save_conf} -eq 1 ] ; then
mkdir -p ${conf_path_output}
fi

if [[ ${copy} == 0 ]]; then
output_smeared="${conf_path_output}/smeared_`printf %04d $i`"
output_wilson="${path_wilson}/wilson_loop_`printf %04d $i`"
output_flux_tube="${path_flux}/flux_tube_`printf %04d $i`"
output_polyakov_correlator="${path_flux}/polyakov_correlator_`printf %04d $i`"
else
output_smeared="${conf_path_output}/smeared_`printf %04d $i`_${copy}"
output_wilson="${path_wilson}/wilson_loop_`printf %04d $i`_${copy}"
output_flux_tube="${path_flux}/flux_tube_`printf %04d $i`_${copy}"
output_polyakov_correlator="${path_polyakov_correlator}/polyakov_correlator_`printf %04d $i`_${copy}"
fi

echo "output_smeared" "${output_smeared}"

if [[ ! "${output_smeared}" ]] || [ ! $calculate_absent -eq 1 ] ; then

#-conf_format_plaket ${conf_format_plaket1} -conf_path_plaket ${conf_path_plaket1} -bytes_skip_plaket ${bytes_skip_plaket1}\

parameters="-conf_format_wilson ${conf_format_wilson} -conf_path_wilson ${conf_path_wilson1} -bytes_skip_wilson ${bytes_skip_wilson} -convert_wilson ${convert_wilson}\
    -conf_format_plaket ${conf_format_plaket} -conf_path_plaket ${conf_path_plaket1} -bytes_skip_plaket ${bytes_skip_plaket} -convert_plaket ${convert_plaket}\
    -HYP_alpha1 ${HYP_alpha1} -HYP_alpha2 ${HYP_alpha2} -HYP_alpha3 ${HYP_alpha3}\
    -APE_alpha ${APE_alpha} -APE_enabled ${APE_enabled} -HYP_enabled ${HYP_enabled}\
    -APE_steps ${APE_steps} -HYP_steps ${HYP_steps} -L_spat ${L_spat} -L_time ${L_time}\
    -path_wilson ${output_wilson} -path_flux ${output_flux_tube} -path_polyakov_correlator ${output_polyakov_correlator}\
    -wilson_enabled ${wilson_enabled} -flux_enabled ${flux_enabled} -polyakov_correlator_enabled ${polyakov_correlator_enabled} -correlator_type ${polyakov_correlator_type}\
    -T_min ${T_min} -T_max ${T_max} -R_min ${R_min} -R_max ${R_max} -calculation_step_APE ${calculation_step_APE}\
    -polyakov_correlator_D ${polyakov_correlator_D} -calculation_step_HYP ${calculation_step_HYP} -calculation_HYP_start ${calculation_HYP_start}\
    -calculation_APE_start ${calculation_APE_start} -save_conf ${save_conf} -conf_path_output ${output_smeared}"

/home/clusters/rrcmpi/kudrov/general_code/apps/smearing/smearing_${matrix_type_wilson}_${matrix_type_plaket}_${arch} $parameters

fi
fi
fi

done
done
