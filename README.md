# q-phone (SIP Client)
- Asterisk 전용 SIP Client
- Audio RTP 서버를 직접 생성하여 음성 데이터를 조작 및 전송 할 수 있음.
- Asterisk Registration 시 'Digest' 인증 사용
- Asterisk Extensions 등록 시 Qualify=no 필수 (OPTIONS 처리 기능 없음)

# 다운로드
```
git clone https://github.com/CheongbinKim/q-phone.git
```

# 설치
- sip-parser(https://github.com/alxgb/sip-parser.git) 설치
```
pip install ./sip-parser
```

# Setup
- Asterisk 에 등록 된 Extensions (Peer) 정보 USERNAME, PASSWORD 환경변수 Set
- Asterisk 서버 정보 ARI_HOST, ARI_PORT Set
```
# Required. User SIP Phone Number in asterisk
export USERNAME=

# Required. User SIP Phone Password in asterisk
export PASSWORD=

# Required. Asterisk Host Address
export ARI_HOST=

# Required. Asterisk Port Number
export ARI_PORT=
```

# 실행
```
python3 app.py
```

# Custom 음성 데이터 처러
- 전화 연결 시 voice_module.py 내 VoiceModule 클래스 receivePacket() 함수로 RTP Packet 전송 됨
## 음성데이터 받기
```
def receivePacket(self,data):
        # 'data' is Rtp packet 172bytes (ulaw)
        print(data)
```

## 음성데이터 보내기 (소켓은 생성하시면 됩니다.) 
- VoiceModule 내 self.caller_address 가 연결 된 고객전화기의 RTP Server (주소,포트번호)
```
def receivePacket(self,data):
    # 음성 전송 시 아래와 같이 전송하시면 됩니다.
    # socket.sendto(rtpBytes, self.caller_address)
```

