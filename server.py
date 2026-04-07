import socket
import ssl
import threading

HOST = "0.0.0.0"
PORT = 5000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain("certs/server.crt", "certs/server.key")

print("Secure Auction Server Started...")

highest_bid = 0
highest_bidder = None
clients = []
lock = threading.Lock()

def broadcast(message):
    for client in clients:
        try:
            client.send(message.encode())
        except:
            pass

def handle_client(client, addr):
    global highest_bid, highest_bidder

    print("Client connected:", addr)
    clients.append(client)

    try:
        client.send(f"Welcome! Current highest bid: {highest_bid}".encode())

        while True:
            message = client.recv(1024).decode()

            if not message:
                break

            print(addr, "sent:", message)

            if message.startswith("BID"):
                bid = int(message.split()[1])

                with lock:
                    if bid > highest_bid:
                        highest_bid = bid
                        highest_bidder = addr

                        response = f"NEW HIGHEST BID: {highest_bid} by {addr}"
                        print(response)

                        broadcast(response)

                    else:
                        client.send(f"Bid rejected! Current highest bid is {highest_bid}".encode())

    except:
        pass

    print("Client disconnected:", addr)
    if client in clients:
        clients.remove(client)
    client.close()

while True:
    client_socket, addr = server_socket.accept()

    secure_client = context.wrap_socket(client_socket, server_side=True)

    thread = threading.Thread(target=handle_client, args=(secure_client, addr))
    thread.start()