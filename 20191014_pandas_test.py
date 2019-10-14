import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

"""
Series 数据结构
DataFrame 数据结构
"""
# print(help(pd.Series))
test_Series = pd.Series([1,2,3,4])
print(test_Series)

indexs_date = pd.date_range(end='20191014', periods=6)
test_DataFrame = pd.DataFrame(np.random.randn(6,4), index=indexs_date, columns=['x', 'y', 'z', 'o'])

print('test_DataFrame:----------------------------------------------------------------------------')
print(test_DataFrame)

print('test_DataFrame[\'x\']:----------------------------------------------------------------------------')
print(test_DataFrame['x'])

test_reshape = np.arange(12).reshape(3,4)
print(test_reshape)
test_DataFrame = pd.DataFrame(test_reshape)
print(test_DataFrame)
print(test_DataFrame.describe())

csv_data = pd.read_csv('11304.csv')
print(csv_data)
csv_data.to_pickle('11304.pickle')

plt_DataFrame = pd.DataFrame(np.random.randn(10,4), index=np.random.randn(10), columns=['A','B','C','D'])
print(plt_DataFrame)
sum_DataFrame = plt_DataFrame.cumsum()
print(sum_DataFrame)
png = sum_DataFrame.plot()
sum_DataFrame.plot.scatter(x='A', y='B', color='DarkBlue', label='class1', ax=png)
plt.savefig('sum_DataFrame')

# plt.show()



"""
pd.date_range(start=None, end=None, periods=None, freq=None, tz=None, normalize=False, name=None, closed=None, **kwargs)
"""
# print(help(pd.Series))
print('test pd.date_range():-----------------------------------------------------------------------------')
t_right = pd.date_range(start='1/1/2019', end='10/1/2019', freq='5H', closed='right')
t_left = pd.date_range(start='1/1/2019', end='10/1/2019', freq='5H', closed='left')
# print(help(pd.date_range))
print(t_right)
print(t_left)


