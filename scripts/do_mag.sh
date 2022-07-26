#!/bin/bash

for((i=${conf_start};i<=${conf_end};i++))
do

if [[ ${conf_path_end} == "/" ]]; then

conf_path_end=""

fi

path_conf="${conf_path_start}`printf %0${padding}d $i`${conf_path_end}"

if [ -f ${path_conf} ] && [ -s ${path_conf} ] ; then

mkdir -p ${output_path_confs_gaugefixed}
mkdir -p ${output_path_conf_spin}
mkdir -p ${output_path_functional}

path_conf_output="${output_path_confs_gaugefixed}/conf_`printf %04d $i`"
path_spins_output="${output_path_conf_spin}/spins_`printf %04d $i`"
path_previous="${output_path_conf_spin}/spins_`printf %04d $i`"
path_functional_output="${output_path_functional}/functional_`printf %04d $i`"

parameters="-conf_format ${conf_format} -path_conf $path_conf -conf_format ${conf_format} -bytes_skip ${bites_skip} \
    -path_spins_output ${path_spins_output} -path_conf_output ${path_conf_output} -path_previous ${path_previous} -path_functional_output ${path_functional_output}\
    -T_step ${T_step} -T_init ${T_init} -T_final ${T_final} -OR_steps ${OR_steps} -thermalization_steps ${thermalization_steps}\
    -tolerance_maximal ${tolerance_maximal} -tolerance_average ${tolerance_average} -tolerance_digits ${tolerance_digits} -gauge_copies ${gauge_copies} -is_new_trial ${is_new_trial}\
    -is_final ${is_final} -is_compare ${is_compare} -is_compare_spins ${is_compare_spins} -is_functional_save ${is_functional_save}
    -x_size ${L_spat} -y_size ${L_spat} -z_size ${L_spat} -t_size ${L_time}"

/home/clusters/rrcmpi/kudrov/general_code/mag_su2/mag_fixation_${arch} $parameters

fi

done
