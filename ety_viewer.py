#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 21:34:32 2020

@author: Nic
"""

import pandas as pd
path = "/Users/Nic/Documents/Python Projects/Etymology_viewer/ety.txt"

code_dict = pd.read_csv("my_code_dict.csv", keep_default_na = False).set_index("id").to_dict()["name"]

def main(eng_only = True, write = True):
    
    df = pd.read_csv(path, sep="\t", names = ["word", "rel", "target"])
    if eng_only:
        df = df[df["word"].str.match("eng:")]
    df[["word_ety","word"]] = df["word"].str.split(": ", expand=True)
    df[["target_ety","target"]] = df["target"].str.split(": ", expand=True)
    df = df[["word", "word_ety", "target", "target_ety"]]
    
#    for the actual database, I used only the eng words, so the word_ety bit
#    is superfluous, and I put the target_ety translation into a column called
#    iso_name
    
    if not eng_only:
        df["word_ety_name"] = df["word_ety"].apply(translate_iso)
    
    df["target_ety_name"] = df["target_ety"].apply(translate_iso)
    
#    df["target_ety"] = df["target_ety"].apply(translate_iso)
    
    
    
    if write:
        df.to_csv("ety-eng_only.csv", index=False)
    
    return df

def translate_iso(string):
    """converts from ISO code to language/dialect name"""
    return code_dict[string]
    
def make_my_dict(df):
    etys = list(df["target_ety"].unique()) #the unique codes used in the actual DataFrame
    
    codes_path = "/Users/Nic/Documents/Python Projects/Etymology_viewer/iso-639-3.tab.txt"
    codes = pd.read_csv(codes_path, sep="\t")[["Id", "Ref_Name"]]
    
    def trans(string):
        return codes.loc[codes["Id"]==string]["Ref_Name"].to_string(index=False).strip()
    
    x = pd.Series(etys).apply(trans).to_frame(name="name")
    x["id"] = etys
    x.to_csv("my_code_dict.csv", index=False)
    
#x = cur.execute("SELECT COUNT(word), target_ety FROM eng_only \
#                WHERE target_ety != 'eng' \
#                GROUP BY target_ety").fetchall().sort(key=lambda x:x[0], reverse=True)  






    