import socket
import threading, requests, time

from voice_module import VoiceModule
from klogging import *

class RtpServer(threading.Thread):
    def __init__(self,caller_number,caller_address,rtp_port):
        threading.Thread.__init__(self)

        self.caller_number = caller_number
        self.caller_address = caller_address
        
        localIP = "0.0.0.0"
        localPort = rtp_port
        self.bufferSize  = 172

        self.server = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.server.bind((localIP, localPort))
        info("Bind Rtp Server %s:%d Inbound %s" % (localIP,localPort,caller_number))


    def close(self):
        self.server.close()

    def run(self):
        vm = VoiceModule(self.caller_number,self.caller_address)
        while True:
            data, addr = self.server.recvfrom(self.bufferSize)
            if not data:
                error("Client has exited")
                break
            
            vm.receivePacket(data)

            # echo tests 
            #self.server.sendto(data,self.caller_address)
            #print(data)

 