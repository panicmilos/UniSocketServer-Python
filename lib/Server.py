from ctypes import *
import os

CB_F_TYPE = CFUNCTYPE(c_int, c_void_p)

class Server(object):

    def __init__(self, port: int):
        super().__init__()
        self._on_new_client = CB_F_TYPE(self._on_new_client_cb)
        self._ServerDLL = cdll.LoadLibrary(os.path.join(os.path.abspath(os.path.dirname(__file__)), "../dll/UniSocketServerPython.dll"))
        self._server = self._ServerDLL.server(port, self._on_new_client)
        self._port = port

    def listen(self):
        self._ServerDLL.start_listening(self._server)

    def _on_new_client_cb(self, socket):
        print("Socket: ", socket)
        return 0
