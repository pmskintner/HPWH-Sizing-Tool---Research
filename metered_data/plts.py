# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 08:49:07 2020

@author: scott
"""

# dataframe imports
import pandas as pd

# plotly
from plotly import subplots
from plotly import graph_objs as go
import plotly.express as px


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
# #### Scatter Plots
# =============================================================================

fig = px.scatter(ejames_peakyness, x='dates', y="value", hover_data=['dates'])
fig.write_html("ejames_scatter.html")

fig = px.scatter(yesler_peakyness, x='dates', y="value", hover_data=['dates'])
fig.write_html("yesler_scatter.html")

fig = px.scatter(stream_peakyness, x='dates', y="value", hover_data=['dates'])
fig.write_html("stream_scatter.html")

fig = px.scatter(sunset_peakyness, x='dates', y="value", hover_data=['dates'])
fig.write_html("sunset_scatter.html")

fig = px.scatter(block11_peakyness, x='dates', y="value", hover_data=['dates'])
fig.write_html("block11_scatter.html")

# =============================================================================
# #### Cummulative Histograms
# =============================================================================

x = ejames_peakyness['value']
fig = go.Figure(data=[go.Histogram(x=x, cumulative_enabled=True, histnorm='probability density')])
fig.write_html("ejames_hist.html")

x = yesler_peakyness['value']
fig = go.Figure(data=[go.Histogram(x=x, cumulative_enabled=True, histnorm='probability density')])
fig.write_html("yesler_hist.html")

x = stream_peakyness['value']
fig = go.Figure(data=[go.Histogram(x=x, cumulative_enabled=True, histnorm='probability density')])
fig.write_html("stream_hist.html")

x = sunset_peakyness['value']
fig = go.Figure(data=[go.Histogram(x=x, cumulative_enabled=True, histnorm='probability density')])
fig.write_html("sunset_hist.html")

x = block11_peakyness['value']
fig = go.Figure(data=[go.Histogram(x=x, cumulative_enabled=True, histnorm='probability density')])
fig.write_html("block11_hist.html")

# =============================================================================
# #### Peakyness Plots
# =============================================================================

# peakyness scatterplots for individual buildings
fig = px.scatter(ejames_peakyness, x='value', y="peak_norm", hover_data=['dates', 'peak_hours'])
fig.write_html("ejames_peakyness.html")

fig = px.scatter(block11_peakyness, x='value', y="peak_norm", hover_data=['dates', 'peak_hours'])
fig.write_html("block11_peakyness.html")

fig = px.scatter(yesler_peakyness, x='value', y="peak_norm", hover_data=['dates', 'peak_hours'])
fig.write_html("yesler_peakyness.html")

fig = px.scatter(stream_peakyness, x='value', y="peak_norm", hover_data=['dates', 'peak_hours'])
fig.write_html("stream_peakyness.html")

fig = px.scatter(sunset_peakyness, x='value', y="peak_norm", hover_data=['dates', 'peak_hours'])
fig.write_html("sunset_peakyness.html")

# combo peakyness scatterplots
df = ejames_peakyness.append(yesler_peakyness).append(stream_peakyness).append(sunset_peakyness).append(block11_peakyness)
fig = px.scatter(df, x='value', y="peak_norm", color = 'site', 
                 hover_data=['dates', 'peak_hours', 'site'])
fig.write_html("sites_peakyness.html")

df = ejames_peakyness.append(yesler_peakyness).append(stream_peakyness).append(sunset_peakyness)
fig = px.scatter(df, x='value', y="peak_norm", color = 'site', 
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
fig.write_html("sites_peakyness_noBlock11.html")

# combo non normalizied peakyness scatterplots
df = ejames_peakyness.append(yesler_peakyness).append(stream_peakyness).append(sunset_peakyness)
fig = px.scatter(df, x='value', y="peak_volumes", color = 'site', 
                 hover_data=['dates', 'peak_hours', 'site','peak_norm'])
fig.add_trace(go.Scatter(x=[1000,6000], y = [305, .305*6000.],  mode='lines', name = '0.3 peak norm',
                 line = dict(color = 'gray', dash='dash')))
fig.write_html("sites_peakyness_actual_noBlock11.html")


# =============================================================================
# #### Peakyness Distributions
# =============================================================================

# ejames
fig = subplots.make_subplots(rows=1,
                  cols=2,
                  start_cell="bottom-left",
                  subplot_titles=('Total Volume [gals]', 'Peak Norm'))

x = ejames_peakyness['value']
trace1 = go.Histogram(x=x, cumulative_enabled=True, histnorm='probability density')
x = ejames_peakyness['peak_norm']
trace2 = go.Histogram(x=x, cumulative_enabled=True, histnorm='probability density')   

fig.append_trace(trace1, row=1,col=1)
fig.append_trace(trace2, row=1,col=2)

fig.update_layout(title_text="ejames peakyness distributions")
fig.write_html("ejames_peakyness_distribution.html")

# sunset
fig = subplots.make_subplots(rows=1,
                  cols=2,
                  start_cell="bottom-left",
                  subplot_titles=('Total Volume [gals]', 'Peak Norm'))

x = sunset_peakyness['value'],
trace1 = go.Histogram(x=x, cumulative_enabled=True, histnorm='probability density')
x = sunset_peakyness['peak_norm']
trace2 = go.Histogram(x=x, cumulative_enabled=True, histnorm='probability density')

fig.append_trace(trace1, row=1,col=1)
fig.append_trace(trace2, row=1,col=2)

fig.update_layout(title_text="sunset peakyness distributions")
fig.write_html("sunset_peakyness_distribution.html")

# yesler
fig = subplots.make_subplots(rows=1,
                  cols=2,
                  start_cell="bottom-left",
                  subplot_titles=('Total Volume [gals]', 'Peak Norm'))

x = yesler_peakyness['value']
trace1 = go.Histogram(x=x, cumulative_enabled=True, histnorm='probability density')
x = yesler_peakyness['peak_norm']
trace2 = go.Histogram(x=x, cumulative_enabled=True, histnorm='probability density')

fig.append_trace(trace1, row=1,col=1)
fig.append_trace(trace2, row=1,col=2)

fig.update_layout(title_text="yesler peakyness distributions")
fig.write_html("yesler_peakyness_distribution.html")

# stream
fig = subplots.make_subplots(rows=1,
                  cols=2,
                  start_cell="bottom-left",
                  subplot_titles=('Total Volume [gals]', 'Peak Norm'))

x = stream_peakyness['value']
trace1 = go.Histogram(x=x, cumulative_enabled=True, histnorm='probability density')
x = stream_peakyness['peak_norm']
trace2 = go.Histogram(x=x, cumulative_enabled=True, histnorm='probability density')

fig.append_trace(trace1, row=1,col=1)
fig.append_trace(trace2, row=1,col=2)

fig.update_layout(title_text="stream peakyness distributions")
fig.write_html("stream_peakyness_distribution.html")

# block11
fig = subplots.make_subplots(rows=1,
                  cols=2,
                  start_cell="bottom-left",
                  subplot_titles=('Total Volume [gals]', 'Peak Norm'))

x = block11_peakyness['value']
trace1 = go.Histogram(x=x, cumulative_enabled=True, histnorm='probability density')
x = block11_peakyness['peak_norm']
trace2 = go.Histogram(x=x, cumulative_enabled=True, histnorm='probability density')

fig.append_trace(trace1, row=1,col=1)
fig.append_trace(trace2, row=1,col=2)

fig.update_layout(title_text="block11 peakyness distributions")
fig.write_html("block11_peakyness_distribution.html")
