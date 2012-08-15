// c++ -Wall get-tbb-station-ref.cpp -ldal -lhdf
#include <iostream>
#include <dal/lofar/TBB_File.h>

using namespace std;

int main() {
	DAL::TBB_File f("test-get-tbb-station-ref-cpp.h5", DAL::TBB_File::CREATE);

	DAL::TBB_Station st(f.station("CSxxx"));

	return 0;
}

