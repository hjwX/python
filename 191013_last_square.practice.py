import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import leastsq

#要测试的函数
def real_func(x):
    real = np.poly1d([2,3,4,5])
    return real(x)

#多项式
def fit_func(p, x):
    fit = np.poly1d(p)
    return fit(x)

#残差函数
def residual_func(p, x, y):
    ret = fit_func(p, x) - y
    return ret

regularization = 0.0001
def residuals_func_regularization(p, x, y):
    ret = fit_func(p, x) - y
    print('ret:', ret)
    ret = np.append(ret, np.sqrt(0.5*regularization*np.square(p)))
    print('ret after append:', ret)
    return ret

x = np.linspace(1, 10, 5)
y_ = real_func(x)
y = [np.random.normal(0, 1) + y1 for y1 in y_]
x_point = np.linspace(1, 10, 10000)

p_init = np.random.rand(4)
p_lsq = leastsq(residual_func, p_init, args=(x, y))
p_lsq_r = leastsq(residuals_func_regularization, p_init, args=(x, y))
print(p_lsq[0])
print(p_lsq_r[0])
plt.plot(x_point, real_func(x_point), label = 'real')
plt.plot(x_point, fit_func(p_init, x_point), label='init')
plt.plot(x_point, fit_func(p_lsq[0], x_point), label='fitted')
plt.plot(x_point, fit_func(p_lsq_r[0], x_point), label='fitted_r')
plt.legend()
plt.show()
