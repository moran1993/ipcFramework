import socket
from threading import Thread
from Util.customException import IpException
import re,time
ERROR = b"ERROR"
OK = b"OK"

class requestHandler:
    def __init__(self):
        pass

    def praseRequest(self,request):
        print(request)
        for i in range(10):
            time.sleep(1)
        return OK


class ServerCore(object):
    def __init__(self,Socket=None,host="localhost",port=6666,listen=10,recvsize=1024):
        ipPattern = r"((25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))"
        if host != "localhost" and not re.match(ipPattern,host):
            raise IpException(ip=host)
        self.__host = host
        if port > 65535 or port < 1024:
            raise IpException(port=port)
        self.__port = port
        self.__listen = listen
        self.__socketThread = None
        self.socketThread = None
        self.__recvsize = recvsize
        self.__handler = requestHandler()
        if Socket and isinstance(Socket,socket.socket):
            self.__socketThread = Socket
        self.initSignle()

    def initSignle(self):
        self.OK = b"OK"
        self.ERROR = b"error"

    def __createSocet(self,timeout=None):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        print(id(s))
        if timeout and timeout > 0:
            s.settimeout(timeout)
        return s

    def __clientThread(self, client):
        print("begin deal")
        client.send(b"OK")
        print("send a signal to client for recive a request")
        rdata = b""
        try:
            rdata = client.recv(self.__recvsize)
            client.sendall(self.__handler.praseRequest(rdata))
        except Exception as e:
            client.close()
            print(e)
        finally:

            client.close()


    def client_handler(self):
        """
        socketserver运行的主要函数 专门处理socket接受到的请求是否需要block处理
        每接收到一个请求就会生成一个线程专门处理接收到的消息
        :return:
        """
        print("socket start")
        while True:
            client,addr = self.__socketThread.accept()
            print(f"get a new request from {addr}")
            messageThread = Thread(target=self.__clientThread,args=(client,))
            messageThread.setDaemon(True)
            messageThread.start()

    def createMainSocketThreadAndRun(self):
        """
        创建一个socket并启动一个专有线程维持socketserver运行
        :return:
        """
        self.__socketThread = self.__createSocet()
        self.__socketThread.bind((self.__host,self.__port))
        self.__socketThread.listen(self.__listen)
        self.socketThread = Thread(target=self.client_handler)
        self.socketThread.setDaemon(True)
        self.socketThread.start()

    def sendRequest(self,requestMessage,timeout=None,block=None):
        """
        发送一个socket请求对当前已启动的socketserver
        :param requestMessage: 要发送的信息
        :param timeout:超时时间，如果不设置默认为block线程
        :return: 请求处理之后的状态码
        """
        def reciveTimeout(client):
            print("timeout so close the client and raise a connect Exception to close server client")
            client.close()
            return self.ERROR

        if not self.socketThread:
            return ERROR
        client = self.__createSocet(timeout)  # 创建一个clientsocket，并设置超时状态
        client.connect((self.__host, self.__port))  # 连接到server
        try:
            client.recv(self.__recvsize)  # 接受从server端发来的已准备好的信号
            print("server state is no problem ready to recive message")
            client.sendall(requestMessage.encode("utf-8"))  # 发送请求
            print("has been send message")
            if block:
                return OK
            return client.recv(self.__recvsize)  # 接受处理后的信号

        except Exception as e:
            print(e)
            return reciveTimeout(client)

