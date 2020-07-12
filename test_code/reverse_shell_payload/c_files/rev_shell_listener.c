#include <stdio.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <stdlib.h>

// Prints out errors from processes

// Takes a string as parameter then spits this out as stderr (1)
/*
 *
 */
void error(char *msg) {
	perror(msg);
	exit(1);
}

int usage(int argc)
{
	if(argc < 2) 
	{
		fprintf(stderr, "ERROR: no port provided\n");
		exit(1);
	}
	return argc;
}

int main(int argc, char **argv)
{
	int sockfd, newsockfd, port_num, clilen;
	// Buffer which is passed through to the target. Amount of characters read from the socket
	char buffer[256];
	struct sockaddr_in serv_addr, cli_addr; // Struct to handle IP addresses 
	int data;

	usage(argc);
	// Make the socket itself implemented the same way as a file descriptor
	sockfd = socket(AF_INET, SOCK_STREAM, 0);
	// If the socket is not a fail 
	if(sockfd < 0) {
		error("ERROR opening socket");
	}
	// Setting 0s in the server address workspace with characters. But you treat it as a string 
	bzero((char *) &serv_addr, sizeof(serv_addr));

	// Char to integer conversion - We take original char * and then turn it into an int
	port_num = atoi(argv[1]);
	

	serv_addr.sin_family = AF_INET;
	// INADDR_ANY - Symbolic constant which gets our local machines IP
	serv_addr.sin_addr.s_addr = INADDR_ANY;
	// Transforms the data from local PC (Host byte order) to transfer to network wire (Network byte order)
	serv_addr.sin_port = htons(port_num);
	// We bind the socket to our address which is host/port. 
	// 1. Socket file descriptor (This actually creates the socket for read/write)
	// 2. sockaddr which is the actual socket which contains the host/port
	// 3. Size of the server address which we're binding to
	if(bind(sockfd, (struct sockaddr *) &serv_addr,
		// Error handling to check the state of socket
		sizeof(serv_addr)) < 0)
		error("ERROR on binding");
	// Number of connections the socket can listen for
	listen(sockfd, 1);
	// Gets the size of the client address
	clilen = sizeof(cli_addr);
	// Opens a new file descriptor on order for the client to come in and connect. This remains blocked until the client connects in which the process wakes up. New fd is returned, second argument is a reference pointer to address of client on other side and third is size of structure.
	// The clilen variable can get how much space is needed
	newsockfd = accept(sockfd, (struct sockaddr *) &cli_addr, &clilen);
	// Same error handling on here
	if(newsockfd < 0)
		error("ERROR on accept");
	// We set 0s in memory on our buffer to then populate some data
	bzero(buffer, 256);
	data = read(newsockfd, buffer, 255);
	if(data < 0) 
		error("ERROR reading from socket");
	printf("Here is the message: %s\n", buffer);
	data = write(newsockfd, "I got your message", 18);
	if(data < 0)
		error("ERROR waiting on socket");
	return 0;
}
