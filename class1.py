from tkinter import *
import math
from tkinter.ttk import *

# 计算class 1的探测能量
# 参数
'''
C4
C5
α 发散角，只与计算实际值相关（mrad）
λ 波长（nm）
f 1s内的脉冲个数（Hz）
T 时间基准
t 脉宽（s）
Z 占空比（%）
Pw 峰值功率（W）
P0 平均功率（W）
'''


# 计算C5的值
def C5_c(t, λ, f):
    a = float(t)
    b = float(λ)
    c = float(f)
    if a <= 5e-6 and 700 < b <= 1050 and c > 600:
        c5 = 5 * c ** -0.25
    elif a <= 0.25 and 1500 < b <= 1800 and c > 600:
        c5 = 5 * c ** -0.25
    else:
        c5 = 1
    if c5 > 0.4:
        return c5
    else:
        return 0.4


# print(C5_c(5e-7,780,700))


# 计算连续激光器的AEL值
def AEL_c(t, λ):
    a = float(t)
    b = float(λ)
    c4 = 10 ** (2e-3 * (b - 700))
    c7 = 1
    if 0.25 < a <= 0.35 and 700 < b <= 1050:
        c = 7E-4 * a ** 0.75 * c4
    elif 0.25 < a <= 0.35 and 1500 < b <= 1800:
        c = 8e-3
    elif 0.35 < a <= 10 and 700 < b <= 1050:
        c = 7E-4 * a ** 0.75 * c4
    elif 0.35 < a <= 10 and 1500 < b <= 1800:
        c = 1.8e-2 * a ** 0.75
    elif 10 < a <= 3e+4 and 700 < b <= 1050:
        c = 3.9e-4 * c4 * c7
    elif 10 < a <= 3e+4 and 1500 < b <= 1800:
        c = 1e-2
    else:
        c = '输入错误'
    return (c)


# 计算脉冲激光器的AEL_single值
def AEL_single(t, λ):
    a = float(t)
    b = float(λ)
    c4 = 10 ** (2e-3 * (b - 700))
    if 5e-6 < a <= 0.25 and 700 < b <= 1050:
        c = 7e-4 * a ** 0.75 * c4
    elif 5e-6 < a <= 0.25 and 1500 < b <= 1800:
        c = 8E-3
    elif 1e-9 <= a <= 5e-6 and 700 < b <= 1050:
        c = 7.7E-8 * c4
    elif 1e-9 <= a <= 5e-6 and 1500 < b <= 1800:
        c = 8e-3
    else:
        c = '输入错误'
    return c


# 判断连续激光器还是脉冲给激光器
def judge_t(t, λ):
    a = float(t)
    b = float(λ)
    if a > 0.25:
        return AEL_c(a, b)
    else:
        return AEL_single(a, b)


# print(judge_t(1.11111e-3,780))

# 连续脉冲激光器的AEL计算
def AEL_spstrain(t, λ, f):
    a = float(t)
    b = float(λ)
    c = float(f)
    return judge_t(a, b) * C5_c(a, b, f)


# 比较值
def AEL_spt(λ, f):
    a = float(λ)
    b = float(f)
    c4 = 10 ** (2e-3 * (a - 700))
    c7 = 1
    if f != 0:
        if 700 < a <= 1050:
            c = (3.9e-4 * c4 * c7) / b
        elif 1500 < a <= 1800:
            c = 1e-2 / b
        else:
            c = '输入错误'
        return c
    else:
        return '输入错误'


# print(AEL_single(1e-8,780))
# print(AEL_spstrain(1e-8,780,1e+8))
# print(AEL_spt(780,1e+8))
# print(C5_c(1e-8,780,1e+8))

'''
#计算单点扫描激光雷达实际测试过程中的能量值
def AEL_s(p0,f):
    a = float(p0)*1e-3
    b = float(f)
    t = (1/b)*(4/360)   #描探测器上的时间=雷达转一圈的时间*光斑落在7mm探测器上的时间
    w = a * t  #探测器上的能量=平均功率*扫描探测器上的时间
    return w
#print(AEL_s(50,10))
'''


# 计算扫描式激光雷达实际测试过程中的AEL值
def AEL_m(FOV_Y, f2, pw):
    d = float(f2)  # 频率单位为Hz
    e = float(pw) * 1e-3  # 功率的单位是w
    n = float(FOV_Y)
    if n > 0:
        b = math.radians(n)  # 角度单位为°
        s_scan = 2 * 0.1 * math.tan(b / 2) * 7e-3  # 计算扫描的区域大小
        s_detector = ((7e-3 / 2) ** 2 * math.pi)  # 计算探测器圆面积
        effficiency = s_detector / s_scan  # 计算探测器上接收到的效率
        scan_time = (1 / d) * 2 * math.degrees(math.atan((7e-3 / 2) / 0.1)) / 360  # 计算每扫描一圈经过探测器上的时间
        if effficiency < 1:  # 判断是否扫描光斑大于探测器的面积
            energy = e * effficiency * scan_time
        else:
            energy = e * scan_time
        return energy
    else:
        scan_time = (1 / d) * 2 * math.degrees(math.atan((7e-3 / 2) / 0.1)) / 360  # 计算每扫描一圈经过探测器上的时间
        energy = e * scan_time
    return energy


# print(AEL_m(0.3,10,5))

