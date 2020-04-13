%% Kalman constant velocity example
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

% Initial position
p_xyz = [1e3, 1.1e3, 3.2e3];

% Initial velocity
v_xyz = [100, 20, 15];

% Measurement and process noise variance
measurement_noise_variance = 10.0;
process_noise_variance = 1e-6;

% Create target trajectory
x_true = zeros(6, number_of_updates);

x = p_xyz(1) + v_xyz(1) * t;
y = p_xyz(2) + v_xyz(2) * t;
z = p_xyz(3) + v_xyz(3) * t;

x_true(1, :) = x;
x_true(2, :) = v_xyz(1);
x_true(3, :) = y;
x_true(4, :) = v_xyz(2);
x_true(5, :) = z;
x_true(6, :) = v_xyz(3);

% Measurement noise
v = sqrt(measurement_noise_variance) * (rand(number_of_updates) - 0.5);

% Initialize state and input control vector
x = zeros(6, 1);
u = zeros(6, 1);

% Initialize the covariance and control matrix
P = 1.0e3 * eye(6);
B = zeros(6, 6);

% Initialize measurement and process noise variance
R = measurement_noise_variance * eye(3);
Q = process_noise_variance * eye(6);

% State transition and measurement transition
A = eye(6);
A(1, 2) = dt;
A(3, 4) = dt;
A(5, 6) = dt;

% Measurement transition matrix
H = zeros(3, 6);
H(1, 1) = 1;
H(2, 3) = 1;
H(3, 5) = 1;

% Generate the measurements
z = zeros(3, number_of_updates);
for i = 1:number_of_updates
    z(:, i) = H * x_true(:, i) + v(i);
end

% An instance of kalman
kf = kalman(x, u, P, A, B, Q, H, R);

% Update the filter for each measurement
kf = kf.filter(z);

% Display the results
figure; subplot(311); hold on
plot(t, x_true(1, :))
plot(t, z(1, :))
plot(t, kf.state(1, :))
ylabel('Postion - X (m)');
title('Kalman Filter');
legend({'True', 'Measurement', 'Filtered'})
grid on;

subplot(312); hold on
plot(t, x_true(3, :))
plot(t, z(2, :))
plot(t, kf.state(3, :))
ylabel('Postion - Y (m)');
legend({'True', 'Measurement', 'Filtered'})
grid on;

subplot(313); hold on;
plot(t, x_true(5, :))
plot(t, z(3, :))
plot(t, kf.state(5, :))
xlabel('Time (s)')
ylabel('Postion - Z (m)');
legend({'True', 'Measurement', 'Filtered'})
grid on;

plot_settings;


figure; subplot(311); hold on
plot(t, x_true(2, :))
plot(t, kf.state(2, :))
ylabel('Velocity - X (m)');
title('Kalman Filter');
legend({'True', 'Filtered'})
grid on;

subplot(312); hold on
plot(t, x_true(4, :))
plot(t, kf.state(4, :))
ylabel('Velocity - Y (m)');
legend({'True', 'Filtered'})
grid on;

subplot(313); hold on;
plot(t, x_true(6, :))
plot(t, kf.state(6, :))
xlabel('Time (s)')
ylabel('Velocity - Z (m)');
legend({'True', 'Filtered'})
grid on;

plot_settings;

figure;
plot(t, kf.residual)
title('Kalman Filter')
xlabel('Time (s)')
ylabel('Residual (m)');
grid on;

plot_settings;
            
            
            