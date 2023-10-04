@echo off
mkdir build

echo Compiling datetime
cd lib\datetime
call compile.bat
cd ..\..
copy lib\datetime\lib\libdatetime.dll lib\

echo Compiling libspline
cd lib\libspline
call compile.bat
cd ..\..
copy lib\libspline\lib\libspline.dll lib\

cd src
call compile.bat
cd ..