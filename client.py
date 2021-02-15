import socket

PORT = 37234
# HOST = '192.168.0.143'
HOST = socket.gethostbyname('M34')
BUFFER = 1024


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

client_host = socket.gethostname()
client_ip = str(socket.gethostbyname(client_host)).encode("utf8")

client_socket.send(client_ip)

info = client_socket.recv(BUFFER).decode("utf8")
print(info)
