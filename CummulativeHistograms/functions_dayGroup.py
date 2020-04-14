# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 08:58:05 2020

@author: scott

daygroup.py - functions that group each day into separate dataframes for 
plotting along the same x-axis. 

"""


import holidays
us_holidays = holidays.UnitedStates()

# ploting imports
import plotly.graph_objects as go



### GROUPING

def group_days_dict(df):
    
    days = {}    
    for i in range(0,len(df)):     
        days[str(df.index[i].date())] = df[str(df.index[i].date()):str(df.index[i].date())]
        
    return days

### PLOTTING
    
def day_lines(days, title):
    
    fig = go.Figure()      
    
    for key in days:
        
        # create times and values lists
        times=[]
        values=[]
        
        # identify times and values
        for i in range(0, len(days[key])):    
            times.append(days[key].index[i].time())
            values.append(days[key]['value'][i])
            
        # plot times and values
        fig.add_trace(go.Scatter(x=times, y=values,
                        mode='lines',
                        name=key))

    fig.write_html(title + ".html")