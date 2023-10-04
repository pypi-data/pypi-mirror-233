#ifndef __T89_H__
#define __T89_H__
#include <stdio.h>
#include <stdlib.h>
#define _USE_MATH_DEFINES
#include <math.h>

void t89(	int iopt, double *parmod, double psi,
			double x, double y, double z, 
			double *bx, double *by, double *bz);

void t89smCoords(	double x, double z, double psi,
				double *sps, double *cps, double *tps,
				double *xsm, double *zsm);

void t89tailCurrentSheetShape(	double xsm, double ysm, 
							double sps, double tps,
							double R_c, double G,
							double *Zs, double *dZsdx, double *dZsdy);

void t89ringCurrentComps(	double x, double y, double z,
						double cps, double sps,
						double zs, double dzsdx, double dzsdy,
						double D_0, double gamma_RC, 
						double a_RC, double C3,
						double *Bx, double *By, double *Bz);

void t89tailCurrentField(	double x, double y, double z,
						double cps, double sps, double psi,
						double zs, double dzsdx, double dzsdy,
						double D_0, double delta, double gamma_T,
						double a_T, double x_0, double D_y,
						double A1, double A2, double A16, double A17,
						double *Bx, double *By, double *Bz);

void t89tailClosureCurrent(double x, double y, double z,
						double C4, double C5, double sps,
						double *Bx, double *By, double *Bz);

void t89cfClosureCurrent(	double x, double y, double z, double deltax,
						double C6, double C7, double C8, double C9,
						double C10, double C11, double C12, double C13,
						double C14, double C15, double cps, double sps,
						double *Bx, double *By, double *Bz);


#endif
