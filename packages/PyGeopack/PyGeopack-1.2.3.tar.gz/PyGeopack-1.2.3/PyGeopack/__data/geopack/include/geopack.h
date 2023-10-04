#ifndef __GEOPACK_H__
#define __GEOPACK_H__
#include <stdio.h>
#include <stdlib.h>

/* need this if we're using C */
#ifndef __cplusplus 
	#include <stdbool.h>
#endif


/* C wrapper functions */
#ifdef __cplusplus
	extern "C" {
#endif

/********************************************************************
* NAME : void ModelField(n,Xin,Yin,Zin,Date,ut,SameTime,Model,iopt,
* 						parmod,Vx,Vy,Vz,CoordIn,CoordOut,WithinMPOnly,
*						Bx,By,Bz)
*
* DESCRIPTION : Calculates the model field at some position given a
* 				time and model parameters.
*
* INPUTS : 
* 		int n					Number of field vectors.
*		double *Xin				Array of x-coordinates (R_E).
*		double *Yin				Array of y-coordinates (R_E).
* 		double *Zin				Array of z-coordinates (R_E).
* 		int Date				Array of dates, format yyyymmdd.
* 		float *ut				UT in hours.
* 		bool SameTime			Set to True if Date and ut are single element
*								arrays (all field vectors are for the same time).
* 		const char *Model		Model name (T89|T96|T01|TS05).
*		int *iopt				T89 parameters.
*		double **parmod			Model parameters for T96, T01, TS05, shape
*								(ntimes,10).
*								All models:
*									parmod[:][0] = Dynamic pressure (nPa).
*									parmod[:][1] = SymH/Dst/SMR (nT).
*									parmod[:][2] = IMF By (nT).
*									parmod[:][3] = IMF Bz (nT).
*								T01:
*									parmod[:][4] = G1 parameter.
*									parmod[:][5] = G2 parameter.
*								TS05:
*									parmod[:][4] = W1 parameter.
*									parmod[:][5] = W2 parameter.
*									parmod[:][6] = W3 parameter.
*									parmod[:][7] = W4 parameter.
*									parmod[:][8] = W5 parameter.
*									parmod[:][9] = W6 parameter.
*		double *Vx				Solar wind velocity (km/s).
*		double *Vy				Solar wind velocity (km/s).
*		double *Vz				Solar wind velocity (km/s).
*		const char *CoordIn		Input coords (GSM|GSE|SM).
*		const char *CoordOut	Output coords (GSM|GSE|SM).
*		bool WithinMPOnly		If true, then vectors outside of the
*								magnetopause with be NAN.
*		double *Bx				Output x-component (nT).
*		double *By				Output y-component (nT).
*		double *Bz				Output z-component (nT).
*								
*
********************************************************************/
void ModelField(	int n, 
					double *Xin, 
					double *Yin, 
					double *Zin,  
					int *Date, 
					float *ut, 
					bool SameTime,
					const char *Model, 
					int *iopt, 
					double **parmod,
					double *Vx, 
					double *Vy, 
					double *Vz,
					const char *CoordIn, 
					const char *CoordOut, 
					bool WithinMPOnly, 
					double *Bx, 
					double *By, 
					double *Bz);

double GetDipoleTiltUT(int Date, float ut, double Vx, double Vy, double Vz);

	/* Coordinate conversion  function */
	void ConvCoords(	double *Xin, double *Yin, double *Zin, int n, 
						double *Vxin, double *Vyin, double *Vzin, 
						int *Date, float *ut, 
						double *Xout, double *Yout, double *Zout,
						const char *CoordIn, const char *CoordOut);


	/***********************************************************************
	 * GSEtoGSM
	 * 
	 * Wrapper for converting GSE to GSM coordinates
	 * ********************************************************************/
	void GSEtoGSM(	double Xin, double Yin, double Zin,
					double Vx, double Vy, double Vz, int recalc,
					int Year, int DayNo, int Hr, int Mn, int Sc, 
					double *Xout, double *Yout, double *Zout);

	/***********************************************************************
	 * GSEtoGSMUT
	 * 
	 * Wrapper for converting GSE to GSM coordinates
	 * ********************************************************************/
	void GSEtoGSMUT(	double *Xin, double *Yin, double *Zin, int n,
						double *Vx, double *Vy, double *Vz, 
						int *Date, float *ut, 
						double *Xout, double *Yout, double *Zout);

	void GSMtoGSE(	double Xin, double Yin, double Zin,
					double Vx, double Vy, double Vz, int recalc,
					int Year, int DayNo, int Hr, int Mn, int Sc,
					double *Xout, double *Yout, double *Zout);
		
	void GSMtoGSEUT(	double *Xin, double *Yin, double *Zin, int n,
						double *Vx, double *Vy, double *Vz, 
						int *Date, float *ut, 
						double *Xout, double *Yout, double *Zout);

	void GSMtoSM(	double Xin, double Yin, double Zin, 
					double Vx, double Vy, double Vz, int recalc,
					int Year, int DayNo, int Hr, int Mn, int Sc, 
					double *Xout, double *Yout, double *Zout);

	void GSMtoSMUT(	double *Xin, double *Yin, double *Zin, int n,
					double *Vx, double *Vy, double *Vz,
					int *Date, float *ut, 
					double *Xout, double *Yout, double *Zout);

	void SMtoGSM(	double Xin, double Yin, double Zin, 
					double Vx, double Vy, double Vz, int recalc,
					int Year, int DayNo, int Hr, int Mn, int Sc, 
					double *Xout, double *Yout, double *Zout);

	void SMtoGSMUT(	double *Xin, double *Yin, double *Zin, int n,
					double *Vx, double *Vy, double *Vz, 
					int *Date, float *ut, 
					double *Xout, double *Yout, double *Zout);

	void GSEtoSM(	double Xin, double Yin, double Zin,
					double Vx, double Vy, double Vz, int recalc,
					int Year, int DayNo, int Hr, int Mn, int Sc, 
					double *Xout, double *Yout, double *Zout);

	void GSEtoSMUT(	double *Xin, double *Yin, double *Zin, int n,
					double *Vx, double *Vy, double *Vz, 
					int *Date, float *ut, 
					double *Xout, double *Yout, double *Zout);

	void GSEtoMAG(	double Xin, double Yin, double Zin, 
					double Vx, double Vy, double Vz, int recalc,
					int Year, int DayNo, int Hr, int Mn, int Sc, 
					double *Xout, double *Yout, double *Zout);

	void GSEtoMAGUT(	double *Xin, double *Yin, double *Zin, int n,
						double *Vx, double *Vy, double *Vz, 
						int *Date, float *ut,
						double *Xout, double *Yout, double *Zout);

	void SMtoGSE(	double Xin, double Yin, double Zin,
					double Vx, double Vy, double Vz, int recalc,
					int Year, int DayNo, int Hr, int Mn, int Sc, 
					double *Xout, double *Yout, double *Zout);

	void SMtoGSEUT(	double *Xin, double *Yin, double *Zin, int n,
					double *Vx, double *Vy, double *Vz,
					int *Date, float *ut, 
					double *Xout, double *Yout, double *Zout);

	void MAGtoGSE(	double Xin, double Yin, double Zin, 
					double Vx, double Vy, double Vz, int recalc,
					int Year, int DayNo, int Hr, int Mn, int Sc, 
					double *Xout, double *Yout, double *Zout);

	void MAGtoGSEUT(	double *Xin, double *Yin, double *Zin, int n,
						double *Vx, double *Vy, double *Vz, 
						int *Date, float *ut, 
						double *Xout, double *Yout, double *Zout);

	void MLONtoMLT(	double MLon, double Vx, double Vy, double Vz, int recalc,
					int Year, int DayNo, int Hr, int Mn, int Sc, double *MLT);

	void MLONtoMLTUT(	double *MLon, int n, 
						double *Vx, double *Vy, double *Vz, 
						int *Date,float *ut, double *MLT);

	void MLTtoMLON(	double MLT, double Vx, double Vy, double Vz, int recalc, 
					int Year, int DayNo, int Hr, int Mn, int Sc, double *MLon);

	void MLTtoMLONUT(	double *MLT, int n,
						double *Vx, double *Vy, double *Vz, 
						int *Date, float *ut, double *MLon);

	void GEOtoMAG(	double Xin, double Yin, double Zin, 
					double Vx, double Vy, double Vz, int recalc,
					int Year, int DayNo, int Hr, int Mn, int Sc, 
					double *Xout, double *Yout, double *Zout);

	void GEOtoMAGUT(	double *Xin, double *Yin, double *Zin, int n, 
						double *Vx, double *Vy, double *Vz, 
						int *Date, float *ut, 
						double *Xout, double *Yout, double *Zout);

	void GEOtoMAG_LL(	double Lon, double Lat, 
						double Vx, double Vy, double Vz, int recalc,
						int Year, int DayNo, int Hr, int Mn, int Sc, 
						double *MLon, double *MLat);

	void GEOtoMAGUT_LL(	double *Lon, double *Lat, int n, 
						double *Vx, double *Vy, double *Vz, 
						int *Date,float *ut, 
						double *MLon, double *MLat);
												
	void MAGtoGEO(	double Xin, double Yin, double Zin, 
					double Vx, double Vy, double Vz, int recalc,
					int Year, int DayNo, int Hr, int Mn, int Sc, 
					double *Xout, double *Yout, double *Zout);

	void MAGtoGEOUT(	double *Xin, double *Yin, double *Zin, int n, 
						double *Vx, double *Vy, double *Vz, 
						int *Date, float *ut, 
						double *Xout, double *Yout, double *Zout);
					
	void MAGtoGEO_LL(	double MLon, double MLat, 
						double Vx, double Vy, double Vz, int recalc,
						int Year, int DayNo, int Hr, int Mn, int Sc, 
						double *Lon, double *Lat);

	void MAGtoGEOUT_LL(	double *MLon, double *MLat, int n, 
						double *Vx, double *Vy, double *Vz, 
						int *Date,float *ut, 
						double *Lon, double *Lat);






	/***********************************************************************
	 * NAME : 			void GEItoGEO(	Xin, Yin, Zin, Vx, Vy, Vz, recalc,
	 *									Year, DayNo, Hr, Mn, Sc, 
	 *									*Xout, *Yout, *Zout)
	 * 
	 * DESCRIPTION : 	Wrapper for converting GEI to GEO coordinates
	 * 
	 * INPUTS : 
	 * 		double	Xin		x GEI coordinate (R_E)
	 * 		double	Yin		y GEI coordinate (R_E)
	 * 		double	Zin		z GEI coordinate (R_E)
	 * 		double 	Vx		x-component of SW velocity in km/s
	 * 		double 	Vy		y-component of SW velocity in km/s
	 * 		double 	Vz		z-component of SW velocity in km/s
	 * 		int		recalc	Set to one ro call recalc_08_
	 * 		int		Year	Year
	 * 		int		DayNo	Day number for that year
	 * 		int		Hr		Hours
	 * 		int		Mn		Minutes
	 * 		int		Sc		Seconds
	 * 
	 * OUTPUTS : 
	 * 		double	*Xout	x GEO coordinate (R_E)
	 * 		double	*Yout	y GEO coordinate (R_E)
	 * 		double	*Zout	z GEO coordinate (R_E)
	 * 
	 * RETURNS : 
	 * 		void
	 * 
	 * PROCESS : 
	 * 		[1] Calls recalc_08_ function in FORTRAN (if recalc != 0)
	 * 		[2] Calls FORTRAN code to convert from GEI to GEO coordinates
	 * 
	 * ********************************************************************/
	void GEItoGEO(	double Xin, double Yin, double Zin, 
					double Vx, double Vy, double Vz, int recalc,
					int Year, int DayNo, int Hr, int Mn, int Sc, 
					double *Xout, double *Yout, double *Zout);
					
	void GEItoGEOUT(	double *Xin, double *Yin, double *Zin, int n, 
						double *Vx, double *Vy, double *Vz, 
						int *Date, float *ut, 
						double *Xout, double *Yout, double *Zout);


	/***********************************************************************
	 * NAME : 			void GEOtoGEI(	Xin, Yin, Zin, Vx, Vy, Vz, recalc,
	 *									Year, DayNo, Hr, Mn, Sc, 
	 *									*Xout, *Yout, *Zout)
	 * 
	 * DESCRIPTION : 	Wrapper for converting GEO to GEI coordinates
	 * 
	 * INPUTS : 
	 * 		double	Xin		x GEO coordinate (R_E)
	 * 		double	Yin		y GEO coordinate (R_E)
	 * 		double	Zin		z GEO coordinate (R_E)
	 * 		double 	Vx		x-component of SW velocity in km/s
	 * 		double 	Vy		y-component of SW velocity in km/s
	 * 		double 	Vz		z-component of SW velocity in km/s
	 * 		int		recalc	Set to one ro call recalc_08_
	 * 		int		Year	Year
	 * 		int		DayNo	Day number for that year
	 * 		int		Hr		Hours
	 * 		int		Mn		Minutes
	 * 		int		Sc		Seconds
	 * 
	 * OUTPUTS : 
	 * 		double	*Xout	x GEI coordinate (R_E)
	 * 		double	*Yout	y GEI coordinate (R_E)
	 * 		double	*Zout	z GEI coordinate (R_E)
	 * 
	 * RETURNS : 
	 * 		void
	 * 
	 * PROCESS : 
	 * 		[1] Calls recalc_08_ function in FORTRAN (if recalc != 0)
	 * 		[2] Calls FORTRAN code to convert from GEO to GEI coordinates
	 * 
	 * ********************************************************************/
	void GEOtoGEI(	double Xin, double Yin, double Zin, 
					double Vx, double Vy, double Vz, int recalc,
					int Year, int DayNo, int Hr, int Mn, int Sc, 
					double *Xout, double *Yout, double *Zout);

	void GEOtoGEIUT(	double *Xin, double *Yin, double *Zin, int n, 
						double *Vx, double *Vy, double *Vz, 
						int *Date, float *ut, 
						double *Xout, double *Yout, double *Zout);




	/***********************************************************************
	 * NAME : 			void GSMtoGEO(	Xin, Yin, Zin, Vx, Vy, Vz, recalc,
	 *									Year, DayNo, Hr, Mn, Sc, 
	 *									*Xout, *Yout, *Zout)
	 * 
	 * DESCRIPTION : 	Wrapper for converting GSM to GEO coordinates
	 * 
	 * INPUTS : 
	 * 		double	Xin		x GSM coordinate (R_E)
	 * 		double	Yin		y GSM coordinate (R_E)
	 * 		double	Zin		z GSM coordinate (R_E)
	 * 		double 	Vx		x-component of SW velocity in km/s
	 * 		double 	Vy		y-component of SW velocity in km/s
	 * 		double 	Vz		z-component of SW velocity in km/s
	 * 		int		recalc	Set to one ro call recalc_08_
	 * 		int		Year	Year
	 * 		int		DayNo	Day number for that year
	 * 		int		Hr		Hours
	 * 		int		Mn		Minutes
	 * 		int		Sc		Seconds
	 * 
	 * OUTPUTS : 
	 * 		double	*Xout	x GEO coordinate (R_E)
	 * 		double	*Yout	y GEO coordinate (R_E)
	 * 		double	*Zout	z GEO coordinate (R_E)
	 * 
	 * RETURNS : 
	 * 		void
	 * 
	 * PROCESS : 
	 * 		[1] Calls recalc_08_ function in FORTRAN (if recalc != 0)
	 * 		[2] Calls FORTRAN code to convert from GSM to GEO coordinates
	 * 
	 * ********************************************************************/
	void GSMtoGEO(	double Xin, double Yin, double Zin, 
					double Vx, double Vy, double Vz, int recalc,
					int Year, int DayNo, int Hr, int Mn, int Sc, 
					double *Xout, double *Yout, double *Zout);
					
	void GSMtoGEOUT(	double *Xin, double *Yin, double *Zin, int n, 
						double *Vx, double *Vy, double *Vz, 
						int *Date, float *ut, 
						double *Xout, double *Yout, double *Zout);


	/***********************************************************************
	 * NAME : 			void GEOtoGSM(	Xin, Yin, Zin, Vx, Vy, Vz, recalc,
	 *									Year, DayNo, Hr, Mn, Sc, 
	 *									*Xout, *Yout, *Zout)
	 * 
	 * DESCRIPTION : 	Wrapper for converting GEO to GSM coordinates
	 * 
	 * INPUTS : 
	 * 		double	Xin		x GEO coordinate (R_E)
	 * 		double	Yin		y GEO coordinate (R_E)
	 * 		double	Zin		z GEO coordinate (R_E)
	 * 		double 	Vx		x-component of SW velocity in km/s
	 * 		double 	Vy		y-component of SW velocity in km/s
	 * 		double 	Vz		z-component of SW velocity in km/s
	 * 		int		recalc	Set to one ro call recalc_08_
	 * 		int		Year	Year
	 * 		int		DayNo	Day number for that year
	 * 		int		Hr		Hours
	 * 		int		Mn		Minutes
	 * 		int		Sc		Seconds
	 * 
	 * OUTPUTS : 
	 * 		double	*Xout	x GSM coordinate (R_E)
	 * 		double	*Yout	y GSM coordinate (R_E)
	 * 		double	*Zout	z GSM coordinate (R_E)
	 * 
	 * RETURNS : 
	 * 		void
	 * 
	 * PROCESS : 
	 * 		[1] Calls recalc_08_ function in FORTRAN (if recalc != 0)
	 * 		[2] Calls FORTRAN code to convert from GEO to GSM coordinates
	 * 
	 * ********************************************************************/
	void GEOtoGSM(	double Xin, double Yin, double Zin, 
					double Vx, double Vy, double Vz, int recalc,
					int Year, int DayNo, int Hr, int Mn, int Sc, 
					double *Xout, double *Yout, double *Zout);

	void GEOtoGSMUT(	double *Xin, double *Yin, double *Zin, int n, 
						double *Vx, double *Vy, double *Vz, 
						int *Date, float *ut, 
						double *Xout, double *Yout, double *Zout);






	/***********************************************************************
	 * NAME : 			void GSEtoGEO(	Xin, Yin, Zin, Vx, Vy, Vz, recalc,
	 *									Year, DayNo, Hr, Mn, Sc, 
	 *									*Xout, *Yout, *Zout)
	 * 
	 * DESCRIPTION : 	Wrapper for converting GSE to GEO coordinates
	 * 
	 * INPUTS : 
	 * 		double	Xin		x GSE coordinate (R_E)
	 * 		double	Yin		y GSE coordinate (R_E)
	 * 		double	Zin		z GSE coordinate (R_E)
	 * 		double 	Vx		x-component of SW velocity in km/s
	 * 		double 	Vy		y-component of SW velocity in km/s
	 * 		double 	Vz		z-component of SW velocity in km/s
	 * 		int		recalc	Set to one ro call recalc_08_
	 * 		int		Year	Year
	 * 		int		DayNo	Day number for that year
	 * 		int		Hr		Hours
	 * 		int		Mn		Minutes
	 * 		int		Sc		Seconds
	 * 
	 * OUTPUTS : 
	 * 		double	*Xout	x GEO coordinate (R_E)
	 * 		double	*Yout	y GEO coordinate (R_E)
	 * 		double	*Zout	z GEO coordinate (R_E)
	 * 
	 * RETURNS : 
	 * 		void
	 * 
	 * PROCESS : 
	 * 		[1] Calls recalc_08_ function in FORTRAN (if recalc != 0)
	 * 		[2] Calls FORTRAN code to convert from GSE to GEO coordinates
	 * 
	 * ********************************************************************/
	void GSEtoGEO(	double Xin, double Yin, double Zin, 
					double Vx, double Vy, double Vz, int recalc,
					int Year, int DayNo, int Hr, int Mn, int Sc, 
					double *Xout, double *Yout, double *Zout);

	void GSEtoGEOUT(	double *Xin, double *Yin, double *Zin, int n, 
						double *Vx, double *Vy, double *Vz, 
						int *Date, float *ut, 
						double *Xout, double *Yout, double *Zout);



	/***********************************************************************
	 * NAME : 			void GEOtoGSE(	Xin, Yin, Zin, Vx, Vy, Vz, recalc,
	 *									Year, DayNo, Hr, Mn, Sc, 
	 *									*Xout, *Yout, *Zout)
	 * 
	 * DESCRIPTION : 	Wrapper for converting GEO to GSE coordinates
	 * 
	 * INPUTS : 
	 * 		double	Xin		x GEO coordinate (R_E)
	 * 		double	Yin		y GEO coordinate (R_E)
	 * 		double	Zin		z GEO coordinate (R_E)
	 * 		double 	Vx		x-component of SW velocity in km/s
	 * 		double 	Vy		y-component of SW velocity in km/s
	 * 		double 	Vz		z-component of SW velocity in km/s
	 * 		int		recalc	Set to one ro call recalc_08_
	 * 		int		Year	Year
	 * 		int		DayNo	Day number for that year
	 * 		int		Hr		Hours
	 * 		int		Mn		Minutes
	 * 		int		Sc		Seconds
	 * 
	 * OUTPUTS : 
	 * 		double	*Xout	x GSE coordinate (R_E)
	 * 		double	*Yout	y GSE coordinate (R_E)
	 * 		double	*Zout	z GSE coordinate (R_E)
	 * 
	 * RETURNS : 
	 * 		void
	 * 
	 * PROCESS : 
	 * 		[1] Calls recalc_08_ function in FORTRAN (if recalc != 0)
	 * 		[2] Calls FORTRAN code to convert from GEO to GSE coordinates
	 * 
	 * ********************************************************************/
	void GEOtoGSE(	double Xin, double Yin, double Zin, 
					double Vx, double Vy, double Vz, int recalc,
					int Year, int DayNo, int Hr, int Mn, int Sc, 
					double *Xout, double *Yout, double *Zout);

	void GEOtoGSEUT(	double *Xin, double *Yin, double *Zin, int n, 
						double *Vx, double *Vy, double *Vz, 
						int *Date, float *ut, 
						double *Xout, double *Yout, double *Zout);






	/***********************************************************************
	 * NAME : 			void SMtoGEO(	Xin, Yin, Zin, Vx, Vy, Vz, recalc,
	 *									Year, DayNo, Hr, Mn, Sc, 
	 *									*Xout, *Yout, *Zout)
	 * 
	 * DESCRIPTION : 	Wrapper for converting SM to GEO coordinates
	 * 
	 * INPUTS : 
	 * 		double	Xin		x SM coordinate (R_E)
	 * 		double	Yin		y SM coordinate (R_E)
	 * 		double	Zin		z SM coordinate (R_E)
	 * 		double 	Vx		x-component of SW velocity in km/s
	 * 		double 	Vy		y-component of SW velocity in km/s
	 * 		double 	Vz		z-component of SW velocity in km/s
	 * 		int		recalc	Set to one ro call recalc_08_
	 * 		int		Year	Year
	 * 		int		DayNo	Day number for that year
	 * 		int		Hr		Hours
	 * 		int		Mn		Minutes
	 * 		int		Sc		Seconds
	 * 
	 * OUTPUTS : 
	 * 		double	*Xout	x GEO coordinate (R_E)
	 * 		double	*Yout	y GEO coordinate (R_E)
	 * 		double	*Zout	z GEO coordinate (R_E)
	 * 
	 * RETURNS : 
	 * 		void
	 * 
	 * PROCESS : 
	 * 		[1] Calls recalc_08_ function in FORTRAN (if recalc != 0)
	 * 		[2] Calls FORTRAN code to convert from SM to GEO coordinates
	 * 
	 * ********************************************************************/
	void SMtoGEO(	double Xin, double Yin, double Zin, 
					double Vx, double Vy, double Vz, int recalc,
					int Year, int DayNo, int Hr, int Mn, int Sc, 
					double *Xout, double *Yout, double *Zout);

	void SMtoGEOUT(	double *Xin, double *Yin, double *Zin, int n, 
						double *Vx, double *Vy, double *Vz, 
						int *Date, float *ut, 
						double *Xout, double *Yout, double *Zout);


	/***********************************************************************
	 * NAME : 			void GEOtoSM(	Xin, Yin, Zin, Vx, Vy, Vz, recalc,
	 *									Year, DayNo, Hr, Mn, Sc, 
	 *									*Xout, *Yout, *Zout)
	 * 
	 * DESCRIPTION : 	Wrapper for converting GEO to SM coordinates
	 * 
	 * INPUTS : 
	 * 		double	Xin		x GEO coordinate (R_E)
	 * 		double	Yin		y GEO coordinate (R_E)
	 * 		double	Zin		z GEO coordinate (R_E)
	 * 		double 	Vx		x-component of SW velocity in km/s
	 * 		double 	Vy		y-component of SW velocity in km/s
	 * 		double 	Vz		z-component of SW velocity in km/s
	 * 		int		recalc	Set to one ro call recalc_08_
	 * 		int		Year	Year
	 * 		int		DayNo	Day number for that year
	 * 		int		Hr		Hours
	 * 		int		Mn		Minutes
	 * 		int		Sc		Seconds
	 * 
	 * OUTPUTS : 
	 * 		double	*Xout	x SM coordinate (R_E)
	 * 		double	*Yout	y SM coordinate (R_E)
	 * 		double	*Zout	z SM coordinate (R_E)
	 * 
	 * RETURNS : 
	 * 		void
	 * 
	 * PROCESS : 
	 * 		[1] Calls recalc_08_ function in FORTRAN (if recalc != 0)
	 * 		[2] Calls FORTRAN code to convert from GEO to SM coordinates
	 * 
	 * ********************************************************************/
	void GEOtoSM(	double Xin, double Yin, double Zin, 
					double Vx, double Vy, double Vz, int recalc,
					int Year, int DayNo, int Hr, int Mn, int Sc, 
					double *Xout, double *Yout, double *Zout);

	void GEOtoSMUT(	double *Xin, double *Yin, double *Zin, int n, 
						double *Vx, double *Vy, double *Vz, 
						int *Date, float *ut, 
						double *Xout, double *Yout, double *Zout);




	/***********************************************************************
	 * NAME : 			void GSEtoGEI(	Xin, Yin, Zin, Vx, Vy, Vz, recalc,
	 *									Year, DayNo, Hr, Mn, Sc, 
	 *									*Xout, *Yout, *Zout)
	 * 
	 * DESCRIPTION : 	Wrapper for converting GSE to GEI coordinates
	 * 
	 * INPUTS : 
	 * 		double	Xin		x GSE coordinate (R_E)
	 * 		double	Yin		y GSE coordinate (R_E)
	 * 		double	Zin		z GSE coordinate (R_E)
	 * 		double 	Vx		x-component of SW velocity in km/s
	 * 		double 	Vy		y-component of SW velocity in km/s
	 * 		double 	Vz		z-component of SW velocity in km/s
	 * 		int		recalc	Set to one ro call recalc_08_
	 * 		int		Year	Year
	 * 		int		DayNo	Day number for that year
	 * 		int		Hr		Hours
	 * 		int		Mn		Minutes
	 * 		int		Sc		Seconds
	 * 
	 * OUTPUTS : 
	 * 		double	*Xout	x GEI coordinate (R_E)
	 * 		double	*Yout	y GEI coordinate (R_E)
	 * 		double	*Zout	z GEI coordinate (R_E)
	 * 
	 * RETURNS : 
	 * 		void
	 * 
	 * PROCESS : 
	 * 		[1] Calls recalc_08_ function in FORTRAN (if recalc != 0)
	 * 		[2] Calls FORTRAN code to convert from GSE to GEI coordinates
	 * 
	 * ********************************************************************/
	void GSEtoGEI(	double Xin, double Yin, double Zin, 
					double Vx, double Vy, double Vz, int recalc,
					int Year, int DayNo, int Hr, int Mn, int Sc, 
					double *Xout, double *Yout, double *Zout);

	void GSEtoGEIUT(	double *Xin, double *Yin, double *Zin, int n, 
						double *Vx, double *Vy, double *Vz, 
						int *Date, float *ut, 
						double *Xout, double *Yout, double *Zout);



	/***********************************************************************
	 * NAME : 			void GEItoGSE(	Xin, Yin, Zin, Vx, Vy, Vz, recalc,
	 *									Year, DayNo, Hr, Mn, Sc, 
	 *									*Xout, *Yout, *Zout)
	 * 
	 * DESCRIPTION : 	Wrapper for converting GEI to GSE coordinates
	 * 
	 * INPUTS : 
	 * 		double	Xin		x GEI coordinate (R_E)
	 * 		double	Yin		y GEI coordinate (R_E)
	 * 		double	Zin		z GEI coordinate (R_E)
	 * 		double 	Vx		x-component of SW velocity in km/s
	 * 		double 	Vy		y-component of SW velocity in km/s
	 * 		double 	Vz		z-component of SW velocity in km/s
	 * 		int		recalc	Set to one ro call recalc_08_
	 * 		int		Year	Year
	 * 		int		DayNo	Day number for that year
	 * 		int		Hr		Hours
	 * 		int		Mn		Minutes
	 * 		int		Sc		Seconds
	 * 
	 * OUTPUTS : 
	 * 		double	*Xout	x GSE coordinate (R_E)
	 * 		double	*Yout	y GSE coordinate (R_E)
	 * 		double	*Zout	z GSE coordinate (R_E)
	 * 
	 * RETURNS : 
	 * 		void
	 * 
	 * PROCESS : 
	 * 		[1] Calls recalc_08_ function in FORTRAN (if recalc != 0)
	 * 		[2] Calls FORTRAN code to convert from GEI to GSE coordinates
	 * 
	 * ********************************************************************/
	void GEItoGSE(	double Xin, double Yin, double Zin, 
					double Vx, double Vy, double Vz, int recalc,
					int Year, int DayNo, int Hr, int Mn, int Sc, 
					double *Xout, double *Yout, double *Zout);

	void GEItoGSEUT(	double *Xin, double *Yin, double *Zin, int n, 
						double *Vx, double *Vy, double *Vz, 
						int *Date, float *ut, 
						double *Xout, double *Yout, double *Zout);


	/***********************************************************************
	 * NAME : 			void GSMtoGEI(	Xin, Yin, Zin, Vx, Vy, Vz, recalc,
	 *									Year, DayNo, Hr, Mn, Sc, 
	 *									*Xout, *Yout, *Zout)
	 * 
	 * DESCRIPTION : 	Wrapper for converting GSM to GEI coordinates
	 * 
	 * INPUTS : 
	 * 		double	Xin		x GSM coordinate (R_E)
	 * 		double	Yin		y GSM coordinate (R_E)
	 * 		double	Zin		z GSM coordinate (R_E)
	 * 		double 	Vx		x-component of SW velocity in km/s
	 * 		double 	Vy		y-component of SW velocity in km/s
	 * 		double 	Vz		z-component of SW velocity in km/s
	 * 		int		recalc	Set to one ro call recalc_08_
	 * 		int		Year	Year
	 * 		int		DayNo	Day number for that year
	 * 		int		Hr		Hours
	 * 		int		Mn		Minutes
	 * 		int		Sc		Seconds
	 * 
	 * OUTPUTS : 
	 * 		double	*Xout	x GEI coordinate (R_E)
	 * 		double	*Yout	y GEI coordinate (R_E)
	 * 		double	*Zout	z GEI coordinate (R_E)
	 * 
	 * RETURNS : 
	 * 		void
	 * 
	 * PROCESS : 
	 * 		[1] Calls recalc_08_ function in FORTRAN (if recalc != 0)
	 * 		[2] Calls FORTRAN code to convert from GSM to GEI coordinates
	 * 
	 * ********************************************************************/
	void GSMtoGEI(	double Xin, double Yin, double Zin, 
					double Vx, double Vy, double Vz, int recalc,
					int Year, int DayNo, int Hr, int Mn, int Sc, 
					double *Xout, double *Yout, double *Zout);

	void GSMtoGEIUT(	double *Xin, double *Yin, double *Zin, int n, 
						double *Vx, double *Vy, double *Vz, 
						int *Date, float *ut, 
						double *Xout, double *Yout, double *Zout);



	/***********************************************************************
	 * NAME : 			void GEItoGSM(	Xin, Yin, Zin, Vx, Vy, Vz, recalc,
	 *									Year, DayNo, Hr, Mn, Sc, 
	 *									*Xout, *Yout, *Zout)
	 * 
	 * DESCRIPTION : 	Wrapper for converting GEI to GSM coordinates
	 * 
	 * INPUTS : 
	 * 		double	Xin		x GEI coordinate (R_E)
	 * 		double	Yin		y GEI coordinate (R_E)
	 * 		double	Zin		z GEI coordinate (R_E)
	 * 		double 	Vx		x-component of SW velocity in km/s
	 * 		double 	Vy		y-component of SW velocity in km/s
	 * 		double 	Vz		z-component of SW velocity in km/s
	 * 		int		recalc	Set to one ro call recalc_08_
	 * 		int		Year	Year
	 * 		int		DayNo	Day number for that year
	 * 		int		Hr		Hours
	 * 		int		Mn		Minutes
	 * 		int		Sc		Seconds
	 * 
	 * OUTPUTS : 
	 * 		double	*Xout	x GSM coordinate (R_E)
	 * 		double	*Yout	y GSM coordinate (R_E)
	 * 		double	*Zout	z GSM coordinate (R_E)
	 * 
	 * RETURNS : 
	 * 		void
	 * 
	 * PROCESS : 
	 * 		[1] Calls recalc_08_ function in FORTRAN (if recalc != 0)
	 * 		[2] Calls FORTRAN code to convert from GEI to GSM coordinates
	 * 
	 * ********************************************************************/
	void GEItoGSM(	double Xin, double Yin, double Zin, 
					double Vx, double Vy, double Vz, int recalc,
					int Year, int DayNo, int Hr, int Mn, int Sc, 
					double *Xout, double *Yout, double *Zout);

	void GEItoGSMUT(	double *Xin, double *Yin, double *Zin, int n, 
						double *Vx, double *Vy, double *Vz, 
						int *Date, float *ut, 
						double *Xout, double *Yout, double *Zout);


	/***********************************************************************
	 * NAME : 			void SMtoGEI(	Xin, Yin, Zin, Vx, Vy, Vz, recalc,
	 *									Year, DayNo, Hr, Mn, Sc, 
	 *									*Xout, *Yout, *Zout)
	 * 
	 * DESCRIPTION : 	Wrapper for converting SM to GEI coordinates
	 * 
	 * INPUTS : 
	 * 		double	Xin		x SM coordinate (R_E)
	 * 		double	Yin		y SM coordinate (R_E)
	 * 		double	Zin		z SM coordinate (R_E)
	 * 		double 	Vx		x-component of SW velocity in km/s
	 * 		double 	Vy		y-component of SW velocity in km/s
	 * 		double 	Vz		z-component of SW velocity in km/s
	 * 		int		recalc	Set to one ro call recalc_08_
	 * 		int		Year	Year
	 * 		int		DayNo	Day number for that year
	 * 		int		Hr		Hours
	 * 		int		Mn		Minutes
	 * 		int		Sc		Seconds
	 * 
	 * OUTPUTS : 
	 * 		double	*Xout	x GEI coordinate (R_E)
	 * 		double	*Yout	y GEI coordinate (R_E)
	 * 		double	*Zout	z GEI coordinate (R_E)
	 * 
	 * RETURNS : 
	 * 		void
	 * 
	 * PROCESS : 
	 * 		[1] Calls recalc_08_ function in FORTRAN (if recalc != 0)
	 * 		[2] Calls FORTRAN code to convert from SM to GEI coordinates
	 * 
	 * ********************************************************************/
	void SMtoGEI(	double Xin, double Yin, double Zin, 
					double Vx, double Vy, double Vz, int recalc,
					int Year, int DayNo, int Hr, int Mn, int Sc, 
					double *Xout, double *Yout, double *Zout);

	void SMtoGEIUT(	double *Xin, double *Yin, double *Zin, int n, 
						double *Vx, double *Vy, double *Vz, 
						int *Date, float *ut, 
						double *Xout, double *Yout, double *Zout);



	/***********************************************************************
	 * NAME : 			void GEItoSM(	Xin, Yin, Zin, Vx, Vy, Vz, recalc,
	 *									Year, DayNo, Hr, Mn, Sc, 
	 *									*Xout, *Yout, *Zout)
	 * 
	 * DESCRIPTION : 	Wrapper for converting GEI to SM coordinates
	 * 
	 * INPUTS : 
	 * 		double	Xin		x GEI coordinate (R_E)
	 * 		double	Yin		y GEI coordinate (R_E)
	 * 		double	Zin		z GEI coordinate (R_E)
	 * 		double 	Vx		x-component of SW velocity in km/s
	 * 		double 	Vy		y-component of SW velocity in km/s
	 * 		double 	Vz		z-component of SW velocity in km/s
	 * 		int		recalc	Set to one ro call recalc_08_
	 * 		int		Year	Year
	 * 		int		DayNo	Day number for that year
	 * 		int		Hr		Hours
	 * 		int		Mn		Minutes
	 * 		int		Sc		Seconds
	 * 
	 * OUTPUTS : 
	 * 		double	*Xout	x SM coordinate (R_E)
	 * 		double	*Yout	y SM coordinate (R_E)
	 * 		double	*Zout	z SM coordinate (R_E)
	 * 
	 * RETURNS : 
	 * 		void
	 * 
	 * PROCESS : 
	 * 		[1] Calls recalc_08_ function in FORTRAN (if recalc != 0)
	 * 		[2] Calls FORTRAN code to convert from GEI to SM coordinates
	 * 
	 * ********************************************************************/
	void GEItoSM(	double Xin, double Yin, double Zin, 
					double Vx, double Vy, double Vz, int recalc,
					int Year, int DayNo, int Hr, int Mn, int Sc, 
					double *Xout, double *Yout, double *Zout);

	void GEItoSMUT(	double *Xin, double *Yin, double *Zin, int n, 
						double *Vx, double *Vy, double *Vz, 
						int *Date, float *ut, 
						double *Xout, double *Yout, double *Zout);









	/***********************************************************************
	 * NAME : 			void MAGtoGEI(	Xin, Yin, Zin, Vx, Vy, Vz, recalc,
	 *									Year, DayNo, Hr, Mn, Sc, 
	 *									*Xout, *Yout, *Zout)
	 * 
	 * DESCRIPTION : 	Wrapper for converting MAG to GEI coordinates
	 * 
	 * INPUTS : 
	 * 		double	Xin		x MAG coordinate (R_E)
	 * 		double	Yin		y MAG coordinate (R_E)
	 * 		double	Zin		z MAG coordinate (R_E)
	 * 		double 	Vx		x-component of SW velocity in km/s
	 * 		double 	Vy		y-component of SW velocity in km/s
	 * 		double 	Vz		z-component of SW velocity in km/s
	 * 		int		recalc	Set to one ro call recalc_08_
	 * 		int		Year	Year
	 * 		int		DayNo	Day number for that year
	 * 		int		Hr		Hours
	 * 		int		Mn		Minutes
	 * 		int		Sc		Seconds
	 * 
	 * OUTPUTS : 
	 * 		double	*Xout	x GEI coordinate (R_E)
	 * 		double	*Yout	y GEI coordinate (R_E)
	 * 		double	*Zout	z GEI coordinate (R_E)
	 * 
	 * RETURNS : 
	 * 		void
	 * 
	 * PROCESS : 
	 * 		[1] Calls recalc_08_ function in FORTRAN (if recalc != 0)
	 * 		[2] Calls FORTRAN code to convert from MAG to GEI coordinates
	 * 
	 * ********************************************************************/
	void MAGtoGEI(	double Xin, double Yin, double Zin, 
					double Vx, double Vy, double Vz, int recalc,
					int Year, int DayNo, int Hr, int Mn, int Sc, 
					double *Xout, double *Yout, double *Zout);

	void MAGtoGEIUT(	double *Xin, double *Yin, double *Zin, int n, 
						double *Vx, double *Vy, double *Vz, 
						int *Date, float *ut, 
						double *Xout, double *Yout, double *Zout);



	/***********************************************************************
	 * NAME : 			void GEItoMAG(	Xin, Yin, Zin, Vx, Vy, Vz, recalc,
	 *									Year, DayNo, Hr, Mn, Sc, 
	 *									*Xout, *Yout, *Zout)
	 * 
	 * DESCRIPTION : 	Wrapper for converting GEI to MAG coordinates
	 * 
	 * INPUTS : 
	 * 		double	Xin		x GEI coordinate (R_E)
	 * 		double	Yin		y GEI coordinate (R_E)
	 * 		double	Zin		z GEI coordinate (R_E)
	 * 		double 	Vx		x-component of SW velocity in km/s
	 * 		double 	Vy		y-component of SW velocity in km/s
	 * 		double 	Vz		z-component of SW velocity in km/s
	 * 		int		recalc	Set to one ro call recalc_08_
	 * 		int		Year	Year
	 * 		int		DayNo	Day number for that year
	 * 		int		Hr		Hours
	 * 		int		Mn		Minutes
	 * 		int		Sc		Seconds
	 * 
	 * OUTPUTS : 
	 * 		double	*Xout	x MAG coordinate (R_E)
	 * 		double	*Yout	y MAG coordinate (R_E)
	 * 		double	*Zout	z MAG coordinate (R_E)
	 * 
	 * RETURNS : 
	 * 		void
	 * 
	 * PROCESS : 
	 * 		[1] Calls recalc_08_ function in FORTRAN (if recalc != 0)
	 * 		[2] Calls FORTRAN code to convert from GEI to MAG coordinates
	 * 
	 * ********************************************************************/
	void GEItoMAG(	double Xin, double Yin, double Zin, 
					double Vx, double Vy, double Vz, int recalc,
					int Year, int DayNo, int Hr, int Mn, int Sc, 
					double *Xout, double *Yout, double *Zout);

	void GEItoMAGUT(	double *Xin, double *Yin, double *Zin, int n, 
						double *Vx, double *Vy, double *Vz, 
						int *Date, float *ut, 
						double *Xout, double *Yout, double *Zout);




	/***********************************************************************
	 * NAME : 			void MAGtoGSM(	Xin, Yin, Zin, Vx, Vy, Vz, recalc,
	 *									Year, DayNo, Hr, Mn, Sc, 
	 *									*Xout, *Yout, *Zout)
	 * 
	 * DESCRIPTION : 	Wrapper for converting MAG to GSM coordinates
	 * 
	 * INPUTS : 
	 * 		double	Xin		x MAG coordinate (R_E)
	 * 		double	Yin		y MAG coordinate (R_E)
	 * 		double	Zin		z MAG coordinate (R_E)
	 * 		double 	Vx		x-component of SW velocity in km/s
	 * 		double 	Vy		y-component of SW velocity in km/s
	 * 		double 	Vz		z-component of SW velocity in km/s
	 * 		int		recalc	Set to one ro call recalc_08_
	 * 		int		Year	Year
	 * 		int		DayNo	Day number for that year
	 * 		int		Hr		Hours
	 * 		int		Mn		Minutes
	 * 		int		Sc		Seconds
	 * 
	 * OUTPUTS : 
	 * 		double	*Xout	x GSM coordinate (R_E)
	 * 		double	*Yout	y GSM coordinate (R_E)
	 * 		double	*Zout	z GSM coordinate (R_E)
	 * 
	 * RETURNS : 
	 * 		void
	 * 
	 * PROCESS : 
	 * 		[1] Calls recalc_08_ function in FORTRAN (if recalc != 0)
	 * 		[2] Calls FORTRAN code to convert from MAG to GSM coordinates
	 * 
	 * ********************************************************************/
	void MAGtoGSM(	double Xin, double Yin, double Zin, 
					double Vx, double Vy, double Vz, int recalc,
					int Year, int DayNo, int Hr, int Mn, int Sc, 
					double *Xout, double *Yout, double *Zout);

	void MAGtoGSMUT(	double *Xin, double *Yin, double *Zin, int n, 
						double *Vx, double *Vy, double *Vz, 
						int *Date, float *ut, 
						double *Xout, double *Yout, double *Zout);



	/***********************************************************************
	 * NAME : 			void GSMtoMAG(	Xin, Yin, Zin, Vx, Vy, Vz, recalc,
	 *									Year, DayNo, Hr, Mn, Sc, 
	 *									*Xout, *Yout, *Zout)
	 * 
	 * DESCRIPTION : 	Wrapper for converting GSM to MAG coordinates
	 * 
	 * INPUTS : 
	 * 		double	Xin		x GSM coordinate (R_E)
	 * 		double	Yin		y GSM coordinate (R_E)
	 * 		double	Zin		z GSM coordinate (R_E)
	 * 		double 	Vx		x-component of SW velocity in km/s
	 * 		double 	Vy		y-component of SW velocity in km/s
	 * 		double 	Vz		z-component of SW velocity in km/s
	 * 		int		recalc	Set to one ro call recalc_08_
	 * 		int		Year	Year
	 * 		int		DayNo	Day number for that year
	 * 		int		Hr		Hours
	 * 		int		Mn		Minutes
	 * 		int		Sc		Seconds
	 * 
	 * OUTPUTS : 
	 * 		double	*Xout	x MAG coordinate (R_E)
	 * 		double	*Yout	y MAG coordinate (R_E)
	 * 		double	*Zout	z MAG coordinate (R_E)
	 * 
	 * RETURNS : 
	 * 		void
	 * 
	 * PROCESS : 
	 * 		[1] Calls recalc_08_ function in FORTRAN (if recalc != 0)
	 * 		[2] Calls FORTRAN code to convert from GSM to MAG coordinates
	 * 
	 * ********************************************************************/
	void GSMtoMAG(	double Xin, double Yin, double Zin, 
					double Vx, double Vy, double Vz, int recalc,
					int Year, int DayNo, int Hr, int Mn, int Sc, 
					double *Xout, double *Yout, double *Zout);

	void GSMtoMAGUT(	double *Xin, double *Yin, double *Zin, int n, 
						double *Vx, double *Vy, double *Vz, 
						int *Date, float *ut, 
						double *Xout, double *Yout, double *Zout);





	/***********************************************************************
	 * NAME : 			void MAGtoSM(	Xin, Yin, Zin, Vx, Vy, Vz, recalc,
	 *									Year, DayNo, Hr, Mn, Sc, 
	 *									*Xout, *Yout, *Zout)
	 * 
	 * DESCRIPTION : 	Wrapper for converting MAG to SM coordinates
	 * 
	 * INPUTS : 
	 * 		double	Xin		x MAG coordinate (R_E)
	 * 		double	Yin		y MAG coordinate (R_E)
	 * 		double	Zin		z MAG coordinate (R_E)
	 * 		double 	Vx		x-component of SW velocity in km/s
	 * 		double 	Vy		y-component of SW velocity in km/s
	 * 		double 	Vz		z-component of SW velocity in km/s
	 * 		int		recalc	Set to one ro call recalc_08_
	 * 		int		Year	Year
	 * 		int		DayNo	Day number for that year
	 * 		int		Hr		Hours
	 * 		int		Mn		Minutes
	 * 		int		Sc		Seconds
	 * 
	 * OUTPUTS : 
	 * 		double	*Xout	x SM coordinate (R_E)
	 * 		double	*Yout	y SM coordinate (R_E)
	 * 		double	*Zout	z SM coordinate (R_E)
	 * 
	 * RETURNS : 
	 * 		void
	 * 
	 * PROCESS : 
	 * 		[1] Calls recalc_08_ function in FORTRAN (if recalc != 0)
	 * 		[2] Calls FORTRAN code to convert from MAG to SM coordinates
	 * 
	 * ********************************************************************/
	void MAGtoSM(	double Xin, double Yin, double Zin, 
					double Vx, double Vy, double Vz, int recalc,
					int Year, int DayNo, int Hr, int Mn, int Sc, 
					double *Xout, double *Yout, double *Zout);

	void MAGtoSMUT(	double *Xin, double *Yin, double *Zin, int n, 
						double *Vx, double *Vy, double *Vz, 
						int *Date, float *ut, 
						double *Xout, double *Yout, double *Zout);



	/***********************************************************************
	 * NAME : 			void SMtoMAG(	Xin, Yin, Zin, Vx, Vy, Vz, recalc,
	 *									Year, DayNo, Hr, Mn, Sc, 
	 *									*Xout, *Yout, *Zout)
	 * 
	 * DESCRIPTION : 	Wrapper for converting SM to MAG coordinates
	 * 
	 * INPUTS : 
	 * 		double	Xin		x SM coordinate (R_E)
	 * 		double	Yin		y SM coordinate (R_E)
	 * 		double	Zin		z SM coordinate (R_E)
	 * 		double 	Vx		x-component of SW velocity in km/s
	 * 		double 	Vy		y-component of SW velocity in km/s
	 * 		double 	Vz		z-component of SW velocity in km/s
	 * 		int		recalc	Set to one ro call recalc_08_
	 * 		int		Year	Year
	 * 		int		DayNo	Day number for that year
	 * 		int		Hr		Hours
	 * 		int		Mn		Minutes
	 * 		int		Sc		Seconds
	 * 
	 * OUTPUTS : 
	 * 		double	*Xout	x MAG coordinate (R_E)
	 * 		double	*Yout	y MAG coordinate (R_E)
	 * 		double	*Zout	z MAG coordinate (R_E)
	 * 
	 * RETURNS : 
	 * 		void
	 * 
	 * PROCESS : 
	 * 		[1] Calls recalc_08_ function in FORTRAN (if recalc != 0)
	 * 		[2] Calls FORTRAN code to convert from SM to MAG coordinates
	 * 
	 * ********************************************************************/
	void SMtoMAG(	double Xin, double Yin, double Zin, 
					double Vx, double Vy, double Vz, int recalc,
					int Year, int DayNo, int Hr, int Mn, int Sc, 
					double *Xout, double *Yout, double *Zout);

	void SMtoMAGUT(	double *Xin, double *Yin, double *Zin, int n, 
						double *Vx, double *Vy, double *Vz, 
						int *Date, float *ut, 
						double *Xout, double *Yout, double *Zout);

bool WithinMP(double x, double y, double z, double Bz, double Pdyn);

	void TraceField(int n, double *xin, double *yin, double *zin,
					int *Date, float *ut, const char *Model,
					int *iopt, double **parmod, 
					double *Vx, double *Vy, double *Vz,
					double alt, int MaxLen, double DSMax, 
					bool Verbose, int TraceDir,
					const char *CoordIn, int *nstep,
					double **xgsm, double **ygsm, double **zgsm, 
					double **bxgsm, double **bygsm, double **bzgsm,
					double **xgse, double **ygse, double **zgse, 
					double **bxgse, double **bygse, double **bzgse,
					double **xsm, double **ysm, double **zsm, 
					double **bxsm, double **bysm, double **bzsm,
					double **s, double **r, double **rnorm, double **FP,
					int nalpha, double *alpha, double *halpha);

typedef void (*ModelFuncPtr)(int*,double*,double*,double*,double*,double*,double*,double*,double*);
typedef void (*InternalFuncPtr) (double*,double*,double*,double*,double*,double*);


/* function prototypes for coordinate system conversion */
	void geigeo_08_(double *xgei, double *ygei, double *zgei, double *xgeo, double *ygeo, double *zgeo, int *j);
	void geomag_08_(double *xgeo, double *ygeo, double *zgeo, double *xmag, double *ymag, double *zmag, int *j);
	void gswgse_08_(double *xgsw, double *ygsw, double *zgsw, double *xgse, double *ygse, double *zgse, int *j);
	void smgsw_08_(double *xsm, double *ysm, double *zsm, double *xgsw, double *ygsw, double *zgsw, int *j);
	void magsm_08_(double *xmag, double *ymag, double *zmag, double *xsm, double *ysm, double *zsm, int *j);
	void geogsw_08_(double *xgeo, double *ygeo, double *zgeo, double *xgsw, double *ygsw, double *zgsw, int *j);

/* prototype for initializing model parameters and rotation matrices */
	void recalc_08_(int *iyear, int *iday, int *ihour, int *min, int *isec, double *vgsex, double *vgsey, double *vgsez);

/* The trace wrapper function */
	void trace_08_(double *xi, double *yi, double *zi, double *dir, double *dsmax, double *err, double *rlim, double *r0, int *iopt, double *parmod, ModelFuncPtr ModelFunc, InternalFuncPtr IntFunc, double *xf, double *yf, double *zf, double *xx, double *yy, double *zz, int *L, int *Lmax);

/* IGRF Model function */
	void igrf_gsw_08_(double *xgsw, double *ygsw, double *zgsw, double *hxgsw, double *hygsw, double *hzgsw);

/* a function to returnt he dipole tilt */
	double getpsi_();

/* different model functions */

	void t89c_(int *iopt, double *parmod, double *ps, double *x, double *y, double *z, double *bx, double *by, double *bz);
	void t96_(int *iopt, double *parmod, double *ps, double *x, double *y, double *z, double *bx, double *by, double *bz);
	void t01_01_(int *iopt, double *parmod, double *ps, double *x, double *y, double *z, double *bx, double *by, double *bz);
	void t04_s_(int *iopt, double *parmod, double *ps, double *x, double *y, double *z, double *bx, double *by, double *bz);


/* stuff below this is C++ only */
#ifdef __cplusplus
	}

	void t89(int iopt, double *parmod, double psi, double x, double y, double z, double *Bx, double *By, double *Bz);

