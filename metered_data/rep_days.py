# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 17:46:05 2020

@author: scott
"""

# dataframe imports
import pandas as pd

# =============================================================================
# #### Import data
# =============================================================================
ejames_volume = pd.read_csv('ejames_volume.csv')
yesler_volume = pd.read_csv('yesler_volume.csv')
stream_volume = pd.read_csv('stream_volume.csv')
sunset_volume = pd.read_csv('sunset_volume.csv')
block11_volume = pd.read_csv('block11_volume.csv')

ejames_peakyness = pd.read_csv('ejames_peakyness.csv')
yesler_peakyness = pd.read_csv('yesler_peakyness.csv')
stream_peakyness = pd.read_csv('stream_peakyness.csv')
sunset_peakyness = pd.read_csv('sunset_peakyness.csv')
block11_peakyness = pd.read_csv('block11_peakyness.csv')

# =============================================================================
# #### Pull Out Representative days
# =============================================================================

df = pd.DataFrame()

ejames_volume = ejames_volume.set_index(['time stamp']).sort_index()
yesler_volume = yesler_volume.set_index(['time stamp']).sort_index()
stream_volume = stream_volume.set_index(['time stamp']).sort_index()
sunset_volume = sunset_volume.set_index(['time stamp']).sort_index()

ejames_day = ejames_volume['2019-09-20':'2019-09-21']
yesler_day = yesler_volume['2020-01-04':'2020-01-05']
stream_day_vol = stream_volume['2018-09-12':'2018-09-13']
stream_day_norm = stream_volume['2018-06-08':'2018-06-09']
sunset_day = sunset_volume['2017-04-12':'2017-04-13']

ejames_day = ejames_day.reset_index()
yesler_day = yesler_day.reset_index()
stream_day_vol = stream_day_vol.reset_index()
stream_day_norm = stream_day_norm.reset_index()
sunset_day = sunset_day.reset_index()

df['ejames_day'] = ejames_day['value']
df['yesler_day'] = yesler_day['value']
df['stream_day_vol'] = stream_day_vol['value']
df['stream_day_norm'] = stream_day_norm['value']
df['sunset_day'] = sunset_day['value']

df.to_csv('representative_days.csv')
