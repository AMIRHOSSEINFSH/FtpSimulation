import os
import socket
import time

import tqdm
from connection.BaseConnectionModel import BaseConnectionModel
from utility import DIS_ONNECTION_STATUS, FTP_CLIENT_STORAGE_PATH, FTP_SERVER_STORAGE_PATH, getDecoded, getEncoded


class ClientUploadConnectionModel(BaseConnectionModel):
    
    def __init__(self, server_ip_addr, server_port):
         super().__init__(server_ip_addr, server_port)
    
    def connect(self):
        server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        
            
        retry = 0
        while(retry < 5):
            try:
                server_socket.connect((self.server_ip_addr, self.server_port))
                print(f"Connected to IO server at {self.server_ip_addr}:{self.server_port}")
                break
            except Exception as e:
                time.sleep(1)
                print("ReConnecting ...\n")
                retry+=1
            
        file_name =getDecoded(server_socket.recv(1024))
        file_size = getDecoded(server_socket.recv(1024),False)
        base = os.path.basename(file_name)
        file = open(FTP_SERVER_STORAGE_PATH+base,"wb")
        file_bytes = b""
        done = False
        progress = tqdm.tqdm(unit="B", unit_scale= True, unit_divisor=1000,total=int(file_size))
        while not done:
            data = server_socket.recv(1024)
            if data == getEncoded(DIS_ONNECTION_STATUS):
                print(done)
                done = True
            else: 
                file_bytes+=data
            progress.update(1024)
        print("\nFile Uploaded Successfully!!\n")
        file.write(file_bytes)
        file.close()