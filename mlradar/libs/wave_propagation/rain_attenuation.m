function attenuation = rain_attenuation(frequency, rain_rate, elevation_angle, polarization_tilt_angle)
%% Calculate the attenuation due to rain.
% :param frequency: The operating frequency (GHz).
% :param rain_rate: The rain rate (mm/hr).
% :param elevation_angle: The elevation angle (radians).
% :param polarization_tilt_angle: The polarization tilt angle (radians).
% :return: The specific attenuation due to rain (dB/km).
%
% Created by: Lee A. Harrison
% On: 6/18/2018
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

% Table 2.3 Coefficients for calculating k_h
a_kh = [-5.33980, -0.35351, -0.23789, -0.94158];
b_kh = [-0.1008, 1.26970, 0.86036, 0.64552];
c_kh = [1.13098, 0.45400, 0.15354, 0.16817];
d_kh = -0.18961;
e_kh = 0.71147;

% Table 2.4 Coefficients for calculating k_v
a_kv = [-3.80595, -3.44965, -0.39902, 0.50167];
b_kv = [0.56934, -0.22911, 0.73042, 1.07319];
c_kv = [0.81061, 0.51059, 0.11899, 0.27195];
d_kv = -0.16398;
e_kv = 0.63297;

% Table 2.5 Coefficients for calculating alpha_h
a_ah = [-0.14318, 0.29591, 0.32177, -5.37610, 16.1721];
b_ah = [1.82442, 0.77564, 0.63773, -0.96230, -3.29980];
c_ah = [-0.55187, 0.19822, 0.13164, 1.47828, 3.43990];
d_ah = 0.67849;
e_ah = -1.95537;

% Table 2.6 Coefficients for calculating alpha_v
a_av = [-0.07771, 0.56727, -0.20238, -48.2991, 48.5833];
b_av = [2.33840, 0.95545, 1.14520, 0.791669, 0.791459];
c_av = [-0.76284, 0.54039, 0.26809, 0.116226, 0.116479];
d_av = -0.053739;
e_av = 0.83433;

% Calculate k_h
k_h = d_kh .* log10(frequency) + e_kh;
for i = 1:numel(a_kh)
    k_h = k_h + a_kh(i) .* exp(-((log10(frequency) - b_kh(i)) ./ c_kh(i)) .^ 2);    
end
k_h = 10.^k_h;

% Calculate k_v
k_v = d_kv .* log10(frequency) + e_kv;
for i = 1:numel(a_kv)
    k_v = k_v + a_kv(i) .* exp(-((log10(frequency) - b_kv(i)) ./ c_kv(i)) .^ 2);
end
k_v = 10.^k_v;

% Calculate alpha_h
alpha_h = d_ah .* log10(frequency) + e_ah;
for i = 1:numel(a_ah)
    alpha_h = alpha_h + a_ah(i) .* exp(-((log10(frequency) - b_ah(i)) / c_ah(i)) .^ 2);
end

% Calculate alpha_v
alpha_v = d_av .* log10(frequency) + e_av;
for i = 1:numel(a_av)
    alpha_v = alpha_v + a_av(i) .* exp(-((log10(frequency) - b_av(i)) / c_av(i)) .^ 2);
end

% Calculate k and alpha based on elevation angle and polarization
k = 0.5 * (k_h + k_v + (k_h - k_v) * cos(elevation_angle)^2 * cos(2. * polarization_tilt_angle));
alpha = 0.5 * (k_h .* alpha_h + k_v .* alpha_v + (k_h .* alpha_h - k_v .* alpha_v) .* cos(elevation_angle)^2 .* cos(2. * polarization_tilt_angle)) ./ k;

attenuation = k .* rain_rate.^alpha;