typedef struct ModelCFG{
	int n;
	int *Date;
	float *ut;
	bool SameTime;
	ModelFuncPtr model;
	int *iopt;
	double **parmod;
	double *Vx;
	double *Vy;
	double *Vz;
	const char *CoordIn;
	const char *CoordOut;
	bool WithinMPOnly;
} ModelCFG;

ModelCFG GetModelCFG(	int n, int *Date, float *ut, bool SameTime,
						const char *Model, int *iopt, double **parmod,
						double *Vx, double *Vy, double *Vz,
						const char *CoordIn, const char *CoordOut, bool WithinMPOnly); 

void ModelFieldNew(	int n, double *Xin, double *Yin, double *Zin, 
					ModelCFG cfg,double *Bx, double *By, double *Bz);




/***********************************************************************
 * This object will store a bunch of field traces within it.
 * 
 * It will have the ability to either allocate and store field vectors
 * and positions, or to accept pointers which can be created externally
 * (e.g. inside Python)
 * 
 * There will be optional member functions which obtain things like 
 * footprints and h_alphas.
 * 
 * The basic trace will be in GSM/GSW.
 * 
 * Other coordinate systems will be calculated as needed.
 * 
 * ********************************************************************/
class Trace {
	
	public:
		/* initialize the object */
		Trace();
		
