#!/bin/bash
conf_type="mon_wl"
smearing=""
for((i=1;i<=1300;i++))
do
a=$(($i/1000))
b=$((($i-$a*1000)/100))
c=$((($i-$a*1000-$b*100)/10))
d=$(($i-$a*1000-$b*100-$c*10))
for mu in 0 10 15 25 30 40
do
w=$(($mu/10))
q=$(($mu-$w*10))
#conf_path="/lustre/rrcmpi/vborn/SU2_dinam/MAG/mu0p${mu}_b1p8_m0p0075_lam0p00075/OFFD/CON_OFF_MAG_${b}${c}${d}.LAT"
#if ! test -f ${conf_path}; then
rm /home/clusters/rrcmpi/kudrov/observables/result/flux_tube/${conf_type}${smearing}/mu0.$w$q/T=8/R=8/electric_${a}${b}${c}${d}
rm /home/clusters/rrcmpi/kudrov/observables/result/flux_tube/${conf_type}${smearing}/mu0.$w$q/T=8/R=8/magnetic_${a}${b}${c}${d}
#echo $i
#fi
done
done
