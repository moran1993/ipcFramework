import socket
from threading import Thread
from Util.customException import IpException
import re,time

class requestHandler:
    def __init__(self):
        pass

    def praseRequest(self,request):
        print(request)
        return b"OK"


class ServerCore(object):
    def __init__(self,Socket=None,host="localhost",port=6667,listen=10,recvsize=1024):
        ipPattern = r"((25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))"
        if host != "localhost" and not re.match(ipPattern,host):
            raise IpException(ip=host)
        self.__host = host
        if port > 65535 or port < 1024:
            raise IpException(port=port)
        self.__port = port
        self.__listen = listen
        self.__socketThread = None
        self.__recvsize = recvsize
        self.__handler = requestHandler()
        if socket and isinstance(Socket,socket.socket):
            self.__socketThread = Socket

    def __createSocet(self):
        return socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    def createMainSocketThreadAndRun(self):
        self.__socketThread = self.__createSocet()
        self.__socketThread.bind((self.__host,self.__port))
        self.__socketThread.listen(self.__listen)
        while True:
            conn,addr = self.__socketThread.accept()
            while True:
                data = conn.recv(self.__recvsize)
                #TODO 这里得有一个处理函数处理接收到的请求，并对这个进行
                conn.send(b"OK")
                if not data:
                    break
            conn.close()
            ret = self.__handler.praseRequest(data)

    def sendRequest(self,requestMessage,block=None,timeout=0):
        client = self.__createSocet()
        client.connect((self.__host,self.__port))
        client.send(requestMessage.encode("utf-8"))
        ret = client.recv(self.__recvsize)
        if ret or not block:
            client.close()
            del client
            return ret
        while timeout:
            ret = client.recv(self.__recvsize)
            if ret:
                break
            time.sleep(1)
            timeout -= 1
            if timeout == 0:
                ret = "timeout"
        client.close()
        del client
        return ret

try:
    a = ServerCore()
    a.sendRequest("ahahah")
    #a.createMainSocketThreadAndRun()
except Exception as e:
    print(e)
