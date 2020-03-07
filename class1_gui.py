from tkinter import *
from tkinter import messagebox
from class1_cal_v3 import *


class Class1_Gui(Tk):
    labels = []

    def __init__(self):
        super().__init__()
        self.win()
        self.input_label_build()
        self.output_label_bulid()
        self.unit_build()
        self.entry_build()
        self.radiobutton_build()
        self.button_build()
        self.output_text_build()

    # 建立界面
    def win(self):
        self.title('class1 激光安全等级计算')
        self.geometry('500x600')
        self.geometry('+300+50')  # 显示在屏幕中的位置

    # 建立输入参数
    def input_label_build(self):
        txt1 = ['波长', '脉宽', '激光器频率', '雷达旋转频率', '垂直扫描角度', '平均功率']
        for i, j in zip(txt1, range(7)):  # 注意这里的zip(),遍历多个数组的方式
            Label(self, text=i).grid(row=j, column=0, padx=10, pady=10, stick=W)

    # 建立输出参数
    def output_label_bulid(self):
        txt2 = ['AEL_single:', 'AEL_s.p.strain:', 'AEL_spt:', 'AEL_c:']
        for i, j in zip(txt2, range(8, 12)):
            Label(self, text=i).grid(row=j, column=0, padx=10, pady=10, stick=W)

    # 单位
    def unit_build(self):
        txt3 = ['nm', 's', 'Hz', 'Hz', '°', 'mW', '', '', 'J  单脉冲能量', 'J  脉冲串能量', 'J  时间基准能量', 'J  雷达计算结果']
        for i, j in zip(txt3, range(12)):
            Label(self, text=i).grid(row=j, column=2, padx=10, pady=10, stick=W)

    # 输入框
    def entry_build(self):  # 如何解决无法调用的问题？
        list1 = ['self.ent1', 'self.ent2', 'self.ent3', 'self.ent4', 'self.ent5', 'self.ent6']
        for i, j in zip(list1, range(7)):
            i = Entry(self)
            i.grid(row=j, column=1, padx=10, pady=10, stick=W)
            self.labels.append(i)
            print(self.labels)

        # self.ent1 = Entry(self)
        # self.ent1.grid(row=0, column=1, padx=10, pady=10, stick=W)
        # self.ent2 = Entry(self)
        # self.ent2.grid(row=1, column=1, padx=10, pady=10, stick=W)
        # self.ent3 = Entry(self)
        # self.ent3.grid(row=2, column=1, padx=10, pady=10, stick=W)
        # self.ent4 = Entry(self)
        # self.ent4.grid(row=3, column=1, padx=10, pady=10, stick=W)
        # self.ent5 = Entry(self)
        # self.ent5.grid(row=4, column=1, padx=10, pady=10, stick=W)
        # self.ent6 = Entry(self)
        # self.ent6.grid(row=5, column=1, padx=10, pady=10, stick=W)

    # 建立选择框
    def radiobutton_build(self):
        v = IntVar()
        rad1 = Radiobutton(self, text='连续', variable=v, value=1, command=self.rbtn1)
        rad1.grid(row=6, column=0)
        rad2 = Radiobutton(self, text='脉冲', variable=v, value=2, command=self.rbtn2)
        rad2.grid(row=6, column=1)

    # 按钮
    def button_build(self):
        btn1 = Button(self, text='计算标准值',
                      command=lambda: self.cal1(self.ent1.get(), self.ent2.get(), self.ent3.get(), self.ent4.get()))
        btn1.grid(row=7, column=0, ipadx=50, columnspan=2, stick=W)
        self.btn2 = Button(self, text='计算雷达值',
                           command=lambda: self.cal2(self.ent4.get(), self.ent5.get(), self.ent6.get()))
        self.btn2.grid(row=7, column=1, ipadx=50, columnspan=2, stick=E)

    # 输出文本
    def output_text_build(self):
        self.txt1 = Text(self, width=21, height=2)
        self.txt1.grid(row=8, column=1, stick=W)
        self.txt2 = Text(self, width=21, height=2)
        self.txt2.grid(row=9, column=1, stick=W)
        self.txt3 = Text(self, width=21, height=2)
        self.txt3.grid(row=10, column=1, stick=W)
        self.txt4 = Text(self, width=21, height=2)
        self.txt4.grid(row=11, column=1, stick=W)

    def rbtn1(self):  # 涉及到同一个class中不同函数下的参数相互调用的问题
        self.entry_build()
        self.ent2.delete(0, END)
        self.ent2.insert(END, '不输入')
        self.ent3.delete(0, END)
        self.ent3.insert(END, '不输入')

    def rbtn2(self):
        self.entry_build()
        self.ent2.delete(0, END)
        self.ent3.delete(0, END)

    def cal2(self, f2, fov_y, pw):
        if fov_y == '' or f2 == '' or pw == '':
            self.output_text_build()
            self.txt4.delete('1.0', END)
            self.txt4.insert(END, '输入不能为空！')
        elif float(f2) == 0:  # 注意此处必须将输入先转化成浮点数，输入的是字符串
            self.output_text_build()
            self.txt4.delete('1.0', END)
            self.txt4.insert(END, '雷达旋转频率不能为0')
        else:
            x = Calcul(0, 0, 0, f2, fov_y, pw)
            self.output_text_build()
            self.txt4.delete('1.0', END)
            self.txt4.insert(END, x.AEL_m())

    def cal1(self, λ, t, f1, f2):
        self.output_text_build()
        if λ == '' or t == '' or f1 == '' or f2 == '':
            # messagebox.showinfo('提示信息:', '输入不能为空')  #可以用提示框来显示
            self.txt1.delete('1.0', END)
            self.txt1.insert(END, '输入不能为空！')
            self.txt2.delete('1.0', END)
            self.txt2.insert(END, '输入不能为空！')
            self.txt3.delete('1.0', END)
            self.txt3.insert(END, '输入不能为空！')
        elif float(f2) == 0:
            # messagebox.showinfo('提示信息:', '雷达转速不能为0')  #可以用提示框来显示
            self.txt1.delete('1.0', END)
            self.txt1.insert(END, '雷达旋转频率不能为0!')
            self.txt2.delete('1.0', END)
            self.txt2.insert(END, '雷达旋转频率不能为0!')
            self.txt3.delete('1.0', END)
            self.txt3.insert(END, '雷达旋转频率不能为0!')
        else:
            a = float(λ)
            # b = float(t)
            # c = float(f1)
            d = float(f2)
            if (t == 0 and f1 == 0) or (t == '不输入' or f1 == '不输入'):  # 计算连续激光器的时候脉冲t和激光脉冲频率不输入
                b = (1 / 90) * (1 / d)  # 脉冲t为旋转1周扫描探测器的时间
                f = d  # 连续激光器的频率为雷达旋转的频率
            else:  # 此时为脉冲激光器，t为激光脉宽，频率为激光器的频率
                b = float(t)
                c = float(f1)
                f = c  # 脉冲激光器的频率
            x = Calcul(a, b, f1, f, 0, 0)  # 此处调用的时候函数是有问题的，f是选择性共用的一个值，此处错误！！！
            self.txt1.delete('1.0', END)
            self.txt1.insert(END, x.judge_t())
            # print(judge_t(b,a))
            self.txt2.delete('1.0', END)
            self.txt2.insert(END, x.AEL_spstrain())
            # print(AEL_spstrain(b,a,f))
            self.txt3.delete('1.0', END)
            self.txt3.insert(END, x.AEL_spt())
            # print(AEL_spt(a,f))


a = Class1_Gui()

a.mainloop()
