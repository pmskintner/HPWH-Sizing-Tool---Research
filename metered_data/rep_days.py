# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 17:46:05 2020

@author: scott
"""

# dataframe imports
import pandas as pd

def get_day(argdf, date_start, date_end):
    day = argdf[date_start:date_end];
    day = day.reset_index()
    return day['value'];
    
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

df['ejames_3hrday_2019-09-20'] = get_day(ejames_volume, '2019-09-20', '2019-09-21');
df['ejames_3hrday_2020-01-28'] = get_day(ejames_volume, '2020-01-28', '2020-01-29');
df['ejames_4hrday_2020-01-28'] = get_day(ejames_volume, '2020-01-28', '2020-01-29');
df['ejames_5hrday_2020-01-28'] = get_day(ejames_volume, '2020-01-28', '2020-01-29');
df['ejames_5hrday_2019-09-26'] = get_day(ejames_volume, '2019-09-26', '2019-09-27');
df['ejames_100percent_day_2019-10-18'] = get_day(ejames_volume, '2019-10-18', '2019-10-19');


df['stream_3hrday_vol_2018-09-12'] = get_day(stream_volume, '2018-09-12','2018-09-13');
df['stream_3hrday_norm_2018-06-08'] = get_day(stream_volume, '2018-06-08', '2018-06-09');
df['stream_3hrday_2018-07-12'] = get_day(stream_volume, '2018-07-12', '2018-07-13');
df['stream_4hrday_2018-04-05'] = get_day(stream_volume, '2018-04-05', '2018-04-06');
df['stream_4hrday_2018-07-12'] = get_day(stream_volume, '2018-07-12', '2018-07-13');
df['stream_5hrday_2018-04-05'] = get_day(stream_volume, '2018-04-05', '2018-04-06');
df['stream_5hrday_2018-04-06'] = get_day(stream_volume, '2018-04-06', '2018-04-07');
df['stream_sized_2017-01-10'] = get_day(stream_volume, '2017-01-10', '2017-01-11');
df['stream_sized_2017-01-13'] = get_day(stream_volume, '2017-01-13', '2017-01-14');
df['stream_sized_2017-01-28'] = get_day(stream_volume, '2017-01-28', '2017-01-29');

df['stream_new_2014-02-10'] = get_day(stream_volume, '2014-02-10', '2014-02-11');
df['stream_new_2018-02-21'] = get_day(stream_volume, '2018-02-20', '2018-02-21');
df['stream_new_2018-04-17'] = get_day(stream_volume, '2018-04-16', '2018-04-17');


df['sunset_3hrday_2017-04-12'] = get_day(sunset_volume, '2017-04-12', '2017-04-13');
df['sunset_3hrday_2015-05-07'] = get_day(sunset_volume, '2015-05-07', '2015-05-08');
df['sunset_4hrday_2017-01-28'] = get_day(sunset_volume, '2017-01-28', '2017-01-29');
df['sunset_5hrday_2017-01-28'] = get_day(sunset_volume, '2017-01-28', '2017-01-29');
df['sunset_5hrday_2015-01-07'] = get_day(sunset_volume, '2015-01-07', '2015-01-08');
df['sunset_5hrday_2017-04-13'] = get_day(sunset_volume, '2017-04-13', '2017-04-14');
df['sunset_5hrday_2017-02-11'] = get_day(sunset_volume, '2017-02-11', '2017-02-12');
df['sunset_sized_2017-01-17'] = get_day(sunset_volume, '2017-01-17', '2017-01-18');
df['sunset_sized_2017-07-15'] = get_day(sunset_volume, '2017-07-15', '2017-07-16');
df['sunset_sized_2018-02-09'] = get_day(sunset_volume, '2018-02-09', '2018-02-10');
df['sunset_sized_2018-02-27'] = get_day(sunset_volume, '2018-02-27', '2018-02-28');


df['yesler_3hrday_2020-01-04'] = get_day(yesler_volume, '2020-01-04', '2020-01-05');
df['yesler_3hrday_2019-02-07'] = get_day(yesler_volume, '2019-02-07', '2019-02-08');
df['yesler_4hrday_2019-01-05'] = get_day(yesler_volume, '2019-01-05', '2019-01-06');
df['yesler_4hrday_2019-10-12'] = get_day(yesler_volume, '2019-10-12', '2019-10-13');
df['yesler_5hrday_2019-01-05'] = get_day(yesler_volume, '2019-01-05', '2019-01-06');
df['yesler_5hrday_2019-02-06'] = get_day(yesler_volume, '2019-02-06', '2019-02-07');



# ejames_day = ejames_volume['2019-09-20':'2019-09-21']
# yesler_day = yesler_volume['2020-01-04':'2020-01-05']
# stream_day_vol = stream_volume['2018-09-12':'2018-09-13']
# stream_day_norm = stream_volume['2018-06-08':'2018-06-09']
# sunset_day = sunset_volume['2017-04-12':'2017-04-13']

# ejames_day = ejames_day.reset_index()
# yesler_day = yesler_day.reset_index()
# stream_day_vol = stream_day_vol.reset_index()
# stream_day_norm = stream_day_norm.reset_index()
# sunset_day = sunset_day.reset_index()

# df['ejames_day'] = ejames_day['value']
# df['yesler_day'] = yesler_day['value']
# df['stream_day_vol'] = stream_day_vol['value']
# df['stream_day_norm'] = stream_day_norm['value']
# df['sunset_day'] = sunset_day['value']

df.to_csv('representative_days.csv')
