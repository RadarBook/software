function [ scattering_matrix ] = po_scattering(theta_inc, phi_inc, theta_obs, phi_obs, frequency, vertices, faces)
%% Calculates the normalized scattering matrix
% Scattering matrix is calculated in linear polarization [VV, HV, VH, HH]

% Created by: Lee A. Harrison
% Cretaed on: 1/17/2019
%
% Copyright (C) 2019 Artech House (artech@artechhouse.com)
% This file is part of Introduction to Radar Using Python and MATLAB
% and can not be copied and/or distributed without the express permission of Artech House.

% Size the scattering matrix
scattering_matrix = zeros(4, numel(frequency));

% Wavelength
wavelength = 299792458.0 / frequency;

% Wavenumber
k = 2.0 * pi / wavelength;

% Number of vertices and faces
nv = numel(vertices(:,1));
nf = numel(faces(:,1));

% Incident angles and direction cosines
cpi = cos(phi_inc);
spi = sin(phi_inc);
cti = cos(theta_inc);
sti = sin(theta_inc);

ui = sti * cpi;
vi = sti * spi;
wi = cti;

incident_direction = [ui, vi, wi];

% Observation angles and direction cosines
cpo = cos(phi_obs);
spo = sin(phi_obs);
cto = cos(theta_obs);
sto = sin(theta_obs);

uo = sto * cpo;
vo = sto * spo;
wo = cto;

uuo = cto * cpo;
vvo = cto * spo;
wwo = -sto;

% Incident field in global Cartesian
Ei = 1.0;
Ei_V = [cti * cpi * Ei, cti * spi * Ei, -sti * Ei];
Ei_H = [-spi * Ei, cpi * Ei, 0.0];

% Position vectors to vertices
r = zeros(nv, 3);
for i_vert = 1:nv
    r(i_vert,:) = [vertices(i_vert,1), vertices(i_vert,2), vertices(i_vert,3)];
end

