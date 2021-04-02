#!/bin/bash
conf_type="qc2dstag"
parameters_dir="/home/clusters/rrcmpi/kudrov/matrix_parameters"
source ${parameters_dir}/${conf_type}
smearing="/HYP_APE"
T_min=4
T_max=10
R_min="4.9"
R_max=20

i=$1
a=$(($i/1000))
b=$((($i-$a*1000)/100))
c=$((($i-$a*1000-$b*100)/10))
d=$(($i-$a*1000-$b*100-$c*10))
for mu in 5 #10 15 25 30
do
w=$(($mu/10))
q=$(($mu-$w*10))

#conf_path="/lustre/rrcmpi/vborn/SU2_dinam/MAG/mu0p${mu}_b1p8_m0p0075_lam0p00075/MON_WL/CON_MON_MAG_${a}${b}${c}${d}.LAT"
#conf_path="/home/clusters/rrcmpi/kudrov/smearing/conf/HYP_APE/time_32/mu0.00/conf_HYP_APE_${a}${b}${c}${d}.fl"
#conf_path="/home/clusters/rrcmpi/kudrov/smearing/conf/APE/time_32/mu0.$w$q/conf_APE_${a}${b}${c}${d}.fl"
#conf_path="/home/clusters/rrcmpi/nikolaev/SU_2_staggered/configurations/N_f=2/improved/32^3x32/mu=0.$w$q/beta=1.8/ma=0.0075/lambda=0.00075/converted_Fort/conf_$a$b$c$d.fl"
#conf_path="/home/clusters/rrcmpi/kudrov/smearing/conf/mag/APE/mu0.$w$q/smeared_${a}${b}${c}${d}"
#conf_path="/lustre/rrcmpi/vborn/SU2_dinam/MAG/mu0p${mu}_b1p8_m0p0075_lam0p00075/OFFD/CON_OFF_MAG_${a}${b}${c}${d}.LAT"
#conf_path="/home/clusters/rrcmpi/kudrov/smearing/conf/mag/HYP_APE/mu0.$w$q/smeared_$a$b$c$d"
#conf_path="/home/clusters/rrcmpi/kudrov/conf/qc2dstag/mu0.$w$q/CONF${a}${b}${c}${d}"
conf_path="/home/clusters/rrcmpi/kudrov/smearing/conf/${conf_type}${smearing}/mu0.$w$q/smeared_${a}${b}${c}${d}"
output_path_wilson="/home/clusters/rrcmpi/kudrov/observables/result/wilson_loop/${conf_type}${smearing}/mu0.$w$q/wilson_loop_$a$b$c$d"
output_path_sizes="/home/clusters/rrcmpi/kudrov/observables/result/wilson_loop/${conf_type}${smearing}/mu0.$w$q/sizes_$a$b$c$d"

parameters="-conf_format $conf_format -conf_path $conf_path -output_path_wilson $output_path_wilson -output_path_sizes $output_path_sizes -L_spat ${L_spat} -L_time ${L_time} -T_min ${T_min} -T_max ${T_max} -R_min ${R_min} -R_max ${R_max}"

if [ -f ${conf_path} ] ; then
	/home/clusters/rrcmpi/kudrov/observables/code/exe/wilson_${matrix_type} $parameters
fi

if false; then
if test $i -lt 1000; then
#conf_path="/lustre/rrcmpi/vborn/SU2_dinam/MAG/mu0p${mu}_b1p8_m0p0075_lam0p00075/MON_WL/CON_MON_MAG_${b}${c}${d}.LAT"
#conf_path="/home/clusters/rrcmpi/kudrov/conf/qc2dstag/mu0.$w$q/CONF${b}${c}${d}"
conf_path="/home/clusters/rrcmpi/kudrov/smearing/conf/${conf_type}${smearing}/mu0.$w$q/smeared_${b}${c}${d}"

parameters="-conf_format $conf_format -conf_path $conf_path -output_path_wilson $output_path_wilson -output_path_sizes $output_path_sizes -L_spat ${L_spat} -L_time ${L_time} -T_min ${T_min} -T_max ${T_max} -R_min ${R_min} -R_max ${R_max}"

if test -f ${conf_path}; then
        /home/clusters/rrcmpi/kudrov/observables/code/exe/wilson_${matrix_type} $parameters
fi
fi
fi
done
