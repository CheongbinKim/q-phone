#from enum import Enum
import os
import sys
import urllib.request
import re

class Env():
    def __init__(self):
        self.HOST = os.environ.get('HOST','0.0.0.0')
        self.PORT = os.environ.get('PORT',5080)
        self.EXTERNAL_ADDRESS = os.environ.get('EXTERNAL_ADDRESS',self.getExternalIpAddress())

        if os.environ.get('USERNAME') is None:
            warning('USERNAME is None, e.g.) export USERNAME=9999')
            sys.exit(0)
        self.USERNAME = os.environ.get('USERNAME')
        
        if os.environ.get('PASSWORD') is None:
            warning('PASSWORD is None, e.g.) export PASSWORD=abcd')
            sys.exit(0)
        self.PASSWORD = os.environ.get('PASSWORD')
        
        if os.environ.get('ARI_HOST') is None:
            warning('ARI_HOST is None, e.g.) export ARI_HOST=external_asterisk_address')
            sys.exit(0)
        self.ARI_HOST = os.environ.get('ARI_HOST')

        if os.environ.get('ARI_PORT') is None:
            warning('ARI_PORT is None, e.g.) export ARI_PORT=external_asterisk_address')
            sys.exit(0)
        self.ARI_PORT = int(os.environ.get('ARI_PORT'))

    def getExternalIpAddress(self):
        request = urllib.request.urlopen("https://ifconfig.me/").read()
        request = request.decode('UTF-8')
        return request

    
