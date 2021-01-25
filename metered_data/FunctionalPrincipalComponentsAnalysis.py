# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 12:42:36 2021

https://towardsdatascience.com/beyond-classic-pca-functional-principal-components-analysis-fpca-applied-to-time-series-with-python-914c058f47a0
https://fdasrsf-python.readthedocs.io/en/latest/fPLS.html
"""
import pandas as pd
import numpy as np

from fdasrsf import fPCA, time_warping, fdawarp, fdahpca

from functions import get_weekdays_df
import matplotlib.pyplot as plt

# Import the CSV file with only useful columns
df = pd.read_csv("stream_volume.csv", sep=",")
df = pd.read_csv("C:/Users/paul/Documents/GitHub/HPWH-Sizing-Tool---Research/metered_data/stream_volume.csv", sep=",")
# Rename columns to simplify syntax
#df = df.set_index('time stamp')
#weekdays = get_weekdays_df(df) # filter for weekdays

# Select 2019 records only
#df = df[weekdays]

df = df.rename(columns={"dates": "date", "hour_pt": "hour", "gal in hr": "galphr"})

# Pivot table to get "Date" as index and regions as columns 
dfhrs = df.pivot(index = 'date', columns='hour', values='galphr')
#df = df.pivot(index='Date', columns='Region', values='Temp')
df = df.pivot(index='hour', columns='date', values='galphr')

pd.plotting.scatter_matrix(dfhrs, alpha=0.1)

plt.matshow(dfhrs.corr())
cb = plt.colorbar()
cb.ax.tick_params(labelsize=12)
plt.title('Correlation Matrix', fontsize=16);
plt.show()

# Get histogram of sums from time periods defined by hour start and hour fin
hr_start  = 6 #midnight is 0
hr_fin = 9 #Goes up to this hour i.e. does not include.
hrs_2_sum = list(range(hr_start,hr_fin))
dfhrs['hrsum'+str(hr_start)+str(hr_fin)] = dfhrs[hrs_2_sum].sum(axis=1)

# Select a set of regions across France
#df = df[["06","25","59","62","83","85","75"]]

#display(df)

# Convert the Pandas dataframe to a Numpy array with time-series only
f = df.to_numpy().astype(float)

# Create a float vector between 0 and 1 for time index
time = np.linspace(0,1,len(f))


# Functional Alignment
a = time_warping.align_fPCA(f, time)
# Align time-series
warp_f = time_warping.fdawarp(f, time)
warp_f.srsf_align(method=1)

warp_f.plot()

# Functional Principal Components Analysis

# Define the FPCA as a vertical analysis
fPCA_analysis = fPCA.fdavpca(warp_f)

# Run the FPCA on a 3 components basis 
fPCA_analysis.calc_fpca(no=6)
fPCA_analysis.plot()

import plotly.graph_objects as go

# Plot of the 3 functions
fig = go.Figure()

# Add traces
fig.add_trace(go.Scatter(y=fPCA_analysis.f_pca[:,0,0], mode='lines', name="PC1"))
fig.add_trace(go.Scatter(y=fPCA_analysis.f_pca[:,0,1], mode='lines', name="PC2"))
#fig.add_trace(go.Scatter(y=fPCA_analysis.f_pca[:,0,2], mode='lines', name="PC3"))

fig.update_layout(
    title_text='<b>Principal Components Analysis Functions</b>', title_x=0.5,
)

fig.show()

# Coefficients of PCs against regions
fPCA_coef = fPCA_analysis.coef

# Plot of PCs against regions
fig = go.Figure(data=go.Scatter(x=fPCA_coef[:,0], y=fPCA_coef[:,1], mode = 'markers'))#, mode='markers+text', text=df.columns))

#fig.update_traces(textposition='top center')

fig.update_layout(
    autosize=False,
    width=800,
    height=700,
    title_text='<b>Fus</b>', title_x=0.5,
    xaxis_title="PC1",
    yaxis_title="PC2",
)
fig.show()