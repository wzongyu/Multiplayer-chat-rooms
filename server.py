import socket
import os.path
import sys
import threading
import queue
import json
import os

# 把服务器的ip设置为127.0.0.1，与我们在课程中学到的一致
# 即127.0.0.1是回送地址，指本地机，一般用来测试使用。
ip = '127.0.0.1'
# 使用的端口号
# 代表2022年的第1个月
port = 20221
messageQueue = queue.Queue() # 使用队列来完成消息的存储
names = []   # 记录在线用户
lock = threading.Lock() # Lock被称为原始锁，原始锁是一个在锁定时不属于特定线程的同步基元组件，它是能用的最低级的同步基元组件
class Server(threading.Thread):
    global names, lock
    def __init__(self):
        threading.Thread.__init__(self)
        self.skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        os.chdir(sys.path[0])

    # 监听消息从而接受
    def listen(self,connection,address):
        name = connection.recv(1024)
        name = name.decode()
        # 这是从客户端传来的消息，如果没有用户名，则默认将其设置为地址
        if name == '无用户名':
            name = address[0] + ':' + str(address[1])
        names.append((name, connection))
        storage = []
        for i in range(len(names)):
            storage.append(names[i][0])
        self.loadMessage(storage,address)
        try:
            while True:
                message = connection.recv(1024).decode()
                message = name + ':' + message
                self.loadMessage(message,address)
            connection.close()
        except:   
            t = 0
            for i in names:
                if i[0] == name:
                    names.pop(j)
                    break
                t = t + 1
            for t in range(len(names)):
                storage.append(names[i][0])
            self.loadMessage(storage,addr)
            connection.close()

    # 加载消息
    def loadMessage(self, data, address):
        lock.acquire()
        try:
            messageQueue.put((address, data))
        finally:
            lock.release()

    # 服务器端发送消息
    def sendMessage(self):
        while  True:
            if not messageQueue.empty():
                message = messageQueue.get()
                if isinstance(message[1], str):
                    for i in range(len(names)):
                        data = ' ' + message[1]
                        names[i][1].send(data.encode())

                if isinstance(message[1], list):
                    data = json.dumps(message[1])
                    for i in range(len(names)):
                        try:
                            names[i][1].send(data.encode())
                        except:
                            pass

    # 继承的线程所以必须重写run函数
    def run(self):
        self.skt.bind((ip,port))
        self.skt.listen(5)
        myThread = threading.Thread(target=self.sendMessage)
        myThread.start()
        while True:
            connection, address = self.skt.accept()
            thread = threading.Thread(target=self.listen, args=(connection, address))
            thread.start()
        # 断开连接
        self.skt.close()
        
if __name__ == '__main__':
    # 初始化服务器
    wzyChatServer = Server()
    # 使用start()函数来执行
    wzyChatServer.start()
