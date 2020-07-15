#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 18:03:46 2020

@author: Nic
"""

from flask import Flask, render_template, request

import sqlite3
import pandas as pd
import ety
import re
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

app = Flask(__name__)  


@app.route('/')
def my_form():
    return render_template('input.html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form["text"]
    
#    table, ety_list = parse_text(text)
#    return render_template("output.html", tables=[table], ety_list=ety_list, click_func = click_func)
    
    table, ety_list = parse_text2(text)
    return render_template("output.html", tables=[table], ety_list=ety_list, click_func = click_func)

@app.route('/#', methods=['POST'])
def click_func(string):
    string = str(ety.tree(string))
    if "─" in string:
        return string.replace("   ","           ")
    else:
        return ""


def parse_text(text):
    path = "/Users/Nic/Documents/Python Projects/Etymology_viewer/ety-db.db"
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    
    words = text.split(" ")
    
    #TODO: clean the words (remove special characters and such)
    #TODO: do some stemming
    
    codes = []
    ety_list = []
    for word in words:
        etym = (cur.execute("SELECT target,target_ety, target_ety_name \
                          FROM eng_only \
                          WHERE word=?",(word,)).fetchall())
        #TODO: recursive query
        if len(etym) > 0:
            ety_list.append((word, etym))
            codes += [item[2] for item in etym]
        else:
            codes += ["other / unknown"]
            ety_list.append((word, "other / unknown"))
    codes_series = pd.Series(codes, name="count")
    counts = codes_series.value_counts().to_frame()
    sum_count = counts["count"].sum()
    counts = codes_series.value_counts().to_frame()
    counts["percent"] = counts["count"].apply(lambda x: round((x/sum_count)*100, 1))
    return counts.to_html(), dict_to_annotations(ety_list)

def parse_text2(text, stem=True):
    """This is much faster than parse_text, or at least it was until I added all the NLP stuff"""
    
    words = re.split("[-/–_\| ]", text)
    
    #TODO: do some stemming
    
    ety_list = []
    codes = []
    for word in words:
        lemma = word
        etym = ety.origins(word)
        if len(etym) == 0:
            etym = ety.origins(re.sub("[^A-Za-z']", "", word))
        if len(etym) == 0:
            etym = ety.origins(word.lower())
        if len(etym) == 0:
            etym = ety.origins(re.sub("[^A-Za-z']", "", word).lower())
        if stem and len(etym) == 0:
            cleaned_word = re.sub("[^A-Za-z']", "", word).lower().strip()
            if len(cleaned_word) > 0:
                word_lemma = lemmatize_word(cleaned_word)
                lemma = word_lemma
                etym = ety.origins(word_lemma)
        if len(etym) == 0:
            ety_list.append((word, lemma, "other / unknown"))
            codes.append("other / unknown")
        else:
            items = [i._word+": "+i._language.name for i in etym]
            ety_list.append((word, lemma, ", ".join(items)))
            codes += [i._language.name for i in etym]
    codes_series = pd.Series(codes, name="count")
    counts = codes_series.value_counts().to_frame()
    sum_count = counts["count"].sum()
    counts = codes_series.value_counts().to_frame()
    counts["percent"] = counts["count"].apply(lambda x: round((x/sum_count)*100, 1))
    return counts.to_html(), ety_list

def lemmatize_word(word):
    print("THIS IS THE WORD: '", word, "'", len(word))
    lemmatizer = WordNetLemmatizer()
    pos = pos_tag([word])[0]
    return lemmatizer.lemmatize(pos[0], get_wordnet_pos(pos[1]))
    
def get_wordnet_pos(treebank_tag):

    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN
        
def dict_to_annotations(ety_list):
    #TODO: sort the elements (put prefixes first, suffixes last), or maybe suffixes and prefixes last
    newlist = []
    for word, etym in ety_list:
        if etym != "other / unknown":
            items = [": ".join((i[0], i[2])) for i in etym]
            new_ety = ", ".join(items)
            newlist.append((word, new_ety))
        else:
            newlist.append((word, etym))
    return newlist
        
           


if __name__ =="__main__":  
    app.run(debug = True)