% Edge vectors and normals
% Loop over faces
for i_face = 1:nf
    A = r(faces(i_face, 2),:) - r(faces(i_face, 1),:);
    B = r(faces(i_face, 3),:) - r(faces(i_face, 2),:);
    C = r(faces(i_face, 1),:) - r(faces(i_face, 3),:);
    
    % Outward directed normals
    normal = cross(A, B);
    
    % Edge lengths
    dist = [norm(A), norm(B), norm(C)];
    
    ss = 0.5 * sum(dist);
    area = sqrt(ss * (ss - dist(1)) * (ss - dist(2)) * (ss - dist(3)));
    
    % Unit normals
    normal = normal / norm(normal);
    
    % Just a normal check for illumination
    if dot(normal, incident_direction) >= 0.0
        % Local angles
        beta = acos(normal(3));
        alpha = atan2(normal(2), normal(1));
        
        % Local direction cosines
        ca = cos(alpha);
        sa = sin(alpha);
        cb = cos(beta);
        sb = sin(beta);
        
        % Rotation matrices
        rotation1 = [[ca, sa, 0.0];  [-sa, ca, 0.0];  [0.0, 0.0, 1.0]];
        rotation2 = [[cb, 0.0, -sb]; [0.0, 1.0, 0.0]; [sb, 0.0, cb]];
        
        % Transform incident direction
        a = rotation2 * (rotation1 * incident_direction');
        ui_t = a(1); vi_t = a(2); wi_t = a(3);
        
        sti_t = sqrt(ui_t * ui_t + vi_t * vi_t) * sign(wi_t);
        cti_t = sqrt(1.0 - sti_t * sti_t);
        
        phi_t = atan2(vi_t, ui_t);
        cpi_t = cos(phi_t);
        spi_t = sin(phi_t);
        
        % Phase at the three vertices
        v1 = faces(i_face, 1);
        v2 = faces(i_face, 2);
        v3 = faces(i_face, 3);
        
        
        alpha1 = k * (vertices(v1, 1) * (uo + ui) + vertices(v1,2) * (vo + vi) + vertices(v1, 3) * (wo + wi));
        alpha2 = k * ((vertices(v2, 1) - vertices(v1, 1)) * (uo + ui) + (vertices(v2, 2) - vertices(v1, 2)) * (vo + vi) + (vertices(v2, 3) - vertices(v1, 3)) * (wo + wi)) + alpha1;
        alpha3 = k * ((vertices(v3, 1) - vertices(v1, 1)) * (uo + ui) + (vertices(v3, 2) - vertices(v1, 2)) * (vo + vi) + (vertices(v3, 3) - vertices(v1, 3)) * (wo + wi)) + alpha1;
        
        
        exp1 = exp(1j * alpha1);
        exp2 = exp(1j * alpha2);
        exp3 = exp(1j * alpha3);
        
        % Incident field in local Cartesian
        Ei_V2 = rotation2 * (rotation1 * Ei_V');
        Ei_H2 = rotation2 * (rotation1 * Ei_H');
        
        %  Incident field in local Spherical
        Et_v = Ei_V2(1) * cti_t * cpi_t + Ei_V2(2) * cti_t * spi_t - Ei_V2(3) * sti_t;
        Ep_v = -Ei_V2(1) * spi_t + Ei_V2(2) * cpi_t;
        
        Et_h = Ei_H2(1) * cti_t * cpi_t + Ei_H2(2) * cti_t * spi_t - Ei_H2(3) * sti_t;
        Ep_h = -Ei_H2(1) * spi_t + Ei_H2(2) * cpi_t;
        
        % Reflection coefficients
        % Rs = 0.001
        Rs = 0.0;
        gamma_perpendicular = -1.0 / (2.0 * Rs * cti_t + 1.0);
        gamma_parallel = 0.0;
        if (2.0 * Rs + cti_t) ~= 0.0
            gamma_parallel = -cti_t / (2.0 * Rs + cti_t);
        end
        
        % Surface currents in local Cartesian
        Jx_v = -Et_v * cpi_t * gamma_parallel + Ep_v * spi_t * cti_t * gamma_perpendicular;
        Jy_v = -Et_v * spi_t * gamma_parallel - Ep_v * cpi_t * cti_t * gamma_perpendicular;
        
        Jx_h = -Et_h * cpi_t * gamma_parallel + Ep_h * spi_t * cti_t * gamma_perpendicular;
        Jy_h = -Et_h * spi_t * gamma_parallel - Ep_h * cpi_t * cti_t * gamma_perpendicular;
        
        % Now loop over all the frequencies
        for i_freq = 1:numel(frequency)
            
            % Area integral
            Ic = surface_integral(alpha1(i_freq), alpha2(i_freq), alpha3(i_freq), exp1(i_freq), exp2(i_freq), exp3(i_freq), area);
            
            % Scattered field components in local coordinates
            Es2_v = [Jx_v * Ic, Jy_v * Ic, 0.0];
            Es2_h = [Jx_h * Ic, Jy_h * Ic, 0.0];
            
            % Transform back to global coordinates
            Es_v = rotation1' * (rotation2' * Es2_v');
            Es_h = rotation1' * (rotation2' * Es2_h');
            
            Ev_v = uuo * Es_v(1) + vvo * Es_v(2) + wwo * Es_v(3);
            Eh_v = -spo * Es_v(1) + cpo * Es_v(2);
            
            Ev_h = uuo * Es_h(1) + vvo * Es_h(2) + wwo * Es_h(3);
            Eh_h = -spo * Es_h(1) + cpo * Es_h(2);
            
            % Set the scattering matrix
            scattering_matrix(1, i_freq) = scattering_matrix(1, i_freq) + Ev_v;
            scattering_matrix(2, i_freq) = scattering_matrix(2, i_freq) + Ev_h;
            scattering_matrix(3, i_freq) = scattering_matrix(3, i_freq) + Eh_v;
            scattering_matrix(4, i_freq) = scattering_matrix(4, i_freq) + Eh_h;
            
        end
    end    
    
end

scattering_matrix = scattering_matrix *  sqrt(4.0 * pi) / wavelength;
end


function [ Ic ] = surface_integral(alpha1, alpha2, alpha3, exp1, exp2, exp3, area)
eps = 1e-10;
if abs(alpha1 - alpha2) < eps && (abs(alpha1 - alpha3) < eps)
    Ic = area * exp1;
elseif abs(alpha1 - alpha2) < eps
    Ic = 2.0 * area / (alpha3 - alpha2) * (1j * exp1 - (exp1 - exp3) / (alpha1 - alpha3));
elseif abs(alpha1 - alpha3) < eps
    Ic = 2.0 * area / (alpha3 - alpha2) * (-1j * exp1 + (exp1 - exp2) / (alpha1 - alpha2));
elseif abs(alpha2 - alpha3) < eps
    Ic = 2.0 * area / (alpha1 - alpha2) * (1j * exp3 - (exp1 - exp3) / (alpha1 - alpha3));
else
    Ic = 2.0 * area / (alpha3 - alpha2) * ((exp1 - exp2) / (alpha1 - alpha2) - (exp1 - exp3) / (alpha1 - alpha3));
end
end