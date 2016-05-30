#!/bin/bash

# Install dependencies
sudo apt-get install -y cmake
sudo apt-get install -y cmake-data
sudo apt-get install -y pkg-config
sudo apt-get install -y g++
sudo apt-get install -y scons
sudo apt-get install -y blender
sudo apt-get install -y git

sudo apt-get install -y python3
sudo apt-get install -y python3-dev
sudo apt-get install -y python3-numpy
sudo apt-get install -y python3-pip

sudo pip3 install --upgrade pip
sudo pip3 install pytoml

# Install Morse simlator
cd /tmp
git clone https://github.com/morse-simulator/morse.git
cd morse
mkdir build && cd build
cmake ..
sudo make install
morse check

# Retrieving the custom simulation files
cd /tmp
FILE=eduMorse
URL="https://robolab.unipv.it/owncloud/index.php/s/pBLtYXr8e6HWLbU/download"
wget --no-check-certificate -O $FILE.tar.gz $URL
tar -xvf /tmp/$FILE.tar.gz -C $HOME

# Setting the environment variables
echo "# EDUMORSE variables" >> $HOME/.bashrc
echo "export EDUMORSEPATH=$HOME/$FILE" >> $HOME/.bashrc
echo "export PYTHONPATH=PYTHONPATH:/usr/local/lib/python3/dist-packages/" >> $HOME/.bashrc
echo "export MORSELABPATH=$HOME/simulator/morseLab/" >> $HOME/.bashrc

mkdir $HOME/.morse
echo "[sites]" > $HOME/.morse/config
echo "edumorse = $HOME/$FILE" >> $HOME/.morse/config
