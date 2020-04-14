# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 09:31:04 2020

@author: scott

Normalize.py - functions that calculate daily total usage and normalize each 
day based on it's total usage. 

"""

# dataframe imports
import pandas as pd

# datetime imports
from datetime import datetime
import holidays
us_holidays = holidays.UnitedStates()

# database imports
import sqlite3
import os

# ploting imports
import plotly.graph_objects as go
import plotly.express as px

def day_sums(df):
    
    # create dates list
    dates = []
    
    # append date strings to list
    for i in range(0,len(df)):
        dates.append(df.index[i].date())
        
    # add dates to df
    df['dates'] = dates    
    # groupby sum() on dates
    sums=df.groupby(['dates']).sum()
        
    return(sums)

def normalize(df):
    
    # create dates list
    dates = []
    
    # append date strings to list
    for i in range(0,len(df)):
        dates.append(df.index[i].date())
        
    # add dates to df
    df['dates'] = dates    
    # groupby sum() on dates
    sums=df.groupby(['dates']).sum()
    
    # create list to store normal values
    norm_val = []
    
    # loop through df and normalize values
    for i in range(0,len(df)):
        
        df_index=df.index[i]
        date = df.index[i].date()
        
        value = df.loc[df_index]['value']
        total = sums.loc[date]['value']
        
        norm_val.append(value/total)
        
    df['value']=norm_val
    
    return(df)
    
        
        
    
    return(sums)