def cal1(λ, t, f1, f2):
    if λ == '' or t == '' or f1 == '' or f2 == '':
        txt1.delete('1.0', END)
        txt1.insert(END, '输入不能为空！')
        txt2.delete('1.0', END)
        txt2.insert(END, '输入不能为空！')
        txt3.delete('1.0', END)
        txt3.insert(END, '输入不能为空！')
    elif float(f2) == 0:
        txt1.delete('1.0', END)
        txt1.insert(END, '雷达旋转频率不能为0!')
        txt2.delete('1.0', END)
        txt2.insert(END, '雷达旋转频率不能为0!')
        txt3.delete('1.0', END)
        txt3.insert(END, '雷达旋转频率不能为0!')
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
        txt1.delete('1.0', END)
        txt1.insert(END, judge_t(b, a))
        # print(judge_t(b,a))
        txt2.delete('1.0', END)
        txt2.insert(END, AEL_spstrain(b, a, f))
        # print(AEL_spstrain(b,a,f))
        txt3.delete('1.0', END)
        txt3.insert(END, AEL_spt(a, f))
        # print(AEL_spt(a,f))


def cal2(FOV_Y, f2, pw):
    if FOV_Y == '' or f2 == '' or pw == '':
        txt4.delete('1.0', END)
        txt4.insert(END, '输入不能为空！')
    else:
        a = float(FOV_Y)
        b = float(f2)
        c = float(pw)
        if b == 0:
            txt4.delete('1.0', END)
            txt4.insert(END, '雷达旋转频率不能为0')
        else:
            txt4.delete('1.0', END)
            txt4.insert(END, AEL_m(a, b, c))


# 设置选择函数

def Rbtn1():
    ent2.delete(0, END)
    ent2.insert(END, '不输入')
    ent3.delete(0, END)
    ent3.insert(END, '不输入')


def Rbtn2():
    ent2.delete(0, END)
    ent3.delete(0, END)


# 界面设计
root = Tk()
root.title('class1 激光安全等级计算')
root.geometry('500x600')

Label(root, text='波长').grid(row=0, column=0, padx=10, pady=10, stick=W)
Label(root, text='脉宽').grid(row=1, column=0, padx=10, pady=10, stick=W)
Label(root, text='激光器频率').grid(row=2, column=0, padx=10, pady=10, stick=W)
Label(root, text='雷达旋转频率').grid(row=3, column=0, padx=10, pady=10, stick=W)
Label(root, text='垂直扫描角度').grid(row=4, column=0, padx=10, pady=10, stick=W)
Label(root, text='平均功率').grid(row=5, column=0, padx=10, pady=10, stick=W)

Label(root, text='AEL_single:').grid(row=8, column=0, padx=10, pady=10, stick=W)
Label(root, text='AEL_s.p.strain:').grid(row=9, column=0, padx=10, pady=10, stick=W)
Label(root, text='AEL_spt:').grid(row=10, column=0, padx=10, pady=10, stick=W)
Label(root, text='AEL_c:').grid(row=11, column=0, padx=10, pady=10, stick=W)

Label(root, text='nm').grid(row=0, column=2, padx=10, pady=10, stick=W)
Label(root, text='s').grid(row=1, column=2, padx=10, pady=10, stick=W)
Label(root, text='Hz').grid(row=2, column=2, padx=10, pady=10, stick=W)
Label(root, text='Hz').grid(row=3, column=2, padx=10, pady=10, stick=W)
Label(root, text='°').grid(row=4, column=2, padx=10, pady=10, stick=W)
Label(root, text='mW').grid(row=5, column=2, padx=10, pady=10, stick=W)

Label(root, text='J  单脉冲能量').grid(row=8, column=2, padx=10, pady=10, stick=W)
Label(root, text='J  脉冲串能量').grid(row=9, column=2, padx=10, pady=10, stick=W)
Label(root, text='J  时间基准能量').grid(row=10, column=2, padx=10, pady=10, stick=W)
Label(root, text='J  雷达计算结果').grid(row=11, column=2, padx=10, pady=10, stick=W)

# 输入框
ent1 = Entry(root)
ent1.grid(row=0, column=1, padx=10, pady=10, stick=W)
ent2 = Entry(root)
ent2.grid(row=1, column=1, padx=10, pady=10, stick=W)
ent3 = Entry(root)
ent3.grid(row=2, column=1, padx=10, pady=10, stick=W)
ent4 = Entry(root)
ent4.grid(row=3, column=1, padx=10, pady=10, stick=W)
ent5 = Entry(root)
ent5.grid(row=4, column=1, padx=10, pady=10, stick=W)
ent6 = Entry(root)
ent6.grid(row=5, column=1, padx=10, pady=10, stick=W)

# 选择框
v = IntVar()
rad1 = Radiobutton(root, text='连续', variable=v, value=1, command=Rbtn1)
rad1.grid(row=6, column=0)
rad2 = Radiobutton(root, text='脉冲', variable=v, value=2, command=Rbtn2)
rad2.grid(row=6, column=1)

# 按钮
btn1 = Button(root, text='计算标准值', command=lambda: cal1(ent1.get(), ent2.get(), ent3.get(), ent4.get()))
btn1.grid(row=7, column=0, ipadx=50, columnspan=2, stick=W)
btn2 = Button(root, text='计算雷达值', command=lambda: cal2(ent5.get(), ent4.get(), ent6.get()))
btn2.grid(row=7, column=1, ipadx=50, columnspan=2, stick=E)

# 输出文本框
txt1 = Text(root, width=21, height=2)
txt1.grid(row=8, column=1, stick=W)
txt2 = Text(root, width=21, height=2)
txt2.grid(row=9, column=1, stick=W)
txt3 = Text(root, width=21, height=2)
txt3.grid(row=10, column=1, stick=W)
txt4 = Text(root, width=21, height=2)
txt4.grid(row=11, column=1, stick=W)

mainloop()
