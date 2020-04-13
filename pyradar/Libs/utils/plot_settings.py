"""
Project: RadarBook
File: plot_settings.py
Created by: Lee A. Harrison
On: 3/18/2018
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""


def settings(plt):
    """
    Set default sizes for plotting, so that all plots are consistent.
    :param plt: The pyplot module.
    :return:
    """
    # Get current size
    fig_size = plt.rcParams["figure.figsize"]

    # Set figure width of 12 and height of 9
    fig_size[0] = 12
    fig_size[1] = 9
    plt.rcParams["figure.figsize"] = fig_size

    # Define the sizes for each item
    title_size = 16
    axis_size = 14
    legend_size = 12

    # Use the tight layout
    plt.tight_layout()

    # Choose the size for each item
    plt.rc('axes', titlesize=title_size)
    plt.rc('axes', labelsize=axis_size)
    plt.rc('xtick', labelsize=axis_size)
    plt.rc('ytick', labelsize=axis_size)
    plt.rc('legend', fontsize=legend_size)

    # Turn on the grid
    plt.grid(linestyle=':', linewidth=0.5)


def default_save(plt, fname):
    """
    A default save utility for figures.
    :param plt: The pyplot module
    :param fname: The filename to use
    :return:
    """
    plt.savefig(fname, dpi=1200, facecolor='w', edgecolor='w', orientation='portrait', papertype='letter',
                format='eps', transparent=False, bbox_inches=None, pad_inches=0.1, frameon=None)
