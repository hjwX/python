import pandas as pd
import numpy as np
import re
import csv
import json

def settle_redmoon_battle(path, seasonId):
    redmoon_settles = pd.read_csv(path)
    # print(redmoon_settles)
    headers = ['战场编号', '势力', '一局城市数', '二局城市数', '三局城市数', '四局城市数', '五局城市数', '六局城市数', '七局城市数', '八局城市数', '九局城市数', ]
    infos = []
    oneTotalCity = ["total",1,0,0,0,0,0,0,0,0,0]
    twoTotalCity = ["total",2,0,0,0,0,0,0,0,0,0]
    threeTotalCity = ["total",3,0,0,0,0,0,0,0,0,0]
    infos.append(headers)
    for settle in np.array(redmoon_settles.iloc[:, [0, 1, 2]]):
        info = []
        info.append(str(settle[0]).replace(seasonId, ''))
        info.append(settle[1])
        # print(settle[2])
        # reg = r'{.*?}'
        reg = r'"afterCitys":\[(.*?)\]'
        afters = re.findall(reg, settle[2])
        afters = [len(i.split(',')) for i in afters]
        info.extend(afters)
        if info[1] == 1:
            for i in range(9):
                oneTotalCity[2+i] += info[2+i]
        if info[1] == 2:
            for i in range(9):
                twoTotalCity[2+i] += info[2+i]
        if info[1] == 3:
            for i in range(9):
                threeTotalCity[2+i] += info[2+i]
        infos.append(info)
    infos.append(oneTotalCity)
    infos.append(twoTotalCity)
    infos.append(threeTotalCity)
    print(infos)
    with open(seasonId +'_battle_info.csv', 'w', newline='') as f:
        f_csv = csv.writer(f)
        for info in infos:
            f_csv.writerow(info)

def settle_redmoon_userInfo():
    user_infos = pd.read_csv('user_info_0.csv')
    infos = []
    headers = ['userId', '局数', '攻击的城市数', '攻击的势力数', '分数' ,'应援城市']
    infos.append(headers)
    all_user_info = user_infos.append(pd.read_csv('user_info_1.csv'))
    for settle in np.array(all_user_info.iloc[:, [0, 1, 2]]):
        atks_citys = re.findall(r'atkCitys":\[(.*?)\]', settle[2])
        atk_partys = re.findall(r'atkPartys":\[(.*?)\]', settle[2])
        scores = re.findall(r'score":(.*?),', settle[2])
        supportCitys = re.findall(r'supportCity":(.*?)}', settle[2])
        for i in range(9):
            info = []
            info.append(settle[0])
            info.append(i+1)
            info.append(atks_citys[i])
            info.append(atk_partys[i])
            info.append(scores[i])
            info.append(supportCitys[i])
            infos.append(info)
    print(len(infos))
    with open('user_info.csv', 'w') as f:
        f_csv = csv.writer(f)
        f_csv.writerows(infos)
    pass

if __name__ == '__main__':
    settle_redmoon_battle('191016_battle.csv', '191016')
   # settle_redmoon_userInfo()

