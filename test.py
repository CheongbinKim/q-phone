import wwwauth

authTools = wwwauth.WWWAuthenticate()

authTools.setNonce("1bd7437f")
authTools.setUri("sip:223.130.135.113:5061")

res = authTools.getResonse('9999','3834c7840b10baa98ecad6e6ff9867d2')

print(res)


#4c9d1c6c52eea0d3d5bd840bd59b6042
#4c9d1c6c52eea0d3d5bd840bd59b6042

#Digest username="9999",realm="asterisk",nonce="15a93a8e",uri="sip:223.130.135.113:5061",response="4c9d1c6c52eea0d3d5bd840bd59b6042",algorithm=MD5
#Digest username="9999",realm="asterisk",nonce="7bd16a01",uri="sip:223.130.135.113:5061",response="9d32addabede40b91176b9229904147f",algorithm=MD5