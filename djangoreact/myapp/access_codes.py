import random
from datetime import datetime, date, time, timedelta
import mysql.connector

test = date.today().day
start_date = date.today()
end_date = start_date + timedelta(days=3)

print(start_date)
ran_num = random.randrange(0, 999999)
add_zeros = str(ran_num).zfill(6)
access_code = add_zeros
#print(access_code)


db = mysql.connector.connect(user = 'admin', database = 'OPI_Signup', host = 'PETERS-PC', password = 'Xopowaeda143!')
cursor = db.cursor()
query = "INSERT INTO access_codes (code, active, test2, test4) VALUES ({}, {}, str_to_date({}, '%Y-%m-%d'), {})".format(access_code, 1, test, end_date)
cursor.execute(query)
db.commit()