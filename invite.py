import socket
import re
from email.parser import Parser
from email.policy import default
from hashlib import md5

from sip_parser import sip_message


serverAddressPort   = ("223.130.135.113", 5061)
bufferSize          = 1200

# 클라이언트 쪽에서 UDP 소켓 생성
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)


msg = sip_message.SipMessage.from_dict(
    {
        "method": "REGISTER",
        "uri": "somecooluri@example.com",
        "version": "2.0",
        "headers": {
            "route": {
                "uri": {
                    "scheme": "sip",
                    "host": "127.0.0.1",
                    "port": 5060,
                    "params": {"lr": None},
                }
            }
        },
    }
)

print(msg)

# 생성된 UDP 소켓을 사용하여 서버로 전송
bytesToSend         = str.encode(registerMsg[0])
UDPClientSocket.sendto(bytesToSend, serverAddressPort)

msgFromServer = UDPClientSocket.recvfrom(bufferSize)

#print(msgFromServer)
#print(msgFromServer[0])

msg = msgFromServer[0].decode('UTF-8')

#print(msg.split('\n'))

first_line = ""
another_line = ""
i=0

for d in msg.split('\n'):
    if i == 0:
        first_line = d
    else:
        another_line += (d+'\n')
    i = i + 1

print(first_line)
print(another_line)

headers = Parser(policy=default).parsestr(another_line)


#msg_split = msg.split('\n')



print(headers)
print(headers['WWW-Authenticate'].split(' ')[1].split(','))


authCls = wwwauth.WWWAuthenticate()


for d in headers['WWW-Authenticate'].split(' ')[1].split(','):
    kv = d.split('=')
    if kv[0] == 'nonce':
        print(kv[1])
        print(type(kv[1]))
        authCls.setNonce(kv[1])
        print(authCls.getResonse('7000','7000'))
        
    


#msg = "{}".format(msgFromServer[0])


# nonce 

bytesToSend         = str.encode(registerMsg[1])
UDPClientSocket.sendto(bytesToSend, serverAddressPort)

#print(msg)

msgFromServer = UDPClientSocket.recvfrom(bufferSize)

msg = "{}".format(msgFromServer[0])