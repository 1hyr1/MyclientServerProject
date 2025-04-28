import socket
import sys

def send_request(server_host, server_port, request_file):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_host, server_port))

    with open(request_file, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            command, *args = line.split()
            if command == "PUT":
                key, value = args
                request = f"{len(line) + 3} P {key} {value}"
            elif command == "READ":
                key = args[0]
                request = f"{len(line) + 3} R {key}"
            elif command == "GET":
                key = args[0]
                request = f"{len(line) + 3} G {key}"
            else:
                print(f"Invalid command: {command}")
                continue

            client_socket.send(request.encode('utf-8'))
            response = client_socket.recv(1024).decode('utf-8')
            print(f"{line}: {response}")

            client_socket.close()

        if __name__ == "__main__":
             if len(sys.argv) != 4:
               print("Usage: python client.py <server_host> <server_port> <request_file>")
               sys.exit(1)

             server_host = sys.argv[1]
             server_port = int(sys.argv[2])
             request_file = sys.argv[3]

             send_request(server_host, server_port, request_file)