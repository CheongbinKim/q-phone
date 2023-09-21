from sip_parser import sip_message

from klogging import *

def inviteOk(sock,pkt,external_address,rtpPort):
    sdp = f'''v=0
o=root 30292919 30292919 IN IP4 {external_address}
s=Asterisk PBX 12.8.0-rc2
c=IN IP4 {external_address}
t=0 0
m=audio {rtpPort} RTP/AVP 0 101
a=rtpmap:0 PCMU/8000
a=rtpmap:101 telephone-event/8000
a=fmtp:101 0-15
a=ptime:20
a=maxptime:150
a=sendrecv'''

    sip_msg = sip_message.SipMessage.from_dict({"status": 200, "reason": "OK", "content":sdp,"headers": pkt.headers})

    sendBytes = str.encode(sip_msg.stringify())

    target = (pkt.headers['via'][0]['host'],pkt.headers['via'][0]['port'])
    sock.sendto(sendBytes,target)

def inviteByeOk(sock,pkt):
    sip_msg = sip_message.SipMessage.from_dict({"status": 200, "reason": "OK", "headers": pkt.headers})

    debug(sip_msg.stringify())

    sendBytes = str.encode(sip_msg.stringify())
    target = (pkt.headers['via'][0]['host'],pkt.headers['via'][0]['port'])
    sock.sendto(sendBytes,target)