
import socket
import time
from pubsub import pub


from connection.BaseConnectionModel import BaseConnectionModel
from utility import FTP_CLIENT_MESSAGE_TOPIC


class ClientDeleteConnectionModel(BaseConnectionModel):
    
    def __init__(self, server_ip_addr, server_port):
         super().__init__(server_ip_addr, server_port)
    
    def connect(self):
        server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        
        retry = 0
        while(retry < 5):
            try:
                server_socket.connect((self.server_ip_addr, self.server_port))
                print(f"Connected to IO server at {self.server_ip_addr}:{self.server_port}")
                pub.sendMessage(topicName= FTP_CLIENT_MESSAGE_TOPIC,data=f"Connected to IO server at {self.server_ip_addr}:{self.server_port}")
                break
            except Exception as e:
                time.sleep(1)
                print("ReConnecting ...\n")
                pub.sendMessage(topicName= FTP_CLIENT_MESSAGE_TOPIC,data="ReConnecting ...\n")
                retry+=1
                
        message = server_socket.recv(1024)
        print(message)
        pub.sendMessage(topicName= FTP_CLIENT_MESSAGE_TOPIC,data=message)
        server_socket.close()
        
