# coding=utf-8 

import numpy as np 
import pymysql

print("User_Name:")
user_name = input() 
print("Password:")
pw = input()

db = pymysql.connect(host = 'localhost', user = user_name, password = pw, db = 'movie', charset = 'utf8mb4',cursorclass = pymysql.cursors.DictCursor)

Tag_List = list() 
#需要初始化

cursor = db.cursor()

#电影的标签表
Init_1 = """Create Tabel MTs(
		Movie_ID varchar(20) Not NULL primary key,
		%s double(5,2) NULL default 0 
		)""" %
cursor.execute(Init_1)

for i in range(1,len(Tag_List)):
	cursor.execute("alter Tabel MTs add %s double(5,2) null default 0" %(Tag_List[i]))















