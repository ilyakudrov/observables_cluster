#!/bin/bash
conf_size="40^4"
conf_type="qc2dstag"
#smearing="HYP2_APE"
#smearing="unsmeared"
HYP_steps=2

x_trans=0

for mu in "0.05" "0.35" "0.45"
#for mu in "0.05"
do

source "/lustre/rrcmpi/kudrov/conf/${conf_type}/${conf_size}/mu${mu}/parameters"
script_path="/home/clusters/rrcmpi/kudrov/observables_cluster/scripts/do_flux_wilson.sh"

#chains=( "s0" "s1" )
#conf_start=( 202 202 )
#conf_end=( 210 210 )

for monopole in "/" "monopole" "monopoless"
#for monopole in "/"
do

if [[ $monopole == "/" ]] ; then

matrix_type="su2"
conf_format="double_qc2dstag"
smeared_format="double"
smearing="HYP${HYP_steps}_APE${APE_steps_flux}"

elif [[ $monopole == "monopole" ]] ; then

matrix_type="abelian"
conf_format="double_fortran"
smeared_format="double_fortran"
smearing="unsmeared"

elif [[ $monopole == "monopoless" ]] ; then

matrix_type="su2"
conf_format="double_fortran"
smearing="HYP${HYP_steps}_APE${APE_steps_decomposition_flux}"
smeared_format="double"

else

echo wrong monopole ${monopole}

fi

calculate_absent=false

number_of_jobs=100
confs_total=0

for i  in ${!chains[@]} ; do
confs_total=$(( $confs_total + ${conf_end[$i]} - ${conf_start[$i]} + 1 ))
done

confs_per_job=$(( ${confs_total} / ${number_of_jobs} + 1 ))
chain_current=0
jobs_done=0

for((i=0;i<${number_of_jobs};i++))
do

conf1=$(( ${conf_start[$chain_current]} + ${confs_per_job} * ($i - ${jobs_done}) ))
conf2=$(( ${conf_start[$chain_current]} + ${confs_per_job} * ($i - ${jobs_done} + 1) - 1 ))

if [[ $conf2 -ge ${conf_end[$chain_current]} ]] ; then
conf2=$(( ${conf_end[$chain_current]} ))
fi

if [[ $chain_current -ge ${#chains[@]} ]] ; then
break
fi

log_path="/home/clusters/rrcmpi/kudrov/observables_cluster/logs/flux_tube_wilson/${monopole}/${conf_type}/${conf_size}/mu${mu}/${chains[${chain_current}]}"
mkdir -p ${log_path}

a1=$((${conf1}/1000))
b1=$(((${conf1}-$a1*1000)/100))
c1=$(((${conf1}-$a1*1000-$b1*100)/10))
d1=$((${conf1}-$a1*1000-$b1*100-$c1*10))

a2=$((${conf2}/1000))
b2=$(((${conf2}-$a2*1000)/100))
c2=$(((${conf2}-$a2*1000-$b2*100)/10))
d2=$((${conf2}-$a2*1000-$b2*100-$c2*10))

qsub -q long -v conf_format=${conf_format},smeared_format=${smeared_format},chain=${chains[$chain_current]},mu=${mu},smearing=${smearing},conf_size=${conf_size},conf_type=${conf_type},monopole=${monopole},\
L_spat=${L_spat},L_time=${L_time},x_trans=${x_trans},matrix_type=${matrix_type},conf1=${conf1},conf2=${conf2},\
 -o "${log_path}/$a1$b1$c1$d1-$a2$b2$c2$d2.o" -e "${log_path}/$a1$b1$c1$d1-$a2$b2$c2$d2.e" ${script_path}
while [ $? -ne 0 ]
do
qsub -q long -v conf_format=${conf_format},smeared_format=${smeared_format},chain=${chains[$chain_current]},mu=${mu},smearing=${smearing},conf_size=${conf_size},conf_type=${conf_type},monopole=${monopole},\
L_spat=${L_spat},L_time=${L_time},x_trans=${x_trans},matrix_type=${matrix_type},conf1=${conf1},conf2=${conf2},\
 -o "${log_path}/$a1$b1$c1$d1-$a2$b2$c2$d2.o" -e "${log_path}/$a1$b1$c1$d1-$a2$b2$c2$d2.e" ${script_path}
done

if [[ $conf2 -ge ${conf_end[$chain_current]} ]] ; then
chain_current=$(( $chain_current + 1 ))
jobs_done=$(( ${i} + 1 ))
fi

done
done

done

