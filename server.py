import socket

PORT = 37234
# HOST = '192.168.0.143'
BUFFER = 1024
hostname = socket.gethostname()
HOST = socket.gethostbyname(hostname)
print(hostname)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

# info = (1, 2, 3, 4, 5, 6, 7, 8)

while True:
    client_socket, adr = server_socket.accept()
    print('Połączenie z ', adr[0], 'Port: ', adr[1])
    # FROM CLIENT
    host_ip = client_socket.recv(BUFFER).decode("utf8")
    print(host_ip)

    info = "Witaj w ePaint 0.001".encode("utf8")
    client_socket.send(info)
