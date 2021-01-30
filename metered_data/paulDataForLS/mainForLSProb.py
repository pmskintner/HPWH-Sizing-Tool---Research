# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 09:06:14 2021

@author: paul
"""
#mainForLSProb


# dataframe imports
import pandas as pd

# datetime imports
from datetime import datetime
import holidays
us_holidays = holidays.UnitedStates()

# database imports
import sqlite3
import os

wrkdir = "C:/Users/paul/Documents/GitHub/HPWH-Sizing-Tool---Research/metered_data/"
os.chdir(wrkdir)

# custom functions import
from functions import (get_weekdays_df, remove_incomplete_days, day_box, group_days_dict, 
                       day_lines, normalize, day_sums, df_iwf, df_peakyness)


# =============================================================================
# #### Let's start ###
# =============================================================================

#path = "F:\\client\\BPA_E3T\\RCC\\RCCViewer\\"
#filename = "RCC_MV.db"
# make connection
#con = sqlite3.connect(os.path.join(path, filename))
path = "F:\client\BPA_E3T\RCC\RCC_MV_full.db"
con = sqlite3.connect(path)

# for stream
df = df_iwf(con, 'stream')  # custom function to query db
con.close()
df = df['2014-01-01':'2020-02-01'] # filter for fully occupied days
df = remove_incomplete_days(df)
stream_flows = df.reset_index()

weekdays = get_weekdays_df(df) # filter for weekdays