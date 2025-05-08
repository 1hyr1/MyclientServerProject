import subprocess
import time
import os


def run_server(port):
    server_command = f"python server.py {port}"
    return subprocess.Popen(server_command, shell=True)

def run_client(server_host, server_port, request_file):
    client_command = f"python client.py {server_host} {server_port} {request_file}"
    return subprocess.Popen(client_command, shell=True)


