#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <readline/readline.h>
#include <readline/history.h>

#define MAXCOM 1000
#define MAXLIST 100

#define clear() printf("\033[H\033[J")

void lsh_loop(void)
{
	char *line;
	char **args;
	int status;

	do {
		printf("$ ");
		line = lsh_read_line();
		args = lsh_split_line(line);
		status = lsh_execute(args);

		free(line);
		free(args);
	} while(status);
}

// https://brennan.io/2015/01/16/write-a-shell-in-c/
int main()
{
	lsh_loop();

	return EXIT_SUCCESS;
}
