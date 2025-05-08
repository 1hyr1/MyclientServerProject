import subprocess
import time
import os


def run_server(port):
    server_command = f"python server.py {port}"
    return subprocess.Popen(server_command, shell=True)

def run_client(server_host, server_port, request_file):
    client_command = f"python client.py {server_host} {server_port} {request_file}"
    return subprocess.Popen(client_command, shell=True)

def main():
    # 设置服务器端口
    SERVER_PORT = 51234

    # 启动服务器
    print("Starting server...")
    server_process = run_server(SERVER_PORT)
    time.sleep(2)  # 等待服务器启动

    # 客户端请求文件列表
    client_files = [f"client_{i}.txt" for i in range(1, 11)]

    # 运行客户端
    print("Starting clients...")
    client_processes = []
    for file in client_files:
        client_processes.append(run_client("localhost", SERVER_PORT, file))

    # 等待客户端完成
    for client in client_processes:
        client.wait()

    # 停止服务器
    print("Stopping server...")
    server_process.terminate()
    server_process.wait()

    print("All processes completed.")


