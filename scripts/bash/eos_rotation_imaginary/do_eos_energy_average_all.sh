#!/bin/bash
base_paths=($base_paths)
lattice_sizes=($lattice_sizes)
velocities=($velocities)
boundaries=($boundaries)
betas=($betas)
for((i=0;i<${#base_paths[@]};i++))
do
result_path="/home/clusters/rrcmpi/kudrov/observables/result/eos_rotation_imaginary/${lattice_size[i]}/${boundary[i]}/${velocity[i]}/${beta[i]}"
python3 /home/clusters/rrcmpi/kudrov/observables/code/python/eos_rotation_imaginary/average.py --base_path ${base_path[i]} --lattice_size ${lattice_size[i]} --velocity ${velocity[i]}\
 --boundary ${boundary[i]} --beta ${beta[i]} --result_path ${result_path} ${add_parameters[@]}
done
