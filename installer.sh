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
sudo apt-get install -y python3-pip
sudo pip3 install pytoml

FILE=eduMorse.tar.gz
URL="https://robolab.unipv.it/owncloud/index.php/s/pBLtYXr8e6HWLbU/download"

cd /tmp
wget --no-check-certificate -O $FILE $URL

tar -xvf /tmp/$FILE -C $HOME

echo "source ~/simulator/environ.sh" >> ~/.bashrc
echo "EDUMORSEPATH=$HOME/$FILE" >> $HOME/.bashrc
echo "edumorse = $HOME/$FILE" >> $HOME/.morse/config
