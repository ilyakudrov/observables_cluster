#!/bin/bash
conf_size="40^4"
mu="0.05"
smearing="unsmeared"

#T_min=4
#T_max=10
#R_min="4.9"
#R_max=20

source "/lustre/rrcmpi/kudrov/conf/${conf_size}/mu${mu}/parameters"

conf_format="double_fortran"
#conf_format="double"
matrix_type="abelian"
#monopole="monopoless"
#monopole=""
monopole="monopole"
axis="on-axis"

#mu0.05
#chains=( "s0" "s1" "s2" "s3" "s4" )
#conf_start=( 201 0 0 0 0 )
#conf_end=( 637 436 423 433 419 )

chains=( "s0" )
conf_start=( 201 )
conf_end=( 637 )

T_min=4
T_max=20
R_min="4.9"
R_max="20.1"

#T_min=4
#T_max=5
#R_min="4.9"
#R_max="6.1"

script_path="/home/clusters/rrcmpi/kudrov/observables_cluster/scripts/do_wilson.sh"

for j in "${!chains[@]}"; do

for((i=${conf_start[j]};i<=${conf_end[j]};i++))
do

a=$(($i/1000))
b=$((($i-$a*1000)/100))
c=$((($i-$a*1000-$b*100)/10))
d=$(($i-$a*1000-$b*100-$c*10))

log_path="/home/clusters/rrcmpi/kudrov/observables_cluster/logs/wilson_loop/${axis}/${monopole}/qc2dstag/${conf_size}/mu${mu}/${chains[j]}"
mkdir -p ${log_path}

#conf_path="/home/clusters/rrcmpi/kudrov/smearing_cluster/confs_smeared/${conf_type}/${conf_size}/${smearing}/mu${mu}/${chains[j]}/conf_APE_alpha=0.7_$a$b$c$d"
#conf_path="/home/clusters/rrcmpi/kudrov/smearing_cluster/confs_smeared/${monopole}/qc2dstag/${conf_size}/HYP6_APE/mu${mu}/${chains[j]}/conf_APE_alpha=0.7_$a$b$c$d"
conf_path="/home/clusters/rrcmpi/kudrov/decomposition/confs_decomposed/${monopole}/qc2dstag/${conf_size}/mu${mu}/${chains[j]}/conf_monopole_$a$b$c$d"
#conf_path="/home/clusters/rrcmpi/kudrov/decomposition/confs_decomposed/test/${monopole}/qc2dstag/${conf_size}/mu${mu}/${chains[j]}/conf_monopole_$a$b$c$d"
#conf_path="/home/clusters/rrcmpi/kudrov/smearing_cluster/confs_smeared/${monopole}/qc2dstag/${conf_size}/${smearing}/mu${mu}/conf_APE_alpha=0.7_$a$b$c$d"

#output_path_wilson="/home/clusters/rrcmpi/kudrov/observables_cluster/result/wilson_loop/${conf_type}/${conf_size}/${smearing}/mu${mu}/${chains[j]}"
output_path_wilson="/home/clusters/rrcmpi/kudrov/observables_cluster/result/wilson_loop/${axis}/${monopole}/${conf_type}/${conf_size}/${smearing}/mu${mu}/${chains[j]}"
#output_path_wilson="/home/clusters/rrcmpi/kudrov/observables_cluster/result/wilson_loop/test/${axis}/${monopole}/${conf_type}/${conf_size}/${smearing}/mu${mu}/${chains[j]}"
mkdir -p ${output_path_wilson}
output_path_wilson="${output_path_wilson}/wilson_loop_$a$b$c$d"

if [ -f ${path_conf} ] ; then

qsub -q long -v conf_format=${conf_format},conf_path=${conf_path},output_path_wilson=${output_path_wilson},matrix_type=${matrix_type},\
L_spat=${L_spat},L_time=${L_time},T_min=${T_min},T_max=${T_max},R_min=${R_min},R_max=${R_max},\
 -o "${log_path}/$a$b$c$d.o" -e "${log_path}/$a$b$c$d.e" ${script_path}
while [ $? -ne 0 ]
do
qsub -q long -v conf_format=${conf_format},path_conf=${path_conf},output_path_wilson=${output_path_wilson},matrix_type=${matrix_type},\
L_spat=${L_spat},L_time=${L_time},T_min=${T_min},T_max=${T_max},R_min=${R_min},R_max=${R_max},\
 -o "${log_path}/$a$b$c$d.o" -e "${log_path}/$a$b$c$d.e" ${script_path}
done

fi

done
done
