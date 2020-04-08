from ctypes import *
import os


class Server(object):

    def __init__(self, port: int):
        super().__init__()
        self._ServerDLL = cdll.LoadLibrary(os.path.normpath(os.getcwd() + os.sep + os.pardir) + R'\dll\UniSocketServerPython.dll')
        self._server = self._ServerDLL.server(port)
        self._port = port

    def listen(self):
        self._ServerDLL.start_listening(self._server)
