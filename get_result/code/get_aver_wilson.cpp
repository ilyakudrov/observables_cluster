#include "result.h"
#include <iostream>
#include <sstream>
#include <sys/stat.h>

using namespace std;

int x_size;
int y_size;
int z_size;
int t_size;

int main(int argc, char* argv[]) {
	string path_wilson = argv[1];
	string path_sizes = argv[2];
	string conf_num;

	int data_size = 104;
	vector<double> data_wilson(data_size);
	vector<double> data_sizes(data_size * 2);
	vector<double> aver_wilson(data_size);

	int q1, q2, q3, q4;

	bool if_first_sizes = true;
	int count_wilson = 0;

	ifstream stream_sizes;
	ifstream stream_wilson;

	for(int i = 1;i <= 1000;i++){
		q1 = i/1000;
                q2 = (i - q1 * 1000)/100;
                q3 = (i - q1 * 1000 - q2 * 100)/10;
                q4 = (i - q1 * 1000 - q2 * 100 - q3 * 10);
		conf_num = to_string(q1) + to_string(q2) + to_string(q3) + to_string(q4);
		struct stat buffer;
		if(stat((path_wilson + conf_num).c_str(), &buffer) == 0) {
			if(if_first_sizes){
				cout<<"sizes read"<<endl;
				stream_sizes.open(path_sizes + conf_num);
				cout<<path_sizes + conf_num<<endl;
				if(!stream_sizes.read((char*)&data_sizes[0], data_size * 2 * sizeof(double))) cout<<"NO"<<endl;;
				if_first_sizes = false;
				stream_sizes.close();
			}
			stream_wilson.open(path_wilson + conf_num);
			stream_wilson.read((char*)&data_wilson[0], data_size * sizeof(double));
			stream_wilson.close();
			//data_wilson.read((path_wilson + conf_num).c_str(), data_size);
			/*if(i == 5){
                                for(int k = 0;k < data_size * 2;k++){
                                        cout<<data_sizes[k]<<endl;
				}
			}*/

			for(int j = 0;j < aver_wilson.size();j++){
				aver_wilson[j] += data_wilson[j];
			}
			count_wilson++;
		}
	}

	/*vector<double> vec_test(8);
	ifstream stream_test;
	stream_test.open("/home/clusters/rrcmpi/kudrov/observables/result/wilson_loop/qc2dstag/HYP_APE/mu0.05/wilson_loop_0005");
	stream_test.read((char*)&vec_test[0], 8 * sizeof(double));
	stream_test.close();

	for(int i = 0;i < vec_test.size();i++){
		cout<<vec_test[i]<<endl;
	}*/

	for(int i = 0;i < aver_wilson.size();i++){
		aver_wilson[i] = aver_wilson[i] / count_wilson;
	}

	ofstream output;
	string path_output = argv[3];
	output.open(path_output);

	output<<"#time_size,space_size,wilson_loop"<<endl;
	for(int i = 0;i < aver_wilson.size();i++){
		output<<data_sizes[2 * i]<<","<<data_sizes[2 * i + 1]<<","<<aver_wilson[i]<<endl;
	}

	output.close();		
}
