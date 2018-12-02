#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 13:53:25 2018

@author: justintimberlake
"""

from flask import Flask, request ,jsonify
import json 
from Get_Store_Data import Data_Op


app = Flask(__name__)
DB = Data_Op()

@app.route('/user/new_user',methods = ['GET','POST'])    # /user/new_user
def GetNewStuInfo():
    result = {}
    a = request.get_data()
    infodict = json.load(a)
    try:
        DB.Store_NewStuInfo(infodict)
        result['error'] = '0'
    except Exception as e:
        result['error'] = str(e)
    
    return jsonify(result)

@app.route('/user/login',methods = ['GET','POST'])
def Login():
    result = {}
    a = request.get_data()
    infodict = json.load(a)
    try:
        ans = DB.Login_Verify(infodict)
        if ans = 'yes':
            result['error'] = 0 
        else:
            result['error'] = 'Wrong Password or Account'
    except Exception as e:
        result['error'] = str(e)

    return jsonify(result)

@app.route('/user/get_table',methods = ['GET','POST'])    #/user/get_table
def GetStuClaTable():
    result = {}
    a = request.get_data()
    infodict = json.load(a)
    result = DB.Return_StuClaTable(infodict)
    result['error'] = '0'
    return jsonify(result)

@app.route('/user/change_info',methods = ['GET','POST'])    #/user/change_info
def ChangeStuInfo():
    result = {}
    a = request.get_data()
    infodict = json.load(a)
    try:
        DB.Change_StuInfo(infodict)
        result['error'] = '0'
    except Exception as e:
        result['error'] = str(e)

    return jsonify(result)

@app.route('/user/add_cla',methods = ['GET','POST'])    #/user/add_cla
def Stu_Add_Cla():
    result = {} 
    a = request.get_data()
    infodict = json.load(a)
    try:
        DB.Stu_Add_Cla(infodict)
        result['error'] = '0'
    except Exception as e:
        result['error'] = str(e)
    return jsonify(result)

@app.route('/user/del_cla',methods = ['GET','POST'])    #/user/del_cla
def Stu_Del_Cla():
    result = {} 
    a = request.get_data()
    infodict = json.load(a)
    try:
        DB.Stu_Del_Cla(infodict)
        result['error'] = '0'
    except Exception as e:
        result['error'] = str(e)
    return jsonify(result)
    
@app.route('/user/search_class',methods = ['GET','POST'])
def Stu_Search_Class():
    result = {} 
    a = request.get_data()
    condition_dict = json.load(a)
    try:
        result = DB.Search_Class(condition_dict)
        if len(result) == 0:
            result['error'] = 'No matched classes were founded'
        result['error'] = '0'
    except Exception as e:
        result['error'] = str(e)
    return jsonify(result)

@app.route('/user/com_cla',methods = ['GET','POST'])    #/user/com_cla
def Stu_Com_Cla():
    result = {}
    a = request.get_data()
    infodict = json.load(a)
    try:
        comment_id = DB.Stu_Com_Cla(infodict)
        result['comment_id'] = comment_id
        result['error'] = '0'
    except Exception as e:
        result['error'] = str(e)
    
    return jsonify(result)

@app.route('/user/del_com_cla',methods = ['GET','POST'])    #/user/del_com_cla
def Stu_Del_Com_Cla():
    result = {} 
    a = request.get_data()
    infodict = request.get_data(a)
    try:
        DB.Stu_Del_Com_Cla(infodict)
        result['error'] = '0'
    except Exception as e:
        result['error'] = str(e)
    
    return jsonify(result)

@app.route('/user/star_com',methods = ['GET','POST'])    #/user/star_com
def Stu_Star_Com():
    result = {} 
    a = request.get_data()
    infodict = request.get_data(a)
    try:
        DB.Stu_Star_Com(infodict)
        result['error'] = '0'
    except Exception as e:
        result['error'] = str(e)
    
    return jsonify(result)

@app.route('/user/unstar_com',methods = ['GET','POST'])    #/user/unstar_com
def Stu_UnStar_Com():
    result = {} 
    a = request.get_data()
    infodict = request.get_data(a)
    try:
        DB.Stu_UnStar_Com(infodict)
        result['error'] = '0'
    except Exception as e:
        result['error'] = str(e)
    
    return jsonify(result)

@app.route('/user/cla_extra_info',methods = ['GET','POST'])    #/user/cla_extra_info
def Return_ClaExtraInfo():
    result = {}
    a = request.get_data()
    infodict = json.load(a)
    try:
        result = DB.Return_ClaExInfo(infodict)
        result['error'] = '0'
    except Exception as e:
        result['error'] = str(e)
    
    return jsonify(result)

@app.route('/user/return_cla_comment',methods = ['GET','POST'])    #/user/return_cla_comment
def Return_ClaComment():
    result = {}
    a = request.get_data()
    infodict = json.load(a)
    try:
        result = DB.Return_ClaComment(infodict)
        result['error'] = '0'
    except Exception as e:
        result['error'] = str(e)
    
    return jsonify(result)

@app.route('/class/add_extra_info',methods = ['GET','POST'])    #/class/add_extra_info
def Add_Cla_ExInfo():
    result = {}
    a = request.get_data()
    infodict = json.load(a)
    try:
        DB.Add_ClaExInfo(infodict)
        result['error'] = '0' 
    except Exception as e:
        result['error'] = str(e)
        
    return result


def run_server(app):
    app.run(debug = False,host = '172.20.10.5', port = 5000)    #host地址待改
    

















