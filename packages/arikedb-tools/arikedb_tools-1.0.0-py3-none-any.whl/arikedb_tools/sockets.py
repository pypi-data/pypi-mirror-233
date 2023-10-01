from queue import Queue, Empty
from socket import socket
from threading import Thread
from typing import Union, Tuple, Iterable, Optional


class Socket:

    prefix_delimiter = "!@#$%^&*(34)12<<"
    suffix_delimiter = ">>+_)(*90%$#@%42"

    def __init__(self, sock: socket):

        self._msg_stack = Queue()
        self._connected = False
        self._thread = None
        self._socket = sock

    def socket_send(self, msg: Union[str, bytes, bytearray]):

        if isinstance(msg, (bytes, bytearray)):
            msg = msg.decode()

        msg = f"{self.prefix_delimiter}{msg}{self.suffix_delimiter}"

        try:
            self._socket.sendall(msg.encode())
        except Exception as err:
            _ = err

    def start(self, chunk_size: int = 1024):

        self._connected = True
        pref = self.prefix_delimiter
        suf = self.suffix_delimiter

        def wrapper():
            stream = ""
            while self._connected:
                try:
                    chunk = self._socket.recv(chunk_size).decode()
                    if not chunk:
                        self._connected = False
                        break
                    else:
                        stream += chunk
                except Exception as err:
                    _ = err
                    self._connected = False
                    break
                messages, stream = Socket.str_split(stream, pref, suf)
                for msg in messages:
                    self._msg_stack.put(msg)

        self._thread = Thread(target=wrapper, daemon=True)
        self._thread.start()

    def messages(self) -> Iterable:
        while self.running:
            try:
                yield self._msg_stack.get(timeout=2)
            except Empty:
                continue

    def join(self, timeout: Optional[float] = None):
        if isinstance(self._thread, Thread):
            return self._thread.join(timeout)

    def connect(self, __address: tuple):
        return self._socket.connect(__address)

    def bind(self, __address: tuple):
        return self._socket.bind(__address)

    def listen(self, __backlog: int):
        return self._socket.listen(__backlog)

    def accept(self):
        return self._socket.accept()

    def close(self):
        self._connected = False
        return self._socket.close()

    def shutdown(self, __how: int):
        self._connected = False
        return self._socket.shutdown(__how)

    def setsockopt(self, __level: int, __optname: int,
                   __value: Union[int, bytes]):
        return self._socket.setsockopt(__level, __optname, __value)

    @staticmethod
    def str_split(string: str, prefix, suffix) -> Tuple[list, str]:
        sl = len(suffix)
        pl = len(prefix)
        messages = []
        remain = string
        while True:
            msg_start = remain.find(prefix)
            msg_end = remain.find(suffix)
            if msg_start != -1 and msg_end != -1:
                msg_str = remain[(msg_start + pl):msg_end]
                messages.append(msg_str)
                remain = remain[(msg_end + sl):]
            else:
                break
        return messages, remain

    @property
    def running(self):
        if isinstance(self._thread, Thread):
            return self._connected or self._thread.is_alive()
        else:
            return False
