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
	$(CCo) argmax.cc -o $(BUILDDIR)/argmax.o
	$(CCo) carttospherical.cc -o $(BUILDDIR)/carttospherical.o
	$(CCo) linterp.cc -o $(BUILDDIR)/linterp.o
	$(CCo) reverseelements.cc -o $(BUILDDIR)/reverseelements.o
	$(CCo) BubbleArgSort.cc -o $(BUILDDIR)/BubbleArgSort.o
		
clean:
	rm -v $(BUILDDIR)/*.o
