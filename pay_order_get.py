import re

str
with open('web1_web-service_debug.txt', encoding='UTF-8') as f:
    str = f.read()

pay_orders = re.findall(r'jsonString:{(.*)}',str)

order_userIds = {}
for order in pay_orders:
    orderNO = re.findall(r'"outOrderNo":\"(.*?)\"', order)[0]
    userId = re.findall(r'"roleId":\"(.*?)\"', order)[0]
    order_userIds[orderNO] = userId

userId_orders = []
for k, v in order_userIds.items():
    user_order = []
    user_order.append(v)
    user_order.append(k)
    userId_orders.append(user_order)
print(userId_orders)


with open('web1_web-service_warn.txt', encoding='UTF-8') as f:
    str = f.read()
errors = re.findall(r'onesdkOrderId:.*? userId:(.*?) parOrderNew is null', str)
error_user = set(errors)
insert = 'INSERT ignore t_pay_order_new(`zoneId`, `userId`, `orderNo`, `callBackInfo`, `time`, `goodId`, `state`) VALUES (1, %s, %s, \'test\', \'2019-10-16 18:05:02\', 204, 0);'
for error in error_user:
    for order in userId_orders:
        if order[0] == error:
            print(insert % (error, order[1]))


