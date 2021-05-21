import socket
import threading
<<<<<<< HEAD
from gui import *
=======

>>>>>>> refs/remotes/origin/intergracja-serwer
class Epserver:
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
        self.start()
        #hostname = socket.gethostname()
        #HOST = socket.gethostbyname(hostname)
    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.HOST, self.PORT))
        self.server_socket.listen()

        self.RUNNING=True
        self.sv_thread = threading.Thread(target=self.serverthread)
        self.sv_thread.start()

    def serverthread(self):
        #try:
        print("Wątek z serwerem uruchomiony!")
        #self.client_socket, self.adr = self.server_socket.accept()
        #info = "Witaj w ePaint 0.001".encode("utf8")
        #client_socket.send(info)
        self.receive()
        print("...")
        #except:
        #    print("closed")
        #while self.RUNNING == True:
        #    print('Połączenie z ', adr[0], 'Port: ', adr[1])
        #    # FROM CLIENT
        #    host_ip = client_socket.recv(BUFFER).decode("utf8")
        #    print(host_ip)
    def receive(self):
        global buffor
        self.clients=[]
        while True:
            self.client_socket, self.adr = self.server_socket.accept()
            print('Połączenie z ', self.adr[0], 'Port: ', self.adr[1])

            self.clients.append(self.client_socket)

            # FROM CLIENT
            self.host_ip = self.client_socket.recv(self.BUFFER).decode("utf8")
            print(self.host_ip)

            #info = "Witaj w ePaint 0.001".encode("utf8")
            #client_socket.send(info)
            if len(self.clients)>0:
                while True:
                    if len(buffor)>=6:
                        for i in self.clients:
                            self.client_socket.send(str(buffor).encode("utf8"))
                        buffor.clear()
    def stop(self):
        #self.server_socket.close()
        self.RUNNING=False
        self.server_socket.close()
    # info = (1, 2, 3, 4, 5, 6, 7, 8)

class epclient:
    def __init__(self, guiInstance, hostip, buffer=1024, port=37234):
        self.guiInstance = guiInstance
        self.RUNNING = True
        self.PORT = port
        self.HOST = socket.gethostbyaddr(hostip)[2][0]
        self.BUFFER = 65536
        print(self.HOST, self.PORT)

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.HOST, self.PORT))

        client_host = socket.gethostname()
        client_ip = str(socket.gethostbyname(client_host)).encode("utf8")

        self.client_socket.send(client_ip)

        self.converted=[]
        receiveThread = threading.Thread(target=self.receive)
        receiveThread.start()
        drawThread = threading.Thread(target=self.draw)
        drawThread.start()

    def receive(self):
        #global self.converted
        while self.RUNNING:
            print("TEST")
            info = self.client_socket.recv(self.BUFFER).decode("utf8")
            try:
                self.converted = eval((info))
            except:
                #print("Cos jest nie tak")
                self.converted = []
            print(self.converted)
            #print(self.converted

    def draw(self):
        #global self.converted
        while self.RUNNING:
            if len(self.converted) > 0:
                x1 = self.converted[0]
                y1 = self.converted[1]
                x2 = self.converted[2]
                y2 = self.converted[3]
                color = self.converted[4]
                thickness = int(self.converted[5])
                self.converted.clear()
                xdiff = x1-x2
                ydiff = y1-y2
                maxnum = max(abs(xdiff), abs(ydiff))
                for i in range(maxnum):
                    x = int(x2 + (float(i)/maxnum * xdiff))
                    y = int(y2 + (float(i)/maxnum * ydiff))
                    self.guiInstance.freeDraw(x,y, thickness, color)
            
                #canva.create_oval(x-1, y-1, x+1, y+1, fill="black", outline="black")


