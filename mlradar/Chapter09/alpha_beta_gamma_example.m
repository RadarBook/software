%% Alpha Beta Gamma example
% Created by: Lee A. Harrison
% On: 4/27/2019
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

clear, clc

% Set the parameters
t_start = 0.0;
t_end = 100.0;
dt = 0.1;
t = t_start:dt:t_end;
number_of_updates = length(t);

initial_position = 1.3;
initial_velocity = 3.5;
initial_acceleration = 3.0;

noise_variance = 10.0;
alpha = 0.06;
beta = 0.0018;
gamma = 2.75e-5;

% True position and velocity
v_true = initial_velocity + initial_acceleration * t;
x_true = initial_position + initial_velocity * t + 0.5 * initial_acceleration * t .^ 2;

% Measurements (add noise)
z = x_true + sqrt(noise_variance) * (rand(1, number_of_updates) - 0.5);

% Initialize
xk_1 = 0.0;
vk_1 = 0.0;
ak_1 = 0.0;

x_filt = zeros(number_of_updates, 1);
v_filt = zeros(number_of_updates, 1);
a_filt = zeros(number_of_updates, 1);
r_filt = zeros(number_of_updates, 1);

% Loop over all measurements
for k = 1:number_of_updates
    % Predict the next state
    xk = xk_1 + vk_1 * dt + 0.5 * ak_1 * dt ^ 2;
    vk = vk_1 + ak_1 * dt;
    ak = ak_1;
    
    % Calculate the residual
    rk = z(k) - xk;
    
    % Correct the predicted state
    xk = xk + alpha * rk;
    vk = vk + beta / dt * rk;
    ak = ak + 2.0 * gamma / dt ^ 2 * rk;
    
    % Set the current state as previous
    xk_1 = xk;
    vk_1 = vk;
    ak_1 = ak;
    
    x_filt(k) = xk;
    v_filt(k) = vk;
    a_filt(k) = ak;
    r_filt(k) = rk;
end

% Display the results
figure; hold on;
plot(t, x_true)
plot(t, z)
plot(t, x_filt)
ylabel('Position (m)')
title('Alpha-Beta-Gamma Filter')
xlabel('Time (s)')
legend({'True', 'Measurement', 'Filtered'})
grid on;
plot_settings;

figure; hold on;
plot(t, v_true)
plot(t, v_filt)
ylabel('Velocity (m/s)')
title('Alpha-Beta-Gamma Filter')
xlabel('Time (s)')
legend({'True', 'Filtered'})
grid on;
plot_settings;

figure; hold on;
plot(t, initial_acceleration * ones(number_of_updates, 1))
plot(t, a_filt)
ylabel('Acceleration (m/s/s)')
title('Alpha-Beta-Gamma Filter')
xlabel('Time (s)')
legend({'True', 'Filtered'})
grid on;
plot_settings;

figure;
plot(t, r_filt)
ylabel('Residual (m)')

% Set the plot title and labels
title('Alpha-Beta-Gamma Filter')
xlabel('Time (s)')

% Turn on the grid
grid on
plot_settings;