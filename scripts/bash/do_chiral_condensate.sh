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

if [[ ${copy} != 0 ]]; then
conf_path_end1="_${copy}${conf_path_end}"
else
conf_path_end1="${conf_path_end}"
fi

conf_path="${conf_path_start}/${chain}/${conf_name}`printf %0${padding}d $i`${conf_path_end1}"

echo "conf_path" ${conf_path}

if [ -f ${conf_path} ] && [ -s ${conf_path} ] ; then

if [[ ${copy} == 0 ]]; then
output_path_cond="${output_path}/ChiralCond_`printf %0${padding}d $i`.txt"
else
output_path_conf="${output_path}/ChiralCond_`printf %0${padding}d $i`_${copy}.txt"
fi

echo "output_path_cond" ${output_path_cond}

if [[ ! -f ${output_path_cond} ]] || [ ! $calculate_absent -eq 1 ] ; then

echo output_path ${output_path}
mkdir -p ${output_path}
output_path1=${output_path_cond}

cd ${output_path}

parameters="${conf_path} --calc -p ${conf_path_start}/param_last.txt --calc-postfix _`printf %0${padding}d $i` --binout --debug 1 --obs-ChiralCond 0"

/lustre/rrcmpi/goy/qc2dstag/bin/qc2dstagEO $parameters

fi
fi

done
done
