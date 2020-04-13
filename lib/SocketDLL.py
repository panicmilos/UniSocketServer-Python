from ctypes import *
import json

CB_DATA_TYPE = CFUNCTYPE(c_int, c_char_p)


class SocketDLL(object):

    def __init__(self, server_dll):
        super().__init__()
        self._ServerDLL = server_dll
        self.on_data = CB_DATA_TYPE(self._on_data_cb)
        self._session_ptr = None
        self._receivers = ""
        self._num_of_receivers = 0
        self._event_handlers = {}

    def set_socket(self, session_ptr):
        self._session_ptr = session_ptr

    def disconnect(self):
        self._ServerDLL.disconnect(self._session_ptr)

    def on(self, event_name, handler):
        self._event_handlers[event_name] = handler

    def to(self, client_name: str):
        self._num_of_receivers += 1
        self._receivers += client_name if self._receivers == "" else "," + client_name
        return self

    def to_clients(self, client_names: list):
        self._num_of_receivers += len(client_names)
        for client_name in client_names:
            self._receivers += client_name if self._receivers == "" else "," + client_name
        return self

    def emit(self, event_name: str, data):
        data_dict = {"event_name": event_name, "data": data}
        data_json_string = json.dumps(data_dict)

        if self._num_of_receivers == 1:
            self._send_to_client(data_json_string)

        elif self._num_of_receivers == 0:
            self._broadcast(data_json_string)

        else:
            self._send_to_clients(data_json_string)

        self._reset_receivers()

    def _send_to_client(self, data: str):
        self._ServerDLL.send_to_client(self._session_ptr, bytes(self._receivers, 'utf-8'), bytes(data, 'utf-8'))

    def _send_to_clients(self, data: str):
        self._ServerDLL.send_to_clients(self._session_ptr, bytes(self._receivers, 'utf-8'), bytes(data, 'utf-8'))

    def _broadcast(self, data):
        self._ServerDLL.broadcast(self._session_ptr, bytes(data, 'utf-8'))

    def _reset_receivers(self):
        self._receivers = ""
        self._num_of_receivers = 0

    def _on_data_cb(self, data):
        data_string = data.decode("utf-8")
        try:
            data_dict = json.loads(data_string)
            event_name = data_dict["event_name"]
            data = data_dict["data"]
            handler = self._event_handlers[event_name]
            handler(data)
        except Exception as e:
            print("Invalid JSON format in: " + data_string)
            print(e)
        return 0
