GCC=/home/itep/kudrov/installed/gcc-9/bin/g++
SRC_PATH=/home/clusters/rrcmpi/kudrov/general_code/lib/cpu/src
INCLUDE_PATH=/home/clusters/rrcmpi/kudrov/general_code/lib/cpu/include
OBJ_PATH=/home/clusters/rrcmpi/kudrov/general_code/lib/cpu/obj
OBJ_FILES=$(OBJ_PATH)/link.o $(OBJ_PATH)/data.o $(OBJ_PATH)/basic_observables.o $(OBJ_PATH)/matrix.o $(OBJ_PATH)/flux_tube.o
C_PATH=/home/clusters/rrcmpi/kudrov/general_code/lib/cpu/src/c-lime
C_FILES=$(C_PATH)/lime_fseeko.c  $(C_PATH)/lime_header.c  $(C_PATH)/lime_reader.c  $(C_PATH)/lime_utils.c  $(C_PATH)/lime_writer.c
FLOAT=double
FLAGS=-fopenmp
MATRIX_PLAKET=su2
MATRIX_WILSON=su2
MATRIX=su2

all: flux_wilson wilson_on-axis wilson_off-axis flux_schwinger monopole_observables polyakov_loop

flux_wilson: flux_wilson.o $(OBJ_FILES)
	$(GCC) flux_wilson.o $(OBJ_FILES) $(C_FILES) -o exe/flux_wilson_$(MATRIX_PLAKET)_$(MATRIX_WILSON)
	rm flux_wilson.o
flux_wilson.o: flux_wilson.cpp
	$(GCC) -O3 -c flux_wilson.cpp -I$(INCLUDE_PATH) $(FLAGS) -DMATRIX_WILSON=$(MATRIX_WILSON) -DMATRIX_PLAKET=$(MATRIX_PLAKET) -o flux_wilson.o

flux_wilson_tr: flux_wilson_tr.o $(OBJ_FILES)
	$(GCC) flux_wilson_tr.o $(OBJ_FILES) $(C_FILES) -o exe/flux_wilson_tr_$(MATRIX_PLAKET)_$(MATRIX_WILSON)
	rm flux_wilson_tr.o
flux_wilson_tr.o: flux_wilson_tr.cpp
	$(GCC) -O3 -c flux_wilson_tr.cpp -I$(INCLUDE_PATH) $(FLAGS) -DMATRIX_WILSON=$(MATRIX_WILSON) -DMATRIX_PLAKET=$(MATRIX_PLAKET) -o flux_wilson_tr.o

wilson_on-axis: wilson_on-axis.o $(OBJ_FILES)
	$(GCC) wilson_on-axis.o $(OBJ_FILES) $(C_FILES) -o exe/wilson_on-axis_$(MATRIX)
	rm wilson_on-axis.o
wilson_on-axis.o: wilson_on-axis.cpp
	$(GCC) -O3 -c wilson_on-axis.cpp -I$(INCLUDE_PATH) $(FLAGS) -DMATRIX_WILSON=$(MATRIX) -o wilson_on-axis.o

wilson_adjoint_on-axis: wilson_adjoint_on-axis.o $(OBJ_FILES)
	$(GCC) wilson_adjoint_on-axis.o $(OBJ_FILES) $(C_FILES) -o exe/wilson_adjoint_on-axis_$(MATRIX)
	rm wilson_adjoint_on-axis.o
wilson_adjoint_on-axis.o: wilson_adjoint_on-axis.cpp
	$(GCC) -O3 -c wilson_adjoint_on-axis.cpp -I$(INCLUDE_PATH) $(FLAGS) -DMATRIX_WILSON=$(MATRIX) -o wilson_adjoint_on-axis.o

wilson_off-axis: wilson_off-axis.o $(OBJ_FILES)
	$(GCC) wilson_off-axis.o $(OBJ_FILES) $(C_FILES) -o exe/wilson_off-axis_$(MATRIX)
	rm wilson_off-axis.o
wilson_off-axis.o: wilson_off-axis.cpp
	$(GCC) -O3 -c wilson_off-axis.cpp -I$(INCLUDE_PATH) $(FLAGS) -DMATRIX_WILSON=$(MATRIX) -o wilson_off-axis.o

wilson_spatial: wilson_spatial.o $(OBJ_FILES)
	$(GCC) wilson_spatial.o $(OBJ_FILES) -o exe/wilson_spatial_$(MATRIX)
	rm wilson_spatial.o
wilson_spatial.o: wilson_spatial.cpp
	$(GCC) -O3 -c wilson_spatial.cpp -I$(INCLUDE_PATH) $(FLAGS) -DMATRIX_WILSON=$(MATRIX) -o wilson_spatial.o

flux_wilson_x: flux_wilson_x.o $(OBJ_FILES)
	$(GCC) flux_wilson_x.o $(OBJ_FILES) -o flux_wilson_x
	rm flux_wilson_x.o
flux_wilson_x.o: flux_wilson_x.cpp
	$(GCC) -O3 -c flux_wilson_x.cpp -I$(INCLUDE_PATH) $(FLAGS)

flux_schwinger: flux_schwinger.o $(OBJ_FILES)
	$(GCC) flux_schwinger.o $(OBJ_FILES) -o exe/flux_schwinger_$(MATRIX)
	rm flux_schwinger.o
flux_schwinger.o: flux_schwinger.cpp
	$(GCC) -O3 -c flux_schwinger.cpp -I$(INCLUDE_PATH) $(FLAGS) -DMATRIX=$(MATRIX) -o flux_schwinger.o

monopole_observables: monopole_observables.o $(OBJ_FILES) $(OBJ_PATH)/monopoles.o $(OBJ_PATH)/loop.o
	$(GCC) monopole_observables.o $(OBJ_FILES) $(OBJ_PATH)/monopoles.o $(OBJ_PATH)/loop.o -o exe/monopole_observables_$(MATRIX)
	rm monopole_observables.o
monopole_observables.o: monopole_observables.cpp
	$(GCC) -O3 -c monopole_observables.cpp -I$(INCLUDE_PATH) $(FLAGS) -DMATRIX=$(MATRIX) -o monopole_observables.o

polyakov_loop_correlator: polyakov_loop_correlator.o $(OBJ_FILES)
	$(GCC) polyakov_loop_correlator.o $(OBJ_FILES) $(C_FILES) -o exe/polyakov_loop_correlator_$(MATRIX)
	rm polyakov_loop_correlator.o
polyakov_loop_correlator.o: polyakov_loop_correlator.cpp
	$(GCC) -O3 -c polyakov_loop_correlator.cpp -I$(INCLUDE_PATH) $(FLAGS) -DMATRIX=$(MATRIX) -o polyakov_loop_correlator.o

polyakov_loop: polyakov_loop.o $(OBJ_FILES)
	$(GCC) polyakov_loop.o $(OBJ_FILES) $(C_FILES) -o exe/polyakov_loop_$(MATRIX)
	rm polyakov_loop.o
polyakov_loop.o: polyakov_loop.cpp
	$(GCC) -O3 -c polyakov_loop.cpp -I$(INCLUDE_PATH) $(FLAGS) -DMATRIX=$(MATRIX) -o polyakov_loop.o
