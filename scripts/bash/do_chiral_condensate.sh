#!/bin/bash
gpu_pstate=$(nvidia-smi --query-gpu=pstate --format=csv,noheader)
if [ ${gpu_pstate:1:1} -lt 8 ]; then
GPU=1
else
GPU=0
fi

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
#output_path_cond="${output_path}/ChiralCond_`printf %0${padding}d $conf_start`-`printf %0${padding}d $conf_end`.txt"
output_path_cond="${output_path}/ChiralCond_`printf %0${padding}d $i`.txt"
else
output_path_cond="${output_path}/ChiralCond_`printf %0${padding}d $i`_${copy}.txt"
fi

echo "output_path_cond" ${output_path_cond}

if [[ ! -f ${output_path_cond} ]] || [ ! $calculate_absent -eq 1 ] ; then

echo output_path ${output_path}
mkdir -p ${output_path}
output_path1=${output_path_cond}

cd ${output_path}

#parameters="--calc --rnd-gpu-seed -p ${conf_path_start}/param_last.txt -c ${conf_path_start} --calc-postfix _`printf %0${padding}d $conf_start`-`printf %0${padding}d $conf_end`\
# -i $conf_start:$conf_end --binout --debug 1 --obs-ChiralCond 0"
parameters="${conf_path} --calc --rnd-gpu-seed -p ${conf_path_start}/param_last.txt --calc-postfix _`printf %0${padding}d $i`\
 --binout --debug 1 --obs-ChiralCond 0 -d $GPU"

/lustre/rrcmpi/goy/qc2dstag/bin/qc2dstagEO $parameters

fi
fi

done
done
