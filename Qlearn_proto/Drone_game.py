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
import sysv_ipc
import time
import subprocess
#proc = subprocess.Popen(["python","thread_test7.py"])
#subprocess.Popen(["python","degree_process.py"])
import sys

if len(sys.argv) == 1:          # 옵션 없으면 도움말 출력하고 종료
  print "숫자로 된 옵션을 입력해 주세요"
  exit(1)

time.sleep(5)
memory = sysv_ipc.SharedMemory(600)
smp = sysv_ipc.Semaphore(128)
PORT = int(sys.argv[1])
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
    smp.acquire(10)
    vari = memory.read()
    smp.release()
    data = float(vari.rstrip('\x00'))
    sendData.Body.acc_gyro =data
    MsgUtil.send(ClientSocket, sendData)
    print data
    """
     recvdata = ClientSocket.recv(1024)
    if recvdata == None :
	break
    """
ClientSocket.close()
