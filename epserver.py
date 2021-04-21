import socket
import threading

class epserver:
    RUNNING=False
    def __init__(self,ip=None, port=37234):
        if ip is None:
            self.ip = socket.gethostbyname(socket.gethostname())
        else:
            self.ip = ip
        self.PORT = 37234
        self.HOST = self.ip
        self.BUFFER = 1024
        self.server_socket = None
        self.sv_thread = None
        
        #hostname = socket.gethostname()
        #HOST = socket.gethostbyname(hostname)
    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.HOST, self.PORT))
        self.server_socket.listen(5)
        def serverthread():
            print("Wątek z serwerem uruchomiony!")
            client_socket, adr = self.server_socket.accept()
            info = "Witaj w ePaint 0.001".encode("utf8")
            client_socket.send(info)
            while self.RUNNING == True:
                print('Połączenie z ', adr[0], 'Port: ', adr[1])
                # FROM CLIENT
                host_ip = client_socket.recv(BUFFER).decode("utf8")
                print(host_ip)
                

        self.RUNNING=True
        self.sv_thread = threading.Thread(target=serverthread)
        self.sv_thread.start()

    def stop(self):
        self.server_socket.close()
        self.RUNNING=False
    # info = (1, 2, 3, 4, 5, 6, 7, 8)
class epclient:
    def __init__(hostip, buffer=1024, port=37234):
        pass
