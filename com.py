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
            ServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1024*1024)
            ServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024*1024)

        elif self.Type == 2:
            ServerSocket = socket.socket(family= socket.AF_INET, type=socket.SOCK_STREAM)
            ServerSocket.bind((self.Ip, self.Port))
            ServerSocket.listen()
        return ServerSocket
    
    def CreateClient(self):
        if self.Type == 1:
            ClientSocket = socket.socket(family= socket.AF_INET, type=socket.SOCK_DGRAM)
            ClientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1024*1024)
            ClientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024*1024)
        elif self.Type == 2:
            ClientSocket = socket.socket(family= socket.AF_INET, type=socket.SOCK_STREAM)
            ClientSocket.connect((self.Ip, self.Port))
        return ClientSocket
    
    def Rec_Message(self):
        if self.Type == 1:
            Addresspair = self.CreateServer().recvfrom(1024)
            data = Addresspair[0]
            Recv_Data = data.decode() 
        elif self.Type == 2:
            conn, addr = self.CreateServer().accept()
            data = conn.recv(1024)
            Recv_Data = data.decode()
        self.CreateServer().close()
        return Recv_Data
    
    def Send_Message(self, data):
        if self.Type == 1:
            self.CreateClient().sendto(str(data).encode(), (self.Ip,self.Port))
        elif self.Type == 2:
            self.CreateClient().send(str(data).encode())
        