		/* delete the object */
		~Trace();
		
		/* copy constructor */
	//	Trace(const Trace &);
		
		/* this will take in the input positions where the traces start*/
		void InputPos(int,double*,double*,double*,int*,float*,const char*, double*, double*, double*);
		void InputPos(int,double*,double*,double*,int*,float*,const char*);
		
		/* set model parameters */
		void SetModelParams(int*, double**);
		void SetModelParams();
		void SetModel(const char *);
		
		/* set the trace configuration */
		void SetTraceCFG(double,int,double,bool,int);
		void SetTraceCFG();
		
		/* polarization stuff */
		void SetAlpha(int,double*,double);

			
		/* trace function to do basic trace in GSW coords */
		void TraceGSM(int*,double**,double**,double**,double**,double**,double**);
		void TraceGSM(int*);
		void TraceGSM();
		
		
		/* these will convert to other coords */
		void TraceGSE(double**,double**,double**,double**,double**,double**);
		void TraceGSE();
		void TraceSM(double**,double**,double**,double**,double**,double**);
		void TraceSM();
	
		/* calculate trace distance,R,Rnorm */
		void CalculateTraceDist(double**);
		void CalculateTraceDist();
		void _CalculateTraceDist();
		void CalculateTraceR(double**);
		void CalculateTraceR();
		void _CalculateTraceR();
		void CalculateTraceRnorm(double**);
		void CalculateTraceRnorm();
		void _CalculateTraceRnorm();
	
