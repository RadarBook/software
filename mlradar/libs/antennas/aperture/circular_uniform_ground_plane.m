classdef circular_uniform_ground_plane
    % Circular aperture, uniform distribution in ground plane
    % Created by: Lee A. Harrison
    % On: 8/2/2018
    
    properties
        % Properties for circular uniform apertures
        radius = 1.0; % The aperture radius (m).
        frequency = 1.0e9; % The operating frequency (Hz).
        r = 1.0e9; % The range to the field point (m).
        theta = pi/2; % The theta angle to the field point (rad).
        phi = pi; % The phi angle to the field point (rad).
    end
    
    methods
        % Methods for circular TE11 apertures
        function obj = circular_uniform_ground_plane(radius, frequency, r, theta, phi)
            % Class constructor
            if(nargin > 0)
                obj.r = r;
                obj.theta = theta;
                obj.phi = phi;
                obj.frequency = frequency;
                obj.radius = radius;
            end
        end
        
        
        function [half_power_eplane, half_power_hplane, first_null_eplane, first_null_hplane] = beamwidth(obj)
            % Calculate the beamwidths for a circular aperture in a ground plane with a uniform distribution of the fields.
            % :param radius: The radius of the aperture (m).
            % :param frequency: The operating frequency (Hz).
            % :return: The half power and first null beamwidths in the E- and H-plane (deg).
            
            % Speed of light
            c = 299792458;
            
            % Calculate the wavelength
            wavelength = c / obj.frequency;
            
            % Calculate the half power beamwidth in the E-plane
            half_power_eplane = 29.2 * wavelength / obj.radius;
            
            % Calculate the half power beamwidth in the H-plane
            half_power_hplane = 29.2 * wavelength / obj.radius;
            
            % Calculate the first null beamwidth in the E-plane
            first_null_eplane = 69.9 * wavelength / obj.radius;
            
            % Calculate the first null beamwidth in the H-plane
            first_null_hplane = 69.9 * wavelength / obj.radius;
            
        end
        
        
        function d = directivity(obj)
            % Calculate the directivity for a circular aperture in a ground plane with a uniform distribution of the fields.
            % :param radius: The radius of the aperture (m).
            % :param frequency: The operating frequency (Hz).
            % :return: The directivity for the circular aperture.
            
            % Speed of light
            c = 299792458;
            
            % Calculate the wavelength
            wavelength = c / obj.frequency;
            
            % Calculate the directivity
            d = (2.0 * pi * obj.radius / wavelength) ^ 2;
        end
        
        
        function [eplane hplane] = side_lobe_level(obj)
            % This is a specific value for a circular aperture in a ground plane with a uniform distribution of the fields.
            % :return: The side lobe level for both the E- and H-planes (dB).
            
            eplane = -17.6;
            hplane = -17.6;
        end
        
        
        function [e_r, e_theta, e_phi, h_r, h_theta, h_phi] = far_fields(obj)
            % Calculate the electric and magnetic fields in the far field of the aperture.
            % :param r: The range to the field point (m).
            % :param theta: The theta angle to the field point (rad).
            % :param phi: The phi angle to the field point (rad).
            % :param radius: The radius of the aperture (m).
            % :param frequency: The operating frequency (Hz).
            % :return: The electric and magnetic fields radiated by the aperture (V/m), (A/m).
            
            % Calculate the wave impedance
            eta = 119.9169832 * pi;
            
            % Speed of light
            c = 299792458;
            
            % Calculate the wavenumber
            k = 2.0 * pi * obj.frequency / c;
            
            % Calculate the argument for the Bessel function
            z = k * obj.radius * sin(obj.theta);
            
            % Calculate the Bessel function
            index = z ~= 0.0;
            bessel_term = 0.5 * ones(size(z));
            bessel_term(index) = besselj(1, z(index)) ./ z(index);
            
            % Define the radial-component of the electric far field (V/m)
            e_r = 0.0;
            
            % Define the theta-component of the electric far field (V/m)
            e_theta = 1j * k * obj.radius ^ 2 * exp(-1j * k * obj.r) / obj.r * sin(obj.phi) .* bessel_term;
            
            % Define the phi-component of the electric far field (V/m)
            e_phi = 1j * k * obj.radius ^ 2 * exp(-1j * k * obj.r) / obj.r * cos(obj.phi) .* bessel_term;
            
            % Define the radial-component of the magnetic far field (A/m)
            h_r = 0.0;
            
            % Define the theta-component of the magnetic far field (A/m)
            h_theta = 1j * k * obj.radius ^ 2 * exp(-1j * k * obj.r) / obj.r * -cos(obj.theta) .* cos(obj.phi) / eta .* bessel_term;
            
            % Define the phi-component of the magnetic far field (A/m)
            h_phi = 1j * k * obj.radius ^ 2 * exp(-1j * k * obj.r) / obj.r * sin(obj.phi) / eta .* bessel_term;
        end
    end
    
    
end

