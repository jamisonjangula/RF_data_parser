import pyarrow.parquet as pq
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, writers

# File specs for opening csv
inFile = './RFExplorer_MultipleSweepData_2022_05_23_17_04_45.csv'
title = 'RF Explorer CSV data file: RFExplorer PC Client - Format v005'
table = pd.read_csv(inFile)

# get frequencies & convert to float
freq = ((table.loc[4, title]).split("\t"))[4:]
for j in range(0, len(freq)):
    freq[j] = float(freq[j])

# get first time point - this will be subtracted from all time points
time0 = ((table.loc[5, title]).split("\t"))[2] + ((table.loc[5, title]).split("\t"))[3]
time0 = time0.split(":")
time0 = float(time0[0])*3600.0 + float(time0[1])*60.0 + float(time0[2])

# get number of sweeps captured
sweeps = int(((table.loc[2, title]).split(" "))[3])

# define figure parameters
fig, ax = plt.subplots()
ax.set_xlim(freq[0], freq[-1])
ax.set_ylim(-120, 0)
line, = ax.plot(0, 0)

# update figure with power values for the current sweep
def animation_frame(i):
    time = ((table.loc[i+5, title]).split("\t"))[2] + ((table.loc[i+5, title]).split("\t"))[3]
    time = time.split(":")
    time = float(time[0])*3600.0 + float(time[1])*60.0 + float(time[2])
    time -= time0
    power = (table.loc[i+5, title]).split("\t")[4:]
    for j in range(0, len(power)):
        power[j] = float(power[j])

    line.set_xdata(freq)
    line.set_ydata(power)
    return line, 

# make animation frame for current sweep values
animation = FuncAnimation(fig, func=animation_frame, frames=np.arange(0, sweeps, 1), interval=10)

# setting up writers object 
Writer = writers['ffmpeg']
writer = Writer(fps=15, metadata={'artist': 'Me'}, bitrate=1800)

# save as mp4
outFile = inFile.split('/')
outFile = (outFile[1].split('.'))[0] + '.mp4'
print('\nVideo saved in ./' + outFile + '\n')
animation.save(outFile, writer)