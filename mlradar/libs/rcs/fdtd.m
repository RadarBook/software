function fdtd(data)
%% 2D Finite Difference Time Domain
% mode: 'TE' or 'TM'
% incident_angle: The angle of the incident field (degrees).
% number_of_time_steps: The number of time steps.
% geometry_file: The geometry file to use.
% gaussian_pulse_width: The width of the Gaussian pulse in time steps.
% gaussian_pulse_amplitude: The amplitude of the Gaussian pulse.
% number_of_pml: The number of PML layers.

%     Created by: Lee A. Harrison
%     On: 1/18/2019

% Speed of light
data.c = 299792458;

% Permeability of free space
data.mu_0 = 4.0 * pi * 1e-7;

% Permittivity of free space
data.epsilon_0 = 1.0 / (data.mu_0 * data.c^2);

% Read the geometry file
[data] = read_fdtd_geometry(data);

% Initialize
data.esctc = zeros(data.nx, data.ny);
data.eincc = zeros(data.nx, data.ny);
data.edevcn = zeros(data.nx, data.ny);
data.ecrlx = zeros(data.nx, data.ny);
data.ecrly = zeros(data.nx, data.ny);
data.dtmdx = zeros(data.nx, data.ny);
data.dtmdy = zeros(data.nx, data.ny);
data.hdhvcn = zeros(data.nx, data.ny);

% Calculate the maximum time step allowed by the Courant stability condition
data.dt = 1.0 / (data.c * (sqrt(1.0 / (data.dx ^ 2) + 1.0 / (data.dy ^ 2))));

for i = 1:data.nx
    for j = 1:data.ny
        eps = data.epsilon_0 * data.eps_r(i, j);
        mu = data.mu_0 * data.mu_r(i, j);
        data.esctc(i, j) = eps / (eps + data.sigma(i, j) * data.dt);
        data.eincc(i, j) = data.sigma(i, j) * data.dt / (eps + data.sigma(i, j) * data.dt);
        data.edevcn(i, j) = data.dt * (eps - data.epsilon_0) / (eps + data.sigma(i, j) * data.dt);
        data.ecrlx(i, j) = data.dt / ((eps + data.sigma(i, j) * data.dt) * data.dx);
        data.ecrly(i, j) = data.dt / ((eps + data.sigma(i, j) * data.dt) * data.dy);
        data.dtmdx(i, j) = data.dt / (mu * data.dx);
        data.dtmdy(i, j) = data.dt / (mu * data.dy);
        data.hdhvcn(i, j) = data.dt * (mu - data.mu_0) / mu;
    end
end

% Amplitude of incident field components
data.amplitude_x = -data.gaussian_pulse_amplitude * sin(deg2rad(data.incident_angle));
data.amplitude_y = data.gaussian_pulse_amplitude * cos(deg2rad(data.incident_angle));

