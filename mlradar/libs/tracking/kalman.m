classdef kalman
    % Kalman class
    % Created by: Lee A. Harrison
    % On: 2/20/2019
    
    properties
        x % State vecotor
        u % Input control vector
        P % Covariance
        A % State transition
        B % Control matrix
        Q % Process noise variance
        H % Measurement transition
        R % Measurement noise variance
        
        state
        residual
        process_noise
        epsilon
        sigma
    end
    
    methods
        
        function obj = kalman(x, u, P, A, B, Q, H, R)
            obj.x = x;
            obj.u = u;
            obj.P = P;
            obj.A = A;
            obj.B = B;
            obj.Q = Q;
            obj.H = H;
            obj.R = R;
            
            obj.state = [];
            obj.residual = [];
            obj.process_noise = [];
            obj.epsilon = [];
            obj.sigma = [];
        end
        
        function obj = filter(obj, varargin)
        % Perform the filtering operation on the measurements.
            
            if nargin < 4
                z = varargin{1};
                type = 'none';
            else
                z = varargin{1};
                threshold = varargin{2};
                scale = varargin{3};
                type = varargin{4};
            end
            
            % Loop over all the measurements
            if strcmp(type, 'epsilon')
                for i = 1:length(z)
                    obj = predict(obj);
                    obj = update(obj, z(:, i));
                    obj = adapt_epsilon(obj, threshold, scale);
                end
            elseif strcmp(type, 'sigma')
                for i = 1:length(z)
                    obj = predict(obj);
                    obj = update(obj, z(:, i));
                    obj = adapt_sigma(obj, threshold, scale);
                end
            else
                for i = 1:length(z)
                    obj = predict(obj);
                    obj = update(obj, z(:, i));
                end
            end
            
            function obj = predict(obj)
                % Predict the state and covariance
                obj.x = obj.A * obj.x + obj.B * obj.u;
                obj.P = (obj.A * obj.P) * obj.A' + obj.Q;
            end
            
            function obj = update(obj, z)
                % Calculate the Kalman gain
                S = (obj.H * obj.P) * obj.H' + obj.R;
                K = (obj.P * obj.H') * inv(S);
                
                % Correction based on the measurement
                res = z - obj.H * obj.x;
                obj.x = obj.x + (K * res);
                obj.P = obj.P - K * obj.H * obj.P;
                
                obj.state = [obj.state, (obj.x)];
                obj.residual = [obj.residual; norm(res)];
                obj.epsilon = [obj.epsilon; (res' * (inv(S) * res))];
                obj.sigma = [obj.sigma; sqrt(S(1, 1) ^ 2 + S(2, 2) ^ 2 + S(3, 3) ^ 2)];
                obj.process_noise = [obj.process_noise; obj.Q(1, 1)];
            end
            
            function obj = adapt_epsilon(obj, threshold, scale)
                % Epsilon method
                if obj.epsilon(end) > threshold
                    obj.Q = obj.Q * scale;
                else
                    obj.Q = obj.Q / scale;
                end
            end
            
            function obj = adapt_sigma(obj, n_sigma, scale)
                % Sigma method
                if obj.residual(end) > n_sigma * obj.sigma(end)
                    obj.Q = obj.Q * scale;
                else
                    obj.Q = obj.Q / scale;
                end
                
            end
            
        end
    end
    
end