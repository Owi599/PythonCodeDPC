import socket


class UDP:
    def __init__(self, IP, PORT):
        self.Ip = IP
        self.Port = PORT

    def CreateServer(self):
        ServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        ServerSocket.bind((self.Ip, self.Port))
        ServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1024 * 1024)
        ServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024 * 1024)
        return ServerSocket

    def CreateClient(self):
        ClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        ClientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1024 * 1024)
        ClientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024 * 1024)
        return ClientSocket

    def Rec_Message(self):
        Addresspair = self.CreateServer().recvfrom(1024)
        data = Addresspair[0]
        Recv_Data = data.decode()
        #self.CreateServer().close()
        return Recv_Data

    def Send_Message(self, data):
        self.CreateClient().sendto(str(data).encode(), (self.Ip, self.Port))
        

class TCP:
    def __init__(self, IP, PORT):
        self.Ip = IP
        self.Port = PORT

    def CreateServer(self):
        ServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        ServerSocket.bind((self.Ip, self.Port))
        ServerSocket.listen()

    def CreateClient(self):
        ClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        ClientSocket.connect((self.Ip, self.Port))
        return ClientSocket

    def Rec_Message(self):
        conn, addr = self.CreateServer().accept()
        data = conn.recv(1024)
        Recv_Data = data.decode()
        # self.CreateServer().close()
        return Recv_Data

    def Send_Message(self, data):
        self.CreateClient().send(str(data).encode())
