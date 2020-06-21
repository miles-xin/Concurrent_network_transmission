import os
import sys
from socket import *
import time


class FTPClient():
    def __init__(self, sock):
        self.sock = sock

    def do_list(self):
        self.sock.send(b"LIST")
        data = self.sock.handle(1024).decode()
        if data == "OK":
            while True:
                file_list = self.sock.handle(1024).decode()
                if file_list == "##":
                    break
                print(file_list)
        else:
            print("文件为空")

    def do_get(self, filename):
        file_name = "GET " + filename
        self.sock.send(file_name.encode())
        data = self.sock.handle(1024).decode()
        if data == "OK":
            f = open(filename, "wb")
            while True:
                info = self.sock.handle(1024 * 1024 * 10)
                if info == b"##":
                    break
                f.write(info)
            f.close()
        else:
            print("未找到该文件")

    def do_put(self, file):
        try:
            f = open(file, "rb")
        except:
            print("文件不存在")
            return
        name = file.split("/")[-1]
        data = "PUT" + name
        self.sock.send(data.encode())
        result = self.sock.handle(1024).decode()
        if result == "OK":
            while True:
                content = f.read(1024 * 1024 * 10)
                if not content:
                    time.sleep(0.1)
                    self.sock.send(b"##")
                    break
                self.sock.send(content)
            f.close()
        else:
            print("该文件存在")

    def do_quit(self):
        self.sock.send(b"EXIT")
        self.sock.close()
        sys.exit("谢谢使用")


def main():
    # 创建tcp套接字
    tcp_socket = socket()

    tcp_socket.connect(("127.0.0.1", 8005))

    f = FTPClient(tcp_socket)  # 实例化对象
    while True:
        print("=========== 命令选项 =============")
        print("***          list           ***")
        print("***        get file         ***")
        print("***        put file         ***")
        print("***          quit           ***")
        print("=================================")

        msg = input("请输入命令：")

        if msg == "list":
            f.do_list()
        elif msg[:3] == "get":
            filename = msg.split(" ")[-1]
            f.do_get(filename)
        elif msg[:3] == "put":
            file = msg.split(" ")[-1]
            f.do_put(file)
        elif msg == "quit":
            f.do_quit()
        else:
            print("输入不正确,请重新输入")


if __name__ == '__main__':
    main()
