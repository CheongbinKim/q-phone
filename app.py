import socket
import re
import os
import sys
import signal

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


def startSIPServer():
    env = Env()

    localIP     = "0.0.0.0"
    localPort   = os.getenv('PORT',10001)
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

        sipMsg = sip_message.SipMessage.from_string(data)

        if sipMsg.type == 0:
            user_number = sipMsg.headers['from']['name']
            if sipMsg.method == 'INVITE':
                info("INVITE" + user_number)
                
                # SDP 추출
                sdpMsg = sdp_message.SdpMessage.from_string(sipMsg.content)

                # Media Channel 생성
                t = RtpServer(sipMsg,sdpMsg)
                t.start()
                calls.append(t)
                    
                inviteOk(server,sipMsg)
            elif sipMsg.method == 'ACK':
                info("ACK" + user_number)
                info(sipMsg.stringify())
            elif sipMsg.method == 'BYE':
                info("BYE" + user_number)
                inviteByeOk(server,sipMsg)

if __name__ == "__main__":
    startSIPServer()
