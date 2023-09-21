import socket
import threading, requests, time

from klogging import *

class RtpServer(threading.Thread):
    def __init__(self,sip,sdp,rtpPort):
        threading.Thread.__init__(self)
        if len(sdp.media_descriptions) > 0:
            localIP = "0.0.0.0"
            localPort = rtpPort
            self.bufferSize  = 172

            self.server = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
            self.server.bind((localIP, localPort))
            info("Bind Rtp Server %s:%d" % (localIP,localPort))
    
    def close(self):
        self.server.close()

    def run(self):
        while True:
            data, addr = self.server.recvfrom(self.bufferSize)
            if not data:
                error("Client has exited")
                break
            
            #print(data)

 