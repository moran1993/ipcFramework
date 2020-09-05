class IpException(Exception):
    def __init__(self,ip=None,port=None):
        self.ip = ip
        self.port = port

    def __str__(self):
        if self.ip:
            return f"{self.__class__.__name__}:{self.ip} is not a corrct ip address please change it"
        if self.port and self.port > 65535:
            return f"{self.__class__.__name__}:port {self.port} is too large"
        return f"{self.__class__.__name__}:port {self.port} is smaller than 1024"

