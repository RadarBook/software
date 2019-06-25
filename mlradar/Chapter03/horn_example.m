%% Horn antenna example
% Created by: Lee A. Harrison
% On: 8/3/2018

clear, clc

% The operating frequency (Hz)
frequency = 300e6;

% The width and width of the waveguide feed (m)
guide_width = 0.5;
guide_height = 0.25;

% The height and width of the horn (m)
horn_height = 2.75;
horn_width = 5.5;

% The effective length of the horn
eplane_effective_length = 6.0;
hplane_effective_length = 6.0;

% The theta and phi grid
n = 400;
m = n/4;
[theta, phi] = meshgrid(linspace(0, 0.5*pi, n), linspace(0, 2*pi, n));

% Create an instance of the horn
horn = eplane_sectoral_horn(guide_width, horn_height, eplane_effective_length, frequency, 0, 0, 1e9, theta, phi);
% horn = hplane_sectoral_horn(horn_width, guide_height, hplane_effective_length, frequency, 0, 0, 1e9, theta, phi);
% horn = pyramidal_horn(horn_width, horn_height, eplane_effective_length, hplane_effective_length, frequency, 0, 0, 1e9, theta, phi);

% Get the far fields
[e_r, e_theta, e_phi, h_r, h_theta, h_phi] = horn.far_fields;

% Get the directivity
d = horn.directivity;
fprintf('Directivity = %.2f\n', d);

% Get the power radiated
prad = horn.power_radiated;
fprintf('Power Radiated = %.2e (W)\n', prad);

% Calculate the normalized magnitude of the electric field
e_mag = sqrt(abs(e_theta .* e_theta + e_phi .* e_phi));
e_mag = e_mag ./ max(max(e_mag));

% U-V coordinates for plotting the antenna pattern
uu = sin(theta) .* cos(phi);
vv = sin(theta) .* sin(phi);

% Plot the results
figure;
pcolor(uu, vv, abs(e_mag)); shading flat
xlabel('U (sines)');
ylabel('V (sines)');
title('Horn Antenna Pattern');
axis equal
plot_settings;

figure;
plot(theta(1,:)*180/pi, 2*db(e_mag(m,:))); hold on;
plot(theta(1,:)*180/pi, 2*db(e_mag(1,:))); 
ylim([-60 5]);
title('Horn Antenna Pattern');
xlabel('Theta (deg)');
ylabel('Normalized |E| (dB)');
legend('E-plane', 'H-plane');
grid on; plot_settings;

