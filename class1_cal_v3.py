import math


# 建立计算函数

class Calcul(object):

    # 初始化
    def __init__(self, λ, t, f1, f2, fov_y, pw):
        self.λ = λ  # 波长（nm）
        self.t = t  # 脉宽（s）
        self.f1 = f1  # 激光器发射频率（Hz）
        self.f2 = f2  # 雷达旋转频率（Hz）
        self.fov_y = fov_y  # 垂直扫描角度（°）
        self.pw = pw  # 激光器平均功率（mw）

        # 判断连续性激光器还是脉冲型激光器
        if (self.t == 0 and self.f1 == 0) or (self.t == '不输入' and self.f1 == '不输入'):  # 如果脉宽和激光器频率不输入的时候
            self.b = (1 / 90) * (1 / float(self.f2))  # 此时的脉冲时间为雷达旋转1周扫描探测器的时间
            self.f = float(self.f2)  # 连续激光器的频率为雷达旋转的频率
        else:  # 此时为脉冲激光器，t为激光脉宽，频率为激光器的频率
            self.b = float(self.t)
            self.f = float(self.f1)

    # 计算C5的值
    def C5_c(self):
        if float(self.t) <= 5e-6 and 700 < float(self.λ) <= 1050 and self.f > 600:
            c5 = 5 * self.f ** -0.25
        elif float(self.t) <= 0.25 and 1500 < float(self.λ) <= 1800 and self.f > 600:
            c5 = 5 * self.f ** -0.25
        else:
            c5 = 1
        if c5 > 0.4:
            return c5
        else:
            return 0.4

    # 判断脉冲激光器还是连续激光器
    def judge_t(self):
        if float(self.t) > 0.25:
            return self.AEL_c()
        else:
            return self.AEL_single()

    # 计算连续脉冲时AEL_c的值
    def AEL_c(self):
        c4 = 10 ** (2e-3 * (float(self.λ) - 700))
        c7 = 1
        if 0.25 < float(self.t) <= 0.35 and 700 < float(self.λ) <= 1050:
            ael_c = 7E-4 * float(self.t) ** 0.75 * c4
        elif 0.25 < float(self.t) <= 0.35 and 1500 < float(self.λ) <= 1800:
            ael_c = 8e-3
        elif 0.35 < float(self.t) <= 10 and 700 < float(self.λ) <= 1050:
            ael_c = 7E-4 * float(self.t) ** 0.75 * c4
        elif 0.35 < float(self.t) <= 10 and 1500 < float(self.λ) <= 1800:
            ael_c = 1.8e-2 * float(self.t) ** 0.75
        elif 10 < float(self.t) <= 3e+4 and 700 < float(self.λ) <= 1050:
            ael_c = 3.9e-4 * c4 * c7
        elif 10 < float(self.t) <= 3e+4 and 1500 < float(self.λ) <= 1800:
            ael_c = 1e-2
        else:
            ael_c = '输入错误'
        return (ael_c)

    # 计算单脉冲的AEL值
    def AEL_single(self):
        c4 = 10 ** (2e-3 * (float(self.λ) - 700))
        if 5e-6 < float(self.t) <= 0.25 and 700 < float(self.λ) <= 1050:
            ael_single = 7e-4 * float(self.t) ** 0.75 * c4
        elif 5e-6 < float(self.t) <= 0.25 and 1500 < float(self.λ) <= 1800:
            ael_single = 8E-3
        elif 1e-9 <= float(self.t) <= 5e-6 and 700 < float(self.λ) <= 1050:
            ael_single = 7.7E-8 * c4
        elif 1e-9 <= float(self.t) <= 5e-6 and 1500 < float(self.λ) <= 1800:
            ael_single = 8e-3
        else:
            ael_single = '输入错误'
        return ael_single

    # 连续脉冲激光器的AEL计算
    def AEL_spstrain(self):
        return self.judge_t() * self.C5_c()

    # 计算AEL_spt
    def AEL_spt(self):
        c4 = 10 ** (2e-3 * (float(self.λ) - 700))
        c7 = 1
        if float(self.f) != 0:
            if 700 < float(self.λ) <= 1050:
                result = (3.9e-4 * c4 * c7) / float(self.f)
            elif 1500 < float(self.λ) <= 1800:
                result = 1e-2 / float(self.f)
            else:
                result = '输入错误'
            return result
        else:
            return '输入错误'

    # 计算扫描式激光雷达实际测试过程中的AEL值
    def AEL_m(self):
        if float(self.fov_y) > 0:
            b = math.radians(float(self.fov_y))  # 角度单位为°
            s_scan = 2 * 0.1 * math.tan(b / 2) * 7e-3  # 计算扫描的区域大小
            s_detector = ((7e-3 / 2) ** 2 * math.pi)  # 计算探测器圆面积
            effficiency = s_detector / s_scan  # 计算探测器上接收到的效率
            scan_time = (1 / float(self.f2)) * 2 * math.degrees(math.atan((7e-3 / 2) / 0.1)) / 360  # 计算每扫描一圈经过探测器上的时间
            if effficiency < 1:  # 判断是否扫描光斑大于探测器的面积
                energy = float(self.pw) * 1e-3 * effficiency * scan_time
            else:
                energy = float(self.pw) * 1e-3 * scan_time
            return energy
        else:
            scan_time = (1 / float(self.f2)) * 2 * math.degrees(math.atan((7e-3 / 2) / 0.1)) / 360  # 计算每扫描一圈经过探测器上的时间
            energy = float(self.pw) * 1e-3 * scan_time
        return energy


if '__main__' == '__name__':
    test = Calcul(780, 1e-3, 1e+7, 10, 20, 5)
    print(test.AEL_m())
