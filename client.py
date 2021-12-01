import socket
from _thread import *
import threading
from tkinter import *
from time import sleep

def send(socket):
    global go_send
    while True:
        if go_send:
            message = (message_input.get(1.0, "end")).rstrip()
            socket.send(message.encode())
            message_input.delete(1.0, "end")
            go_send = False
        else:
            if go_out:
                socket.close()
                exit()
            sleep(0.1)

def receive(socket):
    first = True
    while True:
        try:
            data = socket.recv(1024)
            chat_log['state'] = 'normal'
            if first:
                chat_log.insert("end", str(data.decode( )))
                first = False
            else:
                chat_log.insert("end", '\n' + str(data.decode()))
                chat_log.see('end')
            chat_log['state'] = 'disabled'
        except ConnectionAbortedError as e:
            chat_log['state'] = 'normal'
            chat_log.insert("end", '\n[System] 접속을 종료합니다.\n')
            chat_log['state'] = 'disabled'
            exit()

def login():
    # 서버의 ip주소 및 포트
    HOST = ip_entry.get();
    PORT = int(port_entry.get())
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    threading.Thread(target=send, args=(client_socket, )).start()
    threading.Thread(target=receive, args=(client_socket, )).start()
    exit()

def try_login():
    global go_out
    start_new_thread(login, ())
    login_button['state'] = 'disabled'
    logout_button['state'] = 'active'
    ip_entry['state'] = 'readonly'
    port_entry['state'] = 'readonly'
    go_out = False

def try_logout():
    global go_out
    login_button['state'] = 'active'
    logout_button['state'] = 'disabled'
    ip_entry['state'] = 'normal'
    port_entry['state'] = 'normal'
    go_out = True

def set_go_send(event):
    global go_send
    go_send = True

go_out, go_send = False, False
c_display = Tk()
c_display.geometry('500x480')
c_display.title('Client')
c_display.resizable(False, False)

Label(c_display, text='Server IP : ').place(x=20, y=20)
Label(c_display, text='Port : ').place(x=200, y=20)
ip_entry = Entry(c_display, width=14); ip_entry.place(x=83, y=21)
ip_entry.insert(0, 'localhost')
port_entry = Entry(c_display, width=5); port_entry.place(x=240, y=21)
port_entry.insert(0, '9999')
login_button = Button(c_display, text='접속', command=try_login); login_button.place(x=370, y=18)
logout_button = Button(c_display, text='연결 해제', state='disabled', command=try_logout); logout_button.place(x=415, y=18)

chat_frame = Frame(c_display)
scrollbar = Scrollbar(chat_frame); scrollbar.pack(side='right', fill='y')
chat_log = Text(chat_frame, width=62, height=24, state='disabled', yscrollcommand=scrollbar.set); chat_log.pack(side='left')
scrollbar['command'] = chat_log.yview
chat_frame.place(x=20, y=60)
message_input = Text(c_display, width=55, height=4); message_input.place(x=20, y=390)
send_button = Button(c_display, text='전송', width=7, height=3, command=lambda: set_go_send(None)); send_button.place(x=415, y=390)
message_input.bind("<Return>", set_go_send)

c_display.mainloop()