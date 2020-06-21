"""
author:xinyuyu
email:1625282782@qq.com
time:2020-06-13
env:python3.6
socket and Process exercise
"""
import os
import sys
from socket import *
from threading import Thread
import time

# 全局变量
HOST = "0.0.0.0"
PORT = 8005
ADDR = (HOST, PORT)

FTP = "/home/tarena/day05/"


class FTPServer(Thread):
    def __init__(self, connfd):
        self.connfd = connfd
        super().__init__()

    def do_list(self):
        list_file = os.listdir(FTP)
        if not list_file:
            self.connfd.send(b"Fail")
            return
        else:
            self.connfd.send(b"OK")
            time.sleep(0.1)
            data = "\n".join(list_file)
            self.connfd.send(data.encode())
            time.sleep(0.1)
            self.connfd.send(b"##")

    def do_get(self, filename):
        name = filename.split("/")[-1]
        result = os.path.exists(FTP + name)
        if result:
            self.connfd.send(b"OK")
            while True:
                f = open(FTP + filename, "rb")
                content = f.read(1024*1024*10)
                if not content:
                    break
                time.sleep(0.1)
                self.connfd.send(content)
                time.sleep(0.1)
                self.connfd.send(b"##")

        else:
            self.connfd.send(b"Fail")

    def do_put(self,filename):
        if os.path.exists(FTP+filename):
            self.connfd.send(b"Fail")
            return

        else:
            self.connfd.send(b"OK")
            f=open(FTP+filename,"wb")
            while True:
                content=self.connfd.handle(1024 * 1024 * 10)
                if content==b"##":
                    break
                f.write(content)
            f.close()



    def run(self):
        while True:
            data = self.connfd.handle(1024).decode()
            sp = data.split(" ")
            if data == "EXIT" or not data:
                self.connfd.close()
                return
            elif data == "LIST":
                self.do_list()
            elif sp[0] == "GET":
                self.do_get(sp[1])
            elif data[:3]=="PUT":
                filename=data.split(" ")[-1]
                self.do_put(filename)



def main():
    s = socket()
    s.bind(ADDR)
    s.listen()

    while True:
        try:
            connfd, addr = s.accept()
            print("客户端地址", addr)
        except KeyboardInterrupt as e:
            s.close()
            sys.exit("服务端退出")

        f = FTPServer(connfd)
        f.start()


if __name__ == '__main__':
    main()
