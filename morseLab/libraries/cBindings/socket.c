#include "socket.h"

/*
 * NOTE: SOCK_STREAM is for TCP
 * SOCK_DGRAM is for UDP: listen and ac
 * 
 * server must explicitly accept a connection using:
 * int accept (int socket, struct sockaddr *addr, socklen t *length_ptr)
 * socket	the socket used for connections
 * addr		pointer to the the struct that will contain the address of the client
 * length_ptr	pointer to a integer that will contain the length of the address
 * the 2 pointers can be NULL
 *
 * the function will return the new socket to use or -1 in case of errors
 *
 */


/*
 * opens a socket for listening incoming connections
 *
 * Parameters:
 * serverport	port to bind
 * n		length of the queue of incoming connections
 *
 * Returns:
 * the created socket or -1 in case of errors
 */
int server_doSock(int serverport, int n) {
	struct sockaddr_in addr;
	int sock = socket(AF_INET, SOCK_STREAM, 0);
	if (sock < 0)
		return -1;
	memset(&addr, 0, sizeof(addr));
	addr.sin_family = AF_INET;
	inet_aton("127.0.0.1", &addr.sin_addr);
	addr.sin_port = htons(serverport);
	if (bind(sock, (struct sockaddr *) &addr, sizeof(addr)) < 0)
		return -1;
	if (listen(sock, n) < 0)
		return -1;
	else
		return sock;
}


/*
 * opens a socket to talk with a server
 *
 * Parameters:
 * address	address of the server
 * serverport	server's port
 *
 * Returns:
 * the created socket or -1 in case of errors
 */
int client_doSock(char *address, int serverport) {
	struct sockaddr_in addr;
	int sock = socket(AF_INET, SOCK_STREAM, 0);
	if (sock < 0)
		return -1;
	memset(&addr, 0, sizeof(addr));
	addr.sin_family = AF_INET;
	inet_aton(address, &addr.sin_addr);
	addr.sin_port = htons(serverport);
	if (connect(sock, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
		return -1;
	}
	return sock;
}
