#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include "cJSON.h"

#ifndef MORSE_SENSORS_H
#define MORSE_SENSORS_H

typedef struct Pose {
    double time;

    double x;
    double y;
    double z;

    double roll;
    double pitch;
    double yaw;
} Pose;

typedef struct proxObject {
    char * name;
    double dist;
} proxObject;

typedef struct proxMeas {
    double time;

    proxObject * objects;
    int numObj;
} proxMeas;

typedef struct irMeas {
    double time;

    double * dist;
    int numP;
} irMeas;


int setSpeed(FILE * sock, char* parent, char* name, double v, double w);

int getPose(FILE * sock, char* parent, char* name, Pose * pose);
void freePose(Pose * pose);

int getIR(FILE * sock, char* parent, char* name, irMeas * irM);
void freeIR(irMeas * irM);

int getProx(FILE * sock, char* parent, char* name, proxMeas * proxM);
void freeProx(proxMeas * proxM);


#endif
