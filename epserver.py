import socket
import threading
import queue
import time
import pickle

from gui import *

HEADERLEN=10

class ClientThread(threading.Thread):
    def __init__(self, client_sock):
        threading.Thread.__init__(self)
        self.queue = queue.Queue() # enkodowana wiadomosc powinna znalesc sie w kolejce (razem z headerem)
        self.active = True
        self.client_sock = client_sock

    def addToQueue(self,item):
        self.queue.put(item)

    def run(self):
        print("client thread started")
        while self.active == True:
            if self.queue.empty() == False:
                msg = self.queue.get()
                send_len = str(len(msg)).encode("utf-8")
                send_len += b' ' * (HEADERLEN - len(send_len))
                self.client_sock.sendall(send_len)
                self.client_sock.sendall(msg)

            time.sleep(0.01)

class UberSocket(threading.Thread):
    def __init__(self, ip, port=37234, headerlength=6):
        threading.Thread.__init__(self)
        self.client_thread_list = []
        self.running = False
        self.headerlength = headerlength
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((ip,port))
        self.sock.listen(5) # Maksymalnie 5 w kolejce

    def run(self):
        self.running = True

        while self.running == True:
            client_conn,client_addr = self.sock.accept()
            client_thread = ClientThread(client_conn)
            self.client_thread_list.append(client_thread)
            client_thread.start()
            print("Someone connected!")
    def sendToQueueAll(self,msg):
        for client in self.client_thread_list:
            client.addToQueue(msg)

    def prepMessage(self,data,isEncoded=False):
        # Koduje wiadomosc z naglowkiem zawierajacym dlugosc wiadomosci na poczatku
        # if isEncoded == False:
        #     msg = f'{len(data):<{self.headerlength}}' + data
        #     msg = bytes(msg, encoding="utf-8")
        # else:
        #     msg = bytes(f'{len(data):<{self.headerlength}}', encoding="utf-8") + data
        self.sendToQueueAll(data)
    def stop(self):
        self.running = False
        # TODO Zamknij wszystkie połączenia

class Epclient2(threading.Thread):
    def __init__(self,ip,guiInstance=None,port=37234,headerlength=6):
        threading.Thread.__init__(self, daemon=True)
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.ip,self.port))
        self.headerlength = headerlength
        self.guiInstance = guiInstance
    
    def run(self):
        print("Client recv thread started")
        #isNew = True
        while True:
            full_msg = b''
            msg_len = self.sock.recv(HEADERLEN).decode("utf-8")
            if msg_len:
                msg_len = int(msg_len)
                while msg_len:
                    newbuf = self.sock.recv(msg_len)
                    full_msg += newbuf
                    msg_len -= len(newbuf)
                unpackedMsg = pickle.loads(full_msg)
                self.guiInstance.draw2points(unpackedMsg[0], unpackedMsg[1], unpackedMsg[2], unpackedMsg[3])
'''
class Epserver:
    RUNNING=False
    def __init__(self,ip=None, port=37234):
        customsock = UberSocket(ip,port)
    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.HOST, self.PORT))
        self.server_socket.listen()

        self.RUNNING=True
        self.sv_thread = threading.Thread(target=self.serverthread)
        self.sv_thread.start()

    def serverthread(self):
        print("Wątek z serwerem uruchomiony!")
        self.receive()
        print("...")
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
'''

