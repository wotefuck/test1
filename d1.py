import socket
import threading


class HTMLSERVER:

    def __init__(self):
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        self.tcp_socket.bind(("192.168.204.83", 8888))
        self.tcp_socket.listen(128)

    def client(self, conn):
        data = conn.recv(1024).decode()
        print(data)

        resource_data = data.split(" ")

        if len(resource_data) == 1:
            conn.close()
            return

        resource_dict = resource_data[1]

        if resource_dict == "/":
            resource_dict = "/index.html"

        try:
            with open(r"E:\pc\a\test" + resource_dict, "rb") as f:
                file_data = f.read()

        except Exception as e:
            response_line = "HTTP/1.1 404 Not Found\r\n"
            response_head = "Server:pwd\r\n"
            response_body = open(r"E:\pc\a\test\404 Not Found.html", "rb").read()
            response_data = (response_line + response_head + "\r\n").encode() + response_body
            conn.send(response_data)

        else:
            response_line = "HTTP/1.1 200 ok\r\n"
            response_head = "Server:pwd\r\n"
            response_body = file_data
            response_data = (response_line + response_head + "\r\n").encode() + response_body
            conn.send(response_data)

        finally:
            conn.close()

    def start(self):
        while True:
            conn, address = self.tcp_socket.accept()
            server_thread = threading.Thread(target=self.client, args=(conn,))
            server_thread.start()


if __name__ == '__main__':
    result = HTMLSERVER()
    result.start()
