# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 16:58:48 2020

@author: scott
"""

# dataframe imports
import pandas as pd

# datetime imports
from datetime import datetime
import holidays
us_holidays = holidays.UnitedStates()

# ploting imports
import plotly.graph_objects as go
import plotly.express as px

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms
    
def remove_incomplete_days(df):
    '''
    Remove days were not all hours are recorded in the dataset.
    This function is not very efficient right now and could use some work.
    
    Parameters
    ----------
    df : dataframe
    '''
    
    # create empty lists to add dataframe columns
    dates = []
    timestep = []
    drop_dates = []
    
    for i in range(0, len(df)):        
        dates.append(df.index[i].date()) # append date datetime object
        timestep.append(1) # append a 1 to sum later
             
    # add df columns
    df['dates'] = dates # create dates column    
    df['timestep_sum'] = timestep # create column to sum, will be 24 if all hours are recorded.
       
    # sumby date, timstep sum should equal 24 with hourly data     
    sums=df.groupby(['dates']).sum()
        
    # loop to find dates where timestep does not equal 24
    for i in range(0,len(sums)):
        if sums['timestep_sum'][i] != 24:
            drop_dates.append(sums.index[i]) 
    
    #reset index, needed in case an hour was recorded more than once.
    df = df.reset_index()
    
    # delete rows where date is in drop_dates
    for index, row in df.iterrows():
        if row['dates'] in drop_dates:
            df.drop(index, inplace=True)
    
    # set index back to time stamp
    df = df.set_index(['time stamp']).sort_index()
    
    return df

def df_peakyness(sums_df, weekdays, sumhrs = 3):
    
    '''
    Creates daily dataframe with peak three hour period identified,
    total recorded, and peak norm recorded.
    
    Parameters
    ----------
    sums_df : dataframe, required
        Daily sums flow for timeseries dataframe
    weekdays : dataframe, required
        Time sercies dataframe of flow values
    sumhrs : int
        How many hours to sum over
    '''
    
    peak_volumes = []
    peak_hours = []
    peak_norm = []
    
    for i in range(0, len(sums_df)):    
        # slice dataframe on date
        date_str = str(sums_df.index[i])
        day = weekdays[date_str:date_str]
        
        # find peak in that day
        peak = 0
        hr = 0
        #iterEnd = len(day)-1;
        if sumhrs <= 12 : 
            for j in range(1, len(day)-1 if sumhrs==3 else len(day)-2):
                if sumhrs ==3:
                    # caluclate volumes for hours
                    hr0 = day['value'][j-1] # volume at previous hour
                    hr1 = day['value'][j] # volume at hour
                    hr2 = day['value'][j+1] # volume at furture hour
                    
                    # potential new peak
                    new = hr0 + hr1 + hr2
                elif sumhrs == 4:
                     # caluclate volumes for hours
                    hr0 = day['value'][j-1] # volume at previous hour
                    hr1 = day['value'][j] # volume at hour
                    hr2 = day['value'][j+1] # volume at furture hour
                    hr3 = day['value'][j+2] # volume at furture hour
    
                    # potential new peak
                    new = hr0 + hr1 + hr2 + hr3
                elif sumhrs == 5:
                     # caluclate volumes for hours
                    hr_1 = day['value'][j-2] # volume at previous hour
                    hr0 = day['value'][j-1] # volume at previous hour
                    hr1 = day['value'][j] # volume at hour
                    hr2 = day['value'][j+1] # volume at furture hour
                    hr3 = day['value'][j+2] # volume at furture hour
    
                    # potential new peak
                    new = hr_1 + hr0 + hr1 + hr2 + hr3   
                else: 
                    raise Exception("sumhrs value: "+str(sumhrs)+ " is unsupported.")
                    
                if new > peak:
                    peak = new
                    hr = j
        else:
            diffN = 1./18. - (day['value']/sum(day['value']))
            diffInd = np.where(np.diff(np.sign(diffN))<0)[0]+1;
            peak = 0;
            for peakInd in diffInd:
                diffCum = np.cumsum(diffN[peakInd:]); #Get the rest of the day from the start of the peak
                negCum = diffCum[diffCum<-0.00001]
                if len(negCum) != 0:
                    new = -min(negCum); #Minimum value less than 0 or 0.
                    if new > peak:
                        peak = new
                        hr = peakInd
                        
            peak = peak * sum(day['value']);
            
            # Set hr to be the number of hours for the peak not WHEN the peak
            sign_changes = np.where(np.diff(np.sign(diffN)))[0]
            peak_switch = np.where(sign_changes == (hr-1))[0]; # Hour the peak starts
            
            try: 
                hr = sign_changes[peak_switch[0]+1] - sign_changes[peak_switch[0]]
            except IndexError:
                print("Hit index error diffN is: ")
                print( 1./18. - (day['value']/sum(day['value'])) )
                peak = 0;
                hr = 0;
        
        peak_volumes.append(peak)
        peak_hours.append(hr)
        peak_norm.append(peak/sums_df['value'][i])    
        
    sums_df['peak_volumes'] = peak_volumes
    sums_df['peak_volumes'] = sums_df['peak_volumes']*60 # convert to gallons
    sums_df['peak_hours'] = peak_hours
    sums_df['peak_norm'] = peak_norm
    
    return sums_df

def df_iwf(con, site):
    '''
    Creates time series index dataframe of flows from SQL query.
    
    Parameters
    ----------
    con : SQL connection, required
    site : string, required
        Site name for query
    '''
    
    sql_query = 'SELECT * FROM '+ site +'_hourly WHERE var in ("GPM", "WaterCold")'
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
    return df

def day_sums(df):
    '''
    Sum time series index dataframe by dates
    
    Parameters
    ----------
    df : dataframe, required
    '''
    # create dates list
    dates = []
    
    # append date strings to list
    for i in range(0,len(df)):
        dates.append(df.index[i].date())
        
    # add dates to df
    df['dates'] = dates    
    # groupby sum() on dates
    sums=df.groupby(['dates']).sum()
        
    return(sums)

def normalize(df):
    '''
    Normalized time series index dataframe by sum of daily values.
    
    Parameters
    ----------
    df : dataframe, required
    '''
    # create dates list
    dates = []
    
    # append date strings to list
    for i in range(0,len(df)):
        dates.append(df.index[i].date())
        
    # add dates to df
    df['dates'] = dates    
    # groupby sum() on dates
    sums=df.groupby(['dates']).sum()
    
    # create list to store normal values
    norm_val = []
    
    # loop through df and normalize values
    for i in range(0,len(df)):
        
        df_index=df.index[i]
        date = df.index[i].date()
        
        value = df.loc[df_index]['value']
        total = sums.loc[date]['value']
        
        norm_val.append(value/total)
        
    df['value']=norm_val
    
    return(df)

def get_weekdays_df(df):
    '''
    Filter time series index dataframe for weekdays
    
    Parameters
    ----------
    df : dataframe, required
    '''    
    
    weekdays_list = []
    weekends_list = []
    holidays_list = []
    
    for i in range(0,len(df)):
        date = df.index[i].date()

        if date in us_holidays:
            holidays_list.append(df.index[i])
        
        elif date.isoweekday()>1 and date.isoweekday()<7:
            weekdays_list.append(df.index[i])
        else:
            weekends_list.append(df.index[i])
    
    # create weekdays dataframe
    weekdays = df[~df.index.isin(weekends_list)]
    weekdays = weekdays[~weekdays.index.isin(holidays_list)]
    
    return weekdays

def get_weekends_df(df):
    '''
    Filter time series index dataframe for weekdends
    
    Parameters
    ----------
    df : dataframe, required
    '''            
    weekdays_list = []
    weekends_list = []
    holidays_list = []
    
    for i in range(0,len(df)):
        date = df.index[i].date()

        if date in us_holidays:
            holidays_list.append(df.index[i])
        
        elif date.isoweekday()>1 and date.isoweekday()<7:
            weekdays_list.append(df.index[i])
        else:
            weekends_list.append(df.index[i])
    
    # create weekdays dataframe
    weekends = df[~df.index.isin(weekdays_list)]
    weekends = weekends[~weekends.index.isin(holidays_list)]
    
    return weekends

def get_holidays_df(df):
    '''
    Filter time series index dataframe for holidays
    
    Parameters
    ----------
    df : dataframe, required
    '''    
    weekdays_list = []
    weekends_list = []
    holidays_list = []
    
    for i in range(0,len(df)):
        date = df.index[i].date()

        if date in us_holidays:
            holidays_list.append(df.index[i])
        
        elif date.isoweekday()>1 and date.isoweekday()<7:
            weekdays_list.append(df.index[i])
        else:
            weekends_list.append(df.index[i])
    
    # create weekdays dataframe
    holidays = df[~df.index.isin(weekdays_list)]
    holidays = holidays[~holidays.index.isin(weekends_list)]
    
    return holidays

### GROUPING

def group_days_dict(df):
    '''
    Returns dictionary where keys are dates (string), and values are time series index 
    dataframes sliced from full dataframe for that date only. Used for creating line plot
    of all weekdays plotted on the same 24 hours. 
    
    Parameters
    ----------
    df : dataframe, required
    '''    
    days = {}    
    for i in range(0,len(df)):     
        days[str(df.index[i].date())] = df[str(df.index[i].date()):str(df.index[i].date())]
        
    return days

### PLOTTING
    
def day_lines(days, title):
    '''
    Creates line plot in plotly of days dictionary.
    
    Parameters
    ----------
    days : dictionary, required
    title : string, required
    '''    
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

#### PLOTTING

def day_box(df, title):
    '''
    Creates box plot from time index dataframe.
    
    Parameters
    ----------
    df : dataframe, required
    title : string, required
    '''    
    times = []
    for i in range(0, len(df)):
        times.append(df.index[i].time())
    
    df['times'] = times
    
    fig = px.box(df, x="times", y="value")
    fig.write_html(title+".html")

    
def confidence_ellipse(x, y, ax, n_std=3.0, facecolor='none', **kwargs):
    """
    Create a plot of the covariance confidence ellipse of *x* and *y*.

    Parameters
    ----------
    x, y : array-like, shape (n, )
        Input data.

    ax : matplotlib.axes.Axes
        The axes object to draw the ellipse into.

    n_std : float
        The number of standard deviations to determine the ellipse's radiuses.

    **kwargs
        Forwarded to `~matplotlib.patches.Ellipse`

    Returns
    -------
    matplotlib.patches.Ellipse
    """
    if x.size != y.size:
        raise ValueError("x and y must be the same size")

    cov = np.cov(x, y)
    pearson = cov[0, 1]/np.sqrt(cov[0, 0] * cov[1, 1])
    # Using a special case to obtain the eigenvalues of this
    # two-dimensionl dataset.
    ell_radius_x = np.sqrt(1 + pearson)
    ell_radius_y = np.sqrt(1 - pearson)
    ellipse = Ellipse((0, 0), width=ell_radius_x * 2, height=ell_radius_y * 2,
                      facecolor=facecolor, **kwargs)

    # Calculating the stdandard deviation of x from
    # the squareroot of the variance and multiplying
    # with the given number of standard deviations.
    scale_x = np.sqrt(cov[0, 0]) * n_std
    mean_x = np.mean(x)

    # calculating the stdandard deviation of y ...
    scale_y = np.sqrt(cov[1, 1]) * n_std
    mean_y = np.mean(y)

    transf = transforms.Affine2D() \
        .rotate_deg(45) \
        .scale(scale_x, scale_y) \
        .translate(mean_x, mean_y)

    ellipse.set_transform(transf + ax.transData)
    return ax.add_patch(ellipse);


def plotBinormal(df, title):
    """
    Create a plot of the covariance confidence ellipse of value and peak norm.

    Parameters
    ----------
    df : dataframe, shape (n, )
        Input data.

    title : str
        The title of the plot

    """
    fig, ax_nstd = plt.subplots();
    ax_nstd.scatter(df['value'], df['peak_norm'],s=2.5)
    confidence_ellipse(df['value'], df['peak_norm'], ax_nstd, n_std=2,
                   label=r'$2\sigma$', edgecolor='fuchsia', linestyle='--')
    confidence_ellipse(df['value'], df['peak_norm'], ax_nstd, n_std=3,
                   label=r'$3\sigma$', edgecolor='blue', linestyle=':')
    ax_nstd.legend()
    ax_nstd.set_title(title)
    plt.show()
    
def plotScatMargHisto(df, title, x = 'value', y = 'peak_norm'):
    """
    Create a scatter plot with marginal histograms normalized.

    Parameters
    ----------
    df : dataframe, shape (n, )
        Input data.

    title : str
        The title of the plot

    """   
    colors = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA','#FFA15A','#19d3f3','#FF6692']


    fig = px.scatter(df, x=x, y=y, color = 'site', 
                     hover_data=['dates','peak_hours', 'site'],
                     color_discrete_sequence=colors)    
    ii = 0;
    for ss in df.site.unique():
        fig.add_trace(go.Histogram(
                y = df[y][df.site == ss], 
                name = ss, 
                xaxis = 'x2',
                histnorm='probability',
                marker_color = colors[ii]
            ))
            
        fig.add_trace(go.Histogram(
            x = df[x][df.site == ss], 
            name = ss, 
            yaxis = 'y2',
            histnorm='probability',
            marker_color = colors[ii]
            ))
        ii = ii+1;
        
    fig.update_layout(barmode='overlay')
    fig.update_traces(opacity=0.6)
    
    fig.update_layout(
        xaxis = dict(
            zeroline = False,
            domain = [0,0.85],
            showgrid = False
        ),
        yaxis = dict(
            zeroline = False,
            domain = [0,0.85],
            showgrid = False
        ),
        xaxis2 = dict(
            zeroline = False,
            domain = [0.85,1],
            showgrid = False
        ),
        yaxis2 = dict(
            zeroline = False,
            domain = [0.85,1],
            showgrid = False
        ),
        bargap = 0,
        hovermode = 'closest'
    )
    return fig