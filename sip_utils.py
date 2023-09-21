from sip_parser import sip_message

def inviteOk(sock,pkt):
    print("200 OK")

    sdp = '''v=0
o=root 30292919 30292919 IN IP4 13.124.201.154
s=Asterisk PBX 12.8.0-rc2
c=IN IP4 13.124.201.154
t=0 0
m=audio 12345 RTP/AVP 0 101
a=rtpmap:0 PCMU/8000
a=rtpmap:101 telephone-event/8000
a=fmtp:101 0-15
a=ptime:20
a=maxptime:150
a=sendrecv'''

    sip_msg = sip_message.SipMessage.from_dict({"status": 200, "reason": "OK", "content":sdp,"headers": pkt.headers})

    #print(sip_msg.stringify())

    sendBytes = str.encode(sip_msg.stringify())

    #print(sendBytes)

    target = (pkt.headers['via'][0]['host'],pkt.headers['via'][0]['port'])
    sock.sendto(sendBytes,target)

def inviteByeOk(sock,pkt):
    print("BYE 200 OK")
    sip_msg = sip_message.SipMessage.from_dict({"status": 200, "reason": "OK", "headers": pkt.headers})
    #print(sip_msg.stringify())
    sendBytes = str.encode(sip_msg.stringify())
    target = (pkt.headers['via'][0]['host'],pkt.headers['via'][0]['port'])
    sock.sendto(sendBytes,target)