#!/bin/bash
base_paths=($base_paths)
lattice_sizes=($lattice_sizes)
velocities=($velocities)
boundaries=($boundaries)
betas=($betas)
for((i=0;i<${#base_paths[@]};i++))
do
result_path="/home/clusters/rrcmpi/kudrov/observables/result/eos_rotation_imaginary/${lattice_sizes[i]}/${boundaries[i]}/${velocities[i]}/${betas[i]}"
#echo --base_path ${base_paths[i]} --lattice_size ${lattice_sizes[i]} --velocity ${velocities[i]}\
# --boundary ${boundaries[i]} --beta ${betas[i]} --result_path ${result_path} ${add_parameters[@]}
python3 /home/clusters/rrcmpi/kudrov/observables/code/python/eos_rotation_imaginary/average.py --base_path ${base_paths[i]} --lattice_size ${lattice_sizes[i]} --velocity ${velocities[i]}\
 --boundary ${boundaries[i]} --beta ${betas[i]} --result_path ${result_path} ${add_parameters[@]}
done
