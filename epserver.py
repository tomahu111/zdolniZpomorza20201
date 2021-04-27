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
        self.converted=[]
        socketThread = threading.Thread(target=receive)
        socketThread.start()
        drawThread = threading.Thread(target=draw)
        drawThread.start()
    def receive():
        #global converted
        while True:
        
            info = client_socket.recv(BUFFER).decode("utf8")
            try:
                self.converted = eval((info))
            except:
                #print("Cos jest nie tak")
                self.converted = []
            print(self.converted)
            #print(converted)

    def drawpoint(x1,y1, color, thickness):
        canva.create_oval(x1-thickness, y1-thickness, x1+thickness, y1+thickness, fill=color, outline=color)
    

    def draw():
        #global converted
        while True:
            if len(converted) > 0:
                x1 = self.converted[0]
                y1 = self.converted[1]
                x2 = self.converted[2]
                y2 = self.converted[3]
                color = self.converted[4]
                thickness = self.converted[5]
                converted.clear()
                xdiff = x1-x2
                ydiff = y1-y2
                maxnum = max(abs(xdiff), abs(ydiff))
                for i in range(maxnum):
                    x = int(x2 + (float(i)/maxnum * xdiff))
                    y = int(y2 + (float(i)/maxnum * ydiff))
                    drawpoint(x,y, color, thickness)
            
                #canva.create_oval(x-1, y-1, x+1, y+1, fill="black", outline="black")


