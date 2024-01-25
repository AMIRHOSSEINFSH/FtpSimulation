import sys
import os
import socket
import time
from pubsub import pub

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from connection.BaseConnectionModel import  provideConnectionModel



from utility import COMMAND_NAME, FTP_CLIENT_MESSAGE_TOPIC, FTP_CLIENT_STORAGE_PATH, FTP_SERVER_STORAGE_PATH, INVALID_PATH_STATUS, DataCommand, replace_first_n_chars,server_ip,default_command_port,default_io_port, check_command_match,getEncoded,getDecoded,getCommandName

def connectClient(retry: int = 1):
    while(retry > 0):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((server_ip, default_command_port))
            pub.sendMessage(topicName= FTP_CLIENT_MESSAGE_TOPIC,data=f"Connected to server at {server_ip}:{default_command_port}")
            return client_socket
        except:
            pub.sendMessage(topicName=FTP_CLIENT_MESSAGE_TOPIC, data=f"retry Connect to {server_ip}:{default_command_port}")
            time.sleep(2)
            retry-=1
            
    pub.sendMessage(topicName= FTP_CLIENT_MESSAGE_TOPIC,data=f"Unable Connect to {server_ip}:{default_command_port}")
    return None
            
def startPushCommands(client_socket: any,message):
    if client_socket != None:
            if message.lower() == "exit":
                client_socket.close()
                return
            if check_command_match(message): 

                client_socket.send(getEncoded(message))
                #geting Data ...
                response = client_socket.recv(1024)
                if getDecoded(response) == str(INVALID_PATH_STATUS):
                    pub.sendMessage(topicName=FTP_CLIENT_MESSAGE_TOPIC,data="\nYour File Does not exists in Server Storage!!\n")
                if len(response) >=1 and getDecoded(response) != str(INVALID_PATH_STATUS):
                    pub.sendMessage(topicName= FTP_CLIENT_MESSAGE_TOPIC,data=f"\nServer response: {getDecoded(response)}\n")
                    if   getCommandName(message) in [COMMAND_NAME.DOWNLOAD,COMMAND_NAME.DELETE,COMMAND_NAME.UPLOAD]:
                            path= replace_first_n_chars(message,FTP_CLIENT_STORAGE_PATH,len(COMMAND_NAME.UPLOAD.value)+1)
                            openIoConnection(getCommandName(message),path)
            else: 
                pub.sendMessage(topicName= FTP_CLIENT_MESSAGE_TOPIC,data="\nYour Command Does not Supported!!\n")

            


def openIoConnection(command: COMMAND_NAME,path: str): 
    dataCommand: DataCommand = DataCommand(COMMAND_NAME.UPLOAD,path)
    if command != COMMAND_NAME.UPLOAD: dataCommand = DataCommand(command,path)
    
    
    provideConnectionModel(command != COMMAND_NAME.UPLOAD,commandData=dataCommand).connect()
    
if __name__ == "__main__":
    socket = connectClient()
    startPushCommands(socket,"Nothing")
