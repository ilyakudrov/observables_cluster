#!/bin/bash

for((i=${conf_start};i<=${conf_end};i++))
do

if [[ ${conf_path_end} == "/" ]]; then

conf_path_end=""

fi

path_conf="${conf_path_start}`printf %0${padding}d $i`${conf_path_end}"

echo path_conf ${path_conf}

if [ -f ${path_conf} ] && [ -s ${path_conf} ] && [ -f ${path_inverse_laplacian} ] && [ -s ${path_inverse_laplacian} ]; then

mkdir -p ${path_functional}
mkdir -p ${path_wilson_loops_abelian}
mkdir -p ${path_wilson_loops_monopole}
mkdir -p ${path_clusters_unwrapped_abelian}
mkdir -p ${path_clusters_unwrapped_monopole}
mkdir -p ${path_clusters_unwrapped_monopoless}
mkdir -p ${path_clusters_wrapped_abelian}
mkdir -p ${path_clusters_wrapped_monopole}
mkdir -p ${path_clusters_wrapped_monopoless}
mkdir -p ${path_windings_abelian}
mkdir -p ${path_windings_monopole}
mkdir -p ${path_windings_monopoless}

path_functional_output="${path_functional}/functional_`printf %04d $i`"
path_wilson_loops_abelian_output="${path_wilson_loops_abelian}/wilson_loops_`printf %04d $i`"
path_wilson_loops_monopole_output="${path_wilson_loops_monopole}/wilson_loops_`printf %04d $i`"
path_clusters_unwrapped_abelian_output="${path_clusters_unwrapped_abelian}/clusters_unwrapped_`printf %04d $i`"
path_clusters_unwrapped_monopole_output="${path_clusters_unwrapped_monopole}/clusters_unwrapped_`printf %04d $i`"
path_clusters_unwrapped_monopoless_output="${path_clusters_unwrapped_monopoless}/clusters_unwrapped_`printf %04d $i`"
path_clusters_wrapped_abelian_output="${path_clusters_wrapped_abelian}/clusters_wrapped_`printf %04d $i`"
path_clusters_wrapped_monopole_output="${path_clusters_wrapped_monopole}/clusters_wrapped_`printf %04d $i`"
path_clusters_wrapped_monopoless_output="${path_clusters_wrapped_monopoless}/clusters_wrapped_`printf %04d $i`"
path_windings_abelian_output="${path_windings_abelian}/windings_`printf %04d $i`"
path_windings_monopole_output="${path_windings_monopole}/windings_`printf %04d $i`"
path_windings_monopoless_output="${path_windings_monopoless}/windings_`printf %04d $i`"

parameters="--conf_format ${conf_format} --path_conf $path_conf --bytes_skip ${bytes_skip} --file_precision ${file_precision}\
    --path_inverse_laplacian ${path_inverse_laplacian} --N_dir_gevp ${N_dir_gevp} --HYP_alpha1 ${HYP_alpha1} --HYP_alpha2 ${HYP_alpha2} --HYP_alpha3 ${HYP_alpha3}\
    --path_wilson_loops_abelian_output ${path_wilson_loops_abelian_output} --path_wilson_loops_monopole_output ${path_wilson_loops_monopole_output} --copies_required ${copies_required} --path_functional_output ${path_functional_output} \
    --path_clusters_unwrapped_abelian_output ${path_clusters_unwrapped_abelian_output} --path_clusters_unwrapped_monopole_output ${path_clusters_unwrapped_monopole_output} --path_clusters_unwrapped_monopoless_output ${path_clusters_unwrapped_monopoless_output} \
    --path_clusters_wrapped_abelian_output ${path_clusters_wrapped_abelian_output} --path_clusters_wrapped_monopole_output ${path_clusters_wrapped_monopole_output} --path_clusters_wrapped_monopoless_output ${path_clusters_wrapped_monopoless_output} \
    --path_windings_abelian_output ${path_windings_abelian_output} --path_windings_monopole_output ${path_windings_monopole_output} --path_windings_monopoless_output ${path_windings_monopoless_output} \
    --APE_alpha ${APE_alpha} --APE_steps ${APE_steps} --calculation_step_APE ${calculation_step_APE} --calculation_APE_start ${calculation_APE_start} --HYP_steps ${HYP_steps} \
    --x_size ${L_spat} --y_size ${L_spat} --z_size ${L_spat} --t_size ${L_time}"

/home/clusters/rrcmpi/kudrov/general_code/apps/monopole_decomposition_su2/functional_dependence_${arch} $parameters

fi
done
