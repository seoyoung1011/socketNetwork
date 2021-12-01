from tkinter import *
import random
from server import *
from client import *
from tkinter import messagebox


class APP(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.frame = None
        self.title("소켓통신")
        self.geometry("400x300+400+200")
        self.resizable(0, 0)
        self.switch_frame(main)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self.frame is not None:
            self.frame.destroy()
        self.frame = new_frame
        self.frame.pack()
        self.propagate(0)


class main(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, width=400, height=300, bg="#FFCDD9")
        Button(self, text="서버 열기", command=lambda: master.switch_frame(serverOpen)).place(x="60", y="60")
        Button(self, text="서버 참여", command=lambda: master.switch_frame(serverJoin)).place(x="150", y="60")
        self.propagate(0)


class serverOpen(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, width=400, height=300)
        self.back = PhotoImage(file="other/icon_back.png").subsample(25)
        Button(self, text=" ", image=self.back, command=lambda: master.switch_frame(main)).place(x="0", y="0")
        Label(self, text="서버 이름").place(x=60, y=60)
        self.server_name = Entry(self)
        self.server_name.place(x=125, y=60)
        Label(self, text="서버 포트").place(x=60, y=90)
        self.server_port = Entry(self)
        self.server_port.place(x=125, y=90)
        Button(self, text='시작', command=self.open).place(x=200, y=200)
        self.propagate(0)

    def open(self):
        server = ServerMain(int(Entry.get(self.server_port)))
        server.run()


class serverJoin(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, width=400, height=300)
        self.back = PhotoImage(file="other/icon_back.png").subsample(25)
        Button(self, text=" ", image=self.back, command=lambda: master.switch_frame(main)).place(x="0", y="0")
        Label(self, text="서버 IP").place(x=60, y=60)
        self.server_ip = Entry(self)
        self.server_ip.place(x=125, y=60)
        Label(self, text="서버 포트").place(x=60, y=90)
        self.server_port = Entry(self)
        self.server_port.place(x=125, y=90)
        Label(self, text="사용할 id").place(x=60, y=120)
        self.server_id = Entry(self)
        self.server_id.place(x=125, y=120)
        Button(self, text='시작', command=self.join).place(x=200, y=200)
        self.propagate(0)

    def join(self):
        client = Client(int(Entry.get(self.server_port)))
        client.run()


if __name__ == "__main__":
    app = APP()
    app.mainloop()