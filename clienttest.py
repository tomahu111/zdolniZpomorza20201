import socket
import time
from epserver import *

client = Epclient2(socket.gethostname())
client.start()

while True:
    time.sleep(1)