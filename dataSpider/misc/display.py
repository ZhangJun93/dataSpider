# coding: utf-8
import Tkinter as tk

def input_str():
    r = tk.simpledialog.askstring(u'字符录入', u'请输入字符', initialvalue='hello world!')
    if r:
        print(r)


if __name__ == '__main__':
    #input_str()
    import tkFileDialog

    tk.showinfo(title='中文标题'.decode('gbk'), message='XXX')  # 注意:中文要加.decode('gbk')