		/* Calculate footprints */
		void CalculateTraceFP(double**);
		void CalculateTraceFP();
		void _CalculateTraceFP();
		
		/* calculate halpha */
		void CalculateHalpha();
		void CalculateHalpha(double*);
		void CalculateHalpha(double***);
		void CalculateHalpha(double*,double***);
	
		/* return things*/
		void GetTraceNstep(int*);
		void GetTraceGSM(double**,double**,double**);
		void GetTraceGSM(double**,double**,double**,double**,double**,double**);
		void GetTraceGSE(double**,double**,double**);
		void GetTraceGSE(double**,double**,double**,double**,double**,double**);
		void GetTraceSM(double**,double**,double**);
		void GetTraceSM(double**,double**,double**,double**,double**,double**);
		void GetTraceDist(double**);
		void GetTraceR(double**);
		void GetTraceRnorm(double**);
		void GetTraceFootprints(double**);
		void GetTraceHalpha(double*);	/* python will use this */
		void GetTraceHalpha(double***); /* no idea how to link this to python*/
		
		Trace TracePosition(int,double,double,double);
	

		/* input coords */
		int n_;
		double *x0_, *y0_, *z0_;  
		int *Date_;
		float *ut_;

		/* SW velocity */
		double *Vx_, *Vy_, *Vz_;

