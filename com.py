import socket


class COM:
    def __init__(self, IP, PORT,TYPE):
        self.Ip = IP
        self.Port = PORT
        self.Type = TYPE
        
    def CreateServer(self):
        if self.Type == 1:
            ServerSocket = socket.socket(family= socket.AF_INET, type=socket.SOCK_DGRAM)
            ServerSocket.bind((self.Ip, self.Port))
        elif self.Type == 2:
            ServerSocket = socket.socket(family= socket.AF_INET, type=socket.SOCK_STREAM)
            ServerSocket.bind((self.Ip, self.Port))
            ServerSocket.listen()
        return ServerSocket
    
    def CreateClient(self):
        if self.Type == 1:
            ClientSocket = socket.socket(family= socket.AF_INET, type=socket.SOCK_DGRAM)
        elif self.Type == 2:
            ClientSocket = socket.socket(family= socket.AF_INET, type=socket.SOCK_STREAM)
            ClientSocket.connect((self.Ip, self.Port))
        return ClientSocket
    
    def Rec_Message(self):
        AddressPair = self.CreateServer().recvfrom(1024)
        data = AddressPair[0]
        
        
        Recv_Data = float(data.decode())
        return Recv_Data
    
    def Send_Message(self, data):
        
        self.CreateClient().sendto(str(data).encode(), (self.Ip,self.Port))
        
