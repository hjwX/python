import numpy as np
from scipy.optimize import leastsq
#   3     2
#1 x + 2 x + 3 x + 4
#poly1d
p = np.poly1d([1,2,3,4])
print(type(p))
print(p)
#    3     2
# 1 z + 2 z + 3 z + 4
p = np.poly1d([1,2,3,4], variable='z')
print(p)

#linspace
#               start end num
x = np.linspace(0, 1, 10, endpoint=True, retstep=True)
print(x)
# print(help(np.linspace))

print(help(leastsq))