% Change on mode
switch data.mode
    case 'TE'
        
        % Setup the figure
        figure; hold on;
        title('FDTD - TE')
        xlabel('X (m)');
        ylabel('Y (m)');
        caxis([0, data.gaussian_pulse_amplitude])
        colorbar
        plot_settings;
        
        % Grid for plotting
        x = linspace(0, data.nx * data.dx, data.nx);
        y = linspace(0, data.ny * data.dy, data.ny);
        
        % Initialize the fields
        data.exi = zeros(data.nx, data.ny);
        data.eyi = zeros(data.nx, data.ny);
        data.dexi = zeros(data.nx, data.ny);
        data.deyi = zeros(data.nx, data.ny);
        data.exs = zeros(data.nx, data.ny);
        data.eys = zeros(data.nx, data.ny);
        data.hzs = zeros(data.nx, data.ny);
        data.dhzi = zeros(data.nx, data.ny);
        
        % Start at time = 0
        data.t = 0.0;
        
        % Loop over the time steps
        for n = 1:data.number_of_time_steps
            
            % Update the scattered electric field
            [data] = escattered_te(data);
            
            % Advance the time by 1/2 time step
            data.t = data.t + 0.5 * data.dt;
            
            % Update the scattered magnetic field
            [data] = hscattered_te(data);
            
            % Advance the time by 1/2 time step
            data.t = data.t + 0.5 * data.dt;
            
            % Update the figure
            extotal = data.exi + data.exs;
            eytotal = data.eyi + data.eys;
            etotal = sqrt(extotal .^ 2 + eytotal .^ 2);
            
            % Plot the fields
            pcolor(x, y, abs(etotal));
            shading interp;
            drawnow
            
            % Progress
            if rem(n, 10) == 0
                fprintf('%d of %d time steps\n', n, data.number_of_time_steps);
            end
        end
        
    case 'TM'
        
        % Setup the figure
        figure; hold on;
        title('FDTD - TM')
        xlabel('X (m)');
        ylabel('Y (m)');
        caxis([0, data.gaussian_pulse_amplitude])
        colorbar
        plot_settings;
        
        % Grid for plotting
        x = linspace(0, data.nx * data.dx, data.nx);
        y = linspace(0, data.ny * data.dy, data.ny);
        
        % Initialize the fields
        data.hxs = zeros(data.nx, data.ny);
        data.hys = zeros(data.nx, data.ny);
        data.dhxi = zeros(data.nx, data.ny);
        data.dhyi = zeros(data.nx, data.ny);
        data.ezs = zeros(data.nx, data.ny);
        data.ezi = zeros(data.nx, data.ny);
        data.dezi = zeros(data.nx, data.ny);
        
        % Start at time = 0
        data.t = 0.0;
        
        % Loop over the time steps
        for n = 1:data.number_of_time_steps
            
            % Update the scattered electric field
            [data] = escattered_tm(data);
            
            % Advance the time by 1/2 time step
            data.t = data.t + 0.5 * data.dt;
            
            % Update the scattered magnetic field
            [data] = hscattered_tm(data);
            
            % Advance the time by 1/2 time step
            data.t = data.t + 0.5 * data.dt;
            
            % Update the figure
            etotal = data.ezi + data.ezs;
            
            % Plot the fields
            pcolor(x, y, abs(etotal));
            shading interp;
            drawnow
            
            % Progress
            if rem(n, 10) == 0
                fprintf('%d of %d time steps\n', n, data.number_of_time_steps);
            end
        end
end

end

%% TE E_inc
function [data] = eincident_te(data)

% Calculate the incident electric field and derivative
delay = 0;

% Calculate the decay rate determined by Gaussian pulse width
alpha = (1.0 / (data.dt * data.gaussian_pulse_width / 4.0)) ^ 2;

% Calculate the period
period = 2.0 * data.dt * data.gaussian_pulse_width;

% Spatial delay of each cell
x_disp = -cos(deg2rad(data.incident_angle));
y_disp = -sin(deg2rad(data.incident_angle));

if x_disp < 0
    delay = delay - x_disp * (data.nx - 2.0) * data.dx;
end

if y_disp < 0
    delay = delay - y_disp * (data.ny - 2.0) * data.dy;
end

for i = (data.number_of_pml):(data.nx - data.number_of_pml)
    for j = (data.number_of_pml):(data.ny - data.number_of_pml)
        
        distance = i * data.dx * x_disp + j * data.dy * y_disp + delay;        
        tau = data.t - distance / data.c;
        
        a = 0;  a_prime = 0;
        
        if 0 <= tau && tau <= period
            a = exp(-alpha * (tau - data.gaussian_pulse_width * data.dt) ^ 2);
            a_prime = exp(-alpha * (tau - data.gaussian_pulse_width * data.dt) ^ 2) *...
                (-2.0 * alpha * (tau -data. gaussian_pulse_width * data.dt));
        end
        
        data.exi(i, j) = data.amplitude_x * a;
        data.dexi(i, j) = data.amplitude_x * a_prime;
        
        data.eyi(i, j) = data.amplitude_y * a;
        data.deyi(i, j) = data.amplitude_y * a_prime;
    end
