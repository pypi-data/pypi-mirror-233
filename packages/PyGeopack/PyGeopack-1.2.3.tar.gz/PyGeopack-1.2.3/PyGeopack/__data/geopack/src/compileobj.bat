@echo off
set BUILDDIR=..\build
for %%i in (*.cc) do (
	echo Compiling: %%i
    g++ -fPIC -c -lm -fopenmp "%%~ni.cc" -o %BUILDDIR%\\"%%~ni.o"
)

