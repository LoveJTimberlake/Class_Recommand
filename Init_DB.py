#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 14:23:06 2018

@author: justintimberlake
"""

#数据库创建时要用charser utf-8


import pymysql 

print('User Name:')
user_name = input()
print('Password:')
pw = input()

#连接数据库
db = pymysql.connect(host = 'localhost',user = user_name,password = pw,db = 'class', charset = 'utf8mb4',cursorclass = pymysql.cursors.DictCursor)	#doubts			数据库权限初始化：grant all  on *.* to 'mozart'@'localhost' identified by 'mozewei19980206';

Tag_List = []   #除了专业学科标签以外再加上[有趣，困难，严格]（后面再加）

#学生基本信息表
cursor_1 = db.cursor()
init_SI = '''Create Table Stu_Info(
            Stu_ID varchar(20) NOT NULL primary key,
            Stu_Gender varchar(20) NOT NULL default('unknown'),
            Stu_Major varchar(50) NOT NULL,
            Stu_InYear varchar(20) NOT NULL,
            Stu_Grade varchar(20) NOT NULL,
            Stu_Aca varchar(100) Not NULL,
            Stu_Password varchar(20) NOT NULL,
            Stu_Name varchar(20) NOT NULL  
            )'''        #Aca表示学院
cursor_1.execute(init_SI)
db.commit()
cursor_1.close()

#课程基本信息表        同样一门课，不同老师教，上课不同，其ID也不一样 class_StartTime表达方式是day-order  如星期一第一节课  1-1  然后len 是 2  
cursor_2 = db.cursor()
init_CI = '''Create Table Cla_Info(
            Cla_ID varchar(20) NOT NULL primary key,
            Cla_Title varchar(50) NOT NULL,
            Cla_StartTime varchar(40) NOT NULL,
            Cla_Len varchar(40) NOT NULL,
            Cla_Teacher varchar(50) NOT NULL,
            Cla_Room varchar(20) NOT NULL,
            Cla_Weeks varchar(50) NOT NULL,
            Cla_Term varchar(20) NOT NULL
            )'''        #Start_Time表示上课时间，可有多个 如 '1-1,3-3' Len表示每一节课的课时，可有多个 Term表示一门课开设的学期 为2019-1 的格式
cursor_2.execute(init_CI)
db.commit()
cursor_2.close()

#课程额外信息表    #包括该课程的考核方式 考勤频率 内容难度 内容有趣程度  老师好评....
cursor_3 = db.cursor()
init_CEI = '''Create Table Cla_ExtraInfo(
            Cla_ID varchar(20)  NOT NULL primary key,
            Cla_Exam varchar(20) NOT NULL default 'unknown',
            Cla_Freq varchar(20) NOT NULL default 'unknown',
            Cla_Diff double(2,1) Not NULL default 0,
            Cla_Interest double(2,1) NOT  NULL default 0,
            Cla_Teacher_Score double(2,1) NOT NULL default 0,
            Cla_Score double(2,1) NOT NULL default 0,
            Cla_Have_Been_Num int(4) NOT NULL default 0,
            Cla_Comment_Num int(4) NOT NULL default 0,
            Cla_Now_Stu_Num int(4) NOT NULL default 0
            )'''    #have_been_num 表示已经上过的人 comment_num表示已经评论了的人
cursor_3.execute(init_CEI)
db.commit()
cursor_3.close()

#课程评论信息表    time表示年份加月份
cursor_4 = db.cursor()
init_CCI = '''Create Table Cla_Comment(
            Cla_ID varchar(20) NOT NULL primary key,
            Stu_ID varchar(20) NOT NULL,
            Helpful_Score int NOT NULL default 0,
            Text varchar(200) NOT NULL,
            Time varchar(30) NOT NULL,
            Score int(4) NOT NULL,
            Comment_ID varchar(10) NOT NULL
            )'''
cursor_4.execute(init_CCI)
db.commit()
cursor_4.close()

#学生选课行为表（若取消选课则从该表中删除）  在新用户登陆后，将其当前已选课程传回
cursor_5 = db.cursor()
init_SCC = '''Create Table Stu_Cho_Class(
            Stu_ID varchar(20) NOT NULL primary key,
            Cla_ID varchar(20) NOT NULL,
            Term varchar(30) NOT NULL, 
            )'''        #Term的格式是 2018-1 2018年第一个学期
cursor_5.execute(init_SCC)
db.commit()
cursor_5.close()

#课程特征表      #平常是放进内存里进行运算，但是要一定间隔后存入表中
cursor_6 = db.cursor()
init_CF = '''Create Table Cla_Feat(
            Cla_ID varchar(20) NOT NULL primary key,
            %s double(5,2) NOT NULL default 0
        )'''%(Tag_List[0])
cursor_6.execute(init_CF)
for i in range(1,len(Tag_List)):
    add_Feat = 'alter Table Cla_Feat add %s double(5,2) NOT NULL default 0' %(Tag_List[i])
    cursor_6.execute(add_Feat)
db.commit()
cursor_6.close()

#学生特征表
cursor_7 = db.cursor()
init_SF = '''Create Table Stu_Feat(
            Stu_ID varchar(20) NOT NULL primary key,
            %s double(5,2) NOT NULL default 0
            )'''%(Tag_List[0])
cursor_7.execute(init_SF)
for i in range(1,len(Tag_List)):
    add_Feat = 'alter Table Stu_Feat add %s double(5,2) NOT NULL default 9' %(Tag_List[i])
    cursor_7.execute(add_Feat)
db.commit()
cursor_7.close()








