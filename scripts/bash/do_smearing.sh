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

echo ${conf_path1}

if [ -f ${conf_path1} ] && [ -s ${conf_path1} ]; then

if [ ${wilson_enabled} -eq 1 ] ; then
mkdir -p ${path_wilson}
fi

if [ ${polyakov_correlator_enabled} -eq 1 ] ; then
mkdir -p ${path_polyakov_correlator}
fi

if [ ${polyakov_loop_enabled} -eq 1 ] ; then
mkdir -p ${path_polyakov_loop}
fi

if [ ${save_conf} -eq 1 ] ; then
mkdir -p ${conf_path_output}
fi

if [[ ${gauge_copies} == 0 ]]; then
output_smeared="${conf_path_output}/smeared_`printf %04d $i`"
output_wilson="${path_wilson}/wilson_loop_`printf %04d $i`"
output_polyakov_correlator="${path_polyakov_correlator}/polyakov_correlator_`printf %04d $i`"
output_polyakov_loop="${path_polyakov_loop}/polyakov_loop_`printf %04d $i`"
else
output_smeared="${conf_path_output}/smeared_`printf %04d $i`_${copy}"
output_wilson="${path_wilson}/wilson_loop_`printf %04d $i`_${copy}"
output_polyakov_correlator="${path_polyakov_correlator}/polyakov_correlator_`printf %04d $i`_${copy}"
output_polyakov_loop="${path_polyakov_loop}/polyakov_loop_`printf %04d $i`_${copy}"
fi

echo "output_smeared" "${output_smeared}"

if [[ ! "${output_smeared}" ]] || [ ! $calculate_absent -eq 1 ] ; then

#-conf_format_plaket ${conf_format_plaket1} -conf_path_plaket ${conf_path_plaket1} -bytes_skip_plaket ${bytes_skip_plaket1}\

parameters="--conf_format ${conf_format} --conf_path ${conf_path1} --bytes_skip ${bytes_skip} --convert ${convert}\
    --HYP_alpha1 ${HYP_alpha1} --HYP_alpha2 ${HYP_alpha2} --HYP_alpha3 ${HYP_alpha3} --file_precision ${file_precision}\
    --APE_alpha ${APE_alpha} --APE_enabled ${APE_enabled} --HYP_enabled ${HYP_enabled} --polyakov_loop_enabled ${polyakov_loop_enabled}\
    --APE_steps ${APE_steps} --HYP_steps ${HYP_steps} --L_spat ${L_spat} --L_time ${L_time} --path_polyakov_loop ${output_polyakov_loop}\
    --path_wilson ${output_wilson} --path_polyakov_correlator ${output_polyakov_correlator}\
    --wilson_enabled ${wilson_enabled} --polyakov_correlator_enabled ${polyakov_correlator_enabled} --correlator_type ${polyakov_correlator_type}\
    --T_min ${T_min} --T_max ${T_max} --R_min ${R_min} --R_max ${R_max} --calculation_step_APE ${calculation_step_APE}\
    --polyakov_correlator_D ${polyakov_correlator_D} --calculation_step_HYP ${calculation_step_HYP} --calculation_HYP_start ${calculation_HYP_start}\
    --calculation_APE_start ${calculation_APE_start} --save_conf ${save_conf} --conf_path_output ${output_smeared}"

/home/clusters/rrcmpi/kudrov/general_code/apps/smearing/smearing_${matrix_type_wilson}_${matrix_type_plaket}_${arch} $parameters

fi
fi
fi

done
done