		/* trace params */
		int MaxLen_;
		double DSMax_;
		bool Verbose_;
		double alt_;
		int TraceDir_;
		
		/* model params */
		int *iopt_;
		double **parmod_;

		/* trace coords */
		int *nstep_;
		bool *inMP_;
		double **xgsm_, **ygsm_, **zgsm_;
		double **xgse_, **ygse_, **zgse_;
		double **xsm_, **ysm_, **zsm_;
	
		/* trace fields */
		double **bxgsm_, **bygsm_, **bzgsm_;
		double **bxgse_, **bygse_, **bzgse_;
		double **bxsm_, **bysm_, **bzsm_;

		/* trace end points */
		double *xfn_, *yfn_, *zfn_;
		double *xfs_, *yfs_, *zfs_;
		double *xfe_, *yfe_, *zfe_;

	private:
		/* booleans to tell the object what has been done */
		bool inputPos_;
		bool inputModelParams_,allocModelParams_;
		bool traceConfigured_;
		bool allocV_;
		bool tracedGSM_,allocGSM_;
		bool tracedGSE_,allocGSE_;
		bool tracedSM_,allocSM_;
		bool allocEndpoints_;
		bool hasFootprints_,allocFootprints_;
		bool hasDist_,allocDist_;
		bool hasR_,allocR_;
		bool hasRnorm_,allocRnorm_;
		bool hasHalpha_,allocHalpha_, allocHalpha3D_;
		bool setModel_;
		bool allocNstep_;
		bool allocAlpha_;
		bool allocEqFP_;
		bool allocMP_;

		

	
		/* field length, R, Rnorm, Halpha, Footprints */
		int nalpha_;
		double *alpha0_, *alpha1_;
		double Delta_;
		double **S_;
		double **R_;
		double **Rnorm_;
		double *Halpha_;
		double ***Halpha3D_;
		double **FP_;
		
		/* model */
		const char *Model_;
		ModelFuncPtr ModelFunc_;
	
		/* hidden trace functions */
		void _TraceGSM();
		void _TraceGSE();
		void _TraceSM();

		/* halpha functions */
		bool _CheckHalpha();
		void _CalculateHalpha();
		void _CalculateTraceHalpha(int,int,double*);
		void _CalculateHalphaStartPoints(int i, int j,
							double *xe0, double *ye0, double *ze0,
							double *xe1, double *ye1, double *ze1);
};



#endif

#endif
