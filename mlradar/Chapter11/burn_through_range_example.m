%% Burn through range example
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

% J/S required (dB)
jsr = -20;

% Calculate the burn through range
if strcmp(jammer_type, 'Self Screening')    
    br = burn_through_range_selfscreen(peak_power, lin(radar_antenna_gain), lin(target_rcs),...
    radar_bandwidth, lin(radar_losses), lin(jsr), lin(jammer_erp), jammer_bandwidth);
else
    br = burn_through_range_escort(peak_power, lin(radar_antenna_gain), lin(target_rcs),...
        radar_bandwidth, lin(radar_losses), jammer_range, lin(jsr), lin(jammer_erp), ...
        jammer_bandwidth, lin(radar_antenna_sidelobe));
end

% Display the results
plot(jammer_erp, br)

% Set the plot title and labels
title('Burn Through Range')
xlabel('Jammer ERP (dBW)')
ylabel('Burn Through Range (m)')

% Turn on the grid
grid

% Plot settings
plot_settings