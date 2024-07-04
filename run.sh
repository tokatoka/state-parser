#!/bin/bash

cd ./double-conversion
./double-conversion.py mm
rm -rf task_*

./double-conversion.py no_mm
rm -rf task_*


cd ../libhevc
./libhevc.py mm
rm -rf task_*

./libhevc.py no_mm
rm -rf task_*


cd ../libxml2
./libxml2.py mm
rm -rf task_*

./libxml2.py no_mm
rm -rf task_*

cd ../sqlite3
./sqlite3.py mm
rm -rf task_*

./sqlite3.py no_mm
rm -rf task_*

cd ../stb
./stb.py mm
rm -rf task_*

./stb.py no_mm
rm -rf task_*
