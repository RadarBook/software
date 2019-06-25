function a = sinint(x)
%% Calculate the sin integral
%   :param x: The argument of the sin integral
%   :return: The value of the sin integral.
%
%     Created by: Lee A. Harrison
%     On: 2/20/2019

[m, n] = size(x);

a = zeros(m,n);

for im = 1:m
    for in = 1:n
        a(im, in) =  integral(@sinint_arg, 1e-6, x(im, in));
    end
end

end

