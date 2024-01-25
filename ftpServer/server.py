import os
import socket
import sys

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from connection.BaseConnectionModel import provideConnectionModel


from utility import COMMAND_NAME, FTP_CLIENT_STORAGE_PATH, FTP_SERVER_STORAGE_PATH, INVALID_PATH_STATUS, PATH_STATUS, DataCommand,server_ip,default_command_port, get_files_and_sizes, replace_first_n_chars,checkIfPathValid,getEncoded,getDecoded


def main():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, default_command_port))
    server_socket.listen()

    print(f"Server listening on {server_ip}:{default_command_port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")

        handle_client(client_socket)

def handle_client(client_socket):
    while True:
        data = client_socket.recv(1024)
        
        result = handleCommand(data)
        
            
        if result.name in [COMMAND_NAME.HELP,COMMAND_NAME.PWD,COMMAND_NAME.LIST,COMMAND_NAME.NONE]:
                if result.name == COMMAND_NAME.LIST and not result.data.strip():
                    result.data = "\nServer Storage Directory is Empty!!"
                client_socket.send(getEncoded(result.data))
        else :
                if checkIfPathValid(result.data,PATH_STATUS.IS_FILE):
                    client_socket.send(getEncoded("Opening Connection on { default_io_port }"))
                    openIoConection(result)
                else: 
                    message = "\nThe Path: "+ result.data +" is InValid!!\n";
                    client_socket.send(getEncoded(str(INVALID_PATH_STATUS)))
                    print(message)
                
                
            
        if not data:
            break
            
        message = getDecoded(data)
        print(f"Received from {client_socket.getpeername()}: {message}")

    client_socket.close()
    print(f"Connection closed with {client_socket.getpeername()}")

def handleCommand(dataCommand: str) -> DataCommand:
    dataCommand = dataCommand.rstrip()

    if dataCommand == COMMAND_NAME.HELP.value:
        commandList = '\n'.join([member.name for member in COMMAND_NAME])
        data = f"List of Commands: \n{commandList}\n"
        name = COMMAND_NAME.HELP
    elif dataCommand == COMMAND_NAME.PWD.value:
        name = COMMAND_NAME.PWD
        data = os.getcwd()
    elif dataCommand == COMMAND_NAME.LIST.value:
        name = COMMAND_NAME.LIST
        data = get_files_and_sizes(FTP_SERVER_STORAGE_PATH)
    elif dataCommand.startswith(COMMAND_NAME.UPLOAD.value):
        name = COMMAND_NAME.UPLOAD
        data = replace_first_n_chars(getDecoded(dataCommand),FTP_CLIENT_STORAGE_PATH,len(name.value)+1)
    elif dataCommand.startswith(COMMAND_NAME.DOWNLOAD.value):
        name = COMMAND_NAME.DOWNLOAD
        data = replace_first_n_chars(getDecoded(dataCommand),FTP_SERVER_STORAGE_PATH,len(name.value)+1)
    elif dataCommand.startswith(COMMAND_NAME.DELETE.value):
        name = COMMAND_NAME.DELETE
        data = replace_first_n_chars(getDecoded(dataCommand),FTP_SERVER_STORAGE_PATH,len(name.value)+1)
    else:
        name = COMMAND_NAME.NONE;
        data = "Your Command is Invalid!!"

    return DataCommand(name, data)



def openIoConection(commandData: DataCommand):
    
    provideConnectionModel(commandData.name == COMMAND_NAME.UPLOAD,commandData=commandData).connect()
    

if __name__ == "__main__":
    main()
