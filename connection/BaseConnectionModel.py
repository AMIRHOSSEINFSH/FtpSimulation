# base_connection_model.py

from abc import ABC, abstractmethod
from utility import COMMAND_NAME, DataCommand, server_ip, default_io_port

class BaseConnectionModel(ABC):
    def __init__(self, server_ip_addr, server_port):
        self.server_ip_addr = server_ip_addr
        self.server_port = server_port

    @abstractmethod
    def connect(self):
        pass

def provideConnectionModel(isClient: bool, server_ip_addr=server_ip, server_port=default_io_port, commandData: DataCommand = None):
    # do not forget commandData when wanting a client object!
    if isClient and commandData is None:
        return None
    
    if commandData.name == COMMAND_NAME.DOWNLOAD:
        if isClient:
            from connection.downloadModel.ClientDownloadConnectionModel import ClientDownloadConnectionModel
            return ClientDownloadConnectionModel(server_ip_addr, server_port)
        else:
            from connection.downloadModel.ServerDownloadConnectionModel import ServerDownloadConnectionModel
            return ServerDownloadConnectionModel(server_ip_addr, server_port, commandData)
    elif commandData.name == COMMAND_NAME.UPLOAD: 
        if isClient:
            from connection.uploadModel.ClientUploadConnectionModel import ClientUploadConnectionModel
            return ClientUploadConnectionModel(server_ip_addr, server_port)
        else:
            from connection.uploadModel.ServerUploadConnectionModel import ServerUploadConnectionModel
            return ServerUploadConnectionModel(server_ip_addr, server_port, commandData)
    elif commandData.name == COMMAND_NAME.DELETE:
        if isClient:
            from connection.deleteModel.ClientDeleteConnectionModel import ClientDeleteConnectionModel
            return ClientDeleteConnectionModel(server_ip_addr, server_port)
        else:
            from connection.deleteModel.ServerDeleteConnectionModel import ServerDeleteConnectionModel
            return ServerDeleteConnectionModel(server_ip_addr, server_port, commandData)
        
    return None
