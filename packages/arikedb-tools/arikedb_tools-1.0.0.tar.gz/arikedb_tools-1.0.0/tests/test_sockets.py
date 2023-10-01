import unittest
from threading import Thread
from unittest.mock import patch
from queue import Queue
import socket

from arikedb_tools.sockets import Socket

mock_sock_queue = Queue()


def mock_init(*args, **kwargs):
    pass


def mock_sendall(self, data: bytes):
    _ = self
    for b in data.decode():
        mock_sock_queue.put(b)


def mock_recv(self, size):
    _ = self
    data = ""
    for _ in range(size):
        d = mock_sock_queue.get()
        data += d
    return data.encode()


class SocketToolsTests(unittest.TestCase):

    def test_str_split(self):

        prefx = "123qwe"
        suffx = "09le"

        string = f"{prefx}First string {suffx}" \
                 f"{prefx}Second string {suffx}" \
                 f"{prefx}Other string {suffx}" \
                 f"{prefx}{suffx}" \
                 f"{prefx}Very very very very very very large{suffx}" \
                 f"{prefx}Incomplete string"

        expected_msgs = [
            "First string ",
            "Second string ",
            "Other string ",
            "",
            "Very very very very very very large",
        ]

        messages, remain = Socket.str_split(string, prefx, suffx)

        self.assertListEqual(messages, expected_msgs)
        self.assertEqual(remain, f"{prefx}Incomplete string")

    def test_str_split_empty(self):

        prefx = "123qwe"
        suffx = "09le"

        string = f"{prefx}Incomplete string"

        expected_msgs = []

        messages, remain = Socket.str_split(string, prefx, suffx)

        self.assertListEqual(messages, expected_msgs)
        self.assertEqual(remain, f"{prefx}Incomplete string")

    @patch.object(socket.socket, "__init__", mock_init)
    @patch.object(socket.socket, "sendall", mock_sendall)
    @patch.object(socket.socket, "recv", mock_recv)
    def test_socket_send(self):

        sock = Socket(socket.socket())
        sock.socket_send(b"First message")
        sock.socket_send(b"Second message")
        sock.socket_send(b"Other message")

        pref = Socket.prefix_delimiter
        suf = Socket.suffix_delimiter

        expected_stream = f"{pref}First message{suf}" \
                          f"{pref}Second message{suf}" \
                          f"{pref}Other message{suf}"

        stream = ""
        while not mock_sock_queue.empty():
            stream += mock_sock_queue.get()

        self.assertEqual(stream, expected_stream)

    def test_socket_proc_chunk_size_1(self):
        client_sockets = []

        serv_sock = Socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        serv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serv_sock.bind(("localhost", 8001))
        serv_sock.listen(1)

        def server():
            client_socket, addr = serv_sock.accept()
            client_sockets.append(Socket(client_socket))

        t = Thread(target=server, daemon=True)
        t.start()

        cli_sock = Socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        cli_sock.connect(("localhost", 8001))

        def sender():
            for i in range(10):
                cli_sock.socket_send(f"Message number {i}. Ok")
            serv_sock.shutdown(0)
            client_sockets[0].shutdown(0)
            serv_sock.close()
            client_sockets[0].close()
            cli_sock.close()

        while not client_sockets:
            pass

        client_sock = client_sockets[0]

        client_sock.start(chunk_size=1)

        t2 = Thread(target=sender, daemon=True)
        t2.start()

        x = 0
        for msg in client_sock.messages():
            self.assertEqual(msg, f"Message number {x}. Ok")
            x += 1

        serv_sock.join(timeout=2)
        t.join(timeout=2)

    def test_socket_proc_chunk_size_13(self):
        client_sockets = []

        serv_sock = Socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        serv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serv_sock.bind(("localhost", 8001))
        serv_sock.listen(1)

        def server():
            client_socket, addr = serv_sock.accept()
            client_sockets.append(Socket(client_socket))

        t = Thread(target=server, daemon=True)
        t.start()

        cli_sock = Socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        cli_sock.connect(("localhost", 8001))

        def sender():
            for i in range(10):
                cli_sock.socket_send(f"Message number {i}. Ok" * 1000)
            serv_sock.shutdown(0)
            client_sockets[0].shutdown(0)
            serv_sock.close()
            client_sockets[0].close()
            cli_sock.close()

        while not client_sockets:
            pass

        client_sock = client_sockets[0]

        client_sock.start(chunk_size=13)

        t2 = Thread(target=sender, daemon=True)
        t2.start()

        x = 0
        for msg in client_sock.messages():
            self.assertEqual(msg, f"Message number {x}. Ok" * 1000)
            x += 1

        serv_sock.join(timeout=2)
        t.join(timeout=2)

    def test_socket_proc_chunk_size_1024(self):
        client_sockets = []

        serv_sock = Socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        serv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serv_sock.bind(("localhost", 8001))
        serv_sock.listen(1)

        def server():
            client_socket, addr = serv_sock.accept()
            client_sockets.append(Socket(client_socket))

        t = Thread(target=server, daemon=True)
        t.start()

        cli_sock = Socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        cli_sock.connect(("localhost", 8001))

        def sender():
            for i in range(10):
                cli_sock.socket_send(f"Message number {i}. Ok")
            serv_sock.shutdown(0)
            client_sockets[0].shutdown(0)
            serv_sock.close()
            client_sockets[0].close()
            cli_sock.close()

        while not client_sockets:
            pass

        client_sock = client_sockets[0]

        client_sock.start(chunk_size=13)

        t2 = Thread(target=sender, daemon=True)
        t2.start()

        x = 0
        for msg in client_sock.messages():
            self.assertEqual(msg, f"Message number {x}. Ok")
            x += 1

        serv_sock.join(timeout=2)
        t.join(timeout=2)


if __name__ == '__main__':
    unittest.main()
