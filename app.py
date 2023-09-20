import socket
from sip_parser import sip_message

from register import Register

import sys
import signal

# 앱 종료
def handler(signum, frame):
        sys.exit(1)

signal.signal(signal.SIGTERM, handler)

localIP     = "0.0.0.0"
localPort   = 10001
bufferSize  = 1200 # SIP packets will be between 500-1200 bytes

def startSIPServer():
    server = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    
    server.bind((localIP, localPort))

    print("UDP server up and listening")

    Register(server,"9999","3834c7840b10baa98ecad6e6ff9867d2","223.130.135.113",5061)

    while(True):
        data, addr = server.recvfrom(bufferSize)
        if not data:
            print("client has exited")
            break

        data = data.decode('UTF-8')

        sipMsg = sip_message.SipMessage.from_string(data)

        print(sipMsg.stringify())

        #print(sipMsg.headers)
        #print(sipMsg.type)
        #print(sipMsg.version)
        #print(sipMsg.method)


if __name__ == "__main__":
    startSIPServer()