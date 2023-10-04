@echo off
echo Compiling FORTRAN code
set BUILDDIR=..\..\build
gfortran -w -c -fPIC -fno-automatic -o %BUILDDIR%\T89c.o T89c.f
gfortran -w -c -fPIC -fno-automatic -o %BUILDDIR%\T96.o  T96.f
gfortran -w -c -fPIC -fno-automatic -o %BUILDDIR%\T01_01.o  T01_01.f
gfortran -w -c -fPIC -fno-automatic -o %BUILDDIR%\TS04c.o  TS04c.f
gfortran -w -c -fPIC -fno-automatic -o %BUILDDIR%\wparams.o  wparams.f95
gfortran -w -c -fPIC -fno-automatic -ffree-line-length-none -o %BUILDDIR%\Geopack-2008_mkj_dp.o Geopack-2008_mkj_dp.f
