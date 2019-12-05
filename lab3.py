import control.matlab as cm
from sympy import *
import numpy as np
import matplotlib.pyplot as plt
import control as ctr
import math
from scipy import signal
from scipy import integrate

ky = 20
Tg = 4.0
Ty = 5.0
Tgm = 2.0
# PID
kpid = 67.5
Tdpid = 2.3
Tipid = 1.1

# PI
kpi = 1700
Tipi = 0.023


TimeLine = []
for i in range(0, 300):
    TimeLine.append(i)


def n_w1(num, den):
    w1 = ctr.tf(num, den)
    print('Передаточная функция : \n {0}'.format(w1))
    return w1


def n_w(num, den, name):
    w = cm.tf(num, den)
    print('Передаточная функция {0} : \n {1}'.format(name, w))
    return w


def grafic_step(f, name):
    y1, x1 = cm.step(f, TimeLine)
    plt.plot(x1, y1, "b")
    plt.title('Переходная функция {}'.format(name))
    plt.ylabel('Амплитудное значение')
    plt.xlabel('Время(c)')
    plt.grid(True, linewidth=1, alpha=0.5)
    plt.show()


def grafic_stepw(f, name):
    y1, x1 = cm.step(f, TimeLine)
    plt.plot(x1, y1, "b")
    plt.title('Переходная функция {}'.format(name))
    plt.ylabel('Амплитудное значение')
    plt.xlabel('Время(c)')
    plt.grid(True, linewidth=1, alpha=0.5)
    plt.show()


def grafic_pol(f, name):
    # x = cm.pole(f).real
    # y = cm.pole(f).imag

    # plt.plot(x, y)
    # plt.plot(cm.pole(f))

    ctr.pzmap(f, Plot=True, title='Pole Zero Map {}'.format(name))
    [p, z] = ctr.pzmap(f)
    # x = ctr.pzmap(f).real
    # y = ctr.pzmap(f).imag
    print("Полюса {}: \n".format(name))
    print("p = {}".format(p))
    print("z = {}".format(z))
    # print("x ={} \n".format(x))
    # print("y = {} \n".format(y))
    # plt.title("График полюсов функции {}".format(name))
    # plt.ylabel("Мниманя ось")
    # plt.xlabel("Действительная часть")
    # plt.grid(True)
    plt.show()


def bode_function(f, name):
    mag, phase, omega = cm.bode(f, dB=True, Plot=True)
    plt.title('ЛАЧХ и ЛАФЧХ {}'.format(name))
    plt.show()


def bode_functionw(f, name):
    mag, phase, omega = cm.bode(f, dB=False, Plot=True)
    plt.title("АЧХ и ФЧХ {}".format(name))
    plt.show()


def integral_find(f, name):
    Q = integrate.quad(f, 0, math.inf)
    print("Интегральная функция {0} = {1} ".format(name, Q))
    return Q


W1 = n_w(1, [Tg, 1], "Генератора")
W2 = n_w([0.01 * Tgm, 1], [0.05 * Tg, 1], "Гидравлической турбины")
W3 = n_w(ky, [Ty, 1], "Исполнительного устройства")
# Wk = n_w([k, 0] , [0], "Wk ")
# Wd = n_w ([diff()])
Wkpid = ctr.tf([kpid, 0], [0, 1])
Wtdpid = ctr.tf([Tdpid, 0], [0, 1])
Wtipid = ctr.tf([0, Tipid], [1, 0])
# print("Wtipid = {} \n".format(Wtipid))
Wpid = cm.parallel(Wkpid, Wtdpid, Wtipid)
Wwpid = cm.series(W1, W2, W3, Wpid)
Wwpido = cm.feedback(Wwpid, 1)
Wkpi = ctr.tf([kpi, 0], [0, 1])
Wtipi = ctr.tf([0, Tipi], [1, 0])
Wpi = cm.parallel(Wkpi, Wtipi)
W = cm.series(W1, W2, W3)
Wwpi = cm.series(W, Wpi)
Wwpio = cm.feedback(Wwpi, 1)
Wf = cm.feedback(W, 1)
print("W = \n {}".format(Wf))
print("Wwpid = \n")
print(Wwpido)
print("Wwpi = \n {}".format(Wwpio))
grafic_stepw(Wf, "W")
grafic_step(Wwpido, "PID")
grafic_step(Wwpio, "PI")


grafic_pol(Wwpido, "PID")
grafic_pol(Wwpio, "PI")
grafic_pol(Wf, "Без регулирования")

bode_function(Wwpido, "PID")
bode_function(Wwpio, "PI")
bode_function(Wf, "Обычной функции")


bode_functionw(Wwpido, "PID")
bode_functionw(Wwpio, " PI")
bode_functionw(Wf, "Функции без регуляторов")

integral_find(Wwpido, "PID")
integral_find(Wwpio, "PI")
