function attenuation = atmospheric_attenuation(frequency, temperature, dry_air_pressure, water_vapor_density)
%% Calculate the attenuation due to the atmosphere.
% :param frequency: The frequency of operation (Hz).
% :param temperature: The atmospheric temperature (K).
% :param dry_air_pressure: The dry air pressure (hPa).
% :param water_vapor_density: The water vapor density (g/m^3).
%
% Created by: Lee A. Harrison
% On: 6/18/2018

%% Read in the spectral data for oxygen
fid = fopen('oxygen_spectral_attenuation.txt', 'r');
data = fscanf(fid, '%f', [7, inf]);
fo = data(1,:);
a1 = data(2,:);
a2 = data(3,:);
a3 = data(4,:);
a4 = data(5,:);
a5 = data(6,:);
a6 = data(7,:);
fclose(fid);

%% Read in the spectral data for water
fid = fopen('water_vapor_spectral_attenuation.txt', 'r');
data = fscanf(fid, '%f', [7, inf]);
fw = data(1,:);
b1 = data(2,:);
b2 = data(3,:);
b3 = data(4,:);
b4 = data(5,:);
b5 = data(6,:);
b6 = data(7,:);
fclose(fid);

%% Find the percent temperature
theta = 300 / temperature;

%% Calculate the water vapor partial pressure
water_vapor_pressure = water_vapor_density * temperature / 216.7;

%% Total barometric pressure = dry air pressure + water vapor partial pressure
S_o = a1 * 1e-7 * dry_air_pressure * theta^3 .* exp(a2 * (1. - theta));
S_w = b1 * 0.1 * water_vapor_pressure * theta^3.5 .* exp(b2 * (1. - theta));

%% Calculate the line widths
delta_F_o = a3 * 1e-4 .* (dry_air_pressure * theta.^(0.8 - a4) + 1.1 * water_vapor_pressure * theta);
delta_F_o = sqrt(delta_F_o.^2 + 2.25e-6);

delta_F_w = b3 .* 1e-4 .* (dry_air_pressure .* theta.^b4 + b5 .* water_vapor_pressure .* theta.^b6);
delta_F_w = 0.535 * delta_F_w + sqrt(0.217*delta_F_w.^2 + (2.1316e-12 * fw.^2) / theta);

del_o = (a5 + a6*theta) * 1e-4 * (water_vapor_pressure + dry_air_pressure) * theta^0.8;

N_water_vapor = zeros(1,numel(frequency));
N_oxygen = zeros(1,numel(frequency));

%% Loop over all the frequencies and calculate the O2 and H2O terms
for i = 1:numel(frequency)
    term1_o = (delta_F_o - del_o .* (fo - frequency(i))) ./ ((fo - frequency(i)).^2 + delta_F_o.^2);
    term2_o = (delta_F_o - del_o .* (fo + frequency(i))) ./ ((fo + frequency(i)).^2 + delta_F_o.^2);
    %F_o = f / fo * (term1_o + term2_o)
    
    N_oxygen(i) = sum(S_o .* frequency(i) ./ fo .* (term1_o + term2_o));
    
    term1_w = delta_F_w ./ ((fw - frequency(i)) .^ 2 + delta_F_w .^ 2);
    term2_w = delta_F_w ./ ((fw + frequency(i)) .^ 2 + delta_F_w .^ 2);
    %F_w = f / fw * (term1_w + term2_w)
    
    N_water_vapor(i) = sum(S_w .* frequency(i) ./ fw .* (term1_w + term2_w));
    
end

%% Pressure induced nitrogen attenuation
d = 5.6e-4 * (dry_air_pressure + water_vapor_pressure) * theta^0.8;

N_d = frequency .* dry_air_pressure * theta^2 .*(6.14e-5 ./ (d * (1. + (frequency./d).^2)) + 1.4e-12 .* dry_air_pressure * theta^1.5 ./ (1. + 1.9e-5 .* frequency.^1.5));

attenuation = 0.1820 * frequency .* (N_oxygen + N_d + N_water_vapor);
