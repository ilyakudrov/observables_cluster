#!/bin/bash
job_num=512
log_path="/home/clusters/rrcmpi/kudrov/observables/logs/wilson_loop"
for((i=1;i<= ${job_num};i++))
do
qsub -q long -F "$i" -d $log_path /home/clusters/rrcmpi/kudrov/observables/scripts/do_wilson.sh
while [ $? -ne 0 ]
do
qsub -q long -F "$i" -d $log_path /home/clusters/rrcmpi/kudrov/observables/scripts/do_wilson.sh
done
done

