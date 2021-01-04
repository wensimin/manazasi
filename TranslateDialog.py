from tkinter import *
import tkinter.simpledialog

from Api import Api


# 翻译对话框
class TranslateDialog(tkinter.simpledialog.Dialog):
    def __init__(self, parent, title=None, inText=None, outText=None):
        self.inText = inText
        self.outText = outText
        self.inTextLabel = None
        self.outTextLabel = None
        self.api = Api()
        tkinter.simpledialog.Dialog.__init__(self, parent, title=title)

    def body(self, master):
        self.inTextLabel = Text(self, width=40, height=4)
        self.outTextLabel = Text(self, width=40, height=4)
        self.inTextLabel.pack()
        self.inTextLabel.insert(INSERT, self.inText)
        self.outTextLabel.pack()
        self.outTextLabel.insert(INSERT, self.outText)
        self.center()
        return self

    # 居中
    def center(self):
        ws = self.parent.winfo_screenwidth()
        hs = self.parent.winfo_screenheight()
        w = 300
        h = 200
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.geometry('+0+0')

    def translate(self):
        inText = self.inTextLabel.get("1.0", END)
        outText = self.api.translate(inText)
        self.outTextLabel.insert(INSERT, outText)


def show(title=None, inText=None, outText=None):
    root = Tk()
    root.withdraw()
    TranslateDialog(root, title, inText, outText)


show("aaa", "bbb", "ccc")
