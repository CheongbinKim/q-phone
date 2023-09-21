raw_message='''INVITE sip:9999@172.31.20.149:10001 SIP/2.0
Via: SIP/2.0/UDP 223.130.135.113:5061;branch=z9hG4bK40bc5a44;rport
Max-Forwards: 70
From: "01064498979" <sip:01064498979@223.130.135.113:5061>;tag=as16549d66
To: <sip:9999@172.31.20.149:10001>
Contact: <sip:01064498979@223.130.135.113:5061>
Call-ID: 730b38441622c64738f571ed38a6c21d@223.130.135.113:5061
CSeq: 102 INVITE
User-Agent: FPBX-12.0.76.6(12.8.0)
Date: Wed, 20 Sep 2023 06:29:28 GMT
Allow: INVITE, ACK, CANCEL, OPTIONS, BYE, REFER, SUBSCRIBE, NOTIFY, INFO, PUBLISH, MESSAGE
Supported: replaces, timer
Content-Type: application/sdp
Content-Length: 261

v=0
o=root 1188614393 1188614393 IN IP4 223.130.135.113
s=Asterisk PBX 12.8.0-rc2
c=IN IP4 223.130.135.113
t=0 0
m=audio 13634 RTP/AVP 0 101
a=rtpmap:0 PCMU/8000
a=rtpmap:101 telephone-event/8000
a=fmtp:101 0-16
a=ptime:20
a=maxptime:150
a=sendrecv
'''

lines = [line.strip().split("=", maxsplit=1) for line in raw_message.split("\n")]

print(lines)

fields_order = ""
fields = []

for line in lines:
    if 1 != len(line[0]):
        continue
    name, value = line[0], line[1]
    fields_order += name
    fields.append(FieldRaw(name, value))
