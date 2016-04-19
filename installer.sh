#! /bin/bash

sudo apt-get install cmake
sudo apt-get install python3
sudo apt-get install python3-dev
sudo apt-get install blender
sudo apt-get install python3-numpy
cd /tmp
sudo apt-get install git
git clone https://github.com/morse-simulator/morse.git
cd morse
mkdir build && cd build
sudo apt-get install g++
cmake ..
sudo make install
morse check
