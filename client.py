import socket
import threading
import json
import tkinter
import tkinter.messagebox
import tkinter.filedialog
import time
from tkinter.scrolledtext import ScrolledText

# 首先使用tkinter实现登录界面
loginUI = tkinter.Tk()

# 页面名字
loginUI.title('吴纵宇的多人聊天室')

# 整体页面的大小
loginUI.geometry("400x200")

# 以下均是登录页面要显示的内容及其大小
loginUI.resizable(0, 0)
ipInit = tkinter.StringVar()
ipInit.set('127.0.0.1:20221')
name = tkinter.StringVar().set('')
labeledIp = tkinter.Label(loginUI, text='用户IP地址：')
labeledIp.place(x=20, y=20, width=100, height=40)
entryIP = tkinter.Entry(loginUI, width=60, textvariable=ipInit)
entryIP.place(x=125, y=25, width=100, height=30)
labeledName = tkinter.Label(loginUI, text='用户名：')
labeledName.place(x=20, y=70, width=100, height=40)
entry = tkinter.Entry(loginUI, width=60, textvariable=name)
entry.place(x=125, y=75, width=100, height=30)

ip = ''
port = ''
userName = ''


def UserLogin(*args):
    global userName, ip, port
    userName = entry.get()
    ip, port = entryIP.get().split(':')
    if not userName:
        tkinter.messagebox.showwarning('warning', message='用户名不能为空！')
    else:
        loginUI.destroy()


# 登录的按钮
buttonOfLogin = tkinter.Button(loginUI, text="登录", command=UserLogin, activebackground='white')
buttonOfLogin.place(x=140, y=115, width=40, height=25)

# 如果不正确则再来一次
# 将定义的登录函数绑定在登录界面上
loginUI.bind('<Return>', UserLogin)
loginUI.mainloop()

# 使用socket将用户端和客户端相连接
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((ip, int(port)))

# 如果用户输入了用户名，就发送用户名
if userName:
    clientSocket.send(userName.encode())
# 如果未输入，则使用ip+端口作为默认用户名
else:
    clientSocket.send('无用户名'.encode())
    userName = ip + ':' + port

# 使用tkinter绘制聊天室界面
chatUI = tkinter.Tk()
chatUI.geometry("600x500")
chatUI.resizable(0, 0)
chatUI.title('Mr.Wu\'s chat room')

# 消息界面
informationList = ScrolledText(chatUI)
informationList.place(x=5, y=0, width=600, height=350)
informationList.insert(tkinter.END, '欢迎来到吴纵宇的聊天室')

userInput = tkinter.StringVar()
userInput.set('')
entryIuput = tkinter.Entry(chatUI, width=120, textvariable=userInput)
entryIuput.place(x=10, y=370, width=550, height=80)

usersList = ''  # 用于显示当前在线用户的列表框
usersList = tkinter.Listbox(chatUI)  # 与聊天UI绑定
usersList.place(x=445, y=0, width=140, height=350)

usersOnline = []  # 当前在线用户的用户名列表
RoomType = 'Multi-user chats'


def sendMessage(*args):
    if RoomType not in usersOnline:
        tkinter.messagebox.showerror('error', message='聊天室中当前无其他人')
        return
    if RoomType == userName:
        tkinter.messagebox.showerror('error', message='无法选择与自己聊天！')
        return
    message = entryIuput.get() + ':;' + userName + ':;' + RoomType
    clientSocket.send(message.encode())
    userInput.set('')


ButtonOfSend = tkinter.Button(chatUI, text="发送消息", command=sendMessage)
ButtonOfSend.place(x=500, y=450, width=62, height=25)
# 与发送消息的函数绑定
chatUI.bind('<Return>', sendMessage)


def receiveMessage():
    global uses
    while True:
        info = clientSocket.recv(1024)
        info = info.decode()
        try:
            uses = json.loads(info)
            usersList.delete(0, tkinter.END)
            usersList.insert(tkinter.END, "当前在线用户名单")
            for i in range(len(uses)):
                usersList.insert(tkinter.END, uses[i])
            usersOnline.append('Multi-user chats')
        except:
            info = info.split(':;')
            message, userName, chatType = info[0], info[1], info[2]
            t = time.localtime()
            message = '\n' + message + '\n'
            message = message + str(t.tm_year)+ '/' + str(t.tm_mon) + '/' + str(t.tm_mday) + '/'
            message = message + str(t.tm_hour) + '/' + str(t.tm_min) + '/' + str(t.tm_sec) + '/'
            if chatType == 'Multi-user chats' or userName == userName or chatType == userName:
                informationList.insert(tkinter.END, message)
            informationList.see(tkinter.END)


# 初始化客户端线程
clientThread = threading.Thread(target=receiveMessage)
clientThread.start()
chatUI.mainloop()

# 要记得关闭socket连接
clientSocket.close()
