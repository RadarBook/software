function [ cfar_threshold ] = cfar(signal, guard_cells, reference_cells, bias, cfar_type)
% Calculate the CFAR threshold for each cell in the signal data.
%     :param signal: The signal to be analyzed for detections.
%     :param guard_cells: The number of guard cells on each side of the cell under test.
%     :param reference_cells: The number of reference cells on each side of the cell under test.
%     :param bias: The bias to add to the CFAR threshold (dB).
%     :param cfar_type: The type of CFAR threshold to be calculated.
%     :return: The CFAR threshold for each cell in the signal.
%
%     Created by: Lee A. Harrison
%     On: 10/11/2018
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

% Total number of cells
total_cells = length(signal);

% Initialize threshold
cfar_threshold = zeros(1, total_cells);

% Number of window cells
window_cells = reference_cells + guard_cells;

if strcmp(cfar_type, 'Cell Averaging')
    
    for ix = (window_cells+1):(total_cells - window_cells)
        lead_start = ix - window_cells;
        lead_stop = ix - guard_cells;
        lead_avg = sum(signal(lead_start:lead_stop)) / reference_cells;
        
        trail_start = ix + guard_cells;
        trail_stop = ix + window_cells;
        trail_avg = sum(signal(trail_start:trail_stop)) / reference_cells;
        
        cfar_threshold(ix) = 0.5 * (lead_avg + trail_avg);
    end
    
elseif strcmp(cfar_type, 'Cell Averaging Greatest Of')
    
    for ix = (window_cells+1):(total_cells - window_cells)
        lead_start = ix - window_cells;
        lead_stop = ix - guard_cells;
        lead_avg = sum(signal(lead_start:lead_stop)) / reference_cells;
        
        trail_start = ix + guard_cells;
        trail_stop = ix + window_cells;
        trail_avg = sum(signal(trail_start:trail_stop)) / reference_cells;
        
        cfar_threshold(ix) = max(lead_avg, trail_avg);
    end
    
elseif strcmp(cfar_type, 'Cell Averaging Smallest Of')
    
    for ix = (window_cells+1):(total_cells - window_cells)
        lead_start = ix - window_cells;
        lead_stop = ix - guard_cells;
        lead_avg = sum(signal(lead_start:lead_stop)) / reference_cells;
        
        trail_start = ix + guard_cells;
        trail_stop = ix + window_cells;
        trail_avg = sum(signal(trail_start:trail_stop)) / reference_cells;
        
        cfar_threshold(ix) = min(lead_avg, trail_avg);
    end
    
elseif strcmp(cfar_type, 'Ordered Statistic')
    
    for ix = (window_cells+1):(total_cells - window_cells)
        lead_start = ix - window_cells;
        lead_stop = ix - guard_cells;
        
        trail_start = ix + guard_cells;
        trail_stop = ix + window_cells;
        
        x1 = signal(lead_start:lead_stop);
        x2 = signal(trail_start:trail_stop);
        
        z = zeros(2 * reference_cells);
        for i = 1:reference_cells
            z(i) = x1(i);
            z(i + reference_cells) = x2(i);
        end
        z = sort(z);
        cfar_threshold(ix) = z(round(1.5 * reference_cells));
        
    end
end

cfar_threshold = 10.0 * log10(cfar_threshold) + bias;


end

