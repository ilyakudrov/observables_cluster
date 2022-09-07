#!/bin/bash

for((i=${conf_start};i<=${conf_end};i++))
do

if [[ ${conf_path_end_plaket} == "/" ]]; then

conf_path_end_plaket=""

fi

if [[ ${conf_path_end_wilson} == "/" ]]; then

conf_path_end_wilson=""

fi

conf_path_plaket1="${conf_path_start_plaket}`printf %0${padding}d $i`${conf_path_end_plaket}"
conf_path_wilson1="${conf_path_start_wilson}`printf %0${padding}d $i`${conf_path_end_wilson}"

if [ -f ${conf_path_wilson1} ] && [ -s ${conf_path_wilson1} ] ; then

mkdir -p ${path_wilson}
# mkdir -p ${path_conf_flux_tube}

#-conf_format_plaket ${conf_format_plaket1} -conf_path_plaket ${conf_path_plaket1} -bytes_skip_plaket ${bytes_skip_plaket1}\

parameters="-conf_format_wilson ${conf_format_wilson} -conf_path_wilson ${conf_path_wilson1} -bytes_skip_wilson ${bytes_skip_wilson}\
    -HYP_alpha1 ${HYP_alpha1} -HYP_alpha2 ${HYP_alpha2} -HYP_alpha3 ${HYP_alpha3}\
    -APE_alpha ${APE_alpha} -APE_enabled ${APE_enabled} -HYP_enabled ${HYP_enabled}\
    -APE_steps ${APE_steps} -HYP_steps ${HYP_steps} -L_spat ${L_spat} -L_time ${L_time}\
    -path_wilson ${path_wilson}/wilson_loop_`printf %04d $i` -path_flux ${path_flux}/flux_tube_`printf %04d $i`\
    -wilson_enabled ${wilson_enabled} -flux_enabled ${flux_enabled}\
    -T_min ${T_min} -T_max ${T_max} -R_min ${R_min} -R_max ${R_max} -calculation_step_APE ${calculation_step_APE}\
    -calculation_APE_start ${calculation_APE_start}"

/home/clusters/rrcmpi/kudrov/general_code/apps/smearing/smearing_${matrix_type_wilson}_${matrix_type_plaket}_${arch} $parameters

fi

done