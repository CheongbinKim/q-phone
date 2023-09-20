from sip_parser import sip_message
import random
import string
import socket 
import wwwauth

class Register:
    def __init__(self,sock,username,password,host,port):
        self.sock = sock
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.bufferSize  = 1200 # SIP packets will be between 500-1200 bytes
        self.callId = self.generate_call_id(35)
        self.cSeq = 25555
        self.localhost = socket.gethostbyname(socket.gethostname())
        self.localport = 10001
        self.branch = self.generate_call_id(35)
        self.register()
        

    # Call-ID 생성
    def generate_call_id(self,length):
        characters = string.ascii_lowercase + string.digits  # 소문자와 숫자 사용
        random_string = ''.join(random.choice(characters) for _ in range(length))
        return random_string

    def register(self):
        # REGISTER 메세지 생성
        msg = sip_message.SipMessage.from_dict(
            {
                "method": "REGISTER",
                "uri": ("sip:{}:{}").format(self.host,self.port),
                "version": "2.0",
                "headers": {
                    "via":{
                        "version": "2.0",  # Can be None!
                        "protocol": "UDP",
                        "host": self.localhost,
                        "port": self.localport,
                        "params":{"rport":"","branch":self.branch}
                    },
                    "from": {
                        "uri": {
                            "scheme": "sip",
                            "user":self.username,
                            "host": self.host,
                            "port": self.port
                        },
                        "params": {"tag": "xk7588628423"}
                    },
                    "to": { 
                        "uri": {
                            "scheme": "sip",
                            "user":self.username,
                            "host": self.host,
                            "port": self.port,
                            #"params": {"lr": None},
                        }
                    },
                    "max-Forwards":70,
                    "call-id":self.callId,
                    #"call-id":"81033714372331641429612113113278b33",
                    "cSeq":f"{self.cSeq} REGISTER",
                    "contact":{
                        "uri":{
                            "scheme":"sip",
                            "user":self.username,
                            "host":socket.gethostbyname(socket.gethostname()),
                            "port":10001
                        }
                    },
                    "allow":"ACK,BYE,CANCEL,INVITE,REGISTER,UPDATE,MESSAGE,INFO,OPTIONS,SUBSCRIBE,NOTIFY,REFER,COMET,PUBLISH,PING,DO,SHAREDFN",
                    "allow-events":"presence,refer,telephone-event,keep-alive,dialog",
                    "supported": "replaces, timer",
                    "event": "registration",
                    "user-agent": "QuantumPhone 0.1",
                    "expires":600,
                    "accept": "application/sdp,application/dtmf-relay,audio/telephone-event,message/sipfrag,text/plain,text/html"
                },
            }
        )

        sendBytes = str.encode(msg.stringify())
        
        #sendBytes = str.encode(test)

        #sendSock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        #sendSock.bind((self.localhost,self.localport))

        self.sock.sendto(sendBytes,(self.host,self.port))

        recvData,recvAddr = self.sock.recvfrom(self.bufferSize)

        recvData = recvData.decode('UTF-8')

        sipMsg = sip_message.SipMessage.from_string(recvData)

        print(sipMsg.headers['www-authenticate'])

        nonce = sipMsg.headers['www-authenticate'][0]['nonce']

        wauth = wwwauth.WWWAuthenticate()

        wauth.setNonce(nonce)

        uri = f"sip:{self.host}:{self.port}"
        wauth.setUri("sip:223.130.135.113:5061")

        wauthRes = wauth.getResonse(self.username,self.password)

        msg = sip_message.SipMessage.from_dict(
            {
                "method": "REGISTER",
                "uri": ("sip:{}:{}").format(self.host,self.port),
                "version": "2.0",
                "headers": {
                    "via":{
                        "version": "2.0",  # Can be None!
                        "protocol": "UDP",
                        "host": self.localhost,
                        "port": self.localport,
                        "params":{"rport":"","branch":self.branch}
                    },
                    "from": {
                        "uri": {
                            "scheme": "sip",
                            "user":self.username,
                            "host": self.host,
                            "port": self.port
                        },
                        "params": {"tag": "xk7588628423"}
                    },
                    "to": { 
                        "uri": {
                            "scheme": "sip",
                            "user":self.username,
                            "host": self.host,
                            "port": self.port,
                            #"params": {"lr": None},
                        }
                    },
                    "max-Forwards":70,
                    "call-id":self.callId,
                    #"call-id":"81033714372331641429612113113278b33",
                    "cSeq":f"{self.cSeq+1} REGISTER",
                    "contact":{
                        "uri":{
                            "scheme":"sip",
                            "user":self.username,
                            "host":socket.gethostbyname(socket.gethostname()),
                            "port":10001
                        }
                    },
                    "authorization":{
                        'username':f'"{self.username}"',
                        'scheme':'Digest',
                        'realm':f'"asterisk"',
                        'nonce': nonce,
                        'uri':f'"{uri}"',
                        'response': f'"{wauthRes}"',
                        'algorithm':'MD5'
                    },
                    "allow":"ACK,BYE,CANCEL,INVITE,REGISTER,UPDATE,MESSAGE,INFO,OPTIONS,SUBSCRIBE,NOTIFY,REFER,COMET,PUBLISH,PING,DO,SHAREDFN",
                    "allow-events":"presence,refer,telephone-event,keep-alive,dialog",
                    "supported": "replaces, timer",
                    "event": "registration",
                    "user-agent": "QuantumPhone 0.1",
                    "expires":600,
                    "accept": "application/sdp,application/dtmf-relay,audio/telephone-event,message/sipfrag,text/plain,text/html"
                },
            }
        )

        # msg.headers['authorization'] = [{
        #     'username':f'"{self.username}"',
        #     'scheme':'Digest',
        #     'nonce': nonce,
        #     'realm':f'"asterisk"',
        #     'algorithm':'MD5',
        #     'response': f'"{wauthRes}"',
        #     'uri':f'"{uri}"'
        # }]

        #msg.headers['cSeq'] = f"{self.cSeq+1} REGISTER"
        
        
        #msg = sip_message.SipMessage.from_string(msg.stringify())

        print(msg.stringify())
        
        sendBytes = str.encode(msg.stringify())
        self.sock.sendto(sendBytes,(self.host,self.port))

        
        recvData,recvAddr = self.sock.recvfrom(self.bufferSize)

        recvData = recvData.decode('UTF-8')

        sipMsg = sip_message.SipMessage.from_string(recvData)

        print(sipMsg.stringify())
        



        