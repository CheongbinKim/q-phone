from hashlib import md5
import re 

class WWWAuthenticate:
    method = "Digest"
    algorithm = "md5"
    realm = "asterisk"
    qop="auth"

    def __init__(self):
        self.__nonce = ""
        self.uri = ""

    def setNonce(self,value):
        value = re.sub(r'"','',value)
        self.__nonce = value

    def setUri(self,uri):
        self.uri = uri

    def md5sum(self,data):
        m = md5()
        m.update(data.encode('utf-8'))
        return m.hexdigest()

    def getResonse(self,username,password):
        #A1 = f"{username}:{self.realm}:{password}"
        #A2 = f"REGISTER:{self.uri}"
        #response = md5(f"{A1}:{self.__nonce}:{A2}".encode()).hexdigest()

        h1 = self.md5sum('%s:%s:%s' % (username,self.realm,password))
        h2 = self.md5sum("REGISTER:%s" % (self.uri))
        response = self.md5sum('%s:%s:%s' % (h1,self.__nonce,h2))
        
        # 9e033df1e4859a41d2a7957fbe3b158

        return response