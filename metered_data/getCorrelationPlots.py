# -*- coding: utf-8 -*-
"""
Created on Wed May 27 12:30:08 2020

@author: paul
"""


# dataframe imports
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

import numpy as np
import plotly.express as px
import plotly.graph_objects as go
#from plotly.subplots import make_subplots

from bisect import bisect

#cd documents/github/HPWH-Sizing-Tool---Research\metered_data

def format_Dates(df):
    df['dates'] =  pd.to_datetime(df['dates'], format='%Y-%m-%d') # Make timestamp column datetime
    df['time stamp'] =  pd.to_datetime(df['time stamp'], format='%Y-%m-%d %H:%M:%S') # Make timestamp column datetime
    df['hour'] = df['time stamp'].apply(lambda x: x.hour) # Get hour from time stamp column
    return df

def format_Dates_grow(df):
    df['dates'] =  pd.to_datetime(df['dates'], format='%m/%d/%Y') # Make timestamp column datetime
    df['time stamp'] =  pd.to_datetime(df['time stamp'], format='%m/%d/%Y %H:%M') # Make timestamp column datetime
    df['hour'] = df['time stamp'].apply(lambda x: x.hour) # Get hour from time stamp column
    return df


def getAvgRankedDays(df, top = 0, bottom = 0.05, average = True):
    # Gives the average of tanks ranked between bounds of the top % and bottom % 
    # df should be sorted
    days = df[int(np.ceil(top*len(df))) : int(np.ceil(bottom*len(df)))]
    days = days.reset_index() # Get the middle days of peak agg hour days
    if average:
        return days.mean()
    else:
        return days

# =============================================================================
# #### Import data
# =============================================================================
ejames_volume = format_Dates(pd.read_csv('ejames_volume.csv'))
yesler_volume = format_Dates(pd.read_csv('yesler_volume.csv'))
stream_volume = format_Dates(pd.read_csv('stream_volume.csv'))
sunset_volume = format_Dates(pd.read_csv('sunset_volume.csv'))
#block11_volume = pd.read_csv('block11_volume.csv')

growA_volume = format_Dates_grow(pd.read_csv('growA_volume.csv'))
growB_volume = format_Dates_grow(pd.read_csv('growB_volume.csv'))

gA_people = 18;
gB_people = 30;
EJ_people = 62;
Yes_people = 276;
Stream_people = 140;
Sunset_people = 110;

growA_volume.value = growA_volume.value*60/gA_people
growB_volume.value = growB_volume.value*60/gB_people

ejames_volume.value = ejames_volume.value/EJ_people
yesler_volume.value = yesler_volume.value/Yes_people
stream_volume.value = stream_volume.value/Stream_people
sunset_volume.value = sunset_volume.value/Sunset_people

stream_sunset = stream_volume.copy();
stream_sunset['dates'] = stream_sunset['dates'].apply(lambda x: x - pd.DateOffset(years=10))
stream_sunset = stream_sunset.append(sunset_volume).reset_index()
stream_sunset = stream_sunset.drop(columns = stream_sunset.columns[0:2])

yesss = yesler_volume.copy();
yesss = yesss.drop(columns =  yesss.columns[0:1])
#yesss['dates'] = yesss['dates'].apply(lambda x: x + pd.DateOffset(years=20))
#yesss = yesss.append(stream_sunset).reset_index()
#yesss = yesss.drop(columns = yesss.columns[0:2])

grow = growA_volume.copy()
grow['dates'] = grow['dates'].apply(lambda x: x - pd.DateOffset(years=10))
grow = grow.append(growB_volume).reset_index()
grow = grow.drop(columns = grow.columns[0:2])


# =============================================================================
# #### Some Grow things
# =============================================================================
growInd = grow.groupby('dates').agg('sum').hour!=276
growInd = growInd[growInd==True];
grow = grow[~grow['dates'].isin(growInd.index)]

