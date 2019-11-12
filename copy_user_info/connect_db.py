import pymysql

step = 1000000
tabel_name = 'pjxx'

def getConnect(userId):
    index = userId%step
    part = tabel_name + str(index)
    connect = pymysql.connect(host='10.17.1.171',user='dev',passwd='aoladev',db='pjxx0',port=3306,charset='utf8')
    cursor = connect.cursor()
    cursor.execute("select * from t_item where userId = 15103")
    fields = cursor.description
    for i in fields:
        print(i[0])
    for info in cursor.fetchone():
        print(type(info))

if __name__ == '__main__':
    getConnect(1)
