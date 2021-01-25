# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 12:42:36 2021

https://towardsdatascience.com/beyond-classic-pca-functional-principal-components-analysis-fpca-applied-to-time-series-with-python-914c058f47a0
https://fdasrsf-python.readthedocs.io/en/latest/fPLS.html
"""
import pandas as pd
import numpy as np
import os
import plotly.express as px
import plotly.graph_objects as go
#key
import plotly.io as pio
pio.renderers.default = "chrome"

from functions import get_weekdays_df
import matplotlib.pyplot as plt

# Import the CSV file with only useful columns
df = pd.read_csv("stream_volume.csv", sep=",")
df = pd.read_csv("C:/Users/paul/Documents/GitHub/HPWH-Sizing-Tool---Research/metered_data/stream_volume.csv", sep=",")
# Rename columns to simplify syntax
#df = df.set_index('time stamp')
#weekdays = get_weekdays_df(df) # filter for weekdays

# Select 2019 records only
#df = df[weekdays]

df = df.rename(columns={"dates": "date", "hour_pt": "hour", "gal in hr": "galphr"})

# Pivot table to get "Date" as index and regions as columns 
dfhrs = df.pivot(index = 'date', columns='hour', values='galphr')
#df = df.pivot(index='Date', columns='Region', values='Temp')
df = df.pivot(index='hour', columns='date', values='galphr')

pd.plotting.scatter_matrix(dfhrs, alpha=0.1)

plt.matshow(dfhrs.corr())
cb = plt.colorbar()
cb.ax.tick_params(labelsize=12)
plt.title('Correlation Matrix', fontsize=16);
plt.show()

# Get histogram of sums from time periods defined by hour start and hour fin
hr_start  = 6 #midnight is 0
hr_fin = 9 #Goes up to this hour i.e. does not include.
hrs_2_sum = list(range(hr_start,hr_fin))
dfhrs['galsum'+str(hr_start)+str(hr_fin)] = dfhrs[hrs_2_sum].sum(axis=1)/60.

dfhrs.hist('galsum'+str(hr_start)+str(hr_fin), bins = int(np.sqrt(len(dfhrs))),
            density=1)
dfhrs.hist('galsum'+str(hr_start)+str(hr_fin), bins = int(np.sqrt(len(dfhrs))),
            density=1, cumulative=True)


######################################################
def advanced_coordinates_plot( df, colorBy = 2,  plotName = 'test'):  
    data_col = list();
    maxRange = 0 
    for col in df.columns:
        maxRange = max(maxRange, max(df[col]))
    for col in df.columns:
        data_col.append( dict(range = [0, maxRange ],
                 label = col, values = df[col]))
    
    if type(colorBy) == int:
        colorBy =  df[df.columns[colorBy]]
    elif len(colorBy) == len(df):
        colorBy = colorBy;
    else: 
        colorBy = df.sum(axis=1);
    
    fig = go.Figure(data =
        go.Parcoords(
            line = dict(color = colorBy,
                       colorscale = px.colors.diverging.Tealrose,
                       showscale = True),
            dimensions = data_col)
        )
    return fig


dfhrs_select = dfhrs[hrs_2_sum]/60
fig = advanced_coordinates_plot(dfhrs_select, colorBy = []) 
fig.write_html('temp' + ".html")
os.system("start temp.html")