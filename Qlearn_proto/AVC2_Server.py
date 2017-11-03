#-*- coding: utf-8 -*-
import socket
import struct
import os
import sys
import socket
import Msg

from Msg import Message
from Msg_header import Header
from Msg_body import send_data, PemResponse , fileData, JoinResponse, SignResponse, FilesendRequest, SendResponse
from Msg_util import MsgUtil
from threading import Thread
from time import ctime
from SocketServer import ThreadingMixIn


PORT = 56793
BUFSIZE = 1024
HOST = ''
ADDR = (HOST, PORT)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(ADDR)
threads = []
pem_path = "ka.png"
pem_size = 5
sock.listen(5)
print "Waiting for incoming connections..."
ClientSocket, addr_info = sock.accept()
print('[INFO][%s] New Clinet %s is Connecting.' % (
ctime(), addr_info[0]))  # newthread = ClientThread(addr_info[0],PORT,ClientSocket)
# newthread.start()
# threads.append(newthread)
"""
for t in threads:
    t.join()
"""
acc_gyro = 1
while True:

    sendData = Msg.Message(None)
    sendData.Header = Header(None)
    sendData.Body = send_data(None)
    sendData.Header.MSGTYPE = Msg.DATA_SEND
    sendData.Header.BODYLEN = sendData.Body.GetSize()
    sendData.Body.acc_gyro = acc_gyro
    sendData.Body.acc_pitch =40.1
    sendData.Body.p_ang_vel =40.1
    acc_gyro = acc_gyro + 5
    MsgUtil.send(ClientSocket, sendData)