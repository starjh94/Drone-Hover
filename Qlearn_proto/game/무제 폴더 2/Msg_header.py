#-*- coding: utf-8 -*-
import struct


class Header:
    def __init__(self,buffer):
        self.struct_fmt = '=2I'
        self.struct_len = struct.calcsize(self.struct_fmt)

        if buffer != None:
            unpacked = struct.unpack(self.struct_fmt, buffer)


            self.MSGTYPE = unpacked[0]
            self.BODYLEN = unpacked[1]





    def GetBytes(self):
            return struct.pack(self.struct_fmt,*(self.MSGTYPE, self.BODYLEN) )

    def GetSize(self):
        return self.struct_len
