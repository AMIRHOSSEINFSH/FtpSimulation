from enum import Enum
import os

DIS_ONNECTION_STATUS = "<END>"
FTP_SERVER_STORAGE_PATH = "G:/Courses/Network/FtpSimulation/ftpServer/storage/"
FTP_CLIENT_STORAGE_PATH = "G:/Courses/Network/FtpSimulation/ftpClient/storage/"
server_ip = "127.0.0.1"
default_command_port = 2121
default_io_port = 2222
INVALID_PATH_STATUS = 1001
class COMMAND_NAME(Enum):
    UPLOAD = b"Upload";
    DOWNLOAD= b"Download";
    DELETE = b"Delete";
    HELP = b"Help";
    PWD = b"Pwd";
    LIST = b"List";
    NONE = b"";
                       
    
class PATH_STATUS(Enum) :
    IS_FILE = 1;
    IS_DIRECTORY = 2;
    JUST_EXIST = 0;

class DataCommand():
    def __init__(self, name: COMMAND_NAME, data: str):
        self.name = name
        self.data = data


def get_files_and_sizes(directory_path):
    output: str = "";
    
    for filename in os.listdir(directory_path):
        filepath = os.path.join(directory_path, filename)

        if os.path.isfile(filepath):
            file_size = os.path.getsize(filepath)
            output += (filename+" "+ str(file_size) + "\n")

    return output

def replace_first_n_chars(original_string: str, new_chars: str, n: int):
    if n <= 0:
        return original_string  # Nothing to replace

    replaced_string = new_chars + original_string[n:]
    return replaced_string

def checkIfPathValid(path: str,status: PATH_STATUS): 
    if status == PATH_STATUS.IS_FILE:
        return os.path.isfile(path)
    elif status == PATH_STATUS.IS_DIRECTORY:
        return os.path.isdir(path)
    else: 
        return os.path.exists(path)

def getCommandName(inputCommand: str):
        
        for command in COMMAND_NAME:
            if (command.value.decode("utf-8") == inputCommand and (command.value in [COMMAND_NAME.HELP.value, COMMAND_NAME.LIST.value,COMMAND_NAME.PWD.value]) or 
                inputCommand.startswith(command.value.decode("utf-8")) and len(replace_first_n_chars(command.value.decode("utf-8"),FTP_SERVER_STORAGE_PATH,len(command.value)+1).strip()) != 0
                ) :
                return command
            
        return COMMAND_NAME.NONE

def check_command_match(input_command):
    return getCommandName(input_command) != COMMAND_NAME.NONE
    
def getEncoded(data: str,utfEncoding: bool = True):
    if utfEncoding:
         return data.encode("utf-8")
    else: 
         return data.encode()
     
def getDecoded(data: bytearray, utfEncoding = True):
    if utfEncoding:
         return data.decode("utf-8")
    else: 
         return data.decode()
    
