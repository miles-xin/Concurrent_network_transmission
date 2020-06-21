from socket import *
from multiprocessing import Process
import sys

HOST = "119.3.161.197"
PORT = 8000
ADDR = (HOST, PORT)


# 进入聊天室
def login(sock):
    while True:
        name = input("Name:")
        mag = "L " + name
        sock.sendto(mag.encode(), ADDR)

        data, addr = sock.recvfrom(1024)

        if data.decode() == "OK":
            print("已进入聊天室")
            return name
        else:
            print("输入的名字已存在,请重新输入")


# 接收消息
def getmessage(sock):
    while True:
        data, addr = sock.recvfrom(1024)
        msg="\n"+data.decode()+"\n发言："
        print(msg,end="")

# 发送消息
def sendmessage(sock, name):
    while True:
        try:
            content = input("发言：")
        except:
            content="quit"
        if content == "quit":
            mag = "Q " + name
            sock.sendto(mag.encode(), ADDR)
            sys.exit("您已退出聊天室")
        mag = "C %s %s"%(name,content)
        sock.sendto(mag.encode(), ADDR)


def main():
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind(("0.0.0.0",12345))
    name = login(sock)

    # 创建子进程
    p = Process(target=getmessage, args=(sock,))
    p.daemon = True
    p.start()
    sendmessage(sock, name)


if __name__ == '__main__':
    main()
