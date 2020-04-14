# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 08:42:26 2020

@author: scott

In main.py a dataframe with datetime index is created for time series analysis.
Main.py pulls functions from normalize.py, dayType.py, and daygroup.py to 
analyze load profiles on a daily level. 

Normalize.py - functions that calculate daily total usage and normalize each 
day based on it's total usage. 

dayType.py - functions that divide out weekdays, weekends, and holidays.

daygroup.py - functions that group each day into separate dataframes for 
plotting along the same x-axis. 

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

# custom functions import
from dayType import (get_weekdays_df, day_hist)
from dayGroup import (group_days_dict, day_lines)
from normalize import (normalize, day_sums)

### QUERY DATAFRAME
# define path for database file, you will have to edit to your repository path or it will NOT work
#path = "C:\\Users\\scott\\github\\Load_Profile_Analysis\\"
#filename = "sample.db"
path = "F:\\client\\BPA_E3T\\RCC\\RCCViewer\\"
filename = "RCC_MV.db"
# make connection
con = sqlite3.connect(os.path.join(path, filename))

sql_query = 'SELECT * FROM sunset_hourly WHERE var = "GPM"'
df = pd.read_sql_query(sql_query, con)

### SORT DATAFRAME SO TIMESTAMP IS INDEX
# create timestamps
timestamps = []

for i in range(0, len(df)):
    # create a datetime object
    timestamps.append(datetime.fromisoformat(df['time_pt'][i]))
    
df['time stamp'] = timestamps        
# set index to time stamp
df = df.set_index(['time stamp']).sort_index()


### DayType
weekdays = get_weekdays_df(df)
day_hist(weekdays, "sunset_weekday_hist")

### DayGroup
weekdays_dict = group_days_dict(weekdays)
day_lines(weekdays_dict, "sunset_weekday_lines")

### Normalize
weekdays = normalize(weekdays)

### DayType
day_hist(weekdays, "sunset_weekday_hist_norm")

### DayGroup
day_lines(weekdays_dict, "sunset_weekday_lines_norm")

















