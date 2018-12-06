# coding=utf-8

import pymysql 

user = 'root'
pw = 'root'
db = pymysql.connect(host = 'localhost',user = user,password = pw,db = 'class', charset = 'utf8mb4',cursorclass = pymysql.cursors.DictCursor)
cursor = db.cursor()
Tag_List = ['机械','建筑','美术','音乐','土木','电力','电子','材料','化学','生物','物理','体育','计算机','数学','金融','经济学','工管','自动化','新传','法律','外语','医学','有趣','困难','严格']   #除了专业学科标签以外再加上[有趣，困难，严格]（后面再加）
fr = open(r'class_info.txt')
for line in fr.readlines():
	line = line.split(' ')
	basic_sql = "Insert Into Cla_Info(Cla_ID,Cla_Title,Cla_StartTime,Cla_Len,Cla_Teacher,Cla_Room,Cla_Weeks,Cla_Term) values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')"%(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7])
	extra_sql = "Insert into Cla_ExtraInfo(Cla_ID,Cla_Exam,Cla_Freq,Cla_Diff,Cla_Interest,Cla_Teacher,Cla_Score,Cla_Have_Been_Num,Cla_Comment_Num,Cla_Now_Stu_Num) values(\'%s\',\'%s\',\'%s\',%s,%s,%s,%s,%s,%s,%s)"%(line[0],line[8],line[9],line[10],line[11],line[12],line[13],line[14],line[15],line[16])
	cursor.execute(basic_sql)
	cursor.execute(extra_sql)
	db.commit()

fr.close()

fr2 = open(r'class_feat.txt')

for line in fr2.readlines():
	line = line.split(' ')
	insert_class_sql = 'insert into Cla_Feat(Cla_ID) values(\'%s\')'%(line[0])
	for i in range(len(Tag_List)):
		init_feat_sql = 'update Cla_Feat set %s = %s where Cla_ID = \'%s\''%(Tag_List[i],int(line[i+1]),line[0])
		cursor.execute(init_feat_sql)
		db.commit()
fr2.close()

fr3.open(r'stu_choose_class.txt')
for line in fr3.readlines():
	line = line.split(' ')
	stu_cho_cla_sql = 'insert into Stu_Cho_Class(Stu_ID,Cla_ID,Term) values(\'%s\',\'%s\',\'%s\')'%(line[0],line[1],line[2])
	cursor.execute(stu_cho_cla_sql)
	db.commit()

fr3.close()





























