import math
from queue import Queue
from socket import socket
from typing import Union, Tuple, Iterable, Optional


class Socket:

    prefix = b"!@#$%^&*(34)12<<"
    suffix = b">>+_)(*90%$#@%42"

    def __init__(self, sock: socket):

        self._msg_stack = Queue()
        self._connected = False
        self._thread = None
        self._socket = sock

    def send(self, msg: Union[str, bytes, bytearray]):

        if isinstance(msg, str):
            msg = msg.encode()

        msg = self.prefix + msg + self.suffix

        self._socket.sendall(msg)

    def receive(self, chunk_size: int = 1024, n_max_msg: int = 0,
                iter_timeout: Optional[float] = None) -> Iterable:
        stream = b""
        received = 0
        if n_max_msg <= 0:
            n_max_msg = math.inf
        if isinstance(iter_timeout, (float, int)):
            self._socket.settimeout(float(iter_timeout))
        while received < n_max_msg:
            try:
                sub_str = self._socket.recv(chunk_size)
                # If disconnected recv return None
                if not sub_str:
                    break
                stream += sub_str
            except TimeoutError:
                yield
                continue
            msgs, remain = Socket.str_split(stream, self.prefix, self.suffix)
            for msg in msgs:
                yield msg
            received += len(msgs)

            stream = remain

    def receive_n(self, chunk_size: int = 1024, n: int = 1) -> list:
        assert n >= 1
        return [msg for msg in self.receive(chunk_size, n)]

    @staticmethod
    def str_split(string: bytes, prefix: bytes,
                  suffix: bytes) -> Tuple[list, bytes]:
        sl = len(suffix)
        pl = len(prefix)
        messages = []
        remain = string
        while remain.find(suffix):
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
    def socket(self):
        return self._socket
