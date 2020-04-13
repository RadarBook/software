function [data] = read_fdtd_geometry(data)
%% Read an FDTD cell file

% Created by: Lee A. Harrison
% Cretaed on: 1/17/2019
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

% Open the file
fid = fopen(data.geometry_file, 'r');

% Read the comment
fgetl(fid);

% Read nx, ny
line = strtrim(fgetl(fid));
line_list = strsplit(line, ' ');
data.nx = str2num(line_list{1});
data.ny = str2num(line_list{2});

% Read the comment
fgetl(fid);

% Read dx, dy
line = strtrim(fgetl(fid));
line_list = strsplit(line, ' ');
data.dx = str2num(line_list{1});
data.dy = str2num(line_list{2});

% Set up the PML areas first
data.nx = data.nx + 2 * data.number_of_pml;
data.ny = data.ny + 2 * data.number_of_pml;

data.mu_r = zeros(data.nx, data.ny);
data.eps_r = zeros(data.nx, data.ny);
data.sigma = zeros(data.nx, data.ny);

% Set up the maximum conductivities
sigma_max_x = -3.0 * data.epsilon_0 * data.c * log(1e-5) / (2.0 * data.dx * data.number_of_pml);
sigma_max_y = -3.0 * data.epsilon_0 * data.c * log(1e-5) / (2.0 * data.dy * data.number_of_pml);

% Create the conductivity profile
m = 1:data.number_of_pml;
sigma_v = ((m - 0.5) ./ (data.number_of_pml + 0.5)) .^ 2;

% Back region
for i = 1:data.nx
    for j = 1:data.number_of_pml
        data.mu_r(i, j) = 1.0;
        data.eps_r(i, j) = 1.0;
        data.sigma(i, j) = sigma_max_y * sigma_v(data.number_of_pml + 1 - j);
    end
end

% Front region
for i = 1:data.nx
    for j = (data.ny - data.number_of_pml):(data.ny - 1)
        data.mu_r(i, j) = 1.0;
        data.eps_r(i, j) = 1.0;
        data.sigma(i, j) = sigma_max_y * sigma_v(j - (data.ny - data.number_of_pml) + 1);
    end
end

% Left region
for i = 1:data.number_of_pml
    for j = 1:data.ny
        data.mu_r(i, j) = 1.0;
        data.eps_r(i, j) = 1.0;
        data.sigma(i, j) = data.sigma(i, j) + sigma_max_x * sigma_v(data.number_of_pml + 1 - i);
    end
end

% Right region
for i = (data.nx - data.number_of_pml):(data.nx - 1)
    for j = 1:data.ny
        data.mu_r(i, j) = 1.0;
        data.eps_r(i, j) = 1.0;
        data.sigma(i, j) = data.sigma(i, j) + sigma_max_x * sigma_v(i - (data.nx - data.number_of_pml) + 1);
    end
end

% Read the geometry
for i = data.number_of_pml:(data.nx - data.number_of_pml - 1)
    for j = data.number_of_pml:(data.ny - data.number_of_pml - 1)
        
        line = strtrim(fgetl(fid));
        line_list = strsplit(line, ' ');
        
        % Relative permeability first
        data.mu_r(i, j) = str2num(line_list{1});
        
        % Relative permittivity next
        data.eps_r(i, j) = str2num(line_list{2});
        
        % Finally the conductivity
        data.sigma(i, j) = str2num(line_list{3});
    end
end
fclose(fid);