from lib.ServerDLL import ServerDLL


class Server(object):

    def __init__(self, port: int):
        super().__init__()
        self._serverDLL = ServerDLL(port)

    def listen(self):
        self._serverDLL.listen()

    def on_connection(self, cb):
        self._serverDLL.set_on_connection_cb(cb)
