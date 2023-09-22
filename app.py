import socket
import re
import os
import sys
import signal
import random

from rtpserver import RtpServer
from sip_parser import sip_message
from sip_parser import sdp_message
from register import Register
from sip_utils import inviteOk
from sip_utils import inviteByeOk
from kenv import Env

from klogging import *



# 앱 종료
def handler(signum, frame):
        sys.exit(1)
signal.signal(signal.SIGTERM, handler)

def getShufflePort(start,end):
    port_range = list(range(start,end))

    random.shuffle(port_range)

    return port_range[0]

def startSIPServer():
    env = Env()

    localIP     = env.HOST
    localPort   = env.PORT
    bufferSize  = 1200 # SIP packets will be between 500-1200 bytes

    calls = []

    server = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    
    server.bind((localIP, localPort))

    info("SIP server up and listening")

    Register(server,env.USERNAME,env.PASSWORD,env.ARI_HOST,env.ARI_PORT)

    while(True):
        data, addr = server.recvfrom(bufferSize)
        if not data:
            error("Client has exited")
            break

        data = data.decode('UTF-8')

        sip_msg = sip_message.SipMessage.from_string(data)

        if sip_msg.type == 0:
            caller_number = sip_msg.headers['from']['name']
            
            if sip_msg.method == 'INVITE':
                info("INVITE" + caller_number)
                
                # SDP 추출
                sdp_msg = sdp_message.SdpMessage.from_string(sip_msg.content)

                rtp_port = getShufflePort(env.RTP_PORT_START,env.RTP_PORT_END)
                
                caller_address = (sdp_msg.session_description_fields["c"].connection_address,sdp_msg.media_descriptions[0].media.port)

                # Media Channel 생성
                t = RtpServer(caller_number, caller_address,rtp_port)
                t.start()
                calls.append(t)

                info("200 OK" + caller_number)
                inviteOk(server,sip_msg,env.EXTERNAL_ADDRESS, rtp_port)
            elif sip_msg.method == 'ACK':
                info("ACK" + caller_number)
            elif sip_msg.method == 'BYE':
                info("BYE" + caller_number)
                inviteByeOk(server,sip_msg)

if __name__ == "__main__":
    startSIPServer()
