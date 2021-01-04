import io
import threading
import tkinter.messagebox
import TranslateDialog


# 图片转换翻译线程
class TranslateThread(threading.Thread):
    def __init__(self, image, api):
        threading.Thread.__init__(self)
        self.api = api
        self.image = image

    def run(self):
        try:
            buffer = io.BytesIO()
            self.image.save(buffer, format='PNG')
            self.image.close()
            # 图片转文本
            sourceText = self.api.image2text(buffer.getvalue())
            # 进行翻译0
            targetText = self.api.translate(sourceText)
            showText = sourceText + "\n" + targetText
            #tkinter.messagebox.showinfo(title=None, message=showText)
            TranslateDialog.show(title=None, inText=sourceText, outText=targetText)
        except Exception as e:
            tkinter.messagebox.showinfo(title=None, message=e)
