classdef rectangular_te10_ground_plane
    % Rectangular aperture, TE10 ground plane
    % Created by: Lee A. Harrison
    % On: 8/2/2018
    
    properties
        % Properties for rectangular aperture, TE10 distribution
        width = 1.0; % The aperture width (m).
        height = 1.0; % The aperture height (m).
        frequency = 1.0e9; % The operating frequency (Hz).
        r = 1.0e9; % The range to the field point (m).
        theta = pi/2; % The theta angle to the field point (rad).
        phi = pi; % The phi angle to the field point (rad).
    end
    
    methods
        % Methods for rectangular aperture, TE10 distribution
        function obj = rectangular_te10_ground_plane(width, height, frequency, r, theta, phi)
            % Class constructor
            if(nargin > 0)
                obj.r = r;
                obj.theta = theta;
                obj.phi = phi;
                obj.frequency = frequency;
                obj.width = width;
                obj.height = height;
            end
        end
        
        function [half_power_eplane, half_power_hplane, first_null_eplane, first_null_hplane] = beamwidth(obj)
            % Calculate the beamwidths for a rectangular aperture in a ground plane
            % with a TE10 distribution of fields in the aperture.
            % :param width: The aperture width (m).
            % :param height: The aperture height (m).
            % :param frequency: The operating frequency (Hz).
            % :return: The half power and first null beamwidths in the E- and H-plane (deg).
            
            % Speed of light
            c = 299792458;
            
            % Calculate the wavelength
            wavelength = c / obj.frequency;
            
            % Calculate the half power beamwidth in the E-plane
            half_power_eplane = 50.6 * wavelength / obj.height;
            
            % Calculate the half power beamwidth in the H-plane
            half_power_hplane = 68.8 * wavelength / obj.width;
            
            % Calculate the first null beamwidth in the E-plane
            first_null_eplane = 114.6 * wavelength / obj.height;
            
            % Calculate the first null beamwidth in the H-plane
            first_null_hplane = 171.9 * wavelength / obj.width;
            
        end
        
        
        function d = directivity(obj)
            % Calculate the directivity for a rectangular aperture in a ground plane
            % with a TE10 distribution of fields in the aperture.
            % :param width: The width of the aperture (m).
            % :param height: The height of the aperture (m).
            % :param frequency: The operating frequency (Hz).
            % :return: The directivity for the rectangular aperture.
            
            % Speed of light
            c = 299792458;
            
            % Calculate the wavelength
            wavelength = c / obj.frequency;
            
            % Calculate the directivity
            d = 32.0 / pi * obj.width * obj.height / wavelength ^ 2;
        end
        
        
        function [eplane, hplane] = side_lobe_level(obj)
            % This is a specific value for a rectangular aperture in a ground plane
            % with a TE10 distribution of fields in the aperture.
            % :return: The side lobe level for both the E- and H-planes (dB).
            
            eplane = -13.26;
            hplane = -23.0;
        end
        
        
        function [e_r, e_theta, e_phi, h_r, h_theta, h_phi] = far_fields(obj)
            % Calculate the far zone electric and magnetic fields for a rectangular aperture in a ground plane
            % with a TE10 distribution of fields in the aperture.
            % :param r: The range to the field point (m).
            % :param theta: The theta angle to the field point (rad).
            % :param phi: The phi angle to the field point (rad).
            % :param width: The width of the aperture (m).
            % :param height: The height of the aperture (m).
            % :param frequency: The operating frequency (Hz).
            % :return: The far zone electric and magnetic fields (V/m), (A/m).
            
            % Calculate the wave impedance
            eta = 119.9169832 * pi;
            
            % Speed of light
            c = 299792458;
            
            % Calculate the wavenumber
            k = 2.0 * pi * obj.frequency / c;
                  
            % Define the x and y wavenumber components
            kx = k * obj.width * 0.5 * sin(obj.theta) .* cos(obj.phi);
            ky = k * obj.height * 0.5 * sin(obj.theta) .* sin(obj.phi);
            
            % Define the radial-component of the electric far field (V/m)
            e_r = 0.0;
            
            % Define the theta-component of the electric far field (V/m)
            e_theta = 1j * obj.width * obj.height * k / (2.0 * pi * obj.r) * exp(-1j * k * obj.r) * (-0.5 * pi * sin(obj.phi)) .* ...
            cos(kx) ./ (kx .^ 2 - (0.5 * pi) ^ 2) .* sinc(ky);
            
            % Define the phi-component of the electric far field (V/m)
            e_phi = 1j * obj.width * obj.height * k / (2.0 * pi * obj.r) * exp(-1j * k * obj.r) * (-0.5 * pi * cos(obj.theta) .* cos(obj.phi)) .* ...
            cos(kx) ./ (kx .^ 2 - (0.5 * pi) ^ 2) .* sinc(ky);
            
            % Define the radial-component of the magnetic far field (A/m)
            h_r = 0.0;
            
            % Define the theta-component of the magnetic far field (A/m)
            h_theta = -1j * obj.width * obj.height * k / (2.0 * pi * eta * obj.r) * exp(-1j * k * obj.r) * ...
            (-0.5 * pi * cos(obj.theta) .* cos(obj.phi)) .* cos(kx) ./ (kx .^ 2 - (0.5 * pi) ^ 2) .* sinc(ky);
            
            % Define the phi-component of the magnetic far field (A/m)
            h_phi = 1j * obj.width * obj.height * k / (pi * eta * obj.r) * exp(-1j * k * obj.r) * (-0.5 * pi * sin(obj.phi)) .* ...
            cos(kx) ./ (kx .^ 2 - (0.5 * pi) ^ 2) .* sinc(ky);
            
        end

    end
end
