function a = cosint(x)
%% Calculate the cos integral
%   :param x: The argument of the cos integral
%   :return: The value of the cos integral.
%
%     Created by: Lee A. Harrison
%     On: 2/20/2019

[m, n] = size(x);

a = zeros(m,n);

for im = 1:m
    for in = 1:n
        a(im, in) =  0.57721 + log(x) + integral(@cosint_arg, 1e-6, x(im, in));
    end
end

end

