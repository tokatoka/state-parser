#!/bin/bash

cd ./double-conversion
./double-conversion.py mm

cd ./double-conversion
./double-conversion.py no_mm


cd ../libhevc
./libhevc.py mm

cd ../libhevc
./libhevc.py no_mm


cd ../libxml2
./libxml2.py mm

cd ../libxml2
./libxml2.py no_mm

cd ../sqlite3
./sqlite3.py mm

cd ../sqlite3
./sqlite3.py no_mm

cd ../stb
./stb.py mm

cd ../stb
./stb.py no_mm