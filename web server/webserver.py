"""
author:xinyuyu
email:162528782@qq.com
time: 2020-6-20
env:python3.6
web server程序
完成一个类,提供给使用者
使用者可以通过这个类快速搭建web后端程序,用于展示自己的网页
"""
from socket import *
from select import *
import re

class WebServer:
    def __init__(self,host="0.0.0.0",port=9999,html=None):
        self.host=host
        self.port=port
        self.html=html
        self.createsock()
        self.bind()
        self.rlist=[]
        self.wlist=[]
        self.xlist=[]

    # 创建TCP套接字
    def createsock(self):
        self.sock=socket()
        self.sock.setblocking(False)

    # 绑定地址
    def bind(self):
        self.sock.bind((self.host,self.port))

    # 程序启动
    def start(self):
        self.sock.listen()
        print("Listen to the port",self.port)
        self.rlist.append(self.sock)
        while True:
            rs,ws,xs=select(self.rlist,self.wlist,self.xlist)
            for r in rs:
                if r is self.sock:
                    connfd,addr=r.accept()
                    connfd.setblocking(False) # 设置为非堵塞IO
                    self.rlist.append(connfd)
                else:
                    try:
                        self.handle(r)
                    except:
                        r.close()
                        self.rlist.remove(r)


    # 处理来自客户端的消息
    def handle(self, connfd):
        request=connfd.recv(1024 * 10).decode() # 接受HTTP请求
        pattern="[A-Z]+\s+(?P<info>/\S*)"
        result=re.match(pattern,request)
        if result:
            info=result.group("info")
            print("请求内容：",info)
            self.get_html(connfd,info) # 判断网页是否存在,给客户端发送
        else:
            connfd.close()
            self.rlist.remove(connfd)
            return

    # 负责判断给客户端发送
    def get_html(self,connfd,info):
        if info=="/":
            filename=self.html+"/index.html"
        else:
            filename=self.html+info

        try:
            fd=open(filename,"rb")
        except:
            # 请求网页不存在
            response="HTTP/1.1 404 Not Fount\r\n"
            response+="Content-Type:text/html\r\n"
            response+="\r\n"
            response+="<h1>sorry...</h1>"
            response=response.encode()
        else:
            # 请求网页存在
            data=fd.read()
            response="HTTP/1.1 200 OK\r\n"
            response+="Content-Type:text/html\r\n"
            response+="Content-Length:%d\r\n"%len(data)
            response+="\r\n"
            response=response.encode()+data
            fd.close()
        finally:
            connfd.send(response)

if __name__ == '__main__':
    web=WebServer(host="0.0.0.0",port=8888,html="./static")
    web.start()














