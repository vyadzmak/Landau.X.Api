from socketIO_client import SocketIO, LoggingNamespace
import modules.log_helper_module as log_module
from settings import SOCKET_URL

def emit(type, data):
    try:
        with SocketIO(SOCKET_URL, 8000, LoggingNamespace, wait_for_connection=False) as socketIO:
            socketIO.emit(type, data)
            socketIO.wait(seconds=0)
    except Exception as e:
        log_module.add_log("Socket emit error on "+ type + ": " + str(e))