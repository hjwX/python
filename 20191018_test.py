import datetime
import sys
today = datetime.date.today()
formatted_today=today.strftime('%y%m%d')
print(type(formatted_today))
print(formatted_today)
for i in range(9):
    print(i)

print(sys.maxsize)

with open('oldRecord.txt', 'r') as f:
    for line in f:
        id = line.split('#')[0]
        print(int(id)%128)