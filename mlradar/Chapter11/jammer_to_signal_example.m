%% Jammer to signal example
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

% Target range (m)
target_range = linspace(1e3, 50e3, 1000);

% Target RCS (dBsm)
target_rcs = 3;

% Jammer ERP (dBW)
jammer_erp = 15;

% Jammer bandwidth (Hz)
jammer_bandwidth = 10e6;

% Jammer range (escort) (m)
jammer_range = 100e3;

% Set up the input args based on jammer type
if strcmp(jammer_type, 'Self Screening')
    jammer_range = target_range;
    radar_antenna_sidelobe = radar_antenna_gain;
end

% Calculate the jammer to signal ratio
jsr = jammer_to_signal(peak_power, lin(radar_antenna_gain), lin(target_rcs), ...
                    jammer_range, jammer_bandwidth, lin(jammer_erp), target_range, ...
                    radar_bandwidth, lin(radar_losses), lin(radar_antenna_sidelobe));

% Display the results
plot(target_range / 1e3, db(jsr))

% Set the plot title and labels
title('Jammer to Signal Ratio')
xlabel('Target Range (km)')
ylabel('Jammer to Signal Ratio (dB)')

% Turn on the grid
grid

% Plot settings
plot_settings