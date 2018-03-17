# -*- coding: utf-8 -*-
"""
# plot BReach plot

@author: kveerden, refactored by S. Van Hoey
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec


def breachplot(breach, station_name, hq_data=None,
               result_type='height', data_type='all',
               degrees_of_tolerance=[40, 20, 10, 5, 0],
               savefig=False):
    """Plot output of BReach analysis

    Parameters
    ----------
    breach :

    hq :

    result_type : {'height', 'time'}
        Is the result derived from a time based or rather a height based
        analysis
    degrees_of_tolerance : list of int
    """

    indices = np.arange(breach.shape[0])

    # figure characteristics
    figure_properties = {"space_between" : 0.01,
                         "relative_height_subplot2" : 0.03,
                         "labels_subplot2" : 0.1}

    # overall height of figure as fraction of subplot 1
    figure_height = 1. + figure_properties["space_between"] + \
        figure_properties["height_subpl2"] + \
        figure_properties["labels_subpl2"]
    figure_height_no_label = 1. + figure_properties["space_between"] + \
        figure_properties["height_subpl2"]
    fig = plt.figure(figsize=(6, figure_height_no_label * 6))

    # Large number to have consistency among figures; TO FIX!
    plot_grid = GridSpec(np.int(breach.shape[0] * figure_height * 1000), 1)

    # BReach plot (subplot 1)
    # --------------------------
    ax1 = plt.subplot(plot_grid[0: np.int_(breach.shape[0] * 1000), :],
                      aspect='equal', adjustable='box-forced')
    ax1.set_xlim([0, breach.shape[0] - 1])
    ax1.set_ylim([0, breach.shape[0] - 1])

    for i, _ in enumerate(degrees_of_tolerance):
        color = 0.75 - i * 0.15
        line_color = np.maximum(0.75 - (i + 1) * 0.15, 0)
        ax1.fill_between(indices, breach[:, -2 * i - 1], breach[:, -2 * i - 2],
                         facecolor=str(color), edgecolor=str(line_color))

    ax1.set_xlabel('Index')
    ax1.set_ylabel('Index')

    # Time or height interval plot (subplot 2)
    # -----------------------------------------
    start_grid = np.int_(breach.shape[0] * (1 + figure_properties["space_between"]) * 1000)
    end_grid = np.int_(breach.shape[0] * figure_height_no_label * 1000)
    ax2 = plt.subplot(plot_grid[start_grid : end_grid, :],
                      autoscale_on='false',
                      sharex=ax1)

    # These correction factors were measured, TO FIX!
    pos1 = ax1.get_position()  # get the position of subplot 1
    left = pos1.bounds[0] + 0.056 * pos1.bounds[2]
    bottom = 1 - figure_height_no_label / figure_height
    width = 0.888 * pos1.bounds[2]
    height = figure_properties["height_subpl2"] / figure_height
    pos2 = left, bottom, width, height
    ax2.set(position=pos2, xlim=[0, breach.shape[0] - 1], ylim=[0, 1])

    if result_type == 'time':
        years = hq_data[-1:, 10] - hq_data[0, 10] + 1
        steps = np.array([1, 5, 10, 15, 20, 25, 50, 75, 100])
        step = steps[steps.shape[0] - 1 - np.abs(steps[::-1] - (years / 4) \
                     * np.ones(steps.shape)).argmin()]
        ylabel = 'Year'
        type_column = 10

    if result_type == 'height':
        height_diff = hq_data[-1:, 0] - hq_data[0, 0]
        step = np.int_(height_diff / 4 * 10) / 10
        ylabel = 'Stage [m]'  # ylabel
        type_column = 0  # column in hQ file that provides information about height

    # allocate grayscale to alternating time/height intervals
    classes = np.zeros((hQ.shape[0], 2))
    for i in range(hQ.shape[0]):
        classes[i, 0] = np.floor(hQ[i, col] / step) * step
        if i != 0 and classes[i, 0] != classes[i - 1, 0]:
            j = j + 1
        classes[i, 1] = 0.5 * (j % 2) + 0.25

    for i in range(hQ.shape[0]):
        ax2.fill_between(np.arange(i, i + 2), 0, 1,
                         color=str(classes[i, 1]),
                         edgecolor='none')

    # ticks and labels invisible, ylabel visible
    plt.setp(ax2.get_yticklabels(), visible=False)
    plt.setp(ax2.get_xticklabels(), visible=False)
    ax2.yaxis.set_ticks_position('none')
    ax2.xaxis.set_ticks_position('none')
    ax2.set_ylabel(tekst, rotation=0,
                   horizontalalignment='right',
                   verticalalignment='center')
    pos2 = ax2.get_position()

    # ax3 (subplot 2, separate axis)
    # -----------------------------------------
    labels = np.add(classes[np.concatenate((abs(np.subtract(classes[0:-1, 1],
                                                            classes[1:, 1])),
                                            [0]), axis=0) == 0.5, 0],step))
    x_ticks_2 = np.asarray(np.nonzero(
                np.concatenate((abs(np.subtract(classes[0:-1, 1],
                                                classes[1:, 1])), [0]),
                               axis=0)))
    x_ticks_2 = np.reshape(x_ticks_2, x_ticks_2.shape[1])
    x_ticks_2 += 1
    if x_ticks_2[0] == 0:
        labels[0] = hQ[0, col]
    if x_ticks_2[-1:] == hQ.shape[0]:
        labels[-1:] = hQ[-1:, col]

    # Remove consecutive ticks that are located too close
    test = np.array(np.concatenate(([hQ.shape[0]],
                                    np.diff(x_ticks_2)), axis=0))
    ind = np.array(np.arange(x2.shape[0])[test[:] <= 0.04 * hQ.shape[0]])
    x_ticks_2 = np.delete(x_ticks_2, ind)
    labels = np.delete(labels, ind)

    # Add first and last hQ data point if distance with next interval tick is
    # large enough to guarantee readable labels
    if x_ticks_2[0] > 0.04 * hq_data.shape[0]:
        x_ticks_2 = np.concatenate(([0], x_ticks_2), axis=0)
        labels = (np.concatenate(([hq_data[0, col]], labels), axis=0))

    if hQ.shape[0] - x_ticks_2[-1:] > 0.04 * hq_data.shape[0]:
        x_ticks_2 = np.concatenate((x2, [hq_data.shape[0] - 1]), axis=0)
        labels = (np.concatenate((labels, [hq_data[-1, col]]), axis=0))

    # Create extra axis located on the x axis of subplot 2
    ax3 = fig.add_axes([pos2.bounds[0], pos2.bounds[1],
                        pos2.bounds[2], pos2.bounds[1]],
                       frameon = False)
    ax3.set_xlim([0, breach.shape[0] - 1])
    plt.setp(ax3.get_yticklabels(), visible = False)
    ax3.yaxis.set_ticks_position('none')

    if result_type == 'time':
        ax3.set_xticks(x_ticks_2, np.int_(labels), rotation=-90)
    if result_type == 'height':
        labels = np.int_(labels * 10) / 10  # labels in [m], one decimal number
        ax3.set_xticks(x_ticks_2, labels, rotation=-90)
    ax3.xaxis.set_ticks_position('none')

    if savefig:
        fig_name = 'breach{0}_{1}_{2}.tif'.format(station_name,
                                                  result_type,
                                                  data_type)
        fig.savefig(fig_name)

    return fig, (ax1, ax2, ax3)
