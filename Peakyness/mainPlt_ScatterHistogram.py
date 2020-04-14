# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 12:44:34 2020

@author: scott

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

# plotly
import plotly.graph_objects as go
import plotly.express as px

# custom functions import
from functions import (get_weekdays_df, day_box, group_days_dict, day_lines, normalize, day_sums, df_iwf)

path = "F:\\client\\BPA_E3T\\RCC\\RCCViewer\\"
filename = "RCC_MV.db"
# make connection
con = sqlite3.connect(os.path.join(path, filename))

# =============================================================================
# #### Scatter Plot For Sunset ###
# =============================================================================

df = df_iwf(con, 'sunset')  # custom function to query db
df = df['2015-01-01':'2020-02-01'] # filter for fully occupied days

weekdays = get_weekdays_df(df) # filter for weekdays
sums_df = day_sums(weekdays) # sum on date
values = sums_df['value']*60
sums_df['value'] = values

# scatterplot of total flows on days
plt_df = sums_df.reset_index()
fig = px.scatter(plt_df, x='dates', y="value", hover_data=['dates'])
fig.write_html("sunset_scatter.html")

# cummulative histogram
x = sums_df['value']
fig = go.Figure(data=[go.Histogram(x=x, cumulative_enabled=True, histnorm='probability density')])
fig.write_html("sunset_hist.html")

# =============================================================================
# #### Scatter Plot For Stream ###
# =============================================================================

df = df_iwf(con, 'stream')  # custom function to query db
df = df['2014-01-01':'2020-02-01'] # filter for fully occupied days

weekdays = get_weekdays_df(df) # filter for weekdays
sums_df = day_sums(weekdays) # sum on date
values = sums_df['value']*60
sums_df['value'] = values

# scatterplot of total flows on days
plt_df = sums_df.reset_index()
fig = px.scatter(plt_df, x='dates', y="value", hover_data=['dates'])
fig.write_html("stream_scatter.html")

# cummulative histogram
x = sums_df['value']
fig = go.Figure(data=[go.Histogram(x=x, cumulative_enabled=True, histnorm='probability density')])
fig.write_html("stream_hist.html")

# =============================================================================
# #### Scatter Plot For Yesler ###
# =============================================================================

df = df_iwf(con, 'yesler')  # custom function to query db
df = df['2019-07-10':'2020-02-01'] # filter for fully occupied days

weekdays = get_weekdays_df(df) # filter for weekdays
sums_df = day_sums(weekdays) # sum on date
values = sums_df['value']*60
sums_df['value'] = values

# scatterplot of total flows on days
plt_df = sums_df.reset_index()
fig = px.scatter(plt_df, x='dates', y="value", hover_data=['dates'])
fig.write_html("yesler_scatter.html")

# cummulative histogram
x = sums_df['value']
fig = go.Figure(data=[go.Histogram(x=x, cumulative_enabled=True, histnorm='probability density')])
fig.write_html("yesler_hist.html")

# =============================================================================
# #### Scatter Plot For Eliz James ###
# =============================================================================

df = pd.read_csv('ejh_hrly_cwf.csv')

### SORT DATAFRAME SO TIMESTAMP IS INDEX
# create timestamps
timestamps = []

for i in range(0, len(df)):
    # create a datetime object
    timestamps.append(datetime.fromisoformat(df['time_pt'][i]))
    
df['time stamp'] = timestamps        
# set index to time stamp
df = df.set_index(['time stamp']).sort_index()
df = df[:'2019-06-01'].append(df['2019-06-19':'2020-02-01'])

### DayType
weekdays = get_weekdays_df(df)
#day_hist(weekdays, "sunset_weekday_hist")
sums_df = day_sums(weekdays)

values = sums_df['value']*60
sums_df['value'] = values


# scatterplot of total flows on days
plt_df = sums_df.reset_index()
fig = px.scatter(plt_df, x='dates', y="value", hover_data=['dates'])
fig.write_html("ejh_scatter.html")

# cummulative histogram
x = sums_df['value']
fig = go.Figure(data=[go.Histogram(x=x, cumulative_enabled=True, histnorm='probability density')])
fig.write_html("ejh_hist.html")






