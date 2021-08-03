GCC=g++
SRC_PATH=/home/clusters/rrcmpi/kudrov/general_code/lib/cpu/src
INCLUDE_PATH=/home/clusters/rrcmpi/kudrov/general_code/lib/cpu/include
OBJ_PATH=/home/clusters/rrcmpi/kudrov/general_code/lib/cpu/obj
OBJ_FILES=$(OBJ_PATH)/link.o $(OBJ_PATH)/data.o $(OBJ_PATH)/basic_observables.o $(OBJ_PATH)/result.o $(OBJ_PATH)/matrix.o $(OBJ_PATH)/flux_tube.o
FLOAT=double
FLAGS=-D DOUBLE
MATRIX=abelian

all: flux_wilson wilson

flux_wilson: flux_wilson.o $(OBJ_FILES)
	$(GCC) flux_wilson.o $(OBJ_FILES) -o exe/flux_wilson_$(MATRIX)
	rm flux_wilson.o
flux_wilson.o: flux_wilson.cpp
	$(GCC) -O3 -c flux_wilson.cpp -I$(INCLUDE_PATH) $(FLAGS) -DMATRIX=$(MATRIX) -o flux_wilson.o

wilson: wilson.o $(OBJ_FILES)
	$(GCC) wilson.o $(OBJ_FILES) -o exe/wilson_$(MATRIX)
	rm wilson.o
wilson.o: wilson.cpp
	$(GCC) -O3 -c wilson.cpp -I$(INCLUDE_PATH) $(FLAGS) -DMATRIX=$(MATRIX) -o wilson.o

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
