"""
author:xinyuyu
email:1625282782@qq.com
time:2020-06-13
env:python3.6
socket and Process exercise
"""
from socket import *
from multiprocessing import Process

HOST = "0.0.0.0"
PORT = 8000
ADDR = (HOST, PORT)
dict_user = {}


def do_login(sock, name, addr):
    if name in dict_user or "管理" in dict_user:
        sock.sendto(b"feil", addr)
        return
    else:
        sock.sendto(b"OK", addr)
        mag = "欢迎%s进入聊天室" % name
        for info in dict_user:
            sock.sendto(mag.encode(), dict_user[info])
        dict_user[name] = addr
        # print(dict_user)


def do_chat(sock, name, data):
    info = "%s:%s" % (name, data)
    for item in dict_user:
        if item != name:
            sock.sendto(info.encode(), dict_user[item])


def do_quit(sock, name):
    del dict_user[name]
    mag = name + "已退出聊天室"
    for info in dict_user:
        sock.sendto(mag.encode(), dict_user[info])


def do_request(sock):
    while True:
        data, addr = sock.recvfrom(1024)
        sp = data.decode().split(" ", 2)
        if sp[0] == "L":
            do_login(sock, sp[1], addr)
        if sp[0] == "C":
            do_chat(sock, sp[1], sp[2])
        if sp[0] == "Q":
            do_quit(sock, sp[1])


def main():
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind(ADDR)
    p = Process(target=do_request, args=(sock,))
    p.daemon = True
    p.start()
    while True:
        content = input("管理员消息：")
        if content == "quit":
            break
        msg = "C 管理员消息 " + content
        sock.sendto(msg.encode(), ("127.0.0.1", 8000))



if __name__ == '__main__':
    main()
