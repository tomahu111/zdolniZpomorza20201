import socket
import time
from epserver import *

ubsock = UberSocket(socket.gethostname())
ubsock.start()

while True:
    ubsock.prepMessage("Test test abctt....")
    time.sleep(3)