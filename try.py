from com import COM

UDP = 1
Client = "10.0.8.55"
Port = 5000

udpSend = COM(Client,Port,UDP)
while True:
    udpSend.Send_Message(1)