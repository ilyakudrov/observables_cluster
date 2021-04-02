#include "data.h"
#include "basic_observables.h"
#include "link.h"
#include "matrix.h"
#include "result.h"

#include <iostream>

using namespace std;

int x_size;
int y_size;
int z_size;
int t_size;

int main(int argc, char* argv[]) {
	unsigned int start_time;
	unsigned int end_time;
        unsigned int search_time;

	string conf_format;
	string conf_path;
	string output_path_wilson;
	string output_path_sizes;
	int L_spat, L_time;
	int T_min, T_max;
	FLOAT R_min, R_max;
        for (int i = 1; i < argc; i++) {
                if (string(argv[i]) == "-conf_format") { conf_format = argv[++i]; }
		else if (string(argv[i]) == "-conf_path") { conf_path = argv[++i]; }
		else if (string(argv[i]) == "-output_path_wilson") { output_path_wilson = argv[++i]; }
		else if (string(argv[i]) == "-output_path_sizes") { output_path_sizes = argv[++i]; }
		else if (string(argv[i]) == "-L_spat") { L_spat = stoi(string(argv[++i])); }
		else if (string(argv[i]) == "-L_time") { L_time = stoi(string(argv[++i])); }
		else if (string(argv[i]) == "-T_min") { T_min = stoi(string(argv[++i])); }
		else if (string(argv[i]) == "-T_max") { T_max = stoi(string(argv[++i])); }
		else if (string(argv[i]) == "-R_min") { R_min = stoi(string(argv[++i])); }
		else if (string(argv[i]) == "-R_max") { R_max = stoi(string(argv[++i])); }
        }

	cout<<"conf_format "<<conf_format<<endl;
	cout<<"conf_path "<<conf_path<<endl;
	cout<<"output_path_wilson "<<output_path_wilson<<endl;
	cout<<"output_path_sizes "<<output_path_sizes<<endl;
	cout<<"L_spat "<<L_spat<<endl;	
	cout<<"L_time "<<L_time<<endl;
	cout<<"T_min "<<T_min<<endl;
	cout<<"T_max "<<T_max<<endl;
	cout<<"R_min "<<R_min<<endl;
	cout<<"R_max "<<R_max<<endl;

	x_size = L_spat;
        y_size = L_spat;
        z_size = L_spat;
        t_size = L_time;

	data<MATRIX> conf;

	if(string(conf_format) == "float"){
		conf.read_float(conf_path);
	}
	else if (string(conf_format) == "double"){
		conf.read_double(conf_path);
	}
	else if (string(conf_format) == "double_fortran"){
                conf.read_double_fortran(conf_path);
	}
	else if (string(conf_format) == "float_fortran"){
                conf.read_float_fortran(conf_path);
	}
	else if (string(conf_format) == "double_qc2dstag"){
                conf.read_double_qc2dstag(conf_path);
        }
	start_time =  clock();

	vector<vector<int>> directions;
  	directions = generate_directions(4);

	vector<wilson_result> wilson_offaxis_result = 
		wilson_offaxis(conf.array, directions, R_min, R_max, T_min, T_max);

	end_time = clock();
        search_time = end_time - start_time;
        cout<<" calculating time: "<<search_time*1./CLOCKS_PER_SEC<<endl;

	wilson_offaxis_reduce(wilson_offaxis_result);

	// write data into two separate files
	// one is for wilson loops and the second is for sizes
	
	ofstream ofstream_wilson;

	ofstream_wilson.precision(17);

	ofstream_wilson.open(output_path_wilson);

	ofstream_wilson<<"#time_size,space_size,wilson_loop"<<endl;

	for(int i = 0;i < wilson_offaxis_result.size();i++){
		ofstream_wilson<<wilson_offaxis_result[i].time_size<<","<<wilson_offaxis_result[i].space_size<<","<<wilson_offaxis_result[i].wilson_loop<<endl;
	}

	ofstream_wilson.close();
}
