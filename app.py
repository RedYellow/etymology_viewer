#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 18:03:46 2020

@author: Nic
"""

from flask import Flask, render_template_string, render_template, request
from flask_wtf import Form, FlaskForm
from wtforms.fields import StringField, TextAreaField
from wtforms.widgets import TextArea

import sqlite3
import pandas as pd

app = Flask(__name__)  

class myForm(FlaskForm):
    text = TextAreaField

@app.route('/')
def my_form():
    return render_template('layout.html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form["text"]
    processed_text = parse_text(text)
    return processed_text

def parse_text(text):
    path = "ety-db.db"
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    
    words = text.split(" ")
    
    #do some stemming
    
#    code_dict = pd.read_csv("my_code_dict.csv")
    codes = []
    ety_dict = {}
    for word in words:
        ety = (cur.execute("SELECT target,target_ety, target_ety_name \
                          FROM eng_only \
                          WHERE word=?",(word,)).fetchall())
        if len(ety) > 0:
            print(ety)
            ety_dict[word] = ety
            codes += [item[2] for item in ety]
    codes_series = pd.Series(codes, name="count")
    counts = codes_series.value_counts()
    return counts.to_frame().to_html()
        
    
            


if __name__ =="__main__":  
    app.run(debug = True)