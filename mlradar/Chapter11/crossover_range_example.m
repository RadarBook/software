%% Crossover range example
% Created by: Lee A. Harrison
% On: 5/28/2019

clear, clc

% Set the parameters

% Jammer type
jammer_type = 'Self Screening';
% jammer_type = 'Escort';

% Transmit power (W)
peak_power = 100e3;

% Antenna gain (dB)
radar_antenna_gain = 20;

% Antenna sidelobe level (dB)
radar_antenna_sidelobe = -20;

% Radar bandwidth (Hz)
radar_bandwidth = 100e6;

% Radar Losses (dB)
radar_losses = 3;

% Target RCS (dBsm)
target_rcs = 3;

% Jammer ERP (dBW)
jammer_erp = linspace(0, 15, 1000);

% Jammer bandwidth (Hz)
jammer_bandwidth = 10e6;

% Jammer range (escort) (m)
jammer_range = 100e3;

% Calculate the crossover range
if strcmp(jammer_type, 'Self Screening')
    cr = crossover_range_selfscreen(peak_power, lin(radar_antenna_gain), lin(target_rcs), ...
        jammer_bandwidth, lin(jammer_erp), radar_bandwidth, lin(radar_losses));
else
    cr = crossover_range_escort(peak_power, lin(radar_antenna_gain), lin(target_rcs), ...
        jammer_range, jammer_bandwidth, lin(jammer_erp), radar_bandwidth, ...
        lin(radar_losses), lin(radar_antenna_sidelobe));
end

% Display the results
plot(jammer_erp, cr)

% Set the plot title and labels
title('Crossover Range')
xlabel('Jammer ERP (dBW)')
ylabel('Crossover Range (m)')

% Turn on the grid
grid

% Plot settings
plot_settings