end
end

%% TE E_sct
function [data] =  escattered_te(data)

% Calculate the incident electric field
[data] = eincident_te(data);

% Update the x-component electric scattered field
for i = 1:(data.nx - 1)
    for j = 2:(data.ny - 1)
        data.exs(i, j) = data. exs(i, j) * data.esctc(i, j) - data.eincc(i, j) * data.exi(i, j) - ...
            data.edevcn(i, j) * data.dexi(i, j) + (data.hzs(i, j) - data.hzs(i, j - 1)) * data.ecrly(i, j);
    end
end

% Update the y-component electric scattered field
for i = 2:(data.nx - 1)
    for j = 1:(data.ny - 1)
        data.eys(i, j) = data.eys(i, j) * data.esctc(i, j) - data.eincc(i, j) * data.eyi(i, j) - ...
            data.edevcn(i, j) * data.deyi(i, j) - (data.hzs(i, j) - data.hzs(i - 1, j)) * data.ecrlx(i, j);
    end
end
end


%% TE H_inc
function [data] = hincident_te(data)

% Calculate the incident magnetic field and time derivative
delay = 0.0;
eta = sqrt(data.mu_0 / data.epsilon_0);

% Calculate the decay rate determined by Gaussian pulse width
alpha = (1.0 / (data.gaussian_pulse_width * data.dt / 4.0)) ^ 2;

% Calculate the period
period = 2.0 * data.gaussian_pulse_width * data.dt;

% Spatial delay of each cell
x_disp = -cos(deg2rad(data.incident_angle));
y_disp = -sin(deg2rad(data.incident_angle));

if x_disp < 0
    delay = delay - x_disp * (data.nx - 2.0) * data.dx;
end

if y_disp < 0
    delay = delay - y_disp * (data.ny - 2.0) * data.dy;
end

for i =  (data.number_of_pml):(data.nx - data.number_of_pml)
    for j = (data.number_of_pml):(data.ny - data.number_of_pml)
        
        distance = i * data.dx * x_disp + j * data.dy * y_disp + delay;        
        tau = data.t - distance / data.c;
        
        a_prime = 0;
        
        if 0 <= tau && tau <= period
            a_prime = exp(-alpha * (tau - data.gaussian_pulse_width * data.dt) ^ 2) ...
                * (-2.0 * alpha * (tau - data.gaussian_pulse_width * data.dt));
        end
        
        data.dhzi(i, j) = data.gaussian_pulse_amplitude * a_prime / eta;
        
    end
end
end


%% TE H_sct
function [data] = hscattered_te(data)

% Calculate the incident magnetic field
[data] = hincident_te(data);

% Update the scattered magnetic field
for i = 1:(data.nx - 1)
    for j = 1:(data.ny - 1)
        data.hzs(i, j) = data.hzs(i, j) - (data.eys(i + 1, j) - data.eys(i, j)) * data.dtmdx(i, j) ...
            + (data.exs(i, j + 1) - data.exs(i, j)) * data.dtmdy(i, j) - data.hdhvcn(i, j) * data.dhzi(i, j);
    end
end
end

%% TM E_inc
function [data] = eincident_tm(data)


% Calculate the incident electric field and derivative
delay = 0;

% Calculate the decay rate determined by Gaussian pulse width
alpha = (1.0 / (data.dt * data.gaussian_pulse_width / 4.0)) ^ 2;

% Calculate the period
period = 2.0 * data.dt * data.gaussian_pulse_width;

% Spatial delay of each cell
x_disp = -cos(deg2rad(data.incident_angle));
y_disp = -sin(deg2rad(data.incident_angle));

if x_disp < 0
    delay = delay - x_disp * (data.nx - 2.0) * data.dx;
end

if y_disp < 0
    delay = delay - y_disp * (data.ny - 2.0) * data.dy;
