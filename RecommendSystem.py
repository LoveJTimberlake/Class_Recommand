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

	def Return_RecommendList(self,user_id):
        
        
	def Get_AvaliableClasses(self,user_id,curr_time):
        #先获取该用户现在所有可上的课
        

	def Return_HighestClasses(self,class_list):


	def Sort_ByTime(self,class_list):


	def ChangeClass_Score(self):








