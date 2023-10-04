# CFLAGS for CC
CFLAGS=-g -O3 -std=c++17 -Wextra -fPIC
FCFLAGS=-w -c -fPIC -fno-automatic -std=legacy -ffree-line-length-none -O3

# Compiler
FF=gfortran $(FCFLAGS)
CCo=g++ -c $(CFLAGS)


# set the build directory
ifndef BUILDDIR 
	BUILDDIR=../../build
endif

all: obj

obj:
	$(FF) -o $(BUILDDIR)/T89c.o T89c.f
	$(FF) -o $(BUILDDIR)/T96.o  T96.f
	$(FF) -o $(BUILDDIR)/T01_01.o  T01_01.f
	$(FF) -o $(BUILDDIR)/TS04c.o  TS04c.f
	$(FF) -o $(BUILDDIR)/wparams.o  wparams.f95
	$(FF) -o $(BUILDDIR)/Geopack-2008_mkj_dp.o Geopack-2008_mkj_dp.f
	$(CCo) -o $(BUILDDIR)/t89.o t89.cc

