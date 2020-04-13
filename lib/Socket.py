from lib.SocketDLL import SocketDLL


class Socket(object):

    def __init__(self, socket_dll):
        super().__init__()
        self._socketDLL = socket_dll

    def disconnect(self):
        self._socketDLL.disconnect()

    def on(self, event_name, handler):
        self._socketDLL.on(event_name, handler)

    def to(self, client_name: str):
        return self._socketDLL.to(client_name)

    def to_clients(self, client_names: list):
        return self._socketDLL.to_clients(client_names)