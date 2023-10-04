#ifndef __GETDIPOLETILT_H__
#define __GETDIPOLETILT_H__
#include <stdio.h>
#include <stdlib.h>
#include "modelparams/modelparams.h"
#include "fortran/geopack.h"
#include "../lib/datetime/include/datetime.h"
#endif
using namespace std;

double GetDipoleTilt(int Year, int Doy, int Hr, int Mn, double Vx, double Vy, double Vz);

extern "C" {
	double GetDipoleTiltUT(int Date, float ut, double Vx, double Vy, double Vz);
}
