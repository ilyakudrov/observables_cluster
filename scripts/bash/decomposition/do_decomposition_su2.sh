#!/bin/bash

for((i=${conf_start};i<=${conf_end};i++))
do

if [[ ${conf_path_end} == "/" ]]; then

conf_path_end=""

fi

path_conf="${conf_path_start}`printf %0${padding}d $i`${conf_path_end}"
path_conf_monopole1="${path_conf_monopole}/conf_monopole_`printf %04d $i`"
path_conf_monopoless1="${path_conf_monopoless}/conf_monopoless_`printf %04d $i`"

echo path_conf ${path_conf}
echo path_conf_monopole ${path_conf_monopole}
echo path_conf_monopoless ${path_conf_monopoless}

if [ -f ${path_conf} ] && [ -s ${path_conf} ] && [ -f ${path_inverse_laplacian} ] && [ -s ${path_inverse_laplacian} ]; then

mkdir -p ${path_conf_monopole}
mkdir -p ${path_conf_monopoless}

parameters="-conf_format ${conf_format} -path_conf $path_conf -bytes_skip ${bytes_skip} \
    -path_conf_monopole ${path_conf_monopole1} -path_conf_monopoless ${path_conf_monopoless1} -path_inverse_laplacian ${path_inverse_laplacian}\
    -x_size ${L_spat} -y_size ${L_spat} -z_size ${L_spat} -t_size ${L_time}"

/home/clusters/rrcmpi/kudrov/general_code/apps/monopole_decomposition_su2/decomposition_${arch} $parameters

fi

done
