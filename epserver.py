import socket
import threading

RUNNING = False
PORT = 37234
HOST = 0
BUFFER = 1024
def setup(ip=None, port=37234):
    if ip is None:
        ip = socket.gethostbyname(socket.gethostname())
    global PORT, HOST, BUFFER
    PORT = 37234
    HOST = ip
    BUFFER = 1024
    
    #hostname = socket.gethostname()
    #HOST = socket.gethostbyname(hostname)
def start():
    global PORT,HOST,BUFFER,RUNNING
    if RUNNING == False:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)

        def serverthread():
            print("Wątek z serwerem uruchomiony!")
            while True:
                client_socket, adr = server_socket.accept()
                print('Połączenie z ', adr[0], 'Port: ', adr[1])
                # FROM CLIENT
                host_ip = client_socket.recv(BUFFER).decode("utf8")
                print(host_ip)

                info = "Witaj w ePaint 0.001".encode("utf8")
                client_socket.send(info)
        sv = threading.Thread(target=serverthread)
        sv.start()
        RUNNING=True
        return True
    else:
        return False
    # info = (1, 2, 3, 4, 5, 6, 7, 8)

        
        
    