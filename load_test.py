import socket
import ssl
import threading
import random
import time

SERVER_IP = "localhost"
PORT = 5000
NUM_CLIENTS = 20

def simulate_client(client_id):
    try:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        secure_sock = context.wrap_socket(sock, server_hostname=SERVER_IP)

        secure_sock.connect((SERVER_IP, PORT))

        message = secure_sock.recv(1024).decode()
        print(f"Client {client_id} -> {message}")

        bid = random.randint(1, 1000)
        secure_sock.send(f"BID {bid}".encode())

        time.sleep(0.1)
        secure_sock.close()

    except:
        pass

threads = []
start_time = time.time()

for i in range(NUM_CLIENTS):
    t = threading.Thread(target=simulate_client, args=(i,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

end_time = time.time()

print("\nTest completed")
print("Total time:", end_time - start_time, "seconds")