import pandas as pd
import numpy as np
import re
import csv
import json


if __name__ == '__main__':
    total = []
    paths = ['抽卡.csv', '奖励1.csv', '奖励2.csv', '奖励3.csv']
    for path in paths:
        one = pd.read_csv(path)
        exist = 0
        for settle in np.array(one.iloc[:, :]):
            exist = 0
            for user in total:
                if user[0] == settle[0]:
                    exist = 1
                    user.extend(settle[1:])
            if exist == 0:
                user = []
                user.extend(settle[:])
                total.append(user)

    for x in total:
        print(x)
    with open('second.csv', 'w', newline='') as f:
        f_csv = csv.writer(f)
        for info in total:
            if info[0] != float('nan'):
                f_csv.writerow(info)