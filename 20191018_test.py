import datetime
today = datetime.date.today()
formatted_today=today.strftime('%y%m%d')
print(type(formatted_today))
print(formatted_today)