#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 16:00:57 2018

@author: justintimberlake
"""

import numpy as np
import math 
import pymysql 
import Get_Store_Data as gsd


#推荐系统     从数据库获取数据并在内存中进行必要计算与返回推荐结果

#冷启动推荐（新用户填完信息后）


#在对评论的NLP处理中，将所有的维度列出来，每一个维度单独训练一个模型，对一个评论，将其放入每一个模型进行训练，

#由于课程的专选性   很多课都是学生一定要上的  那些不能反映其兴趣，但是可以一定程度上
#反映学生的方向  但是我们的RS需要考虑到学生对其课表上的空余时间上的课才会有更大的兴趣
#同时同专业学生之间的相似性很容易很大  所以要更加依赖于标签来过滤

#所以优先从课表上可以上的课里面挑选出备选课表L1

#然后根据用户定义的标签选出评分最好的同时又在L1中的课程列表L2     

#同时又将L2中的课按照用户在对应时段上的课的个数进行排序   少的排后面

#同时对于课程   初始先给均分  然后根据用户对其的评分进行课程tag分数调整

class Class_RS:
	def __init__(self):
		self.Taglist = [] 
		self.ClassList = []
		self.DataGetter = gsd.Data_Op()   
        
	def Return_RecommendList(self,user_id,curr_term):
        #先获取该用户现在所有可上的课
        info = {'stu_id':user_id,'term':curr_term}
        Choosable_ClassesInfo_List = self.DataGetter.Get_Available_Class(info)
        
        #获取用户的标签向量
        User_Feats = self.DataGetter.Get_User_Feats(info)
        #获取课程的标签向量
        class_info = {'cla_id':Choosable_ClassesInfo_List}
        Class_Feats = self.DataGetter.Get_Class_Feats(class_info)  #返回的是所有可上课程的标签多维数组

        #然后计算最近的课程(这个矩阵每一行对应着Choosable_ClassesInfo_List的每一个课程id)
        dist_dict = {} 
        for i in range(len(Class_Feats)):
        	dist = 0
        	dist_dict[Choosable_ClassesInfo_List[i]] = 0
        	for j in range(len(User_Feats)):
        		dist += math.sqrt(pow(Class_Feats[i][j] - User_Feats[j],2))
        	dist_dict[Choosable_ClassesInfo_List[i]] = dist 

        #对距离字典进行排序
        class_dist_list = sorted(dist_dict.items(), key = lambda x : x[1])
        Result_Classes_IDs = []
        for i in range(10):
        	Result_Classes_IDs.append(class_dist_list[i][0])

        #去取推荐课程的信息并返回
        Result_Classes_Infos = [] 
        for class_id in Result_Classes_IDs:
        	Result_Classes_Infos.append(self.DataGetter.Get_Cla_BasicInfo({'cla_id':class_id}))

        return Result_Classes_Infos








