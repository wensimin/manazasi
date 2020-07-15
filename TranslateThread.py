import io
import threading
import tkinter.messagebox

from Api import Api


# 图片转换翻译线程
class TranslateThread(threading.Thread):
    def __init__(self, image):
        threading.Thread.__init__(self)
        self.api = Api()
        self.image = image

    def run(self):
        buffer = io.BytesIO()
        self.image.save(buffer, format='PNG')
        self.image.close()
        # 图片转文本
        sourceText = self.api.image2text(buffer.getvalue())
        # 进行翻译
        targetText = Api.translate(sourceText)
        tkinter.messagebox.showinfo(title=None, message=targetText)
        print(targetText)
