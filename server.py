import socket
import threading
from collections import defaultdict

class TupleSpace:
    def __init__(self):
        self.tuples = {}
        self.lock = threading.Lock()
        self.total_clients = 0
        self.total_operations = 0
        self.total_reads = 0
        self.total_gets = 0
        self.total_puts = 0
        self.total_errors = 0

    def read(self, key):
        with self.lock:
            self.total_operations += 1
            self.total_reads += 1
            if key in self.tuples:
                return f"OK ({key}, {self.tuples[key]}) read"
            else:
                self.total_errors += 1
                return f"ERR {key} does not exist"

    def get(self, key):
        with self.lock:
            self.total_operations += 1
            self.total_gets += 1
            if key in self.tuples:
                value = self.tuples.pop(key)
                return f"OK ({key}, {value}) removed"
            else:
                self.total_errors += 1
                return f"ERR {key} does not exist"

    def put(self, key, value):
        with self.lock:
            self.total_operations += 1
            self.total_puts += 1
            if key not in self.tuples:
                self.tuples[key] = value
                return f"OK ({key}, {value}) added"
            else:
                self.total_errors += 1
                return f"ERR {key} already exists"

    def print_statistics(self):
        with self.lock:
            num_tuples = len(self.tuples)
            total_tuple_size = sum(len(key) + len(value) for key, value in self.tuples.items())
            avg_tuple_size = total_tuple_size / num_tuples if num_tuples > 0 else 0
            avg_key_size = sum(len(key) for key in self.tuples.keys()) / num_tuples if num_tuples > 0 else 0
            avg_value_size = sum(len(value) for value in self.tuples.values()) / num_tuples if num_tuples > 0 else 0
            print(f"Statistics:")
            print(f"Number of tuples: {num_tuples}")
            print(f"Average tuple size: {avg_tuple_size:.2f}")
            print(f"Average key size: {avg_key_size:.2f}")
            print(f"Average value size: {avg_value_size:.2f}")
            print(f"Total clients: {self.total_clients}")
            print(f"Total operations: {self.total_operations}")
            print(f"Total READs: {self.total_reads}")
            print(f"Total GETs: {self.total_gets}")
            print(f"Total PUTs: {self.total_puts}")
            print(f"Total errors: {self.total_errors}")

def handle_client(client_socket, tuple_space):
    tuple_space.total_clients += 1
    while True:
        try:
            request = client_socket.recv(1024).decode('utf-8')
            if not request:
                break
            print(f"Received: {request}")
            parts = request.split()
            if len(parts) < 3:
                client_socket.send("ERR Invalid request".encode('utf-8'))
                continue
            msg_len = int(parts[0])
            command = parts[1]
            key = parts[2]
            value = " ".join(parts[3:]) if len(parts) > 3 else None
            if command == "R":
                response = tuple_space.read(key)
            elif command == "G":
                response = tuple_space.get(key)
            elif command == "P":
                response = tuple_space.put(key, value)
            else:
                response = "ERR Invalid command"
            client_socket.send(response.encode('utf-8'))
        except Exception as e:
            print(f"Error handling client: {e}")
            break
    client_socket.close()

def start_server(port):
    tuple_space = TupleSpace()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(5)
    print(f"Server listening on port {port}")
    try:
        while True:
            client_socket, addr = server_socket.accept()
            print(f"Accepted connection from {addr}")
            client_thread = threading.Thread(target=handle_client, args=(client_socket, tuple_space))
            client_thread.start()
    except KeyboardInterrupt:
        print("Server shutting down")
    finally:
        server_socket.close()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python server.py <port>")
        sys.exit(1)

    port = int(sys.argv[1])
    start_server(port)