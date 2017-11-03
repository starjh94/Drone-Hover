#-*- coding: utf-8 -*-
# 메시지 타입(MSGTYPE) 상수 정의
DATA_SEND = 0x01
REQ_PEM = 0x01
REP_PEM = 0x02
SEND_PEM =0x03
REQ_SIGN =0x04
REP_SIGN = 0x05
REQ_SEND = 0x06
REP_SEND = 0x07
# 파일 분할 여부(FRAGMENTED) 상수 정의
NOT_FRAGMENTED = 0x00
FRAGMENTED = 0x01

# 분할된 메시지의 마지막 여부(LASTMSG) 상수 정의
NOT_LASTMSG = 0x00
LASTMSG = 0x01

# 파일 전송 수락 여부 (RESPONSE) 상수 정의
ACCEPTED = 0x00
DENIED = 0x01

# 파일 전송 여부(RESULT) 상수 정의
FAIL = 0x00
SUCCESS = 0x01
NOT_DENY = 0x02
#유저 로그인 거부 코드 - Response 정의
ID_INCORRECT = 0x00
PW_INCORRECT = 0x01


class ISerializable:
    def GetBytes(self):  # 메시지, 헤더, 바디는 모두 이 클래스를 상속합니다. 즉, 이들은 자신의 데이터를 바이트 배열로 변환하고 그 바이트 배열의 크기를 반환해야 합니다.
        pass

    def GetSize(self):
        pass


class Message:  # Message 클래스는 ISerializable로부터 상속을 받은 Header와 Body로 구성됩니다.
    def __init__(self,buffer):
        self.Header = ISerializable()
        self.Body = ISerializable()

    def GetBytes(self):
        if self.Body == None:
            buffer = bytes(self.GetSize())
            header = self.Header.GetBytes()
        else:
            buffer = bytes(self.GetSize())
            header = self.Header.GetBytes()
            body = self.Body.GetBytes()

        if self.Body == None:

            return header
        else:
            return header + body
    def GetSize(self):
        if(self.Body == None):
            return self.Header.GetSize()
        else:

            return self.Header.GetSize() + self.Body.GetSize()