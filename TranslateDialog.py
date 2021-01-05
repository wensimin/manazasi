from tkinter import *
import tkinter.simpledialog

from Api import Api


# 翻译对话框
class TranslateDialog(tkinter.simpledialog.Dialog):
    # noinspection PyMissingConstructor
    def __init__(self, parent, title=None, inText=None, outText=None):
        self.inText = inText
        self.outText = outText
        self.inTextLabel = None
        self.outTextLabel = None
        self.api = Api()
        self.init(parent, title)

    # 未直接调用dialog类的init 无法处理geometry问题
    def init(self, parent, title):

        """Initialize a dialog.

        Arguments:

            parent -- a parent window (the application window)

            title -- the dialog title
        """
        Toplevel.__init__(self, parent)

        self.withdraw()  # remain invisible for now
        # If the master is not viewable, don't
        # make the child transient, or else it
        # would be opened withdrawn
        if parent.winfo_viewable():
            self.transient(parent)

        if title:
            self.title(title)

        self.parent = parent

        self.result = None

        body = Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)

        self.buttonbox()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        # 居中处理
        if self.parent is not None:
            ws = self.parent.winfo_screenwidth()
            hs = self.parent.winfo_screenheight()
            w = 300
            h = 200
            x = (ws / 2) - (w / 2)
            y = (hs / 2) - (h / 2)
            self.geometry("+%d+%d" % (x, y))

        self.deiconify()  # become visible now

        self.initial_focus.focus_set()

        # wait for window to appear on screen before calling grab_set
        self.wait_visibility()
        self.grab_set()
        self.wait_window(self)

    # body重写 翻译框部分
    def body(self, master):
        self.inTextLabel = Text(self, width=40, height=4)
        self.outTextLabel = Text(self, width=40, height=4)
        self.inTextLabel.pack()
        self.inTextLabel.insert(INSERT, self.inText)
        self.outTextLabel.pack()
        self.outTextLabel.insert(INSERT, self.outText)
        return self.inTextLabel

    # button重写,按钮部分
    def buttonbox(self):

        box = Frame(self)

        w = Button(box, text="翻译", width=10, command=self.ok, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        w = Button(box, text="退出", width=10, command=self.cancel)
        w.pack(side=LEFT, padx=5, pady=5)

        self.bind("<Escape>", self.cancel)

        box.pack()

    # ok重写
    def ok(self, event=None):
        self.translate()

    # 翻译
    def translate(self):
        inText = self.inTextLabel.get("1.0", END)
        outText = self.api.translate(inText)
        self.outTextLabel.delete("1.0", END)
        self.outTextLabel.insert(INSERT, outText)


def show(title=None, inText=None, outText=None):
    root = Tk()
    root.withdraw()
    TranslateDialog(root, title, inText, outText)

