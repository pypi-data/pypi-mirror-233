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
        data += mock_sock_queue.get()
    return data.encode()


def clean_queue():
    while mock_sock_queue.qsize():
        mock_sock_queue.get()


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
            b"First string ",
            b"Second string ",
            b"Other string ",
            b"",
            b"Very very very very very very large",
        ]

        messages, remain = Socket.str_split(string.encode(), prefx.encode(),
                                            suffx.encode())

        self.assertListEqual(messages, expected_msgs)
        self.assertEqual(remain, f"{prefx}Incomplete string".encode())

    def test_str_split_empty(self):

        prefx = "123qwe"
        suffx = "09le"

        string = f"{prefx}Incomplete string"

        expected_msgs = []

        messages, remain = Socket.str_split(string.encode(), prefx.encode(),
                                            suffx.encode())

        self.assertListEqual(messages, expected_msgs)
        self.assertEqual(remain, f"{prefx}Incomplete string".encode())

    @patch.object(socket.socket, "__init__", mock_init)
    @patch.object(socket.socket, "sendall", mock_sendall)
    @patch.object(socket.socket, "recv", mock_recv)
    def test_socket_send(self):
        clean_queue()

        sock = Socket(socket.socket())
        sock.send(b"First message")
        sock.send(b"Second message")
        sock.send(b"Other message")

        pref = Socket.prefix.decode()
        suf = Socket.suffix.decode()

        expected_stream = f"{pref}First message{suf}" \
                          f"{pref}Second message{suf}" \
                          f"{pref}Other message{suf}"

        stream = ""
        while not mock_sock_queue.empty():
            stream += mock_sock_queue.get()

        self.assertEqual(stream, expected_stream)

    def test_socket_receive(self):
        clean_queue()

        client_sockets = []

        server = Socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.socket.bind(("localhost", 8001))
        server.socket.listen(1)

        def server_acp():
            client_socket, addr = server.socket.accept()
            client_sockets.append(Socket(client_socket))

        t = Thread(target=server_acp, daemon=True)
        t.start()

        cli = Socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        cli.socket.connect(("localhost", 8001))

        def sender():
            for i in range(12):
                cli.send(f"Message number {i}. Ok")

        while not client_sockets:
            pass

        client_sock = client_sockets[0]

        t2 = Thread(target=sender, daemon=True)
        t2.start()

        x = 0
        for msg in client_sock.receive(1024, 4):
            self.assertEqual(msg, f"Message number {x}. Ok".encode())
            x += 1

        for msg in client_sock.receive(1, 4):
            self.assertEqual(msg, f"Message number {x}. Ok".encode())
            x += 1

        for msg in client_sock.receive(5, 4):
            self.assertEqual(msg, f"Message number {x}. Ok".encode())
            x += 1

        server.socket.close()
        client_sockets[0].socket.close()
        cli.socket.close()

        t.join(timeout=2)

    def test_socket_receive_n(self):
        clean_queue()

        client_sockets = []

        server = Socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.socket.bind(("localhost", 8001))
        server.socket.listen(1)

        def server_acp():
            client_socket, addr = server.socket.accept()
            client_sockets.append(Socket(client_socket))

        t = Thread(target=server_acp, daemon=True)
        t.start()

        cli = Socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        cli.socket.connect(("localhost", 8001))

        def sender():
            for i in range(12):
                cli.send(f"Message number {i}. Ok")

        while not client_sockets:
            pass

        client_sock = client_sockets[0]

        t2 = Thread(target=sender, daemon=True)
        t2.start()

        expected_output_1 = [
            f"Message number {i}. Ok".encode() for i in range(4)
        ]

        expected_output_2 = [
            f"Message number {i + 4}. Ok".encode() for i in range(8)
        ]

        output1 = client_sock.receive_n(4, 4)
        output2 = client_sock.receive_n(1024, 8)

        self.assertListEqual(output1, expected_output_1)
        self.assertListEqual(output2, expected_output_2)

        server.socket.close()
        client_sockets[0].socket.close()
        cli.socket.close()

        t.join(timeout=2)


if __name__ == '__main__':
    unittest.main()
