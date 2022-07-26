GCC=/home/itep/kudrov/installed/gcc-9/bin/g++
SRC_PATH=/home/clusters/rrcmpi/kudrov/general_code/lib/cpu/src
INCLUDE_PATH=/home/clusters/rrcmpi/kudrov/general_code/lib/cpu/include
OBJ_PATH=/home/clusters/rrcmpi/kudrov/general_code/lib/cpu/obj
OBJ_FILES=$(OBJ_PATH)/link_$(ARCH).o $(OBJ_PATH)/data_$(ARCH).o $(OBJ_PATH)/basic_observables_$(ARCH).o $(OBJ_PATH)/flux_tube_$(ARCH).o $(OBJ_PATH)/matrix_$(ARCH).o \
$(OBJ_PATH)/smearing_$(ARCH).o $(OBJ_PATH)/monopoles_$(ARCH).o $(OBJ_PATH)/loop_$(ARCH).o $(OBJ_PATH)/eigen_$(ARCH).o $(OBJ_PATH)/abelian_projection_su3_$(ARCH).o \
$(OBJ_PATH)/Landau_gauge_$(ARCH).o $(OBJ_PATH)/mag_$(ARCH).o
C_PATH=/home/clusters/rrcmpi/kudrov/general_code/lib/cpu/src/c-lime
C_FILES=$(C_PATH)/lime_fseeko.c  $(C_PATH)/lime_header.c  $(C_PATH)/lime_reader.c  $(C_PATH)/lime_utils.c  $(C_PATH)/lime_writer.c
FLOAT=double
FLAGS=-Ofast -fopenmp -march=native -mtune=native
ARCH=rrcmpi
MATRIX_PLAKET=abelian
MATRIX_WILSON=su2
MATRIX=abelian


flux_wilson: flux_wilson_$(ARCH).o $(OBJ_FILES)
	$(GCC) flux_wilson_$(ARCH).o $(OBJ_FILES) $(C_FILES) -o exe/flux_wilson_$(MATRIX_PLAKET)_$(MATRIX_WILSON)_$(ARCH)
	rm flux_wilson.o
flux_wilson_$(ARCH).o: flux_wilson.cpp
	$(GCC) -O3 -c flux_wilson.cpp -I$(INCLUDE_PATH) $(FLAGS) -DMATRIX_WILSON=$(MATRIX_WILSON) -DMATRIX_PLAKET=$(MATRIX_PLAKET) -o flux_wilson_$(ARCH).o

flux_wilson_tr: flux_wilson_tr_$(ARCH).o $(OBJ_FILES)
	$(GCC) flux_wilson_tr_$(ARCH).o $(OBJ_FILES) $(C_FILES) -o exe/flux_wilson_tr_$(MATRIX_PLAKET)_$(MATRIX_WILSON)_$(ARCH)
	rm flux_wilson_tr_$(ARCH).o
flux_wilson_tr_$(ARCH).o: flux_wilson_tr.cpp
	$(GCC) -O3 -c flux_wilson_tr.cpp -I$(INCLUDE_PATH) $(FLAGS) -DMATRIX_WILSON=$(MATRIX_WILSON) -DMATRIX_PLAKET=$(MATRIX_PLAKET) -o flux_wilson_tr_$(ARCH).o

wilson_on-axis: wilson_on-axis_$(ARCH).o $(OBJ_FILES)
	$(GCC) wilson_on-axis_$(ARCH).o $(OBJ_FILES) $(C_FILES) -o exe/wilson_on-axis_$(MATRIX)_$(ARCH)
	rm wilson_on-axis_$(ARCH).o
wilson_on-axis_$(ARCH).o: wilson_on-axis.cpp
	$(GCC) -O3 -c wilson_on-axis.cpp -I$(INCLUDE_PATH) $(FLAGS) -DMATRIX_WILSON=$(MATRIX) -o wilson_on-axis_$(ARCH).o

wilson_adjoint_on-axis: wilson_adjoint_on-axis_$(ARCH).o $(OBJ_FILES)
	$(GCC) wilson_adjoint_on-axis_$(ARCH).o $(OBJ_FILES) $(C_FILES) -o exe/wilson_adjoint_on-axis_$(MATRIX)_$(ARCH)
	rm wilson_adjoint_on-axis_$(ARCH).o
wilson_adjoint_on-axis_$(ARCH).o: wilson_adjoint_on-axis.cpp
	$(GCC) -O3 -c wilson_adjoint_on-axis.cpp -I$(INCLUDE_PATH) $(FLAGS) -DMATRIX_WILSON=$(MATRIX) -o wilson_adjoint_on-axis_$(ARCH).o

