import numpy as np
import scipy as sp
from scipy.optimize import leastsq
import matplotlib.pyplot as plt
"""
最小二乘法 求拟合函数
"""


#目标函数 要拟合的函数sin(2*Pi*x)
def real_func(x):
    return np.sin(2*np.pi*x)

#多项式
def fit_func(p, x):
    f = np.poly1d(p)
    return f(x)

#残差函数
def residuals_fun(p, x, y):
    ret = fit_func(p, x) - y
    return ret

# 等差的十个点
x = np.linspace(0, 1, 10)
# 等差的1000个点
x_points = np.linspace(0, 1, 1000)
# x点函数正确的值
y_ = real_func(x)
#将正确的值 加上随机正太分布的值
y = [np.random.normal(0, 0.1) + y1 for y1 in y_]

# 拟合函数
def fitting(M=0):
    #随机M+1个（0,1）的值作为初始二项式的值
    p_init = np.random.rand(M+1)
    # 最小二乘
    p_lsq = leastsq(residuals_fun, p_init, args=(x, y))
    print('Fitting Parameters:', p_lsq[0])

    # plt.plot(x_points, real_func(x_points), label = 'real')
    # plt.plot(x_points, fit_func(p_lsq[0], x_points), label = 'fitted curve')
    # plt.plot(x, y , 'bo', label = 'noise')
    # plt.legend()
    # plt.show()
    return p_lsq

# p_lsq_0 = fitting(0)
# p_lsq_1 = fitting(1)
# p_lsq_2 = fitting(2)
# p_lsq_5 = fitting(5)
p_lsq_9 = fitting(9)

regularization = 0.0001

def residuals_func_regularization(p, x, y):
    ret = fit_func(p, x) - y
    ret = np.append(ret, np.sqrt(0.5*regularization*np.square(p))) # L2范数作为正则化项
    return ret
p_init = np.random.rand(9+1)
p_lsq_regularization = leastsq(residuals_func_regularization, p_init, args=(x, y))
plt.plot(x_points, real_func(x_points), label='real')
plt.plot(x_points, fit_func(p_lsq_9[0], x_points), label='fitted curve')
plt.plot(x_points, fit_func(p_lsq_regularization[0], x_points), label='regularization')
plt.plot(x, y, 'bo', label='noise')
plt.legend()
plt.show()







