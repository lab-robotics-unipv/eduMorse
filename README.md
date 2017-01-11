# Morse simulator environment

The aim of this project is to enhance the existing educational tool for the robotics course based on [Morse](https://www.openrobots.org/morse/doc/stable/morse.html).

### features to implement
- [x] Simplify the installation through an installer script
- [x] Configure and start a simulation from a conf file
- [x] Detect collisions
- [x] Scoring
- [ ] Simulate energy losses
- [x] Robot2robot communication with bandwidth limits
- [x] Possibility to use different machines for environment and robots

<!-- [] gestione multi robot -->


## Installation

Bash script installer.sh installs Morse simulator and all dependencies useful to the project.  
To run the script open a terminal and type:  
```$ chmod +x installer.sh```  
```$ ./installer.sh```  
The installer needs an Internet connection and ```apt-get``` command, it was tested on Xubuntu 14.04.4 and Xubuntu 16.04.1.  
Check your system requirements and find other informations about Morse simulator [here](https://www.openrobots.org/morse/doc/stable/user/installation.html).  

### Dependencies list:
- cmake
- cmake-data
- pkg-config
- g++
- scons
- openjdk-8-jre-headless
- openjdk-8-jdk
- blender
- git
- python3
- python3-dev
- python3-numpy
- python3-pip
- pytoml

### Directory diagram  
After the installation new files are added in _/opt_. At the top of directory hierarchy there is _eduMorse_ folder, it contains:  
- games -> blend files for maps and objects, conf files for games and robots
- libraries -> C and Java libraries to support programming in these languages
- score -> scripts to count score and collisions, a layer manages communication between them
- socket -> client-server communication
- project_template -> configuration files (TOML format) to set a simulation, main function in C and Java, example of Python script to control a robot

See [directory diagram](https://github.com/danieledema/eduMorse/wiki/Directory-structure).
