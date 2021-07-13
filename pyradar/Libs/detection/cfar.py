"""
Project: RadarBook
File: cfar.py
Created by: Lee A. Harrison
One: 10/12/2018
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
from numpy import zeros, array, arange, sort, log10

import sys


def cfar(signal, guard_cells, reference_cells, bias, cfar_type):
    """
    Calculate the CFAR threshold for each cell in the signal data.
    :param signal: The signal to be analyzed for detections.
    :param guard_cells: The number of guard cells on each side of the cell under test.
    :param reference_cells: The number of reference cells on each side of the cell under test.
    :param bias: The bias to add to the CFAR threshold (dB).
    :param cfar_type: The type of CFAR threshold to be calculated.
    :return: The CFAR threshold for each cell in the signal.
    """
    # Total number of cells to process
    total_cells = len(signal)

    # The CFAR threshold
    cfar_threshold = zeros(total_cells)

    # Total number of cells in the window
    window_cells = reference_cells + guard_cells

    # The type of CFAR to apply
    if cfar_type == 'Cell Averaging':

        for ix in range(window_cells, total_cells - window_cells):
            lead_start = ix - window_cells
            lead_stop = ix - guard_cells
            lead_avg = sum(signal[lead_start:lead_stop]) / float(reference_cells)

            trail_start = ix + guard_cells
            trail_stop = ix + window_cells
            trail_avg = sum(signal[trail_start:trail_stop]) / float(reference_cells)

            cfar_threshold[ix] = 0.5 * (lead_avg + trail_avg)

    elif cfar_type == 'Cell Averaging Greatest Of':

        for ix in range(window_cells, total_cells - window_cells):
            lead_start = ix - window_cells
            lead_stop = ix - guard_cells
            lead_avg = sum(signal[lead_start:lead_stop]) / float(reference_cells)

            trail_start = ix + guard_cells
            trail_stop = ix + window_cells
            trail_avg = sum(signal[trail_start:trail_stop]) / float(reference_cells)

            cfar_threshold[ix] = max(lead_avg, trail_avg)

    elif cfar_type == 'Cell Averaging Smallest Of':

        for ix in range(window_cells, total_cells - window_cells):
            lead_start = ix - window_cells
            lead_stop = ix - guard_cells
            lead_avg = sum(signal[lead_start:lead_stop]) / float(reference_cells)

            trail_start = ix + guard_cells
            trail_stop = ix + window_cells
            trail_avg = sum(signal[trail_start:trail_stop]) / float(reference_cells)

            cfar_threshold[ix] = min(lead_avg, trail_avg)

    elif cfar_type == 'Ordered Statistic':

        for ix in range(window_cells, total_cells - window_cells):
            lead_start = ix - window_cells
            lead_stop = ix - guard_cells

            trail_start = ix + guard_cells
            trail_stop = ix + window_cells

            x1 = array(signal[lead_start:lead_stop])
            x2 = array(signal[trail_start:trail_stop])

            z = zeros(2 * reference_cells)
            for i in arange(reference_cells):
                z[i] = x1[i]
                z[i + reference_cells] = x2[i]

            z = sort(z)

            cfar_threshold[ix] = z[int(1.5 * reference_cells)]

    return 10.0 * log10(cfar_threshold + sys.float_info.min) + bias