grow1 = grow[grow['time stamp']<"2017-05-28 00:00:00" ]
grow2 = grow[grow['time stamp']>"2017-08-17 00:00:00" ]
grow1.append(grow2).reset_index()
grow1 = grow1.drop(columns = grow1.columns[0:1])

grow_daily = grow1.groupby(['Date','site']).agg('sum').reset_index()
fig = px.line(grow_daily, x="Date", y="value", color = "site")
fig.write_html('grow' + ".html")

fig = px.line(grow1, x="time stamp", y="value", color = "site")
fig.write_html('grow1' + ".html")
grow = grow1.copy()
# =============================================================================
# #### Plotting Functions
# =============================================================================
def plotCorrforWeek(df, aggHr = 2, plotWeekdays = 'D', normalized = False, plotName = 'test'):
   
    # Aggregate by given number of hours or list of hours
    if type(aggHr) == np.ndarray:
        df['agghour'] = 0;
        for ind2, ele in enumerate(df.hour):
            i = bisect(aggHr, ele, hi=aggHr.size-1)
            i1, i2 = aggHr[i], aggHr[i-1]
            df['agghour'][ind2] = i1 if abs(i1 - ele) < abs(i2 - ele) else i2
                
        dfa = df.groupby(['dates','agghour']).agg({'value':'sum'})
        dfa = dfa.reset_index();
        
    elif aggHr > 0:
        df['agghour'] = df.hour.apply(lambda x: np.floor(x/aggHr)*aggHr)
    
        dfa = df.groupby(['dates','agghour']).agg({'value':'sum'})
        dfa = dfa.reset_index();
    else:
        dfa = df.reset_index();
    
    #Normalize!
    if normalized == True:
        daytotals = dfa.groupby(['dates']).agg({'value':'sum'}).reset_index()
        # iterate through each row and select  
        for i in range(len(dfa)): # issue with dataframe copys here....
            dfa.value[i] = dfa.value[i] / daytotals.value[dfa.dates[i] == daytotals.dates]
            
    
    #Split into weekDays and weekEnd
    dfa['weekday'] = dfa['dates'].apply(lambda x: x.weekday() < 5)
    dfD = dfa[dfa.weekday == True]
    dfE = dfa[dfa.weekday == False]
    
    dfa  = dfa.pivot( index='dates', columns = 'agghour', values = 'value')
    dfD = dfD.pivot(index='dates', columns = 'agghour', values = 'value')
    dfE = dfE.pivot(index='dates', columns = 'agghour', values = 'value')
    
    #Looking at weekends, weekdays, or all?
    if plotWeekdays.upper() == 'D' :
        pdf = dfD;
    elif plotWeekdays.upper() == 'E':
        pdf = dfE;
    else:
        pdf = dfa;
        
    # scatter_matrix(pdf)
    # plt.show()
    
    # corrPlot(pdf, plotName)
    
    return pdf; 

######################################################
def corrPlot(df, name):
    fig = go.Figure(data=go.Heatmap(z=df.corr()))

    fig.write_html(name + ".html")

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

# Take the 24 hour day and turn it into a 
def day_to_cumulativeday( day ):
    if len(day) != 24:
        raise Exception('Day must be of length 24')
    if type(day) != np.ndarray:
        day = np.array(day)
    
    newday = np.zeros(24)
    newday[0] = max(day)
    newday[23] = sum(day)
    for i in range(2,24): 
        newday[i -1] = max(rolling_sum(day, n = i))
    
    #Quick error check
    if newday[23]==1 and newday[3] ==1:
        newday[:] = 0;
    return newday


def rolling_sum(a, n=4) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[ n:] - ret[ :-n]
    return ret[ n - 1:]       
# =============================================================================
# #### Analysis
# =============================================================================
#df = stream_sunset.copy()
df = yesss.copy();
df = ejames_volume.copy()
df = grow.copy()
df = stream_volume.copy()

hours_to_agg = 3
hours_to_agg = np.array([0,2,6,10,14,18,22])

