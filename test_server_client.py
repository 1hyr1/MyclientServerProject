import subprocess
import time
import os


def run_server(port):
    """运行服务器"""
    server_command = f"python server.py {port}"
    return subprocess.Popen(server_command, shell=True)





