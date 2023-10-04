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
	$(CCo) converttracecoords.cc -o $(BUILDDIR)/converttracecoords.o
	$(CCo) fieldlinedist.cc -o $(BUILDDIR)/fieldlinedist.o
	$(CCo) fieldlinemidpoint.cc -o $(BUILDDIR)/fieldlinemidpoint.o
	$(CCo) fieldliner.cc -o $(BUILDDIR)/fieldliner.o
	$(CCo) fieldlinernorm.cc -o $(BUILDDIR)/fieldlinernorm.o
	$(CCo) getmagequatorfp.cc -o $(BUILDDIR)/getmagequatorfp.o
	$(CCo) latlonlt.cc -o $(BUILDDIR)/latlonlt.o
	$(CCo) tracefield.cc -o $(BUILDDIR)/tracefield.o
	$(CCo) tracefieldline.cc -o $(BUILDDIR)/tracefieldline.o
	$(CCo) tracefootprints.cc -o $(BUILDDIR)/tracefootprints.o
	$(CCo) calculatehalpha.cc -o $(BUILDDIR)/calculatehalpha.o
	$(CCo) trace.cc -o $(BUILDDIR)/trace.o
	$(CCo) interptraceclosestpos.cc -o $(BUILDDIR)/interptraceclosestpos.o
	#$(CCo) tracerotationmatrices.cc -o $(BUILDDIR)/tracerotationmatrices.o
		
clean:
	rm -v $(BUILDDIR)/*.o
