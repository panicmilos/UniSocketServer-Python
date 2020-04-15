from ctypes import *
import os
from lib.SocketDLL import SocketDLL
from lib.Socket import Socket

CB_F_TYPE = CFUNCTYPE(c_int, c_void_p)

dll_path = os.path.abspath(__file__)
dll_path = os.path.realpath(dll_path)
dll_path = os.path.dirname(dll_path)

os.environ['PATH'] = dll_path + ";" + os.environ['PATH']


class ServerDLL(object):

    def __init__(self, port: int):
        super().__init__()
        self._on_new_client = CB_F_TYPE(self._on_new_client_cb)
        self._ServerDLL = cdll.LoadLibrary("UniSocketServer.dll")
        self._server = self._ServerDLL.server(port, self._on_new_client)
        self._port = port
        self._on_connection_cb = None

    def listen(self):
        self._ServerDLL.start_listening(self._server)

    def set_on_connection_cb(self, cb):
        self._on_connection_cb = cb

    def _on_new_client_cb(self, session_ptr):
        socket = SocketDLL(self._ServerDLL)
        socket_ptr = self._ServerDLL.new_socket(session_ptr, socket.get_data_callback())
        socket.set_socket(socket_ptr)
        if self._on_connection_cb:
            self._on_connection_cb(Socket(socket))
        return 0
