function [ code ] = mls( register_length, feedback_taps )
%% Generate a maximum length sequence based on the register length and feedback taps.
%     :param register_length: The length of the linear feedback shift register.
%     :param feedback_taps: The bits to use as feedback.
%     :return: The maximum length sequence.
%
%     Created by: Lee A. Harrison
%     On: 4/27/2019

% Initialize the linear feedback shift register
i = 1:register_length;
register = mod(i, 2);

% For the output sequence
sequence_length = 2 ^ register_length - 1;
sequence = zeros(sequence_length, 1);

% Generate the output PRN based on the register length
for i = 1:sequence_length
    
    % Calculate the feedback based on the taps and modulo 2 addition
    s = mod(sum(register(feedback_taps)), 2);
    
    % Shift bits to the rights
    for k = register_length:-1:2
        register(k) = register(k-1);
    end
    
    % Stored feedback into bit 0
    register(1) = s;
    
    % Append the output sequence
    sequence(i) = register(end);
end

code = sequence - (sequence == 0);