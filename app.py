#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 18:03:46 2020

@author: Nic
"""

from flask import Flask, render_template_string, render_template, request

import sqlite3
import pandas as pd
import ety

app = Flask(__name__)  


@app.route('/')
def my_form():
    return render_template('input.html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form["text"]
    table, ety_list = parse_text(text)
    return render_template("output.html", tables=[table], ety_list=ety_list, click_func = click_func)

@app.route('/#', methods=['POST'])
def click_func(string):
    print("THIS IS THE STRING",string,"ADSASDFXXXXXXX")
    return str(ety.tree(string)).replace("   ","           ")


def parse_text(text):
    path = "ety-db.db"
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    
    words = text.split(" ")
    
    #TODO: clean the words (remove special characters and such)
    #TODO: do some stemming
    
#    code_dict = pd.read_csv("my_code_dict.csv")
    codes = []
    ety_list = []
    for word in words:
        ety = (cur.execute("SELECT target,target_ety, target_ety_name \
                          FROM eng_only \
                          WHERE word=?",(word,)).fetchall())
        #TODO: recursive query
        if len(ety) > 0:
            ety_list.append((word, ety))
            codes += [item[2] for item in ety]
        else:
            codes += ["other"]
            ety_list.append((word, "other"))
    codes_series = pd.Series(codes, name="count")
    counts = codes_series.value_counts().to_frame()
    sum_count = counts["count"].sum()
    counts = codes_series.value_counts().to_frame()
    counts["percent"] = counts["count"].apply(lambda x: round((x/sum_count)*100, 1))
    return counts.to_html(), dict_to_annotations(ety_list)
        
def dict_to_annotations(ety_list):
    #TODO: sort the elements (put prefixes first, suffixes last), or maybe suffixes and prefixes last
    newlist = []
    for word, ety in ety_list:
        if ety != "other":
            items = [": ".join((i[0], i[2])) for i in ety]
            new_ety = ", ".join(items)
            newlist.append((word, new_ety))
        else:
            newlist.append((word, ety))
    return newlist
        
           


if __name__ =="__main__":  
    app.run(debug = True)