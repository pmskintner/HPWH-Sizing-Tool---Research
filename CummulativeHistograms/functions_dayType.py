# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 08:48:00 2020

@author: scott

dayType.py - functions that divide out weekdays, weekends, and holidays.

"""

import holidays
us_holidays = holidays.UnitedStates()

# ploting imports
import plotly.graph_objects as go
import plotly.express as px

def get_weekdays_df(df):
        
    weekdays_list = []
    weekends_list = []
    holidays_list = []
    
    for i in range(0,len(df)):
        date = df.index[i].date()

        if date in us_holidays:
            holidays_list.append(df.index[i])
        
        elif date.isoweekday()>1 and date.isoweekday()<7:
            weekdays_list.append(df.index[i])
        else:
            weekends_list.append(df.index[i])
    
    # create weekdays dataframe
    weekdays = df[~df.index.isin(weekends_list)]
    weekdays = weekdays[~weekdays.index.isin(holidays_list)]
    
    return weekdays

def get_weekends_df(df):
        
    weekdays_list = []
    weekends_list = []
    holidays_list = []
    
    for i in range(0,len(df)):
        date = df.index[i].date()

        if date in us_holidays:
            holidays_list.append(df.index[i])
        
        elif date.isoweekday()>1 and date.isoweekday()<7:
            weekdays_list.append(df.index[i])
        else:
            weekends_list.append(df.index[i])
    
    # create weekdays dataframe
    weekends = df[~df.index.isin(weekdays_list)]
    weekends = weekends[~weekends.index.isin(holidays_list)]
    
    return weekends

def get_holidays_df(df):
        
    weekdays_list = []
    weekends_list = []
    holidays_list = []
    
    for i in range(0,len(df)):
        date = df.index[i].date()

        if date in us_holidays:
            holidays_list.append(df.index[i])
        
        elif date.isoweekday()>1 and date.isoweekday()<7:
            weekdays_list.append(df.index[i])
        else:
            weekends_list.append(df.index[i])
    
    # create weekdays dataframe
    holidays = df[~df.index.isin(weekdays_list)]
    holidays = holidays[~holidays.index.isin(weekends_list)]
    
    return holidays

#### PLOTTING

def day_hist(df, title):

    times = []
    for i in range(0, len(df)):
        times.append(df.index[i].time())
    
    df['times'] = times
    
    fig = px.box(df, x="times", y="value")
    fig.write_html(title+".html")








