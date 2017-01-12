#include "morse.h"

int parsePoseJson(char * json, Pose * pose);
int insertPose(char * type, double val, Pose * pose);

int parseIrJson(char * json, irMeas* irM);
int insertIr(cJSON * JS, irMeas * irM);

int parseProxJson(char * json, proxMeas * proxM);
int insertProx(cJSON * JS, proxMeas * proxM);
proxObject * parseNear(cJSON * JS, int * n);

int setSpeed(FILE * sock, char* parent, char* name, double v, double w) {
    char req[100];
    int flag = sprintf(req,"id1 %s.%s set_speed [%f,%f]\n", parent, name, v, w);
    if (flag < 0)
        return -1;

    ssize_t written = fprintf(sock, "%s", req);
    if (written < 0)
        return -1;

    char * buff = NULL;
    size_t len = 0;
    ssize_t red = getline(&buff, &len, sock);
    buff[red-1] = '\0';

    char ans[] = "id1 SUCCESS";
    if ( strcmp(buff, ans) == 0)
        return 1;

    return -1;
}

int getPose(FILE * sock, char* parent, char* name, Pose * pose) {
    char req[100];
    int flag = sprintf(req,"id1 %s.%s get_local_data\n", parent, name);
    if (flag < 0)
        return -1;

    ssize_t written = fprintf(sock, "%s", req);
    if (written < 0)
        return -1;

    char * buff = NULL;
    size_t len = 0;
    ssize_t red = getline(&buff, &len, sock);
    buff[red-1] = '\0';

    int parsed = parsePoseJson(buff, pose);
    return parsed;
}

void freePose(Pose * pose) {
    free(pose);
}

int getIR(FILE * sock, char* parent, char* name, irMeas * irM) {
    char req[100];
    int flag = sprintf(req,"id1 %s.%s get_local_data\n", parent, name );
    if (flag < 0)
        return -1;

    ssize_t written = fprintf(sock, "%s", req);
    if (written < 0)
        return -1;

    char * buff = NULL;
    size_t len = 0;
    ssize_t red = getline(&buff, &len, sock);
    buff[red-1] = '\0';

    int parsed = parseIrJson(buff, irM);
    return parsed;
}

void freeIR(irMeas * irM) {
    free(irM->dist);
    free(irM);
}

int getProx(FILE * sock, char* parent, char* name, proxMeas * proxM) {
    char req[100];
    int flag = sprintf(req,"id1 %s.%s get_local_data\n", parent, name);
    if (flag < 0)
        return -1;

    ssize_t written = fprintf(sock, "%s", req);
    if (written < 0)
        return -1;

    char * buff = NULL;
    size_t len = 0;
    ssize_t red = getline(&buff, &len, sock);
    buff[red-1] = '\0';

    int parsed = parseProxJson(buff, proxM);
    return parsed;
}

void freeProx(proxMeas * proxM) {
    int i;

    for ( i = 0 ; i < proxM->numObj ; i++ ) {
        free(proxM->objects[i].name);
    }
    free(proxM->objects);

    free(proxM);
}

int parsePoseJson(char * json, Pose * pose) {

    char success[] = "id1 SUCCESS";
    size_t len = strlen(success);
    if ( strncmp(json, success, len) != 0 )
        return -1;

    char * s = json;
    s += len+1;

    int n;

    cJSON * JS = cJSON_Parse(s);
    cJSON * JSchild = JS->child;
    while ( JSchild != NULL ) {
        n = insertPose(JSchild->string, JSchild->valuedouble, pose);
        if ( n < 0 ) {
            cJSON_Delete(JS);
            return -1;
        }
        JSchild = JSchild->next;
    }
    cJSON_Delete(JS);
    return 1;
}

int insertPose(char * type, double val, Pose * pose) {
    if (strcmp(type, "timestamp") == 0 ) {
        pose->time = val;
    } else if ( strcmp(type, "x" ) == 0 ) {
        pose->x = val;
    } else if ( strcmp(type, "y" ) == 0 ) {
        pose->y = val;
    } else if ( strcmp(type, "z" ) == 0 ) {
        pose->z = val;
    } else if ( strcmp(type, "roll" ) == 0 ) {
        pose->roll = val;
    } else if ( strcmp(type, "pitch" ) == 0 ) {
        pose->pitch = val;
    } else if ( strcmp(type, "yaw" ) == 0 ) {
        pose->yaw = val;
    } else {
        return -1;
    }
    return 1;
}

int parseIrJson(char * json, irMeas* irM) {
    char success[] = "id1 SUCCESS";
    size_t len = strlen(success);
    if ( strncmp(json, success, len) != 0 )
        return -1;

    char * s = json;
    s += len+1;

    int n;

    cJSON * JS = cJSON_Parse(s);
    cJSON * JSchild = JS->child;

    while ( JSchild != NULL ) {
        n = insertIr(JSchild, irM);
        if ( n < 0 ) {
            cJSON_Delete(JS);
            return -1;
        }
        JSchild = JSchild->next;
    }
    cJSON_Delete(JS);

    return 1;
}

int insertIr(cJSON * JS, irMeas * irM) {
    if (strcmp(JS->string, "timestamp") == 0 ) {
        irM->time = JS->valuedouble;
    } else if ( strcmp(JS->string, "range_list" ) == 0 ) {
        irM->numP = cJSON_GetArraySize(JS);

        if ( !(irM->dist = malloc(irM->numP*sizeof(double))))
            return -1;

        int i;
        for ( i = 0 ; i < irM->numP ; i++ ) {
            cJSON * JSchild = cJSON_GetArrayItem(JS, i);
            irM->dist[i] = JSchild->valuedouble;
        }
    } else if ( strcmp(JS->string, "point_list" ) == 0 ) {
    } else {
        return -1;
    }
    return 1;
}

int parseProxJson(char * json, proxMeas * proxM) {
    char success[] = "id1 SUCCESS";
    size_t len = strlen(success);
    if ( strncmp(json, success, len) != 0 )
        return -1;

    char * s = json;
    s += len+1;

    int n;

    cJSON * JS = cJSON_Parse(s);
    cJSON * JSchild = JS->child;
    while ( JSchild != NULL ) {
        n = insertProx(JSchild, proxM);
        if ( n < 0 ) {
            cJSON_Delete(JS);
            return -1;
        }
        JSchild = JSchild->next;
    }
    cJSON_Delete(JS);
    return 1;
}

int insertProx(cJSON * JS, proxMeas * prox) {
    if ( strcmp(JS->string, "timestamp") == 0 ) {
        prox->time = JS->valuedouble;
    } else if ( strcmp(JS->string, "near_objects" ) == 0 ) {
        prox->objects = parseNear(JS->child, &(prox->numObj));
    } else if ( strcmp(JS->string, "near_robots" ) == 0 ) {
    } else {
        return -1;
    }
    return 1;
}

proxObject * parseNear(cJSON * JS, int * n) {
    int dim = 5;
    proxObject * obj, * v;

    *n = 0;
    if ( !(v = malloc(dim * sizeof(*v))))
        return NULL;

    while ( JS != NULL ) {
        obj = v + (*n);
        obj->name = strdup(JS->string);

        obj->dist = JS->valuedouble;
        (*n)++;
        JS = JS->next;

        if ( *n > dim ) {
            dim *= 2;
            if ( !(v = realloc(v, dim*sizeof(*v)))) {
                free(v);
                return NULL;
            }
        }
    }
    return v;
}
