# coding=utf-8

import pandas as pd
from flask import Flask
from flask import request
import pymysql

class FlaskServer():
    def __init__(self):
        app = flask(__name__)
        DB_conn = pymysql.connect(host = 'localhost', user = user_name, password = pw,db = 'movie', charset = 'utf8mb4',cursorclass = pymysql.cursors.DictCursor)
    
    @app.route('',method = ['POST'])     #api口
    def Create_NewUsers(self):
        data = request.get_data()
        data_dict = json.load(data)
        user_id = data_dict['id']
        gender = data_dict['gender']
        birthday = data_dict['Birth']
        Tags = data_dict['tags']
        cursor = self.DB_conn.cursor()
        sql_UI = 'Insert INTO UIs(User_ID,Gender,Birth) values(%s,%s,%s)'%(user_id,gender,birthday)
        sql_UT = 'Insert INTO UTs(User_ID) values(%s)'%(user_id)
        json_response = {}
        try:
            cursor.execute(sql_UI)
            cursor.execute(sql_UT)
            for tag in Tags:
                cursor.execute('update UTs set %s = 1 where User_ID = %s'%(tag,user_id))
            cursor.commit()
            self.DB_conn.commit()
            json_response['error'] = '0'
        except Exception:
            json_response['error'] = Exception
            self.DB_conn.rollback()
        cursor.close()
        return jsonify(json_response)

    @app.route('',method = ['POST'])
    def Create_NewMovie(self):
        data = request.get_data()
        data_dict = json.load(data)
        movie_id = data_dict['id']
        directors = data_dict['Directors']
        actors = data_dict['Actors']
        pic_url = data_dict['Pic_URLs']
        Tags = data_dict['tags']
        region = data_dict['Region']
        date = data_dict['date']
        year = data_dict['year']
        name = data_dict['name']
        length = data_dict['timelength']
        cursor = self.DB_conn.cursor()
        json_response = {}
        sql_MIs = 'Insert Into MIs(Movie_ID,Directors,Actors,Pic_URLs,Region,Date,Year,Name,TimeLength) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'%(movie_id,directors,actors,pic_url,region,date,year,name,length)
        sql_MTs = 'Insert INTO MTs(Movie_ID) values(%s)'%user_id

        try:
            cursor.execute(sql_MIs)
            cursor.execute(sql_MTs)
            for tag in Tags:
                cursor.execute('update MTs set %s = 1 where Movie_ID = %s'%(tag,movie_id))
            cursor.commit()
            self.DB_conn.commit()
            json_response['error'] = '0'
        except Exception:
            json_response['error'] = Exception
            self.DB_conn.rollback()
        cursor.close()
        return jsonify(json_response)

    @app.route('',method = ['POST'])
    def User_Watch_Info(self):
        data = request.get_data()
        data_dict = json.load(data)
        movie_id = data_dict['movie_id']
        user_id = data_dict['user_id']
        date = data_dict['date']
        time = data_dict['time']
        watched_len = data_dict['w_len']
        full_len = data_dict['f_len']

        cursor = self.DB_conn.cursor()
        json_response = {}
        sql_uwms = 'Insert INTO UWMs(User_ID,Date,Day_Time,Movie_ID,Watched_TimeLength,Full_TimeLength) values(%s,%s,%s,%s,%s,%s)' %(user_id,date,time,movie_id,watched_len,full_len)

        try:
            cursor.execute(sql_uwms)
            cursor.commit()
            self.DB_conn.commit()
            json_response['error'] = '0'
        except Exception:
            json_response['error'] = Exception
            self.DB_conn.rollback()
        cursor.close()
        return jsonify(json_response)

    @app.route('',method = ['POST'])
    def User_Comment_Movie(self):
        data = request.get_data()
        data_dict = json.load(data)
        user_id = data_dict['user_id']
        movie_id = data_dict['movie_id']
        score = data_dict['score']
        comment = data_dict['comment']
        date = data_dict['date']
        time = data_dict['time']

        cursor = self.DB_conn.cursor()
        json_response = {}
        sql_ucis = 'Insert INTO MIs(User_Id,Movie_ID,Score,Comment,Date,Day_Time) values(%s,%s,%s,%s,%s,%s)'%(user_id,movie_id,score,comment,date,time)
        sql_mcs = 'Insert INTO MCs(Movie_ID,User_ID,Comment,Date,DayTime) values(%s,%s,%s,%s,%s)'%(movie_id,user_id,comment,date,time)


        try:
            cursor.execute(sql_ucis)
            cursor.execute(sql_mcs)
            cursor.commit()
            self.DB_conn.commit()
            json_response['error'] = '0'
        except Exception:
            json_response['error'] = Exception
            self.DB_conn.rollback()
        cursor.close()

        #基于评分与评价进行对电影和用户的标签更改

        return jsonify(json_response)

    @app.route('',method = ['POST'])
    def Update_User_Info(self)



    @app.route('',method = ['POST'])
    def Update_Movie_Info(self)


    @app.route('',method = ['POST'])
    def Return_Recommand_Result(self)


    @app.route('',method = ['POST'])
    def Add_Fav_Movie(self)


    @app.route('',method - ['POST'])
    def Del_Fav_Movie(self)


    @app.route('',method = ['POST'])
    def Add_Collect_Movie(self)


    @app.route('',method = ['POST'])
    def Del_Collected_Movie(self)



























        
                            
