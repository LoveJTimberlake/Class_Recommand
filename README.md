# Class_RS Docs

---------------------------
API:

1. URL: /user/new_user 当有新用户时传数据到该URL  传入数据：学生ID 学生性别 学生专业 学生入学学年 学生年级 学生学院  （全为字符串）返回数据：{'Error':error_message}  (当无错误信息时则error_message为0)

2. URL: /user/get_table  返回学生的课表   传入数据：学生ID  要查询的学期（格式如 '2019-1'）  返回数据：{class_id1:{'Cla_ID':,'Cla_Title':,...},class_id2:{'Cla_ID':,'Cla_Title':,...}}  当有错误时，则返回{'Error':error_message}

3. URL: /user/change_info 用户修改信息  传入数据：学生ID 学生性别 学生专业 学生入学学年 学生年级 学生学院 (全为字符串）  返回数据：{'Error':error_message}  (当无错误信息时则error_message为0)

4. URL: /user/add_cla 用户增加课程  传入数据：学生ID  课程ID （全为字符串）   返回数据：{'Error':error_message}  (当无错误信息时则error_message为0)

5. URL: /user/del_cla 用户删除课程  传入数据：学生ID  课程ID （全为字符串）   返回数据：{'Error':error_message}  (当无错误信息时则error_message为0)

6. URL: /user/com_cla 用户评价课程 传入数据：学生ID 课程ID 评论内容 评论时间 评分(int) 评论ID(int) (其余为字符串）  返回数据： {'comment_id':comment_id}

7. URL: del_com_cla 用户删除评论 传入数据 ： 评论ID(int) 课程ID(string)  返回数据： {'Error':error_message}  (当无错误信息时则error_message为0)

8. URL: /user/star_com 用户给评论点赞   传入数据： 评论ID(int)  返回数据： {'Error':error_message}  (当无错误信息时则error_message为0)

9. URL: /user/unstar_com 用户评论取消点赞  传入数据：评论ID(int)  返回数据：  {'Error':error_message}  (当无错误信息时则error_message为0)

10. URL: /user/cla_extra_info 用户查看课程额外信息  传入数据：课程ID(字符串）  返回数据： {class_id:{'Cla_ID':,'Cla_Title':,...}}

11. URL: /user/return_cla_comment 用户查看课程评论  传入数据：课程ID(字符串）  返回数据： {'Top_Comments':[...],'All_Comments':[...]}

12. URL: /user/login 用户登录 传入数据：用户ID(字符串） 用户密码（字符串（20位）） 返回数据：{'result': 0 } (密码错误时则返回{'result': 'Wrong Password or Account'}, 当有其他错误时则返回{'result':error_message}

13. URL: /user/search_class 用户查找课程 传入数据: 查找条件（字符串）  返回数据 {'classes':[ {'cla_id':'id1',...},{'cla_id':'id2',...},... ],'error':error_message}  
