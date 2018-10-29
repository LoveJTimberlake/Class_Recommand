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
    )""" %Tag_List[0]
cursor.execute(Init_1)
cursor.commit()

for i in range(1,len(Tag_List)):
    cursor.execute("alter Tabel MTs add %s double(5,2) null default 0" %(Tag_List[i]))
cursor.commit()

#用户的标签表
Init_2 = """ Create Table UTs(
        User_ID varchar(20) Not NULL primary key,
        %s double(5,2) NULL default 0
        )"""%Tag_List[0]
cursor.execute(Init_2)
cursor.commit()

for i in range(1,len(Tag_List)):
    cursor.execute("alter Tabel UTs add %s double(5,2) NULL default 0" %Tag_List[i])
cursor.commit()

#用户的观影时间信息表
Init_3 = """Create Tabel UWMs(
        User_ID varchar(20) NOT NULL primary key,
        Date varchar(30) NOT NULL,
        Day_Time varchar(20) NOT NULL,
        Movie_ID varchar(20) NOT NULL,
        Watched_TimeLength int(10) NOT NULL default 0,
        Full_TimeLength int(10) NOT NULL
        )"""
cursor.execute(Init_3)
cursor.commit()

#用户评价信息表
Init_4 = """Create Tabel UCIs(
        User_ID varchar(20) NOT NULL,
        Movie_ID varchar(20) NOT NULL,
        Score int(4) NULL,
        Comment varchar(1000) NULL,
        Date varchar(30) NOT NULL,
        Day_Time varchar(30) NOT NULL
        )"""
cursor.execute(Init_4)
cursor.commit()

#电影信息表
Init_5 = """Create Tabel MIs(
        Movie_ID varchar(20) NOT NULL primary key,
        Directors varchar(50) NOT NULL,
        Actors varchar(500) NOT NULL,
        Pic_URLs varchar(500) NULL,
        Region varchar(20) NOT NULL,
        Date varchar(50) NOT NULL,
        Score int(4) NOT NULL default 0,
        Year varchar(10) NOT NULL,
        Name varchar(50) NOT NULL,
        TimeLength int(10) NOT NULL
        )"""
cursor.execute(Init_5)
cursor.commit()

#电影评价表
Init_6 = """Create Table MCs(
        Movie_ID varchar(20) NOT NULL,
        User_ID varchar(20) NOT NULL,
        Comment varchar(500) NOT NULL,
        Date varchar(50) NOT NULL,
        DayTime varchar(50) NOT NULL
        )"""
cursor.execute(Init_6)
cursor.commit()

#用户信息表
Init_7 = """Create Table UIs(
        User_ID varchar(20) NOT NULL primary key,
        Gender varchar(7) NOT NULL default 'unknown',
        Birth varchar(20) NOT NULL default 'unknown',
        Interest_Ms varchar(5000) NULL,
        Comments varchar(50000) NULL,
        Scores varchar(500) NULL,
        )"""
cursor.execute(Init_7)
cursor.commit()

db.commit()
db.close()





















