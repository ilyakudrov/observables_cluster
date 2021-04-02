#include "data.h"
#include "observables.h"
#include "link.h"
#include "matrix.h"
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
	x_size = 32;
    	y_size = 32;
    	z_size = 32;
    	t_size = 32;

	string path_electric = argv[1];
	string path_magnetic = argv[2];
	int R = atof(argv[3]);
        string conf_num;

	result res_electric;
	result res_magnetic;
	int data_size = R + 11;
	vector<result> correlator_electric(data_size);
	vector<result> correlator_magnetic(data_size);
	result wilson_electric;
	result plaket_electric;
	result plaket_magnetic;

	double aver[2];

	int q1, q2, q3, q4;
	for(int i = 1;i <= 2000;i++){
		q1 = i/1000;
                q2 = (i - q1 * 1000)/100;
                q3 = (i - q1 * 1000 - q2 * 100)/10;
                q4 = (i - q1 * 1000 - q2 * 100 - q3 * 10);
		conf_num = static_cast<ostringstream*>( &(ostringstream() << q1 << q2 << q3 << q4) )->str();
		struct stat buffer;
		if(stat((path_electric + conf_num).c_str(), &buffer) == 0 && stat((path_magnetic + conf_num).c_str(), &buffer) == 0) {
			res_electric.read((path_electric + conf_num).c_str(), data_size + 2);
			res_magnetic.read((path_magnetic + conf_num).c_str(), data_size + 2);
			for(int j = 0;j < data_size;j++){
				correlator_electric[j].array.push_back(res_electric.array[j]);
				correlator_magnetic[j].array.push_back(res_magnetic.array[j]);
			}
			wilson_electric.array.push_back(res_electric.array[data_size]);
			plaket_electric.array.push_back(res_electric.array[data_size + 1]);
			plaket_magnetic.array.push_back(res_magnetic.array[data_size + 1]);
		}
	}

	/*correlator_electric[5].average(aver);
	cout<<"electric "<<aver[0]<<" "<<aver[1]<<endl;
	wilson_electric.average(aver);
	cout<<"wilson "<<aver[0]<<" "<<aver[1]<<endl;
	plaket_electric.average(aver);
	cout<<"plaket "<<aver[0]<<" "<<aver[1]<<endl;*/
	
	ofstream output_electric;
	ofstream output_magnetic;
	ofstream output_energy;
	ofstream output_action;
	output_electric.open(argv[4]);
	output_magnetic.open(argv[5]);
        output_energy.open(argv[6]);
        output_action.open(argv[7]);
	for(int i = 0;i < data_size;i++){
		average_jack_wilson(aver, correlator_electric[i], wilson_electric, plaket_electric);
		output_electric<<(i-5-R/2)<<" "<<aver[0]<<" "<<aver[1]<<endl;
		average_jack_wilson(aver, correlator_magnetic[i], wilson_electric, plaket_magnetic);
                output_magnetic<<(i-5-R/2)<<" "<<aver[0]<<" "<<aver[1]<<endl;
                average_jack_difference(aver, correlator_electric[i], correlator_magnetic[i], wilson_electric, plaket_electric, plaket_magnetic);
                output_energy<<(i-5-R/2)<<" "<<aver[0]*2<<" "<<aver[1]*2<<endl;
                average_jack_sum(aver, correlator_electric[i], correlator_magnetic[i], wilson_electric, plaket_electric, plaket_magnetic);
                output_action<<(i-5-R/2)<<" "<<aver[0]/2<<" "<<aver[1]/2<<endl;
	}
	output_electric.close();
	output_magnetic.close();
        output_energy.close();
        output_action.close();
}
