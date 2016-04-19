#!/bin/bash

sudo apt-get install -y cmake
sudo apt-get install -y python3
sudo apt-get install -y python3-dev
sudo apt-get install -y blender
sudo apt-get install -y python3-numpy
cd /tmp
sudo apt-get install -y git
git clone https://github.com/morse-simulator/morse.git
cd morse
mkdir build && cd build
sudo apt-get install -y g++
cmake ..
sudo make install
morse check
