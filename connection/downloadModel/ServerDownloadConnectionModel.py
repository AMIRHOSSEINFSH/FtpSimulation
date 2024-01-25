import os
import socket
import time

import tqdm
from connection.BaseConnectionModel import BaseConnectionModel
from utility import DIS_ONNECTION_STATUS, FTP_CLIENT_STORAGE_PATH, DataCommand, getDecoded, getEncoded


class ServerDownloadConnectionModel(BaseConnectionModel):
    
    def __init__(self, server_ip_addr, server_port,commandData: DataCommand):
         super().__init__(server_ip_addr, server_port)
         self.commandData = commandData
    
    def connect(self):
        #Server impl
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.server_ip_addr, self.server_port))
        server_socket.listen()

        print(f"Server is listening on {self.server_ip_addr}:{self.server_port} for {self.commandData.name.value} file: {self.commandData.data}")

        client_socket, client_address = server_socket.accept()
        print(f"IO Executation is Executing for Port {client_address}")
        
        file = open(self.commandData.data, "rb")
        
        file_size = os.path.getsize(self.commandData.data)
            # Send file Data Info
            
        client_socket.send(getEncoded(file.name))
        time.sleep(1)
        
        client_socket.send(getEncoded(str(file_size),False))
        file_content = file.read()
        print("File Content is "+getDecoded(file_content))
        client_socket.sendall(file_content)
        time.sleep(1)
        client_socket.send(getEncoded(DIS_ONNECTION_STATUS))
        
        file.close()
        client_socket.close()
        server_socket.close()