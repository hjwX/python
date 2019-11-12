import pandas as pd
import numpy as np
import re
import csv

one = pd.read_csv('problem_user.csv')
insert = 'INSERT INTO `Problem_Users` (`accountType`, `accountName`, `userId`, `state`, `stateOp`, `nickname`, `startDateTime`, `endDateTime`, `latestHandler`, `cause`) VALUES;'
with open("problem_user.sql", 'w') as sql_f:
    sql_f.writelines('INSERT ignore `Problem_Users` (`accountType`, `accountName`, `userId`, `state`, `stateOp`, `nickname`, `startDateTime`, `endDateTime`, `latestHandler`, `cause`) VALUES')
    for settle in np.array(one.iloc[:, :]):
        rewardCode = []
        new_line = '(%s, \'%s\', %s, 2, 6, \' \', \'2019-03-05 10:55:38\', \'2029-03-05 10:55:38\', \'someone\', \'cheat\'),\n' % (settle[0], settle[2], settle[1])
        sql_f.writelines(new_line)



