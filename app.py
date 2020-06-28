#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 18:03:46 2020

@author: Nic
"""

from flask import Flask, render_template_string, render_template, request

import sqlite3
import pandas as pd

app = Flask(__name__)  


@app.route('/')
def my_form():
    return render_template('input.html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form["text"]
    processed_text = parse_text(text)
    tex = ['<span class="tooltip Tooltip Text">My Text </span>', '<span class="tooltip yeet2">My Text2</span>']
    return render_template("output.html", texts = tex, tables=[processed_text])

def parse_text(text):
    path = "ety-db.db"
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    
    words = text.split(" ")
    
    #clean the words (remove special characters and such)
    #do some stemming
    
#    code_dict = pd.read_csv("my_code_dict.csv")
    codes = []
    ety_dict = {}
    for word in words:
        ety = (cur.execute("SELECT target,target_ety, target_ety_name \
                          FROM eng_only \
                          WHERE word=?",(word,)).fetchall())
        if len(ety) > 0:
            ety_dict[word] = ety
            codes += [item[2] for item in ety]
        else:
            codes += ["other"
                      ]
    codes_series = pd.Series(codes, name="count")
    counts = codes_series.value_counts().to_frame()
    sum_count = counts["count"].sum()
    counts = codes_series.value_counts().to_frame()
    counts["percent"] = counts["count"].apply(lambda x: round((x/sum_count)*100, 1))
    return counts.to_html()
        
    
            


if __name__ =="__main__":  
    app.run(debug = True)