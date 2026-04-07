import socket
import ssl
import threading

SERVER_IP = "localhost"   # CHANGE for different computers
PORT = 5000

context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
secure_client = context.wrap_socket(client_socket, server_hostname=SERVER_IP)

try:
    secure_client.connect((SERVER_IP, PORT))
    print("Connected to Secure Auction Server")
except:
    print("Connection failed")
    exit()

def receive_messages():
    while True:
        try:
            message = secure_client.recv(1024).decode()
            if not message:
                break
            print("\nSERVER:", message)
        except:
            break

thread = threading.Thread(target=receive_messages)
thread.daemon = True
thread.start()

while True:
    bid = input("Enter bid (BID 500) or exit: ")

    if bid.lower() == "exit":
        break

    secure_client.send(bid.encode())

secure_client.close()