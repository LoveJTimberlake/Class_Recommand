#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 14:15:37 2018

@author: justintimberlake
"""

from flask import Flask 

app = Flask(__name__)

@app.route('/user/new_user',methods = ['POST','GET'])
def new_user():
    return "Hi new user"

@app.route('/class/add_ex_info',methods = ['POST','GET'])
def ex_info():
    return 'no ex_info'

app.run(host = '172.20.10.5', port = 5000)

