#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <geopack.h>

int main(int argc, char *argv[]) {
	

	
	/* intialize the parameters for the model */
	//InitParams(argv[argc-1]);
	printf("Testing C...\n");

	/* set up the initial tracing position etc. */
	int Date[] = {20120101};
	float ut[] = {12.0};
	double xin[] = {0.0};
	double yin[] = {10.0};
	double zin[] = {0.0};
	const char *Model = "T96";
	const char *CoordIn = "GSM";
	int n = 1;
	double Vx = -359.0;
	double Vy = 11.0;
	double Vz = -17.4;
	int iopt = 1;
	double *parmod = (double*) malloc(sizeof(double)*10);
	int i;
	parmod[0] = 1.34;
	parmod[1] = -9.0;
	parmod[2] = 0.2;
	parmod[3] = -1.96;
	for (i=4;i<10;i++) {
		parmod[i] = 0.0;
	}
	
	/* output parameters */
	int nstep, nalpha = 2;
	double *xgsm = malloc(1000*sizeof(double));
	double *ygsm = malloc(1000*sizeof(double));
	double *zgsm = malloc(1000*sizeof(double));
	double *bxgsm = malloc(1000*sizeof(double));
	double *bygsm = malloc(1000*sizeof(double));
	double *bzgsm = malloc(1000*sizeof(double));

	double *xgse = malloc(1000*sizeof(double));
	double *ygse = malloc(1000*sizeof(double));
	double *zgse = malloc(1000*sizeof(double));
	double *bxgse = malloc(1000*sizeof(double));
	double *bygse = malloc(1000*sizeof(double));
	double *bzgse = malloc(1000*sizeof(double));

	double *xsm = malloc(1000*sizeof(double));
	double *ysm = malloc(1000*sizeof(double));
	double *zsm = malloc(1000*sizeof(double));
	double *bxsm = malloc(1000*sizeof(double));
	double *bysm = malloc(1000*sizeof(double));
	double *bzsm = malloc(1000*sizeof(double));

	double *s = malloc(1000*sizeof(double));
	double *r = malloc(1000*sizeof(double));
	double *rnorm = malloc(1000*sizeof(double));
	double *FP = malloc(1000*sizeof(double));

	double alpha[] = {0.0,90.0};
	double halpha[2000];

	TraceField(n,xin,yin,zin,Date,ut,Model,&iopt,&parmod,
				&Vx,&Vy,&Vz,100.0,1000,1.0,true,0,CoordIn,
				&nstep,&xgsm,&ygsm,&zgsm,&bxgsm,&bygsm,&bzgsm,
				&xgse,&ygse,&zgse,&bxgse,&bygse,&bzgse,
				&xsm,&ysm,&zsm,&bxsm,&bysm,&bzsm,
				&s,&r,&rnorm,&FP,nalpha,alpha,halpha);
	printf("Done\n");
}
