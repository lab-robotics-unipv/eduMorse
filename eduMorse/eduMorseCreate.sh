#!/bin/bash

if [ "$#" -ne 1 ]; then
	echo "Name of project not found"
else
	morse create $1
	cd $1
	rm default.py
	rm -r scripts/
	rm -r src/
	cp -r /opt/eduMorse/project_template/* .
fi