wilson_off-axis: wilson_off-axis_$(ARCH).o $(OBJ_FILES)
	$(GCC) wilson_off-axis_$(ARCH).o $(OBJ_FILES) $(C_FILES) -o exe/wilson_off-axis_$(MATRIX)_$(ARCH)
	rm wilson_off-axis_$(ARCH).o
wilson_off-axis_$(ARCH).o: wilson_off-axis.cpp
	$(GCC) -O3 -c wilson_off-axis.cpp -I$(INCLUDE_PATH) $(FLAGS) -DMATRIX_WILSON=$(MATRIX) -o wilson_off-axis_$(ARCH).o

wilson_spatial: wilson_spatial_$(ARCH).o $(OBJ_FILES)
	$(GCC) wilson_spatial_$(ARCH).o $(OBJ_FILES) -o exe/wilson_spatial_$(MATRIX)_$(ARCH)
	rm wilson_spatial_$(ARCH).o
wilson_spatial_$(ARCH).o: wilson_spatial.cpp
	$(GCC) -O3 -c wilson_spatial.cpp -I$(INCLUDE_PATH) $(FLAGS) -DMATRIX_WILSON=$(MATRIX) -o wilson_spatial_$(ARCH).o

flux_wilson_x: flux_wilson_x_$(ARCH).o $(OBJ_FILES)
	$(GCC) flux_wilson_x_$(ARCH).o $(OBJ_FILES) -o flux_wilson_x_$(ARCH)
	rm flux_wilson_x_$(ARCH).o
flux_wilson_x_$(ARCH).o: flux_wilson_x.cpp
	$(GCC) -O3 -c flux_wilson_x.cpp -I$(INCLUDE_PATH) $(FLAGS) -o flux_wilson_x_$(ARCH).o

flux_schwinger: flux_schwinger_$(ARCH).o $(OBJ_FILES)
	$(GCC) flux_schwinger_$(ARCH).o $(OBJ_FILES) -o exe/flux_schwinger_$(MATRIX)_$(ARCH)
	rm flux_schwinger_$(ARCH).o
flux_schwinger_$(ARCH).o: flux_schwinger.cpp
	$(GCC) -O3 -c flux_schwinger.cpp -I$(INCLUDE_PATH) $(FLAGS) -DMATRIX=$(MATRIX) -o flux_schwinger_$(ARCH).o

monopole_observables: monopole_observables_$(ARCH).o $(OBJ_FILES)
	$(GCC) monopole_observables_$(ARCH).o $(OBJ_FILES) -o exe/monopole_observables_$(MATRIX)_$(ARCH)
	rm monopole_observables_$(ARCH).o
monopole_observables_$(ARCH).o: monopole_observables.cpp
	$(GCC) -O3 -c monopole_observables.cpp -I$(INCLUDE_PATH) $(FLAGS) -DMATRIX=$(MATRIX) -o monopole_observables_$(ARCH).o

polyakov_loop_correlator: polyakov_loop_correlator_$(ARCH).o $(OBJ_FILES)
	$(GCC) polyakov_loop_correlator_$(ARCH).o $(OBJ_FILES) $(C_FILES) -o exe/polyakov_loop_correlator_$(MATRIX)_$(ARCH)
	rm polyakov_loop_correlator_$(ARCH).o
polyakov_loop_correlator_$(ARCH).o: polyakov_loop_correlator.cpp
	$(GCC) -O3 -c polyakov_loop_correlator.cpp -I$(INCLUDE_PATH) $(FLAGS) -DMATRIX=$(MATRIX) -o polyakov_loop_correlator_$(ARCH).o

polyakov_loop: polyakov_loop_$(ARCH).o $(OBJ_FILES)
	$(GCC) polyakov_loop_$(ARCH).o $(OBJ_FILES) $(C_FILES) -o exe/polyakov_loop_$(MATRIX)_$(ARCH)
	rm polyakov_loop_$(ARCH).o
polyakov_loop_$(ARCH).o: polyakov_loop.cpp
	$(GCC) -O3 -c polyakov_loop.cpp -I$(INCLUDE_PATH) $(FLAGS) -DMATRIX=$(MATRIX) -o polyakov_loop_$(ARCH).o

plaket: plaket_$(ARCH).o $(OBJ_FILES)
	$(GCC) plaket_$(ARCH).o $(OBJ_FILES) $(C_FILES) -fopenmp -o exe/plaket_$(MATRIX_PLAKET)_$(ARCH)
	rm plaket_$(ARCH).o
plaket_$(ARCH).o: plaket.cpp
	$(GCC) -O3 -c plaket.cpp -I$(INCLUDE_PATH) $(FLAGS) -DMATRIX_PLAKET=$(MATRIX_PLAKET) -o plaket_$(ARCH).o
