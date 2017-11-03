import struct
class send_data:
    def __init__(self,buffer):
        self.struct_fmt  =str.format('3f')
        self.struct_len = struct.calcsize(self.struct_fmt)
        print buffer

        if buffer != None:
            unpacked = struct.unpack(self.struct_fmt, buffer)


            self.acc_gyro = unpacked[0]
            self.acc_pitch= unpacked[1]
            self.p_ang_vel = unpacked[2]

    def GetBytes(self):
            return struct.pack(self.struct_fmt,self.acc_gyro,self.acc_pitch,self.p_ang_vel )

    def GetSize(self):
        return self.struct_len

class PemResponse:
    def __init__(self,buffer,size):
        self.struct_fmt  =str.format('{0}s2I',size)
        self.struct_len = struct.calcsize(self.struct_fmt)


        if buffer != None:
            unpacked = struct.unpack(self.struct_fmt, buffer)


            self.PEMNAME = unpacked[0].replace("\x00","")
            self.PEMSIZE = unpacked[1]
            self.RESPONSE = unpacked[2]

    def GetBytes(self):
            return struct.pack(self.struct_fmt,self.PEMNAME,self.PEMSIZE,self.RESPONSE)

    def GetSize(self):
        return self.struct_len
class JoinResponse:
    def __init__(self,buffer):
        self.struct_fmt  =str.format('2I')
        self.struct_len = struct.calcsize(self.struct_fmt)


        if buffer != None:
            unpacked = struct.unpack(self.struct_fmt, buffer)
            self.MSGID = unpacked[0]
            self.RESPONSE = unpacked[1]

    def GetBytes(self):
            return struct.pack(self.struct_fmt,self.MSGID,self.RESPONSE)

    def GetSize(self):
        return self.struct_len
class JoinRequest:
    def __init__(self,buffer,size1,size2,size3):
        self.struct_fmt  =str.format('{0}s{0}s{0}s',size1,size2,size3)
        self.struct_len = struct.calcsize(self.struct_fmt)


        if buffer != None:
            unpacked = struct.unpack(self.struct_fmt, buffer)
            self.USERID = unpacked[0].replace("\x00","")
            self.USERPW = unpacked[1].replace("\x00","")
            self.USERERMAIL = unpacked[2].replace("\x00","")


    def GetBytes(self):
            return struct.pack(self.struct_fmt,self.USERIDLEN,self.USERPWLEN,self.USERERMAILLEN)

    def GetSize(self):
        return self.struct_len
class SignRequest:
    def __init__(self,buffer):
        self.struct_fmt  =str.format('{0}s{0}s',10,10)
        self.struct_len = struct.calcsize(self.struct_fmt)


        if buffer != None:
            unpacked = struct.unpack(self.struct_fmt, buffer)
            self.USERID = unpacked[0].replace("\x00","")
            self.USERPW = unpacked[1].replace("\x00","")


    def GetBytes(self):
            return struct.pack(self.struct_fmt,self.USERID,self.USERPW)

    def GetSize(self):
        return self.struct_len
class SignResponse:
    def __init__(self,buffer):
        self.struct_fmt  =str.format('2IB')
        self.struct_len = struct.calcsize(self.struct_fmt)


        if buffer != None:
            unpacked = struct.unpack(self.struct_fmt, buffer)
            self.MSGID = unpacked[0]
            self.RESPONSE = unpacked[1]
            self.DENY = unpacked[2]
    def GetBytes(self):
            return struct.pack(self.struct_fmt,self.MSGID,self.RESPONSE,self.DENY)

    def GetSize(self):
        return self.struct_len


class FilesendRequest:
    def __init__(self,buffer):
        self.struct_fmt  =str.format('{0}s{0}sI',100,100)
        self.struct_len = struct.calcsize(self.struct_fmt)


        print buffer

        if buffer != None:
            unpacked = struct.unpack(self.struct_fmt, buffer)

            self.ROOTNAME = unpacked[0].replace("\x00", "")
            self.PATH = unpacked[0].replace("\x00","")
            self.FILESIZE = unpacked[1]


    def GetBytes(self):
            return struct.pack(self.struct_fmt,self.ROOTNAME,self.PATH,self.FILESIZE )

    def GetSize(self):
        return self.struct_len
class SendResponse:
    def __init__(self,buffer):
        self.struct_fmt  =str.format('IB')
        self.struct_len = struct.calcsize(self.struct_fmt)


        if buffer != None:
            unpacked = struct.unpack(self.struct_fmt, buffer)
            self.MSGID = unpacked[0]
            self.RESPONSE = unpacked[1]

    def GetBytes(self):
            return struct.pack(self.struct_fmt,self.MSGID,self.RESPONSE)

    def GetSize(self):
        return self.struct_len
class fileData:
    def __init__(self,buffer):
        if(buffer != None):
            self.data = buffer
    def GetBytes(self):
        return self.data
    def GetSize(self):
        return len(self.data)