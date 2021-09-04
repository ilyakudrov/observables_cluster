GCC=/home/itep/kudrov/installed/gcc-9/bin/g++
SRC_PATH=/home/clusters/rrcmpi/kudrov/general_code/lib/cpu/src
INCLUDE_PATH=/home/clusters/rrcmpi/kudrov/general_code/lib/cpu/include
OBJ_PATH=/home/clusters/rrcmpi/kudrov/general_code/lib/cpu/obj
OBJ_FILES=$(OBJ_PATH)/link.o $(OBJ_PATH)/data.o $(OBJ_PATH)/basic_observables.o $(OBJ_PATH)/result.o $(OBJ_PATH)/matrix.o $(OBJ_PATH)/flux_tube.o
FLOAT=double
FLAGS=-D DOUBLE -fopenmp
MATRIX=su2

all: flux_wilson wilson

flux_wilson: flux_wilson.o $(OBJ_FILES)
	$(GCC) flux_wilson.o $(OBJ_FILES) -o exe/flux_wilson_$(MATRIX) -fopenmp
	rm flux_wilson.o
flux_wilson.o: flux_wilson.cpp
	$(GCC) -O3 -c flux_wilson.cpp -I$(INCLUDE_PATH) $(FLAGS) -DMATRIX=$(MATRIX) -o flux_wilson.o

wilson_on-axis: wilson_on-axis.o $(OBJ_FILES)
	$(GCC) wilson_on-axis.o $(OBJ_FILES) -o exe/wilson_on-axis_$(MATRIX)
	rm wilson_on-axis.o
wilson_on-axis.o: wilson_on-axis.cpp
	$(GCC) -O3 -c wilson_on-axis.cpp -I$(INCLUDE_PATH) $(FLAGS) -DMATRIX=$(MATRIX) -o wilson_on-axis.o

wilson_off-axis: wilson_off-axis.o $(OBJ_FILES)
	$(GCC) wilson_off-axis.o $(OBJ_FILES) -o exe/wilson_off-axis_$(MATRIX)
	rm wilson_off-axis.o
wilson_off-axis.o: wilson_off-axis.cpp
	$(GCC) -O3 -c wilson_off-axis.cpp -I$(INCLUDE_PATH) $(FLAGS) -DMATRIX=$(MATRIX) -o wilson_off-axis.o

wilson_spatial: wilson_spatial.o $(OBJ_FILES)
	$(GCC) wilson_spatial.o $(OBJ_FILES) -o exe/wilson_spatial_$(MATRIX)
	rm wilson_spatial.o
wilson_spatial.o: wilson_spatial.cpp
	$(GCC) -O3 -c wilson_spatial.cpp -I$(INCLUDE_PATH) $(FLAGS) -DMATRIX=$(MATRIX) -o wilson_spatial.o

flux_wilson_x: flux_wilson_x.o $(OBJ_FILES)
	$(GCC) flux_wilson_x.o $(OBJ_FILES) -o flux_wilson_x
	rm flux_wilson_x.o
flux_wilson_x.o: flux_wilson_x.cpp
	$(GCC) -O3 -c flux_wilson_x.cpp -I$(INCLUDE_PATH) $(FLAGS)

monopole_observables: monopole_observables.o $(OBJ_FILES) $(OBJ_PATH)/monopoles.o $(OBJ_PATH)/loop.o
	$(GCC) monopole_observables.o $(OBJ_FILES) $(OBJ_PATH)/monopoles.o $(OBJ_PATH)/loop.o -o exe/monopole_observables_$(MATRIX)
	rm monopole_observables.o
monopole_observables.o: monopole_observables.cpp
	$(GCC) -O3 -c monopole_observables.cpp -I$(INCLUDE_PATH) $(FLAGS) -DMATRIX=$(MATRIX) -o monopole_observables.o
