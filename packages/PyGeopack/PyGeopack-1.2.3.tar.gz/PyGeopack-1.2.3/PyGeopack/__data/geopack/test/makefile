# CFLAGS for CC
CFLAGS=-fopenmp -g -O3 -Wextra -fPIC -I../include
CXXFLAGS=-fopenmp -g -O3 -std=c++17 -Wextra -fPIC -I../include

OS=$(shell uname -s)
ifeq ($(OS),Linux)
	CC=gcc $(CFLAGS)
	CXX=g++ $(CXXFLAGS)
	LDFLAGS=-lm -Wl,-rpath='$$ORIGIN/../lib' -L ../lib -lgeopack -lgfortran
else
	CC=gcc -Xpreprocessor $(CFLAGS)
	CXX=g++ -Xpreprocessor $(CXXFLAGS)
	LDFLAGS=-lm -L../lib -lgeopack -L$(shell dirname `locate libgfortran.a | head -n 1`) -lgfortran "-L/usr/local/opt/libomp/lib" -lomp
endif


# Compiler


all:
	$(CC) -o testc test.c $(LDFLAGS)
	$(CXX) -o testcc test.cc $(LDFLAGS)
	LD_LIBRARY_PATH=$LD_LIBRARY_PATH:../lib 
	./testc
	./testcc
	cd fortran; make all

clean:
	-rm -v testc
	-rm -v testcc