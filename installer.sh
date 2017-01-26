#!/bin/bash

sudo cp -R ./eduMorse /opt
sudo ln -s /opt/eduMorse/eduMorseCreate.sh /usr/bin/eduMorseCreate
sudo ln -s /opt/eduMorse/eduMorseRunner.py /usr/bin/eduMorseRunner
sudo apt-get install -y scons
cd /opt/eduMorse/libraries/cBindings
sudo scons
sudo scons -c

# Install dependencies
sudo apt-get install -y cmake
sudo apt-get install -y cmake-data
sudo apt-get install -y pkg-config
sudo apt-get install -y g++
sudo apt-get install -y openjdk-8-jre-headless
sudo apt-get install -y openjdk-8-jdk
sudo apt-get install -y blender
sudo apt-get install -y git

sudo apt-get install -y python3
sudo apt-get install -y python3-dev
sudo apt-get install -y python3-numpy
sudo apt-get install -y python3-pip

sudo pip3 install --upgrade pip
sudo pip3 install pytoml

# Install Morse simulator
cd /tmp
git clone https://github.com/morse-simulator/morse.git
cd morse
mkdir build && cd build
cmake ..
sudo make install
morse check

# Setting the environment variables
echo "# MORSELAB variables" >> $HOME/.bashrc
echo "export PYTHONPATH=PYTHONPATH:/usr/local/lib/python3/dist-packages/" >> $HOME/.bashrc
echo "export EDUMORSEPATH=/opt/eduMorse" >> $HOME/.bashrc
