#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <string.h>

int server_doSock(int serverport, int n);

int client_doSock(char *address, int serverport);
