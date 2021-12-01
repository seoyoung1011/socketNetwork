''' 서버 예제
각 클라이어언트가 보낸 메세지를 서버에서 클라이언트 정보와 조합하여 각 클라이언트 채팅창에 띄워 보내 주는 역할 '''
import socket
from _thread import *
from tkinter import *

def threaded(client_socket, addr):
    global chat_log
    chat_log['state'] = 'normal'
    chat_log.insert("end", 'Connected by ' + addr[0] + ' [' + str(addr[1]) + ']\n')
    chat_log['state'] = 'disabled'
    for c in c_list:
        c.sendall(('[System] ' + str(addr[1]) + ' 님이 접속하였습니다.').encode())
    while 1:
        try:
            data = client_socket.recv(1024)
            chat_log['state'] = 'normal'
            chat_log.insert("end", 'Received from ' + addr[0] + ' - ' + str(addr[1]) + ' : ' + str(data.decode()) + '\n')
            chat_log['state'] = 'disabled'
            for c in c_list:
                c.sendall((str(addr[1]) + ' : ' + data.decode()).encode())
        except ConnectionResetError as e:
            c_list.remove(client_socket)
            for c in c_list:
                c.sendall(('[System] ' + str(addr[1]) + ' 님이 나갔습니다.').encode())
            chat_log['state'] = 'normal'
            chat_log.insert("end", 'Disconnected by ' + addr[0] + ' [' + str(addr[1]) + ']\n')
            chat_log['state'] = 'disabled'
            break
    client_socket.close()

def server_open():
    HOST = ip_entry.get();
    PORT = int(port_entry.get())
    start_new_thread(make_server, (HOST, PORT))
    open_button['state'] = 'disabled'
    ip_entry['state'] = 'readonly'
    port_entry['state'] = 'readonly'

def server_close():
    exit()

def make_server(HOST, PORT):
    global server_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((HOST, PORT))
    server_socket.listen()
    chat_log['state'] = 'normal'
    chat_log.insert("end", 'Server Start\n')
    chat_log['state'] = 'disabled'

    while 1:
        client_socket, addr = server_socket.accept()
        c_list.append(client_socket)
        start_new_thread(threaded, (c_list[-1], addr))

c_list = []
close = False
server_socket = None

s_display = Tk()
s_display.geometry('500x500')
s_display.title('Server')
s_display.resizable(False, False)

Label(s_display, text='Server IP : ').place(x=20, y=20)
Label(s_display, text='Port : ').place(x=200, y=20)
ip_entry = Entry(s_display, width=14, text='127.0.0.1'); ip_entry.place(x=83, y=21)
ip_entry.insert(0, 'localhost')
port_entry = Entry(s_display, width=5, text='9999'); port_entry.place(x=240, y=21)
port_entry.insert(0, '9999')
open_button = Button(s_display, text='Server Open', command=server_open); open_button.place(x=400, y=18)

chat_log = Text(s_display, width=65, height=29, state='disabled', spacing2=2); chat_log.place(x=20, y=60)
close_button = Button(s_display, text='Server Close', command=server_close); close_button.place(x=200, y=460)

s_display.mainloop()