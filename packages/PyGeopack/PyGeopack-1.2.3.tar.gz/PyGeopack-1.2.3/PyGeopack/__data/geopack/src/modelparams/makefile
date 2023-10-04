# CFLAGS for CC
CFLAGS=-g -O3 -std=c++17 -Wextra -fPIC 

# Compiler
CCo=g++ -c $(CFLAGS)
CC=g++ $(CFLAGS)

# set the build directory
ifndef BUILDDIR 
	BUILDDIR=../../build
endif

all: obj

obj:
	$(CCo) calculatew.cc -o $(BUILDDIR)/calcualtew.o
	$(CCo) calculateg.cc -o $(BUILDDIR)/calculateg.o
	$(CCo) tsygdata.cc -o $(BUILDDIR)/tsygdata.o
	$(CCo) modelparams.cc -o $(BUILDDIR)/modelparams.o
	$(CCo) checkv.cc -o $(BUILDDIR)/checkv.o
	$(CCo) fillinkp.cc -o $(BUILDDIR)/fillinkp.o

clean:
	rm -v $(BUILDDIR)/*.o