#Chop top outlier
ind = df.groupby(['dates']).agg({'value':'sum'})
ind = ind.sum(axis=1).idxmax()
df = df[df.dates != ind]

dfD = plotCorrforWeek(df.copy(), aggHr = hours_to_agg, plotWeekdays = 'D', normalized = False)

# Coordinates plot if coordinates are hours of day.
fig = advanced_coordinates_plot(dfD, colorBy = 2) 
fig.write_html('test' + ".html")

dfall = plotCorrforWeek(df.copy(), aggHr = 1, plotWeekdays = 'D', normalized = True) #Get the hourly data frame to average days out of
# Coordinates plot if coordinates are hours of day.
fig = advanced_coordinates_plot(dfall, colorBy = 7) 
fig.write_html('test1' + ".html")

### Go to cumulative not normalized
dfall = plotCorrforWeek(df.copy(), aggHr = 1, plotWeekdays = 'D', normalized = False) #Get the hourly data frame to average days out of
dfallc = dfall.apply(lambda x: day_to_cumulativeday(x), axis=1, result_type='expand')
dfallc = dfallc[(dfallc.T != 0).any()] # drop zero rows
fig = advanced_coordinates_plot(dfallc, colorBy = 23) 
fig.write_html('testC' + ".html")

### Go to cumulative normalized 
dfalln = plotCorrforWeek(df.copy(), aggHr = 1, plotWeekdays = 'D', normalized = True) #Get the hourly data frame to average days out of
dfallcn = dfalln.apply(lambda x: day_to_cumulativeday(x), axis=1, result_type='expand')
dfallcn = dfallcn[(dfallcn.T != 0).any()] # drop zero rows
fig = advanced_coordinates_plot(dfallcn, colorBy = dfall.sum(axis=1)) 
fig.write_html('testCN' + ".html")


#24 Cumulative
dfall24 = plotCorrforWeek(df.copy(), aggHr = 24, plotWeekdays = 'D', normalized = False) #Get the hourly data frame to average days out of
dfall24 = dfall24.reset_index()
    
fig = go.Figure(data=[go.Histogram(x=dfall24[0.0], cumulative_enabled=True, histnorm='probability density')])
fig.update_layout(xaxis_title = "GPD per Person", yaxis_title = "Percentile")
fig.write_html("test_cdf.html")


# Top % of days at the hourly level
sort_by_index_grouping = 23 # The index to sort by

dfallc = dfallc.sort_values(by=dfallc.columns[sort_by_index_grouping], ascending = False) #Sort data frame by column values
# drop top row use in for EJ case
dfallc = dfallc[1:]
top_days    = getAvgRankedDays(dfallc, top = .02, bottom = 0.05, average = False) # Get top five % of peak agg hour days
middle_days = getAvgRankedDays(dfallc, top = .05, bottom = 0.95, average = False) # Get the middle days of peak agg hour days

dfall1 = dfall.reset_index()
# drop top
temp = np.zeros(24)
tempdf = pd.DataFrame()
days_to_avg = top_days
for date in days_to_avg.dates:
    tempdf = tempdf.append(dfall1[dfall1.dates==date].iloc[0,1:])
    temp = temp + dfall1[dfall1.dates==date].iloc[0,1:]
temp = temp/len(days_to_avg)
print(temp)


top_days = tempdf.T
top_days.to_csv('top_days.csv')
###############################################################################
# # testing with hours_to_agg = 24 getting day sums
# hours_to_agg = 24
# dfA = plotCorrforWeek(df, aggHr = hours_to_agg, plotWeekdays = 'A')


# future = 1
# dfA['day'] = dfD[0.0][0:-future]
# dfA['next'] = 0
# dfA['next'][0:-future] = dfA[0.0][future:]

# dfA['diff'] = dfA['next'] - dfA['day']
# fig = px.histogram(dfD, x = 'diff',histnorm='probability density', marginal="box")
# fig = px.scatter(dfD, y = 'day')
# fig.write_html('test' + ".html")
