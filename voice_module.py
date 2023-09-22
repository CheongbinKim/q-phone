import socket

class VoiceModule:
    def __init__(self,call_number,caller_address):
        self.call_number = call_number # 고객 전화번호, 식별자
        self.caller_address = caller_address # (ip,port) 형식, 모듈 -> 고객 음성데이터 전송 채널

        pass

    def receivePacket(self,data):
        # 'data' is Rtp packet 172bytes (ulaw)
        print(data)

        # 음성 전송 시 아래와 같이 전송하시면 됩니다.
        # socket.sendto(rtpBytes, self.caller_address)