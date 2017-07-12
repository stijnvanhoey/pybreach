# -*- coding: utf-8 -*-
"""
# plot BReach plot
Created on Tue May 16 16:00:42 2017

@author: kveerden
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec


##############################!!!!!!!!!!!!!!!!!!!!!!!
## vervang dit op termijn door functie met o.a. BReach en hQ data als input (later uit te breiden met moments of floods, official RC changes en afgebakende consistente periodes)
# define station and type of results to analyze
unc_type = '2'  # type of uncertainty assessment ('2' = Belgian and McMillan, 2010, '4' = Coxon, 2015)
result_type = 'h'  # type of breach results (t = chronologically, h = along height)
sname = 'maa02a'  # name of station to analyze
data_type = '0'  # type of dataset ('0' = all data, '5' = winter data)

# Load BReach file and hQ data
# -----------------------------
breach = np.load(
    'breach{0}_{1}_{2}_{3}.npy'.format(unc_type, sname, result_type,
                                       data_type))  # load breach data
breach = breach - 1  # adapt to indexing in Python (0,1,2 vs Matlab 1,2,3)
hQ = np.load('hQ_{0}_{1}_{2}.npy'.format(sname, result_type,
                                         data_type))  # load hQ data (sorted along time tof data_type == 't', along height if data type == 'h'. Col0 = h, col1 = Q, col2 = Area, col3/col4 = moment start measurement (hour/minutes), col5/col6 = moment end measurement (hour/minutes), col7 = ???? col8 = day, col9 = month, col10 = year, col11 = contin. registred height, col12 = calculated area based on height and section data)
x1 = np.arange(breach.shape[0])  # indices of data points

# Specify figure characteristics
# -------------------------------
space_betw = 0.01  # space between two subplots (as fraction of heiight of subplot 1)
height_subpl2 = 0.03  # height of subplot 2 as a fraction of height of subplot 1)
labels_subpl2 = 0.1
height_fig = 1 + space_betw + height_subpl2 + labels_subpl2  # overall height of figure as fraction of subplot 1
fig = plt.figure(figsize=(6, (
1 + space_betw + height_subpl2) * 6))  # height figure = height subplot1 + space between subpl 1 and 2 + height subplot 2
G = GridSpec(np.int(breach.shape[0] * height_fig * 1000),
                      1)  # heb aantal grids in height zeer groot gemaakt om voor alle plots (ook met weinig datapunten) dezelfde verhouding van subplots en afstand tussenin te krijgen.

# BReach plot (subplot 1)
# ------------------------
ax1 = plt.subplot(G[0: np.int_(breach.shape[0] * 1000), :], aspect='equal',
                  adjustable='box-forced')  # create square plot
ax1.set_xlim([0, breach.shape[0] - 1])
ax1.set_ylim([0, breach.shape[0] - 1])
plt.hold(True)

for i in range(
        5):  # for every degree of tolerance (DoT) - largest degrees first
    kleur = 0.75 - (i) * 0.15  # light gray to black
    lijnkleur = np.maximum(0.75 - (i + 1) * 0.15,
                           0)  # color of the following DoT
    ax1.fill_between(x1, breach[:, -2 * i - 1], breach[:, -2 * i - 2],
                     facecolor=str(kleur), edgecolor=str(lijnkleur))

ax1.set_ylabel('Index')
ax1.set_xlabel('Index')
pos1 = ax1.get_position()  # get the position of subplot 1

# time or height interval plot (subplot 2)
# -----------------------------------------
ax2 = plt.subplot(G[
                  np.int_(breach.shape[0] * (1 + space_betw) * 1000): np.int_(
                      breach.shape[0] * (
                      1 + space_betw + height_subpl2) * 1000), :],
                  autoscale_on='false',
                  sharex=ax1)  #:np.int(((7/28-0.15)*breach.shape[0]+(breach.shape[0]*1.15))*1000), :], autoscale_on = 'false', sharex=ax1)
# position of subplot 1 is (the x axis shrunk) by the options aspect='equal', adjustable='box-forced'
# and thus, using this position (pos 1) for subplot 2 results in a wider x axis
# Therefore, this position is corrected using the relative position of both axes using pos1
# The measures mentioned in the comment explain where the float value in the multiplication comes from.
# These measures are measured in CorrelDRAW, only relative measured values are used.
# Warning! If changing the height of subplot 1, these values will change
left = pos1.bounds[0] + 0.056 * pos1.bounds[
    2]  # 0.056 = (left point of x_subplot 2 - left point of x_subplot 1) / width of x axis in subplot 2
bottom = 1 - (1 + space_betw + height_subpl2) / height_fig
width = 0.888 * pos1.bounds[
    2]  # 0.888 = width of x axis in subplot 1 / width of x axis in subplot 2
height = height_subpl2 / height_fig
pos2 = left, bottom, width, height
ax2.set(position=pos2, xlim=[0, breach.shape[0] - 1], ylim=[0, 1])

plt.hold(True)

# set timestep for intervals to use in figure
if result_type == 't':
    years = hQ[-1:, 10] - hQ[0, 10] + 1  # length (in years) of hQ series
    steps = np.array(
        [1, 5, 10, 15, 20, 25, 50, 75, 100])  # possible time intervals
    step = steps[steps.shape[0] - 1 - np.abs(
        steps[::-1] - (years / 4) * np.ones(
            steps.shape)).argmin()]  # Pick time interval from steps that is closest to the step that results from a restricion of the amount of intervals based on length of data series. By inverting largest timestep is picked if values are equal
    tekst = 'Year'  # ylabel
    col = 10  # column in hQ file that provides information about the year

# set height classes to use in figure
if result_type == 'h':
    height_diff = hQ[-1:, 0] - hQ[
        0, 0]  # height difference covered by the hQ data series sorted along height
    step = np.int_(
        height_diff / 4 * 10) / 10  # Pick height interval that results from a restricion of the amount of intervals based on height_diff of data series ([m], one decimal number)
    tekst = 'Stage [m]'  # ylabel
    col = 0  # column in hQ file that provides information about height

# allocate grayscale to alternating time/height intervals
j = 0  # indicator that interval changes
classes = np.zeros((hQ.shape[0],
                    2))  # first column = start value of interval, second column = corresponding grayscale value for plot
for i in range(hQ.shape[0]):  # allocate a class for each hQ data point
    classes[i, 0] = np.floor(
        hQ[i, col] / step) * step  # first column = start value of interval
    if i != 0 and classes[i, 0] != classes[
                i - 1, 0]:  # if class value changes in a point
        j = j + 1
    classes[i, 1] = 0.5 * (
    j % 2) + 0.25  # allocate grayscale (alternating dark gray (0.25) and light gray (0.75))

# plot time intervals
for i in range(hQ.shape[0]):
    ax2.fill_between(np.arange(i, i + 2), 0, 1, color=str(classes[i, 1]),
                     edgecolor='none')  # str(classes[i,1]))

# ticks and labels invisible, ylabel visible
plt.setp(ax2.get_yticklabels(), visible=False)
plt.setp(ax2.get_xticklabels(), visible=False)
ax2.yaxis.set_ticks_position('none')
ax2.xaxis.set_ticks_position('none')
ax2.set_ylabel(tekst, rotation=0, horizontalalignment='right',
               verticalalignment='center')
pos2 = ax2.get_position()  # get the position of subplot 2

# ax3 = axis for subplot 2 (add new, independent x axis)
# -------------------------------------------------
# Set ticks and labels for this axis (and thus for subplot 2)
labels = (np.add(classes[np.concatenate(
    (abs(np.subtract(classes[0:-1, 1], classes[1:, 1])), [0]),
    axis=0) == 0.5, 0],
                 step))  # value (year or height) of the start of an interval
x2 = []  # initiate ticks for x-axis (indices in hQ series that correspond with an interval change)
x2 = np.asarray(np.nonzero(
    np.concatenate((abs(np.subtract(classes[0:-1, 1], classes[1:, 1])), [0]),
                   axis=0)))  # keep indices (i) for which start value of the interval changes in (i+1)
x2 = np.reshape(x2, x2.shape[
    1])  # make 2dim array in order for concatenation underneath
x2 = x2 + 1  # change of interval was not in (i) but in (i+1)
if x2[0] == 0:
    labels[0] = hQ[
        0, col]  # if first hQ point is member of ticks, replace value of start of interval by real year/height of that first data point
if x2[-1:] == hQ.shape[0]:
    labels[-1:] = hQ[-1:,
                  col]  # if last hQ point is member of ticks, replace value of start of interval by real year/height of that last data point

# test if two consecutive ticks are located too close to eachother to have a readable label
test = np.array(
    np.concatenate(([hQ.shape[0]], np.diff(x2)), axis=0))  # distance on x-axis
ind = np.array(np.arange(x2.shape[0])[test[:] <= 0.04 * hQ.shape[
    0]])  # test if smaller than disctance that allows a readable label
x2 = np.delete(x2, ind)  # delete second tick value if distance is too small
labels = np.delete(labels,
                   ind)  # delete second label value if distance is too small

# Add first and last hQ data point if distance with next interval tick is large enough to guarantee readable labels
if x2[0] > 0.04 * hQ.shape[0]:  # test for first hQ data point
    x2 = np.concatenate(([0], x2),
                        axis=0)  # add position of first data point to ticks
    labels = (np.concatenate(([hQ[0, col]], labels),
                             axis=0))  # Add year of first data point to labels
if hQ.shape[0] - x2[-1:] > 0.04 * hQ.shape[0]:  # test for last hQ data point
    x2 = np.concatenate((x2, [hQ.shape[0] - 1]),
                        axis=0)  # add position of last data point to ticks
    labels = (np.concatenate((labels, [hQ[-1, col]]),
                             axis=0))  # Add year of last data point to labels

# Create extra axis located on the x axis of subplot 2
ax3 = fig.add_axes(
    [pos2.bounds[0], pos2.bounds[1], pos2.bounds[2], pos2.bounds[1]],
    frameon=False)  # no height allocated
ax3.set_xlim([0, breach.shape[0] - 1])
plt.setp(ax3.get_yticklabels(),
         visible=False)  # no original ticks visible, mainly important for y axis
ax3.yaxis.set_ticks_position(
    'none')  # no original labels visible, , mainly important for y axis
if result_type == 't':
    plt.xticks(x2, np.int_(labels), rotation=-90)
if result_type == 'h':
    labels = np.int_(labels * 10) / 10  # labels in [m], one decimal number
    plt.xticks(x2, labels, rotation=-90)

ax3.xaxis.set_ticks_position('none')
#   eigenlijk liever wel tocks plaatsen, alleen zit er kleine verschuiving op de ticks aan het begin van de lichtgrijze intervallen die ik niet snap en niet kan oplossen

fig_name = 'breach{0}_{1}_{2}_{3}.tif'.format(unc_type, sname, result_type,
                                              data_type)
fig.savefig(fig_name)