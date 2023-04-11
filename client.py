import socket
import os

# Constants
SERVER_IP = "192.168.174.130"
SERVER_PORT = 1234
CHUNK_SIZE = 65507
FILES_DIRECTORY = "FilesReceived"

# Create UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Send message to server to indicate readiness
client_socket.sendto(b"Ready", (SERVER_IP, SERVER_PORT))

# Receive file chunks from server
file_chunks = []
file_path = "Cliente-Prueba-.txt"
bytes = 0

with open(file_path, 'wb') as f:
    while True:
        # Receive a chunk of data from the server
        data, addr = client_socket.recvfrom(65507)

        # Check if the server has finished sending the file
        if not data:
            print('File received successfully')
            break
        bytes += len(data)
        print(bytes)
        # Write the received data to the file
        f.write(data)