end

for i = (data.number_of_pml):(data.nx - data.number_of_pml)
    for j = (data.number_of_pml):(data.ny - data.number_of_pml)
        
        distance = i * data.dx * x_disp + j * data.dy * y_disp + delay;
        
        tau = data.t - distance / data.c;
        
        a = 0;  a_prime = 0;
        
        if 0 <= tau && tau <= period
            a = exp(-alpha * (tau - data.gaussian_pulse_width * data.dt) ^ 2);
            a_prime = exp(-alpha * (tau - data.gaussian_pulse_width * data.dt) ^ 2) ...
                * (-2.0 * alpha * (tau - data.gaussian_pulse_width * data.dt));

        end
        
        data.ezi(i, j) = data.gaussian_pulse_amplitude * a;
        data.dezi(i, j) = data.gaussian_pulse_amplitude * a_prime;
        
    end
end
end

%% TM E_sct
function [data] = escattered_tm(data)

% Calculate the incident electric field
[data] = eincident_tm(data);

% Update the z-component electric scattered field
for i = 2:(data.nx - 1)
    for j = 2:(data.ny - 1)
        data.ezs(i, j) = data.ezs(i, j) * data.esctc(i, j) - data.eincc(i, j) * data.ezi(i, j) ...
            - data.edevcn(i, j) * data.dezi(i, j) + (data.hys(i, j) - data.hys(i - 1, j)) ...
            * data.ecrlx(i, j) - (data.hxs(i, j) - data.hxs(i, j - 1)) * data.ecrly(i, j);
    end
end
end


%% TM H_inc
function [data] = hincident_tm(data)

% Calculate the incident magnetic field and derivative
delay = 0;
eta = sqrt(data.mu_0 / data.epsilon_0);

% Calculate the decay rate determined by Gaussian pulse width
alpha = (1.0 / (data.dt * data.gaussian_pulse_width / 4.0)) ^ 2;

% Calculate the period
period = 2.0 * data.dt * data.gaussian_pulse_width;

% Spatial delay of each cell
x_disp = -cos(deg2rad(data.incident_angle));
y_disp = -sin(deg2rad(data.incident_angle));

if x_disp < 0
    delay = delay - x_disp * (data.nx - 2.0) * data.dx;
end

if y_disp < 0
    delay = delay - y_disp * (data.ny - 2.0) * data.dy;
end

for i = (data.number_of_pml):(data.nx - data.number_of_pml)
    for j = (data.number_of_pml):(data.ny - data.number_of_pml)
        
        distance = i * data.dx * x_disp + j * data.dy * y_disp + delay;
        
        tau = data.t - distance / data.c;
        
        a = 0;  a_prime = 0;
        
        if 0 <= tau && tau <= period
            a = exp(-alpha * (tau - data.gaussian_pulse_width * data.dt) ^ 2);
            a_prime = exp(-alpha * (tau - data.gaussian_pulse_width * data.dt) ^ 2) ...
                * (-2.0 * alpha * (tau - data.gaussian_pulse_width * data.dt));
        end
        data.dhxi(i, j) = data.gaussian_pulse_amplitude * a_prime / eta;
        data.dhyi(i, j) = data.gaussian_pulse_amplitude * a_prime / eta;
    end
end
end

%% TM H_sct

function [data] = hscattered_tm(data)


% Calculate the incident magnetic field
[data] = hincident_tm(data);

% Update the X component of the magnetic scattered field
for i = 1:(data.nx - 1)
    for j = 1:(data.ny - 1)
        data.hxs(i, j) = data.hxs(i, j) - (data.ezs(i, j + 1) - data.ezs(i, j)) * data.dtmdx(i, j);
    end
end

for i = 1:(data.nx - 1)
    for j = 1:(data.ny - 1)
        data.hys(i, j) = data.hys(i, j) + (data.ezs(i + 1, j) - data.ezs(i, j)) * data.dtmdx(i, j);
    end
end
end