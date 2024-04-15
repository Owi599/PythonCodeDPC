import socket


class UDP:
    def __init__(self, IP, PORT):
        self.UDP_IP = IP
        self.UDP_PORT = PORT
        
    def CreateServer(self):
        UDPServerSocket = socket.socket(family= socket.AF_INET, type=socket.SOCK_DGRAM)
        UDPServerSocket.bind((self.UDP_IP, self.UDP_PORT))
        return UDPServerSocket
    
    def CreateClient(self):
        UDPClientSocket = socket.socket(family= socket.AF_INET, type=socket.SOCK_DGRAM)
        return UDPClientSocket
    
    def Rec_Message(self):
        AddressPair = self.CreateServer().recvfrom(1024)
        data = AddressPair[0]
        address = AddressPair[1]
        
        Recv_Data = float(data.decode())
        
        return Recv_Data ,address
    
    def Send_Message(self, data):
        
        self.CreateClient().sendto(str(data).encode(), (self.UDP_IP,self.UDP_PORT))
        
