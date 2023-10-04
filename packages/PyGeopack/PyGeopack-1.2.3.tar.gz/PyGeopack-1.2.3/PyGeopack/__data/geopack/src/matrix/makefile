# CFLAGS for CC
CFLAGS=-g -O3 -std=c++17 -Wextra -fPIC
LDFLAGS=-lm 


# set the build directory
ifndef BUILDDIR 
	BUILDDIR=../../build
endif

ifeq ($(OS),Windows_NT)
#windows stuff here
	MD=mkdir
	CCo=g++ -c $(CFLAGS) -fopenmp 
	CC=g++ $(CFLAGS) -fopenmp 
else
#linux and mac here
	OS=$(shell uname -s)
	MD=mkdir -p
	ifeq ($(OS),Linux)
		CCo=g++ -c $(CFLAGS) -fopenmp 
		CC=g++ $(CFLAGS) -fopenmp 
	else
		LDFLAGS=-lm -lstdc++ "-L/usr/local/opt/libomp/lib" -lomp
		CPPFLAGS="-I/usr/local/opt/libomp/include"
		CCo=g++ -Xpreprocessor -fopenmp -c $(CFLAGS) $(CPPFLAGS) 
		CC=g++ -Xpreprocessor -fopenmp $(CFLAGS) $(CPPFLAGS) 
	endif
endif

all: obj lib

obj:
	$(CCo) matrix.cc -o $(BUILDDIR)/matrix.o
	$(CCo) matrixarray.cc -o $(BUILDDIR)/matrixarray.o
	$(CCo) matrixmath.cc -o $(BUILDDIR)/matrixmath.o
	$(CCo) identity.cc -o $(BUILDDIR)/identity.o
	$(CCo) rotmatrix.cc -o $(BUILDDIR)/rotmatrix.o
	$(CCo) libmatrix.cc -o $(BUILDDIR)/libmatrix.o


lib: 
	$(CC) -shared -o libmatrix.so $(BUILDDIR)/*.o $(LDFLAGS)

clean:
	rm -v $(BUILDDIR)/*.o
