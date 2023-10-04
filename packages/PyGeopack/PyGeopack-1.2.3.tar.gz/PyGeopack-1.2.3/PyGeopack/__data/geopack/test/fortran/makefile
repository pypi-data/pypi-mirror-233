# CFLAGS for CC
CFLAGS=-fopenmp -g -O3 -Wextra -fPIC -I../../include
CXXFLAGS=-fopenmp -g -O3 -std=c++17 -Wextra -fPIC -I../../include
FCFLAGS=-fopenmp -w -c -fPIC -fno-automatic -std=legacy -ffree-line-length-none -O3


OS=$(shell uname -s)
ifeq ($(OS),Linux)
	CC=gcc $(CFLAGS)
	CXX=g++ $(CXXFLAGS)
	FF=gfortran $(FCFLAGS)
	LDFLAGS=-lm -Wl,-rpath='$$ORIGIN/../../lib' -L ../../lib -lgeopack -lgfortran -L../../lib -ldatetime -L../../lib -lspline
else
	CC=gcc -Xpreprocessor$(CFLAGS)
	CXX=g++ -Xpreprocessor $(CXXFLAGS)
	FF=gfortran -Xpreprocessor $(FCFLAGS)	
	LDFLAGS=-lm -L../lib -lgeopack -lgfortran -L../../lib -ldatetime -L../../lib -lspline "-L/usr/local/opt/libomp/lib" -lomp
endif


# Compiler


all:
	$(FF) -o t89c.o T89c.f 
	$(CXX) -o testfortran testfortran.cc $(LDFLAGS)
	LD_LIBRARY_PATH=../../lib ./testfortran
	-rm -v t89c.o
	-rm -v testfortran
