# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 08:49:07 2020

@author: scott
"""

# dataframe imports
import pandas as pd
import numpy as np

# plotly
from plotly import subplots
from plotly import graph_objs as go
import plotly.express as px

from functions import plotBinormal, plotScatMargHisto

EJ_people = 62;
Yes_people = 276;
Stream_people = 140;
Sunset_people = 110;

# =============================================================================
# #### Import data
# =============================================================================
ejames_volume = pd.read_csv('ejames_volume.csv')
yesler_volume = pd.read_csv('yesler_volume.csv')
stream_volume = pd.read_csv('stream_volume.csv')
sunset_volume = pd.read_csv('sunset_volume.csv')
block11_volume = pd.read_csv('block11_volume.csv')

ejames_3peakyness = pd.read_csv('ejames_3hr_peakyness.csv')
yesler_3peakyness = pd.read_csv('yesler_3hr_peakyness.csv')
stream_3peakyness = pd.read_csv('stream_3hr_peakyness.csv')
sunset_3peakyness = pd.read_csv('sunset_3hr_peakyness.csv')
block11_3peakyness = pd.read_csv('block11_3hr_peakyness.csv')

ejames_4peakyness = pd.read_csv('ejames_4hr_peakyness.csv')
yesler_4peakyness = pd.read_csv('yesler_4hr_peakyness.csv')
stream_4peakyness = pd.read_csv('stream_4hr_peakyness.csv')
sunset_4peakyness = pd.read_csv('sunset_4hr_peakyness.csv')

ejames_5peakyness = pd.read_csv('ejames_5hr_peakyness.csv')
yesler_5peakyness = pd.read_csv('yesler_5hr_peakyness.csv')
stream_5peakyness = pd.read_csv('stream_5hr_peakyness.csv')
sunset_5peakyness = pd.read_csv('sunset_5hr_peakyness.csv')

ejames_18peakyness = pd.read_csv('ejames_18hr_peakyness.csv')
yesler_18peakyness = pd.read_csv('yesler_18hr_peakyness.csv')
stream_18peakyness = pd.read_csv('stream_18hr_peakyness.csv')
sunset_18peakyness = pd.read_csv('sunset_18hr_peakyness.csv')


#Get the value per person
ejames_5peakyness['valuepp'] = ejames_5peakyness['value'] / EJ_people
yesler_5peakyness['valuepp'] = yesler_5peakyness['value'] / Yes_people
stream_5peakyness['valuepp'] = stream_5peakyness['value'] / Stream_people
sunset_5peakyness['valuepp'] = sunset_5peakyness['value'] / Sunset_people


yesler_18peakyness['valuepp'] = yesler_18peakyness['value'] / Yes_people
stream_18peakyness['valuepp'] = stream_18peakyness['value'] / Stream_people
ejames_18peakyness['valuepp'] = ejames_18peakyness['value'] / EJ_people
sunset_18peakyness['valuepp'] = sunset_18peakyness['value'] / Sunset_people
# =============================================================================
# #### Scatter Plots
# =============================================================================

# fig = px.scatter(ejames_3peakyness, x='dates', y="value", hover_data=['dates'])
# fig.write_html("ejames_scatter.html")

# fig = px.scatter(yesler_3peakyness, x='dates', y="value", hover_data=['dates'])
# fig.write_html("yesler_scatter.html")

# fig = px.scatter(stream_3peakyness, x='dates', y="value", hover_data=['dates'])
# fig.write_html("stream_scatter.html")

# fig = px.scatter(sunset_3peakyness, x='dates', y="value", hover_data=['dates'])
# fig.write_html("sunset_scatter.html")

# fig = px.scatter(block11_3peakyness, x='dates', y="value", hover_data=['dates'])
# fig.write_html("block11_scatter.html")

# =============================================================================
# #### Cummulative Histograms
# =============================================================================

x = ejames_3peakyness['value']/EJ_people
fig = go.Figure(data=[go.Histogram(x=x, cumulative_enabled=True, histnorm='probability density')])
fig.update_layout(xaxis_title = "GPD per Person", yaxis_title = "Percentile")
fig.write_html("ejames_hist.html")

x = yesler_3peakyness['value']/Yes_people
fig = go.Figure(data=[go.Histogram(x=x, cumulative_enabled=True, histnorm='probability density')])
fig.update_layout(xaxis_title = "GPD per Person", yaxis_title = "Percentile")
fig.write_html("yesler_hist.html")

x = stream_3peakyness['value']/Stream_people
fig = go.Figure(data=[go.Histogram(x=x, cumulative_enabled=True, histnorm='probability density')])
fig.update_layout(xaxis_title = "GPD per Person", yaxis_title = "Percentile")
fig.write_html("stream_hist.html")

x = sunset_3peakyness['value']/Sunset_people
fig = go.Figure(data=[go.Histogram(x=x, cumulative_enabled=True, histnorm='probability density')])
fig.update_layout(xaxis_title = "GPD per Person", yaxis_title = "Percentile")
fig.write_html("sunset_hist.html")

# =============================================================================
# #### Peakyness Plots
# =============================================================================
def new_peak_plot(df):
    # peakyness scatterplots for individual buildings
    hist, xedges, yedges = np.histogram2d(df['value'], df['peak_norm'], bins=100)
    cumhist = np.cumsum(np.cumsum(hist,axis=1), axis = 0)
    cumhist = cumhist/np.amax(cumhist) #normalize the array.
    xedges = np.append(xedges[0],xedges[2:]); 
    yedges = np.append(yedges[0],yedges[2:]);

    fig = go.Figure(data = go.Contour( z= cumhist, x = xedges, y = yedges,
                                      contours=dict(start=.15,end=1, size=.05,),
                                      colorbar=dict(len=0.6,lenmode='fraction',)
                ))
    fig.add_trace(go.Scatter( x=df['value'], 
                             y=df["peak_norm"],  mode='markers',
                             text = 'Date: '+ df['dates'],
                             hoverinfo = 'text'))
    fig.update_xaxes(range=[xedges[0], max(xedges)])
    fig.update_yaxes(range=[yedges[0], max(yedges)])
    return fig;

fig = new_peak_plot(ejames_3peakyness);
fig.write_html("ejames_3peakyness.html")
fig = new_peak_plot(yesler_3peakyness)
fig.write_html("yesler_3peakyness.html")
fig = new_peak_plot(stream_3peakyness)
fig.write_html("stream_3peakyness.html")
fig = new_peak_plot(sunset_3peakyness)
fig.write_html("sunset_3peakyness.html")

fig = new_peak_plot(ejames_4peakyness);
fig.write_html("ejames_4peakyness.html")
fig = new_peak_plot(yesler_4peakyness)
fig.write_html("yesler_4peakyness.html")
fig = new_peak_plot(stream_4peakyness)
fig.write_html("stream_4peakyness.html")
fig = new_peak_plot(sunset_4peakyness)
fig.write_html("sunset_4peakyness.html")

fig = new_peak_plot(ejames_5peakyness);
fig.write_html("ejames_5peakyness.html")
fig = new_peak_plot(yesler_5peakyness)
fig.write_html("yesler_5peakyness.html")
fig = new_peak_plot(stream_5peakyness)
fig.write_html("stream_5peakyness.html")
fig = new_peak_plot(sunset_5peakyness)
fig.write_html("sunset_5peakyness.html")

# combo non normalizied peakyness scatterplots
df = ejames_3peakyness.append(yesler_3peakyness).append(stream_3peakyness).append(sunset_3peakyness)
fig = px.scatter(df, x='value', y="peak_volumes", color = 'site', 
                 hover_data=['dates', 'peak_hours', 'site','peak_norm'])
fig.add_trace(go.Scatter(x=[1000,6000], y = [305, .305*6000.],  mode='lines', name = '0.3 peak norm',
                 line = dict(color = 'gray', dash='dash')))
fig.write_html("sites_peakyness_actual_noBlock11.html")

# combo peak scatterplots
def plot_peak_scatters(df, x = 'value', y = 'peak_norm'):
    fig = px.scatter(df, x=x, y=y, color = 'site', 
                     hover_data=['dates', 'peak_hours', 'site'])
    fig.add_trace(go.Scatter(x=[1000,6000], y = [.305,.305],  mode='lines', name = 'ASHRAE Low',
                     line = dict(dash='dash')))
    fig.add_trace(go.Scatter(x=[1000,6000], y = [.225, .225],  mode='lines', name = 'ASHRAE Medium',
                     line = dict(dash='dash')))
    fig.add_trace(go.Scatter(x=[1000,6000], y = [.6, 600./6000.],  mode='lines', name = '600 gal peak',
                     line = dict(color = 'lightgray', dash='dash')))
    fig.add_trace(go.Scatter(x=[1000,6000], y = [.5, 500./6000.],  mode='lines', name = '500 gal peak',
                     line = dict(color = 'lightgray', dash='dash')))
    fig.add_trace(go.Scatter(x=[1000,6000], y = [.4, 400./6000.],  mode='lines', name = '400 gal peak',
                     line = dict(color = 'lightgray',dash='dash')))
    fig.add_trace(go.Scatter(x=[1000,6000], y = [.3, 300./6000.],  mode='lines', name = '300 gal peak',
                     line = dict(color = 'lightgray',dash='dash')))
    fig.add_trace(go.Scatter(x=[1000,6000], y = [.2, 200./6000.],  mode='lines', name = '200 gal peak',
                     line = dict(color = 'lightgray',dash='dash')))
    return fig;

df = ejames_3peakyness.append(yesler_3peakyness).append(stream_3peakyness).append(sunset_3peakyness)
#df['peak_norm'] = df['peak_norm']/3
fig = plot_peak_scatters(df)
fig.update_layout(
        xaxis_title="Daily HW Use (Gal)",
        yaxis_title="Normalized 3 Hour Peak")
fig.write_html("sites_3hr_peakyness_noBlock11.html")

df = ejames_4peakyness.append(yesler_4peakyness).append(stream_4peakyness).append(sunset_4peakyness)
#df['peak_norm'] = df['peak_norm']/4
fig = plot_peak_scatters(df)
fig.update_layout(
        xaxis_title="Daily HW Use (Gal)",
        yaxis_title="Normalized 4 Hour Peak")
fig.write_html("sites_4hr_peakyness_noBlock11.html")

df = ejames_5peakyness.append(yesler_5peakyness).append(stream_5peakyness).append(sunset_5peakyness)
#df['peak_norm'] = df['peak_norm']/5
fig = plot_peak_scatters(df)
fig.update_layout(
        xaxis_title="Daily HW Use (Gal)",
        yaxis_title="Normalized 5 Hour Peak")
fig.write_html("sites_5hr_peakyness_noBlock11.html")


df = ejames_5peakyness.append(yesler_5peakyness).append(stream_5peakyness).append(sunset_5peakyness)
#df['peak_norm'] = df['peak_norm']/5
fig = plot_peak_scatters(df, x = 'valuepp')
fig.update_layout(
        xaxis_title="Daily HW Use per Person (gpdpp)",
        yaxis_title="Normalized 5 Hour Peak")
fig.write_html("sites_5hr_peakyness_pp_noBlock11.html")


fig = plotScatMargHisto(df,"",x = 'valuepp')
fig.update_layout(
        xaxis_title="Daily HW Use per Person (gpdpp)",
        yaxis_title="Normalized 5 Hour Peak")
fig.write_html("sites_5hr_peakyness_pp_noBlock11.html")


df = ejames_18peakyness.append(yesler_18peakyness).append(stream_18peakyness).append(sunset_18peakyness)
df =  df[df.peak_hours != 0] #Remove rows where the peak hours is 0 because this is zero, really is like 15 days
fig = plot_peak_scatters(df)
fig.update_layout(
        xaxis_title="Daily HW Use (Gal)",
        yaxis_title="Normalized Volume Sized from Peak")
fig.write_html("sites_sized_volume_noBlock11.html")


##############################################################################
# Histogram plot of the peak hours!
fig = px.histogram(df, x="peak_hours", color = 'site', histnorm='probability density', marginal="box")
fig.update_layout(barmode='overlay',
        xaxis_title="Hours in Peak for 18 Hour Runtime",
        yaxis_title="Probability")
# Reduce opacity to see both histograms
fig.update_traces(opacity=0.75)

fig.write_html("sites_HistogramHours_inPeak_noBlock11.html")


# Peak hours vs....
fig = px.scatter(df,x='valuepp', y="peak_hours", color = 'site', facet_col="site",
                     hover_data=['dates', 'peak_hours', 'site'],
                     marginal_x="box", marginal_y="box")
fig.update_layout(barmode='overlay',
        xaxis_title="Gallons Per Person",
        yaxis_title="Hours in Peak for 18 Hour Runtime")
# Reduce opacity to see both histograms
fig.update_traces(opacity=0.65)
fig.write_html("sites_GPDPP_vs_HoursinPeak_noBlock11.html")

# Peak hours vs....
fig = px.scatter(df,x='peak_norm', y="peak_hours", color = 'site', facet_col="site",
                     hover_data=['dates', 'peak_hours', 'site'],
                     marginal_x="box", marginal_y="box")
fig.update_layout(barmode='overlay',
        xaxis_title="Normalized Peak Volume",
        yaxis_title="Hours in Peak for 18 Hour Runtime")
# Reduce opacity to see both histograms
fig.update_traces(opacity=0.65)
fig.write_html("sites_PeakVol_vs_HoursinPeak_noBlock11.html")
#fig.write_html("sites_Hours_inPeak_noBlock11.html")



##############################################################################


# =============================================================================
# #### Peakyness Distributions
# =============================================================================

def plot_peak_scatters(df1, namedf1, people, divide = [3,0,0], df2 =  pd.DataFrame(), namedf2="", df3 =  pd.DataFrame(), namedf3 = ""):
    
    df = [df1, df2 , df3]
    names = [namedf1, namedf2, namedf3]
    
    fig = subplots.make_subplots(rows=1,
                      cols=2,
                      start_cell="bottom-left",
                      subplot_titles=('Total Volume Per Person [gpdpp]', 'Peak Norm'))    
    x = df1['value']/people
    trace1 = go.Histogram(x=x, cumulative_enabled=True, histnorm='probability density',
                          nbinsx = 100, name = "Daily HW Volume" )
    trace2 = [];
    for i in range(3):
        if df[i].empty: continue
        x = df[i]['peak_norm']/divide[i]
        trace2.append( go.Histogram(x=x, cumulative_enabled=True, histnorm='probability density',
                          nbinsx = 100, showlegend=True, name = names[i] )  )      
    fig.add_trace(trace1, row=1,col=1)
    for t in trace2:
        fig.add_trace(t, row=1,col=2)
        # Overlay both histograms
        fig.update_layout(barmode='overlay')
        # Reduce opacity to see both histograms
        fig.update_traces(opacity=0.6)
    
    return fig

# ejames
fig = plot_peak_scatters(ejames_3peakyness,"3 hr peakyness", EJ_people, [3,4,5],
                         ejames_4peakyness,"4 hr peakyness",ejames_5peakyness,"5 hr peakyness")
fig.update_layout(title_text="ejames peakyness distributions")
fig.write_html("ejames_3peakyness_distribution.html")
# stream 
fig = plot_peak_scatters(stream_3peakyness,"3 hr peakyness", Stream_people, [1,1,1],
                         stream_4peakyness,"4 hr peakyness",stream_5peakyness,"5 hr peakyness")
fig.update_layout(title_text="stream peakyness distributions")
fig.write_html("stream_peakyness_distribution.html")
# sunset
fig = plot_peak_scatters(sunset_3peakyness,"3 hr peakyness", Sunset_people, [3,4,5],
                         sunset_4peakyness,"4 hr peakyness",sunset_5peakyness,"5 hr peakyness")
fig.update_layout(title_text="sunset peakyness distributions")
fig.write_html("sunset_peakyness_distribution.html")
# yesler
fig = plot_peak_scatters(yesler_3peakyness,"3 hr peakyness", Yes_people, [3,4,5],
                         yesler_4peakyness,"4 hr peakyness",yesler_5peakyness,"5 hr peakyness")
fig.update_layout(title_text="yesler peakyness distributions")
fig.write_html("yesler_peakyness_distribution.html")


# block11
fig = subplots.make_subplots(rows=1,
                  cols=2,
                  start_cell="bottom-left",
                  subplot_titles=('Total Volume [gals]', 'Peak Norm'))

x = block11_3peakyness['value']
trace1 = go.Histogram(x=x, cumulative_enabled=True, histnorm='probability density')
x = block11_3peakyness['peak_norm']
trace2 = go.Histogram(x=x, cumulative_enabled=True, histnorm='probability density')

fig.append_trace(trace1, row=1,col=1)
fig.append_trace(trace2, row=1,col=2)

fig.update_layout(title_text="block11 peakyness distributions")
fig.write_html("block11_peakyness_distribution.html")
