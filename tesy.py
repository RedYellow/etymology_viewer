#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 12:55:57 2020

@author: Nic
"""

import ety

def click_func(string):
    print(type(string))
    print("THIS IS THE STRING",string,"ADSASDF-tesy")
    return str(ety.tree(string)).replace("   ","           ")

click_func()
