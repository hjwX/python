from tkinter import *
import subprocess
import chardet
import sys
import datetime
import os

root = Tk()
record = "Record.txt"
MAX_COUNT = 2000000000
# id range 1 - 128
BEGIN_ID = 11

var = StringVar()

root.title("redeemCodeGen")  #设置标题
root.geometry("400x200") #设置大小

def get_date():
    today = datetime.date.today()
    formatted_today = today.strftime('%y%m%d')
    return formatted_today

#生成兑换码开始index
def get_index(Type, num):
     print(Type,num)
     
     file = open(record, "r")
     before = []
     for eachline in file:
          before.append(eachline.strip().split("#"))
     file.close()

     file = open(record, "w")
     file.truncate()
     new_num = 0
     maxId = 0
     for eachId in before:
         if int(eachId[0]) > maxId:
             maxId = int(eachId[0])
         if int(eachId[1]) <= MAX_COUNT:
             eachId[1] = int(eachId[1]) + int(num)
             new_num = eachId[1]
     if maxId == 0:
         before.append([BEGIN_ID, num])
         new_num = num
         maxId = BEGIN_ID
     if new_num == 0:
         maxId +=1
         before.append([maxId, num])
         new_num = num

     for oneId in before:
          oneLine = str(oneId[0])
          for s in oneId[1:]:
               oneLine += "#" + str(s)
          file.write(oneLine)
          file.write('\n')
          
     file.close()
     return str(int(new_num) - int(num) + 1), str(maxId)
          
#生成兑换码的逻辑
def gen_code(x , y , z):        
        command = "java -jar redeemCode.jar"
        arg1 = y
        arg2, arg0= get_index(y ,z)
        arg3 = z
        cmd = [command,arg0,arg1,arg2,arg3]
        new_cmd = " ".join(cmd)
        print(new_cmd)
        stdout,stderr = subprocess.Popen(new_cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()
        encoding = chardet.detect(stdout)["encoding"]
        result = stdout.decode(encoding)
        file_path = './' + get_date()
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        fileName = file_path + '/' + x + ".txt"
        file = open(fileName, 'w')
        file.truncate()
        # print(result)
        strings = result.split("\n")
        for string in strings:
             file.write(string.strip())
             file.write("\n")
        file.close()
        return fileName + "---"+gen_sql(x, y, file_path)

def gen_sql(n, m, file_path):
    with open(file_path + '/' + n + ".txt") as f:
        with open(file_path + '/' + n +".sql", 'w') as sql_f:
            sql_f.writelines('INSERT INTO t_redeem_code (redeemCode, hasGotten, userId, type, id) VALUES')
            for line in f.readlines():
                line = line.strip()
                if len(line) == 0:
                    continue
                new_line = '(\'%s\', 0, 0, %d, %d),\n' % (line, int(m), int(n))
                sql_f.writelines(new_line)
    return n+".sql"

#获取数值
def reg():
          Id = e_id.get()
          Type = e_type.get()
          Num = e_num.get()
          len_id = len(Id)
          e_id.delete(0,len_id)
          len_type = len(Type)
          e_type.delete(0,len_type)
          len_num = len(Num)
          e_num.delete(0,len_num)
          
          if len_id == 0 or len_type == 0 or len_num==0:
               l_msg['text'] = '数据错误'
          else:
               var.set(gen_code(Id,Type,Num))

#第一行，兑换码的类型
l_id =Label(root,text='兑换码Id：')
l_id.grid(row=1,sticky=W)
e_id =Entry(root)
e_id.grid(row=1,column=1,sticky=E)
 
#第二行，兑换码的类型
l_type = Label(root,text='兑换码的类型：')
l_type.grid(row=2,sticky=W)
e_type = Entry(root)
e_type.grid(row=2,column=1,sticky=E)

#第三行，兑换码的数量
l_num = Label(root,text='兑换码的数量：')
l_num.grid(row = 3,sticky=W)
e_num = Entry(root)
e_num.grid(row=3,column=1,sticky=E)

#第三行登陆按扭，command绑定事件
b_login = Button(root,text='生成兑换码',command=reg)
b_login.grid(row=4,column=1,sticky=E)
 
#是否成功提示
l_msg = Label(root,text='')
l_msg.grid(row=5)

# 设置标签
l_way =Label(root,text='路径:')
l_way.grid(row=6,sticky=W)
l = Label(textvar=var, bg='white', width=29, height=1)  # 参数textvar不同于text,bg是backgroud
l.grid(row=6,column=1, sticky=E)


root.mainloop()
