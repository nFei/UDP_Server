import socket
import threading
import os
import time
import datetime

HOST = '192.168.174.130'  # the server's hostname or IP address
PORT = 1234        # the port used by the server
BUFFER_SIZE = 65507  # the buffer size in bytes
FILES_DIR = 'FilesReceived' # the directory to store received files
conectados = True
CHUNK_SIZE = 65507
event = threading.Event()

# function to handle a client connection
def handle_client(client_socket, addr, filename, num):
    print(f"Client {addr} connected.")

    event.wait()
    error = False
    print(f"Enviando chunks a Cliente {addr}")
    # Send each chunk to client
    start_time = datetime.datetime.now()
    total_bytes = 0
    for i, chunk in enumerate(file_chunks):
        total_bytes += len(chunk)
        try:
            server_socket.sendto(chunk, addr)
        except socket.error:
            print(f"Error sending chunk {i+1} to {addr}.")
            error = True
            break
        #print(f"Sent chunk {i+1} ({len(chunk)} bytes) to client {addr}")
    print(total_bytes)
    end_time = datetime.datetime.now()
    duration = end_time - start_time
    log_filename = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S-log.txt")
    with open(log_filename, "a") as f:
       f.write(f"Client number:  {num}\n")
       f.write(f"Total time: {duration.total_seconds()} seconds\n")
       if(error):
            f.write("Unseccessful transaction\n")
       else:
            f.write("Successful transaction\n")
    #client_socket.close()

filename = input("Enter file name (100MB or 250MB): ")
if filename == "100MB":
    file_size = 100 * 1024 * 1024
elif filename == "250MB":
    file_size = 250 * 1024 * 1024
else:
    print("Invalid file name.")
    exit()

# Read file into memory
with open(filename, "rb") as f:
    file_data = f.read()

# Divide file into chunks
num_chunks = file_size // CHUNK_SIZE + 1
file_chunks = [file_data[i*CHUNK_SIZE:(i+1)*CHUNK_SIZE] for i in range(num_chunks)]

# create a UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))
print(f"Server started on {HOST}:{PORT}")
print("Waiting for clients to connect...")
# wait for up to 25 clients to connect
for i in range(10):
    data, addr = server_socket.recvfrom(BUFFER_SIZE)
    # extract filename from data
    filename = data.decode()
    # create a thread to handle the client connection
    num = i+1
    t = threading.Thread(target=handle_client, args=(server_socket, addr, filename, num))
    t.start()
    

event.set()