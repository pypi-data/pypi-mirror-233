#include <stdio.h>
#define _USE_MATH_DEFINES
#include <geopack.h>
#include <math.h>

bool testT89();

int main() {

	
	testT89();
}


bool testT89() {
	printf("Testing T89...");
	bool pass = true;

	/* create some test position vectors */
	double x[] = {5.0,10.0,-10.0,-5.0};
	double y[] = {0.0,-4.0,3.0,-2.0};
	double z[] = {1.0,0.0,-2.0,-1.0};
	double psi[] = {0.0,0.35,-0.2,0.1};
	int iopt[] = {1,3,5,6};
	double parmod[10];

	/* variables to store field vectors */
	double Bxc[4], Byc[4], Bzc[4];
	double Bxf[4], Byf[4], Bzf[4];

	/* get the vectors */
	int i;
	double dx, dy, dz;
	for (i=0;i<4;i++) {
		t89c_(&iopt[i],parmod,&psi[i],&x[i],&y[i],&z[i],&Bxf[i],&Byf[i],&Bzf[i]);
		t89(iopt[i],parmod,psi[i],x[i],y[i],z[i],&Bxc[i],&Byc[i],&Bzc[i]);
	}

	/* compare them */
	for (i=0;i<4;i++) {
		dx = abs(Bxf[i]-Bxc[i]);
		dy = abs(Byf[i]-Byc[i]);
		dz = abs(Bzf[i]-Bzc[i]);
		if ((dx > 1e-5) || (dy > 1e-5) || (dz > 1e-5)) {
			pass = false;
			break;
		}
	}
	if (pass) {
		printf(" pass\n");
	} else {
		printf(" fail\n");
	}
	return pass;
}

