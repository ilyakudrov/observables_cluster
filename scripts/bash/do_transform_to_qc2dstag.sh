#!/bin/bash

for((i=${conf_start};i<=${conf_end};i++))
do

if [[ ${conf_path_end} == "/" ]]; then
conf_path_end=""
fi

if [[ ${gauge_copies} == 0 ]]; then
starting_copy=0
else
starting_copy=1
fi

for((copy=${starting_copy};copy<=${gauge_copies};copy++))
do

conf_path="${conf_path_start}/${chain}/${conf_name}`printf %0${padding}d $i`${conf_path_end}"

if [[ ${copy} == 0 ]]; then
conf_path="${conf_path}"
else
conf_path="${conf_path}_${copy}"
fi

echo ${conf_path}

if [ -f ${conf_path} ] && [ -s ${conf_path} ]; then

mkdir -p "${conf_path_start}/qc2dstag/${chain}"

if [[ ${copy} == 0 ]]; then
conf_path_output="${conf_path_start}/qc2dstag/${chain}/${conf_name}`printf %0${padding}d $i`${conf_path_end}"
else
conf_path_output="${conf_path_start}/qc2dstag/${chain}/${conf_name}`printf %0${padding}d $i`_${copy}${conf_path_end}"
fi

echo "conf_path_output" "${conf_path_output}"

if [[ ! "${conf_path_output}" ]] || [ ! $calculate_absent -eq 1 ] ; then

parameters="-conf_format ${conf_format} -conf_path ${conf_path} -bytes_skip ${bytes_skip} -convert ${convert}\
    -L_spat ${L_spat} -L_time ${L_time} -conf_path_output ${conf_path_output}"

/home/clusters/rrcmpi/kudrov/general_code/apps/conf_transform/transform_to_qc2dstag_${matrix_type}_${arch} $parameters

fi
fi
fi

done
done
