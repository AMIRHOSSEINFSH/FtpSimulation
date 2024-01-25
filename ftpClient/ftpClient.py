import sys
import os
import socket

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from connection.BaseConnectionModel import  provideConnectionModel



from utility import COMMAND_NAME, FTP_CLIENT_STORAGE_PATH, FTP_SERVER_STORAGE_PATH, INVALID_PATH_STATUS, DataCommand, replace_first_n_chars,server_ip,default_command_port,default_io_port, check_command_match,getEncoded,getDecoded,getCommandName

def main():

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, default_command_port))

    print(f"Connected to server at {server_ip}:{default_command_port}")

    while True:
        message = input("Enter message: ")
        if check_command_match(message): 
            
            client_socket.send(getEncoded(message))
            #geting Data ...
            response = client_socket.recv(1024)
            if len(response) >=1 and getDecoded(response) != str(INVALID_PATH_STATUS):
                print(f"\nServer response: {getDecoded(response)}\n")
                if   getCommandName(message) in [COMMAND_NAME.DOWNLOAD,COMMAND_NAME.DELETE,COMMAND_NAME.UPLOAD]:
                        path= replace_first_n_chars(message,FTP_CLIENT_STORAGE_PATH,len(COMMAND_NAME.UPLOAD.value)+1)
                        openIoConnection(getCommandName(message),path)
        else: 
            print("\nYour Command Does not Supported!!\n")
            

        if message.lower() == "exit":
            break

    client_socket.close()

def openIoConnection(command: COMMAND_NAME,path: str): 
            
    dataCommand: DataCommand = DataCommand(COMMAND_NAME.UPLOAD,path)
    if command != COMMAND_NAME.UPLOAD: dataCommand = DataCommand(command,path)
    
    
    provideConnectionModel(command != COMMAND_NAME.UPLOAD,commandData=dataCommand).connect()
    
if __name__ == "__main__":
    main()
