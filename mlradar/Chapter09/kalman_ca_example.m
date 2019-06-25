%% Kalman constant acceleration example
% Created by: Lee A. Harrison
% On: 4/29/2019

clear, clc

% Set the parameters
t_start = 0.0; % seconds
t_end = 100.0; % seconds
dt = 0.1; % seconds
t = t_start:dt:t_end; % seconds
number_of_updates = length(t);

% Initial position (m)
p_xyz = [1e3, 1.1e3, 3.2e3];

% Initial velocity (m/s)
v_xyz = [10, 20, 15];

% Initial acceleration (m/s/s)
a_xyz = [0.5, 1.0, 0.75];

% Measurement and process noise variance
measurement_noise_variance = 10.0;
process_noise_variance = 1e-6;

% Create target trajectory
x_true = zeros(9, number_of_updates);

x = p_xyz(1) + v_xyz(1) * t + 0.5 * a_xyz(1) * t .^ 2;
y = p_xyz(2) + v_xyz(2) * t + 0.5 * a_xyz(2) * t .^ 2;
z = p_xyz(3) + v_xyz(3) * t + 0.5 * a_xyz(3) * t .^ 2;

x_true(1, :) = x;
x_true(2, :) = v_xyz(1) + a_xyz(1) * t;
x_true(3, :) = a_xyz(1);

x_true(4, :) = y;
x_true(5, :) = v_xyz(2) + a_xyz(2) * t;
x_true(6, :) = a_xyz(2);

x_true(7, :) = z;
x_true(8, :) = v_xyz(3) + a_xyz(3) * t;
x_true(9, :) = a_xyz(3);

% Measurement noise
v = sqrt(measurement_noise_variance) * (rand(number_of_updates) - 0.5);

% Initialize state and input control vector
x = zeros(9, 1);
u = zeros(9, 1);

% Initialize the covariance and control matrix
P = 1.0e3 * eye(9);
B = zeros(9, 9);

% Initialize measurement and process noise variance
R = measurement_noise_variance * eye(3);
Q = process_noise_variance * eye(9);

% State transition and measurement transition
A = eye(9);
A(1, 2) = dt;
A(1, 3) = 0.5 * dt * dt;
A(2, 3) = dt;

A(4, 5) = dt;
A(4, 6) = 0.5 * dt * dt;
A(5, 6) = dt;

A(7, 8) = dt;
A(7, 9) = 0.5 * dt * dt;
A(8, 9) = dt;

% Measurement transition matrix
H = zeros(3, 9);
H(1, 1) = 1;
H(2, 4) = 1;
H(3, 7) = 1;

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
plot(t, x_true(4, :))
plot(t, z(2, :))
plot(t, kf.state(4, :))
ylabel('Postion - Y (m)');
legend({'True', 'Measurement', 'Filtered'})
grid on;

subplot(313); hold on;
plot(t, x_true(7, :))
plot(t, z(3, :))
plot(t, kf.state(7, :))
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
plot(t, x_true(5, :))
plot(t, kf.state(5, :))
ylabel('Velocity - Y (m)');
legend({'True', 'Filtered'})
grid on;

subplot(313); hold on;
plot(t, x_true(8, :))
plot(t, kf.state(8, :))
xlabel('Time (s)')
ylabel('Velocity - Z (m)');
legend({'True', 'Filtered'})
grid on;

plot_settings;

figure; subplot(311); hold on
plot(t, x_true(3, :))
plot(t, kf.state(3, :))
ylabel('Acceleration - X (m)');
title('Kalman Filter');
legend({'True', 'Filtered'})
grid on;

subplot(312); hold on
plot(t, x_true(6, :))
plot(t, kf.state(6, :))
ylabel('Acceleration - Y (m)');
legend({'True', 'Filtered'})
grid on;

subplot(313); hold on;
plot(t, x_true(9, :))
plot(t, kf.state(9, :))
xlabel('Time (s)')
ylabel('Acceleration - Z (m)');
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
            
            
            