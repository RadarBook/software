%% Physical optics example
% Created by: Lee A. Harrison
% On: 1/15/2019

clear, clc

% Set the parameters
facet_file = 'plate.facet';
% facet_file = 'cone.facet';
% facet_file = 'frustum.facet';
% facet_file = 'double_ogive.facet';
frequency = 1e9; % Hz
theta_inc = 15; % degrees
phi_inc = 0; % degrees

% Set the scattering angles
phi_obs = 0; % degrees
theta_obs = linspace(0, 180, 721); % degrees

% Read the facet file
[vertices, faces] = read_facet_model(facet_file);

% Initialize
rcs_theta = zeros(numel(theta_obs), numel(frequency));
rcs_phi = zeros(numel(theta_obs), numel(frequency));

% Monostatic or bistatic
mb = 'Monostatic';
% mb = 'Bistatic';

if strcmp(mb, 'Monostatic')
    
    for i = 1:numel(theta_obs)
        sm = po_scattering(theta_obs(i) * pi / 180, phi_inc * pi / 180, theta_obs(i) * pi / 180, phi_obs * pi / 180, frequency, vertices, faces);      
        rcs_theta(i,:) = 20.0 * log10(abs(sm(1,:)) + 1e-10);
        rcs_phi(i,:) = 20.0 * log10(abs(sm(4,:)) + 1e-10);
    end
    
else
    
    for i = 1:numel(theta_obs)
        sm = po_scattering(theta_inc * pi / 180, phi_inc * pi / 180, theta_obs(i) * pi / 180, phi_obs * pi / 180, frequency, vertices, faces);
        rcs_theta(i,:) = 20.0 * log10(abs(sm(1,:)) + 1e-10);
        rcs_phi(i,:) = 20.0 * log10(abs(sm(4,:)) + 1e-10);
    end
end


% Display the results
figure;
plot(theta_obs, rcs_phi); hold on
plot(theta_obs, rcs_theta, '--')

% Set the plot title and labels
title('Physical Optics RCS vs Observation Angle')
ylabel('RCS (dBsm)')
xlabel('Observation Angle (deg)')
ylim([-40, max(rcs_theta) + 3])

% Set the legend
legend({'TE^{z}', 'TM^{z}'})

% Turn on the grid
grid on

% Plot settings
plot_settings;
