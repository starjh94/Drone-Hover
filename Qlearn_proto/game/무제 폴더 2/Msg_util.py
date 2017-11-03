# -*- coding: utf-8 -*-
from socket import *
from time import ctime
import Msg

from Msg import Message
from Msg_header import Header
import struct
import sys
import os

from Msg_body import PemResponse, JoinRequest, SignRequest, FilesendRequest
class MsgUtil:
    @staticmethod
    def send(sock, msg):
        sent = 0
        # bytes[] 구하기
        buffer = msg.GetBytes()
        # msg 크기만큼 send() 반복z
        while sent < msg.GetSize():
            sent += sock.send(buffer)

    @staticmethod
    def receive(socket):

        # 헤더[MSGID+MSGTYPE+BODYLEN+FRAGMENTED+LASTMSG+SEQ]
        # 헤더크기
        headerSize = 8
        # 헤더버퍼
        headerBuffer = bytes()

        # 헤더읽기
        while headerSize > 0:
            buffer = socket.recv(headerSize)  # 헤더크기만큼 읽기
            if not buffer:
                return None

            # 헤더(bytes)읽어서 담기
            headerBuffer += buffer;
            headerSize -= len(buffer)  # 헤더크기에서 빼서 헤더크기만큼 다읽었으면 반복문 나오기
        header = Header(headerBuffer)  # 바디

        # 바디크기
        bodySize = header.BODYLEN
        # 바디버퍼
        bodyBuffer = bytes()

        # 바디읽기
        a = 1
        while bodySize > 0:
            buffer = socket.recv(bodySize)  # 바디크기만큼 읽기
            if not buffer:
                return None


            bodyBuffer += buffer
            bodySize -= len(buffer)  # 바디크기에서 빼서 바디크기만큼 다읽었으면 반복문 나오기

        # 바디객체 생성
        body = None
        if header.MSGTYPE == Msg.REQ_PEM:
            body = PemResponse(bodyBuffer,len("  "))
        elif header.MSGTYPE == Msg.REQ_SIGN:
            body = SignRequest(bodyBuffer)
        elif header.MSGTYPE == Msg.REQ_SEND:
            body = FilesendRequest(bodyBuffer)
        else:
            # Exception 타입 에러 발생
            raise Exception("Unknown MSGTYPE : {0}".format(header.MSGTYPE))


        # 메시지 = 헤더+바디 객체 생성
        msg = Message(None)
        msg.Header = header
        msg.Body = body

        return msg
