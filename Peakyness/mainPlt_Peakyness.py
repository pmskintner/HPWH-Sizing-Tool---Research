# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 17:09:50 2020

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
from functions import (get_weekdays_df, day_box, group_days_dict, 
                       day_lines, normalize, day_sums, df_iwf, df_peakyness)


path = "F:\\client\\BPA_E3T\\RCC\\RCCViewer\\"
filename = "RCC_MV.db"
# make connection
con = sqlite3.connect(os.path.join(path, filename))

# =============================================================================
# #### Peakyness Plot For Sunset ###
# =============================================================================

df = df_iwf(con, 'sunset')  # custom function to query db
df = df['2015-01-01':'2020-02-01'] # filter for fully occupied days

weekdays = get_weekdays_df(df) # filter for weekdays
sums_df = day_sums(weekdays) # sum on date

# add three hour peak, volumes, times, and normalized volumes to sums_df
sums_df = df_peakyness(sums_df, weekdays)

# convert to gallons
# must be after peakyness function for proper normalization
sums_df['value'] = sums_df['value']*60 

# scatterplot of total flows on days
sunset_df = sums_df.reset_index()
fig = px.scatter(sunset_df, x='value', y="peak_norm", hover_data=['dates', 'peak_hours'])
fig.write_html("sunset_peakyness.html")

site = []
for i in range(0,len(sunset_df)):
    site.append('sunset')

sunset_df['site'] = site

# =============================================================================
# #### Peakyness Plot For Stream ###
# =============================================================================

df = df_iwf(con, 'stream')  # custom function to query db
df = df['2014-01-01':'2020-02-01'] # filter for fully occupied days

weekdays = get_weekdays_df(df) # filter for weekdays
sums_df = day_sums(weekdays) # sum on date

# add three hour peak, volumes, times, and normalized volumes to sums_df
sums_df = df_peakyness(sums_df, weekdays)

# convert to gallons
# must be after peakyness function for proper normalization
sums_df['value'] = sums_df['value']*60 

# scatterplot of total flows on days
stream_df = sums_df.reset_index()
fig = px.scatter(stream_df, x='value', y="peak_norm", hover_data=['dates', 'peak_hours'])
fig.write_html("stream_peakyness.html")

site = []
for i in range(0,len(stream_df)):
    site.append('stream')

stream_df['site'] = site

# =============================================================================
# #### Peakyness Plot For Yesler ###
# =============================================================================

df = df_iwf(con, 'yesler')  # custom function to query db
df = df['2019-07-10':'2020-02-01'] # filter for fully occupied days

weekdays = get_weekdays_df(df) # filter for weekdays
sums_df = day_sums(weekdays) # sum on date

# add three hour peak, volumes, times, and normalized volumes to sums_df
sums_df = df_peakyness(sums_df, weekdays)

# convert to gallons
# must be after peakyness function for proper normalization
sums_df['value'] = sums_df['value']*60 

# scatterplot of total flows on days
yesler_df = sums_df.reset_index()
fig = px.scatter(yesler_df, x='value', y="peak_norm", hover_data=['dates', 'peak_hours'])
fig.write_html("yesler_peakyness.html")

site = []
for i in range(0,len(yesler_df)):
    site.append('yesler')

yesler_df['site'] = site

# =============================================================================
# #### Peakyness Plot For Eliz James ###
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
df = df[:'2019-06-01'].append(df['2019-06-19':'2020-02-01']) # remove flood event

# look at weekdays only
weekdays = get_weekdays_df(df) # filter for weekdays
sums_df = day_sums(weekdays) # sum on date


# add three hour peak, volumes, times, and normalized volumes to sums_df
sums_df = df_peakyness(sums_df, weekdays)

# convert to gallons
# must be after peakyness function for proper normalization
sums_df['value'] = sums_df['value']*60 

# scatterplot of total flows on days
ejames_df = sums_df.reset_index()
fig = px.scatter(ejames_df, x='value', y="peak_norm", hover_data=['dates', 'peak_hours'])
fig.write_html("ejh_peakyness.html")

site = []
for i in range(0,len(ejames_df)):
    site.append('ejames')

ejames_df['site'] = site

# =============================================================================
# #### Plot all on same Scatter ###
# =============================================================================

df = ejames_df.append(yesler_df).append(stream_df).append(sunset_df)
fig = px.scatter(df, x='value', y="peak_norm", color = 'site', 
                 hover_data=['dates', 'peak_hours', 'site'])
fig.write_html("sites_peakyness.html")

