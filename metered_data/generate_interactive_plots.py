# -*- coding: utf-8 -*-
"""
Created on Thu May  7 14:41:22 2020

@author: paul
"""

import plotly.graph_objects as go

import pandas as pd
# Generate dataset
import numpy as np

df = pd.read_csv("representative_days.csv")


cols = [5, 15, 26, 33]
multiplier = 22;

# Create figure
fig = go.Figure()
 
button_list = list()
for ii in cols:
    # Add traces
    fig.add_trace(
        go.Scatter(x=list(df.index),
                   y=list(df[df.columns[ii]]),
                   name=df.columns[ii], 
                   visible = False))
    #Add buttons to the list
    which_is_true = [False for i in range(len(cols))]
    for jj in range(0,len(cols)):
        if ii == cols[jj]:
            which_is_true[jj] = True;
            break
        
    button_list.append(dict(label=df.columns[ii],
                     method="update",
                     args=[{"visible": which_is_true},
                           {"title": df.columns[ii]}]))
fig.data[0].visible = True
  
# https://plotly.com/python/custom-buttons/
fig.update_layout(
    updatemenus=[
        dict(
            active = 0,
            buttons = button_list             
        )
    ])


fig.show()

fig.write_html("plotly_testing.html")
