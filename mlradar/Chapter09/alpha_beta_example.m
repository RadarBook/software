%% Alpha Beta example
% Created by: Lee A. Harrison
% On: 4/27/2019

clear, clc

% Set the parameters
t_start = 0.0;
t_end = 10.0;
dt = 0.1;
t = t_start:dt:t_end;
number_of_updates = length(t);

initial_position = 2.3;
initial_velocity = 3.5;

noise_variance = 10.0;
alpha = 0.1;
beta = 0.001;

% True position and velocity
x_true = initial_position + initial_velocity * t;

% Measurements (add noise)
z = x_true + sqrt(noise_variance) * (rand(1, number_of_updates) - 0.5);

% Initialize
xk_1 = 0.0;
vk_1 = 0.0;

x_filt = zeros(number_of_updates, 1);
v_filt = zeros(number_of_updates, 1);
r_filt = zeros(number_of_updates, 1);

% Loop over all measurements
for k = 1:number_of_updates
    % Predict the next state
    xk = xk_1 + vk_1 * dt;
    vk = vk_1;
    
    % Calculate the residual
    rk = z(k) - xk;
    
    % Correct the predicted state
    xk = xk + alpha * rk;
    vk = vk + beta / dt * rk;
    
    % Set the current state as previous
    xk_1 = xk;
    vk_1 = vk;
    
    x_filt(k) = xk;
    v_filt(k) = vk;
    r_filt(k) = rk;
end

% Display the results
figure; hold on;
plot(t, x_true)
plot(t, z)
plot(t, x_filt)
ylabel('Position (m)')
title('Alpha-Beta Filter')
xlabel('Time (s)')
legend({'True', 'Measurement', 'Filtered'})
grid on;
plot_settings;

figure; hold on;
plot(t, initial_velocity * ones(number_of_updates, 1))
plot(t, v_filt)
ylabel('Velocity (m/s)')
title('Alpha-Beta Filter')
xlabel('Time (s)')
legend({'True', 'Filtered'})
grid on;
plot_settings;

figure;
plot(t, r_filt)
ylabel('Residual (m)')

% Set the plot title and labels
title('Alpha-Beta Filter')
xlabel('Time (s)')

% Turn on the grid
grid on
plot_settings;