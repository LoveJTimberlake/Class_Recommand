#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 16:02:56 2018

@author: justintimberlake
"""

import pymysql 
import numpy

#"%s" -> "\'%s\'"
#f-string不能用

user_name = 'root'
pw = 'root'

#db = pymysql.connect(host = 'localhost',user = user,password = pw,db = 'class', charset = 'utf8mb4',cursorclass = pymysql.cursors.DictCursor)	#doubts			数据库权限初始化：grant all  on *.* to 'mozart'@'localhost' identified by 'mozewei19980206';

class Data_Op:
    def __init__(self):
        self.db = pymysql.connect(host = 'localhost',user = user,password = pw,db = 'class', charset = 'utf8mb4',cursorclass = pymysql.cursors.DictCursor)
        self.feats_list = []   #需要一开始初始化
        
#存储新学生的信息 
    def Store_NewStuInfo(self,info):    #info是字典 由json信息在flask那里得到再传过来
        cursor = self.db.cursor()
        result = {}
        Add_Stu_Info = "Insert INTO Stu_Info(Stu_ID,Stu_Gender,Stu_Major,Stu_InYear,Stu_Grade,Stu_Aca,Stu_Password,Stu_Name) values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')"%(info['stu_id'],info['gender'],info['major'],info['inyear'],info['grade'],info['aca'],info['password'],info['name'])
        cursor.execute(Add_Stu_Info)
        self.db.commit()
        cursor.close()

#返回该学生的课表
    def Return_StuClaTable(self,info):   #返回一个dict的信息 课程:其基本信息
        #info中包括的是学生ID + 要查看的选课学期 哪个学期的课
        cursor= self.db.cursor()
        result = {}
        search_classes = "select Cla_ID from Stu_Cho_Class where Stu_ID = \'%s\' and Term = \'%s\'" %(info['stu_id'],info['term'])
        cursor.execute(search_classes)
        All_Classes = [] 
        for d  in cursor.fetchall():
            All_Classes.append(d['Cla_ID'])
        
        #当选择的选课学期上该学生没有选课（历史记录上也没有）时
        if len(All_Classes) == 0:
            result['class_num'] = 0
            return result 
        else:
            result['class_num'] = len(All_Classes)
        
        for class_id in All_Classes:
            result[class_id] = {}
            get_class_info = "select * from Cla_Info where Cla_ID = \'%s\'" %class_id
            cursor.execute(get_class_info)
            class_info = cursor.fetchone()  #dict类型
            for class_feat in ['Cla_ID','Cla_Title','Cla_StartTime','Cla_Len','Cla_Teacher','Cla_Room','Cla_Weeks','Cla_Term']:
                result[class_id][class_feat] = class_info[class_feat]
        cursor.close()
        return result
        
#学生修改他的信息
    def Change_StuInfo(self,new_info):   #new_info中包括了完整的学生信息
        cursor = self.db.cursor()
        result = {}
        update_stu_info = "update Stu_Info set Stu_Gender = \'%s\', Stu_Major = \'%s\', Stu_Inyear = \'%s\', Stu_Grade = \'%s\', Stu_Aca = \'%s\',Stu_Password = \'%s\',Stu_Name = \'%s\' where Stu_ID = \'%s\'"%(new_info['gender'], new_info['major'],new_info['inyear'],new_info['grade'], new_info['aca'],new_info['password'],new_info['name'],new_info['stu_id'])
        cursor.execute(update_stu_info)
        self.db.commit()
        cursor.close()
        
        
#学生添加课程
    def Stu_Add_Cla(self,info):  #time去classinfo的表里面查 里面只有 stu_id 与 cla_id
        cursor = self.db.cursor()
        get_class_time = "select * from Cla_Info where Cla_ID = \'%s\'" %(info['cla_id'])
        cursor.execute(get_class_time)
        class_time = cursor.fetchone()['Cla_Term']
        stu_add_class = "Insert INTO Stu_Cho_Class(Stu_ID,Cla_ID,Term) values(\'%s\',\'%s\',\'%s\')"%(info['stu_id'],info['cla_id'],class_time)
        cursor.execute(stu_add_class)
        increase_cla_stu_num = "update Cla_ExtraInfo set Cla_Now_Stu_Num = Cla_Now_Stu_Num + 1, Cla_Have_Been_Num = Cla_Have_Been_Num + 1 where Cla_ID = \'%s\'"%info['cla_id']
        cursor.execute(increase_cla_stu_num)
        self.db.commit()
        cursor.close()
        
#学生取消已选课程
    def Stu_Del_Cla(self,info):
        cursor = self.db.cursor()
        del_class = "delete from Stu_Cho_Class where Stu_ID = \'%s\'and Cla_ID = \'%s\'"%(info['stu_id'],info['cla_id'])
        cursor.execute(del_class)
        decrease_cla_stu_num = "update Cla_ExtraInfo set Cla_Now_Stu_Num = Cla_Now_Stu_Num - 1, Cla_Have_Been_Num = Cla_Have_Been_Num - 1 where Cla_ID = \'%s\'"%info['cla_id']
        cursor.execute(decrease_cla_stu_num)
        self.db.commit()
        cursor.close()

#学生评论课程
    def Stu_Com_Cla(self,info):
        cursor = self.db.cursor()
        
        #生成该评论的ID
        get_com_total_num = 'select Comment_ID from Cla_Comment'
        cursor.execute(get_com_total_num)
        com_total_num = len(cursor.fetchall())      #要回去试验对空表这样操作的结果
        comment_id = str(com_total_num + 1)
        
        add_comment = f"Insert INTO Cla_Comment(Cla_ID,Stu_ID,Text,Time,Score,Comment_ID) values(\'%s\',\'%s\',\'%s\',\'%s\',%s,\'%s\')"%(info['cla_id'],info['stu_id'],info['comment'],info['time'],info['score'],comment_id)
        cursor.execute(add_comment)
        increase_cla_com_num = "update Cla_ExtraInfo set Cla_Comment_Num = Cla_Comment_Num + 1 where Cla_ID = \'%s\'" %info['cla_id']
        cursor.execute(increase_cla_com_num)

        #对课程分数进行修改
        #先获取课程平均分与被评论次数
        get_avescore_num = 'select Cla_Comment_Num, Cla_Score from Cla_ExtraInfo where Cla_ID = \'%s\''%(info['cla_id'])
        cursor.execute(get_avescore_num)
        needed_info_dict = cursor.fetchone()
        origin_ave = needed_info_dict['Cla_Score']
        comment_num = needed_info_dict['Cla_Comment_Num']
        origin_score = origin_ave * comment_num
        #在原分数基础上加上这次的分数最后求出最终的平均分数
        new_ave = round((origin_score + info['score'])/(comment_num + 1),1)
        new_comment_num = comment_num + 1 

        cursor.execute('update Cla_ExtraInfo set Cla_Comment_Num = %s,Cla_Score = %s where Cla_ID = \'%s\''%(new_comment_num,new_ave,info['cla_id']))

        self.db.commit()
        cursor.close()
        
        #返回评论的ID
        return {'comment_id':comment_id}
        
#学生取消评论课程
    def Stu_Del_Com_Cla(self,info):
        cursor = self.db.cursor()
        #先获取这次的分数
        get_comment_score = 'select Score from Cla_Comment where Cla_ID = \'%s\''%(info['comment_id'])
        cursor.commit(get_comment_score)
        comment_score_dict = cursor.fetchone()
        comment_score = comment_score_dict['Score']

        del_comment = "delete from Cla_Comment where Comment_ID = \'%s\'" %info['comment_id']
        cursor.execute(del_comment)
        reduce_cla_com_num = "update Cla_ExtraInfo set Cla_Comment_Num = Cla_Comment_Num - 1 where Cla_ID = \'%s\'" %info['cla_id']
        cursor.execute(reduce_cla_com_num)

        get_avescore_num = 'select Cla_Comment_Num, Cla_Score from Cla_ExtraInfo where Cla_ID = \'%s\''%(info['cla_id'])
        cursor.execute(get_avescore_num)
        needed_info_dict = cursor.fetchone()
        origin_ave = needed_info_dict['Cla_Score']
        comment_num = needed_info_dict['Cla_Comment_Num']
        origin_score = origin_ave * comment_num
        #在原分数基础上加上这次的分数最后求出最终的平均分数
        new_ave = round((origin_score - comment_score)/(comment_num - 1),1)
        new_comment_num = comment_num - 1 

        cursor.execute('update Cla_ExtraInfo set Cla_Comment_Num = %s,Cla_Score = %s where Cla_ID = \'%s\''%(new_comment_num,new_ave,info['cla_id']))


        self.db.commit()
        cursor.close()
        
#学生给评论点赞
    def Stu_Star_Com(self,info):
        cursor = self.db.cursor()
        add_comment_star = "update Cla_Comment set Helpful_Score = HelpfulScore + 1 where Comment_ID = \'%s\'" %info['comment_id']
        cursor.execute(add_comment_star)
        self.db.commit()
        cursor.close()
        
#学生给评论取消点赞
    def Stu_UnStar_Com(self,info):
        cursor = self.db.cursor()
        add_comment_star = "update Cla_Comment set Helpful_Score = HelpfulScore - 1 where Comment_ID = \'%s\'" %info['comment_id']
        cursor.execute(add_comment_star)
        self.db.commit()
        cursor.close()

#学生查看课程额外信息
    def Return_ClaExInfo(self,info):
        cursor = self.db.cursor()
        result = {}
        
        find_cla_extrainfo = "select * from Cla_ExtraInfo where Cla_ID = \'%s\'" %info['cla_id']
        cursor.execute(find_cla_extrainfo)
        cla_extrainfo = cursor.fetchone()
        for key,value in cla_extrainfo.items():
            result[key] = value
        cursor.close()
        
        return result
        
#返回该课程的评价
    def Return_ClaComment(self,info):
        cursor = self.db.cursor()
        get_cla_comments = " select * from Cla_Comment where Cla_ID = \'%s\'" %info['cla_id']
        cursor.execute(get_cla_comments)
        all_comments = cursor.fetchall()
        if len(all_comments) == 0:
            result['Top_Comments'] = 'None'
            result['All_Comments'] = 'None'
            return result
        #对其进行排序
        
        #按照评论star数进行排序
        sorted_bystar_comments = sorted(all_comments, key = lambda x: x.__getitem__('Helpful_Score'), reverse = True)
        Top_5_Star_Comments_Info = [x for x in sorted_bystar_comments[:5]]
        
        #按照评论时间进行排序
        sorted_bytime_comments = sorted(all_comments, key = lambda x : x.__getitem__('Time'), reverse = True)
        for x in Top_5_Star_Comments_Info:
            if x in sorted_bytime_comments:
                sorted_bytime_comments.remove(x)
        
        cursor.close()
        result = {} 
        result['Top_Comments'] = Top_5_Star_Comments_Info 
        result['All_Comments'] = sorted_bytime_comments
        return result
        
        
#给课程添加额外信息 （通过现有资料填充） 对于同一个老师讲授的不同时期的同一内容的课，我们使用不同的ID 
#在已有2018-01《中国文化概论》的情况下 要增加2018-02《中国文化概论》的额外信息时，需要根据cla_title cla_teacher来选择旧的已有课程信息 从而获取其Cla_ID来获取其extrainfo 然后叠加到新的课程中
    '''
    def Add_ClaExInfo(self,info):
        cursor = self.db.cursor()
        add_cla_extrainfo = f"Update Cla_ExtraInfo set Cla_Exam = {info['cla_exam']}, Cla_Freq = {info['cla_freq']}, Cla_Diff = {info['cla_diff']}, Cla_Interest = {info['cla_interest']}, Cla_Teacher_Score = {info['cla_teacher_score']}, Cla_Have_Been_Num = {info['cla_have_been_num']}, Cla_Comment_Num = {info['cla_comment_num']}, Cla_Now_Stu_Num = {info['cla_now_stu_num']} where Cla_ID = {info['cla_id']}"
        cursor.execute(add_cla_extrainfo)
        self.db.commit()
        cursor.close()
    '''

#info是在推荐系统模块中的功能计算出该学生一定行为后带给其的分数更改
#Example:
#推荐系统中得到的权重是一个理工科的学生选了一门《中国语文》并且收藏了（或还给了好评）表示这位学生对这门课可能有好感 那么这门课的非理工属性给这位学生
#增加的个人偏好向量分量值更大。添加的这个值不可以只依靠其评分 还需要依靠这个人的四类标签(初期假设)的权重分布  非文科类的权重若越大，则表明这个人对
#这门课所代表的学科爱恨程度越大    对于特征向量 其分量值的区间为[0,5]              
        
        
#在数据库中更新学生特征  更新特征时要一个一个对应加上去 所以比较繁琐 后面再弄  
#隔一段时间运行该函数将特征矩阵存入数据库中
#在用户编辑标签时则给其赋予最高分
    '''
    def Update_StuFeats(self,info,matrix):  #info里面包括了User_id list  还有feat list
        cursor = self.db.cursor()
        feat_list = info['feat_list']
        user_id_list = info['user_list']
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                update_stu_feat = f'update Stu_Feat set {feat_list[j]} = {matrix[i,j]} where Stu_ID = {user_id_list[i]}'
                cursor.execute(update_stu_feat)
        self.db.commit()
        cursor.close()
    '''
                            
        
#在数据库中更新课程特征  
    def Update_ClaFeats(self,info):     #info中有 cla_id feats
        cursor = self.db.cursor()
        feat_list = info['feats']
        class_id = info['cla_id']
        for i in range(len(feat_list)):
            update_cla_feat = 'update Cla_Feat set %s = %s where Cla_ID = %s'%(self.feats_list[i],%feat_list[i],class_id)
            cursor.execute(update_cla_feat)

        self.db.commit()
        cursor.close()

#获得用户之前没上过的课
    def Get_Class_NotinPast(self,info): #info中有class_id curr_term 查找的可上课程应是过滤了当前学期的课程之后的结果
        All_Class_ID = [] 
        Ava_Class_ID = []
        Had_Class_ID = []
        cursor = self.db.cursor()
        get_all_class_id = 'select Cla_ID from Cla_Info'
        cursor.execute(get_all_class_id)
        for row in cursor.fetchall():
            All_Class_ID.append(row['Cla_ID'])
        cursor.execute('select Cla_ID from Stu_Cho_Class where Stu_ID =\'%s\''%(info['stu_id']))
        for row in cursor.fetchall():
            Had_Class_ID.append(row['Cla_ID'])
        cursor.close()
        for uk_class in All_Class_ID:
            if uk_class not in Had_Class_ID:
                Ava_Class_ID.append(uk_Class)
        
        return Ava_Class_ID
        

#根据学生id与当前学期来获得该学生这个学期所有可以上的课及其信息
    def Get_Available_Class(self,info):     #info有 stu_id curr_term
        #先构造出表示当前课表的矩阵
        cursor = self.db.cursor()
        now_class_dict = self.Return_StuClaTable(info)
        #该形式为：now_class_dict = {'a':{'Cla_Start_Time':'1-1,2-3','Cla_Len':'2'}}
        Origin_Class_Table = np.zeros((11,7))
        for per_class,per_class_info in now_class_dict.items():
            times = per_class_info['Cla_StartTime'].split(',')
            for i in range(len(times)):
                times[i] = str(times[i])
            class_length = int(per_class_info['Cla_Len'])
            lengths = [class_length for x in range(len(times))]
            for i in range(len(times)):
                day = int(times[i].split('-')[0])
                order = int(times[i].split('-')[1])
                Origin_Class_Table[order-1:order-1+ lengths[i],day-1] = [x %(x-1) for x in range(3,3+lengths[i])]
            
        #然后在课程信息的表中找出用户还未上过的课
        Choosable_ClassID_List = self.Get_Class_NotinPast(info)
        #先获取未上过的课的信息
        cursor.execute('select * from Cla_Info')
        All_Free_Classes_Info = cursor.fetchall()
        Final_Free_Classes_List = []
        for per_free_class_info in All_Free_Classes_Info:
            times = per_free_class_info['Cla_StartTime'].split(',')
            for i in range(len(times)):
                times[i] = str(times[i])
            class_length = int(per_free_class_info['Cla_Len'])
            lengths = [class_length for x in range(len(times))]
            for i in range(len(times)):
                day = int(times[i].split('-')[0])
                order = int(times[i].split('-')[1])
                length = lengths[i]
                if Origin_Class_Table[order-1:order-1+ lengths[i],day-1].sum() == 0:
                    Final_Free_Classes_List.append(per_free_class_info)
        cursor.close()
        return Final_Free_Classes_List

    def Get_User_Feats(self,info):
        cursor = self.db.cursor()
        cursor.execute('select * from Stu_Feat where Stu_ID = \'%s\''%(info['stu_id']))
        feats_dict = cursor.fetchone()
        feats_dict.pop('Stu_ID')
        feats_vector = []
        for k,v in feats_dict.items():
            feats_vector.append(v)
        cursor.close()
        return feats_vector

    def Get_Cla_Feats(self,info):  #传入的是info:{'cla_id':[,,]}
        All_Classes_Feats = []
        cursor = self.db.cursor()
        for class_id in info['cla_id']:
            cursor.execute('select * from Cla_Feat where Cla_ID = \'%s\''%(class_id))
            feats_dict = cursor.fetchone()
            feats_dict.pop('Cla_ID')
            feats_vector = []
            for k,v in feats_dict.items():
                feats_vector.append(v)
            All_Classes_Feats.append(feats_vector)
        cursor.close()
        return All_Classes_Feats
        
    def Get_Cla_BasicInfo(self,info):  #info: {'cla_id':id1}
        cursor = self.db.cursor()
        class_id = info['cla_id']
        get_cla_basic_info = 'select * from Cla_Info where Cla_ID = \'%s\''%(class_id)
        cursor.execute(get_cla_basic_info)
        class_basicinfo_dict = cursor.fetchone()
        cursor.close()
        return class_basicinfo_dict

    def Search_Class(self,info):
        cursor = self.db.cursor()
        result = []
        condition = info['condition']  #这个名词默认是课程名字中的字段 
        condition = str(condition)
        #先选择所有的课程名字
        get_all_title = 'select * from Cla_Info'
        cursor.execute(get_all_title)
        all_basic_info = cursor.fetchall()  #所有课程的所有基本信息
        #匹配名字
        for d in all_basic_info:
            if condition in str(d['Cla_Title']):
                cur_info = d.copy()
                get_extra_info = "select * from Cla_ExtraInfo where Cla_ID = \'%s\'"%(d['Cla_ID'])
                cursor.execute(get_extra_info)
                extra_info_dict = cursor.fetchone()
                for extra_info_key in extra_info_dict.keys():
                    if extra_info_key not in d.keys():
                        cur_info[extra_info_key] = extra_info_dict[extra_info_key]
                result.append(cur_info)
        cursor.close()
        return result
        
    def Login_Verify(self,info):
        cursor = self.db.cursor()
        result = 'unknown'
        cursor.execute('select Stu_Password from Stu_Info where Stu_ID = \'%s\''%(info['stu_id']))
        correct_password = cursor.fetchone()['Stu_Password']
        if info['password'] == correct_password:
            result = 'yes'
        else:
            result = 'no'
        cursor.close()
        return result
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        


