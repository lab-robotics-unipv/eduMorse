#!/bin/bash

sudo rm -rf /opt/eduMorse
sudo cp -R ./eduMorse /opt
cd /opt/eduMorse/libraries/cBindings
sudo scons
sudo scons -c
