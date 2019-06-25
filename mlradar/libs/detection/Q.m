function [ val ] = Q(x, y, eps)
% Marcum's Q function algorithm by Parl.
%     :param x: The first argument of the Q function.
%     :param y: The second argument of the Q function.
%     :param eps: The convergence criteria.
%     :return: The evaluation of the Q function of (x, y, eps).
% 
%     
%     Created by: Lee A. Harrison
%     On: 10/11/2018

    n = 1;

    alpha_n_1 = 0;    
    d1 = y / x;

    if x < y
        alpha_n_1 = 1;
        d1 = x / y;
    end

    alpha_n_2 = 0.0;
    beta_n_1 = 0.5;
    beta_n_2 = 0.0;
    beta_n = 0.0;
    dn = d1;

    while beta_n < 1.0 / eps
        alpha_n = dn + 2.0 * n / (x * y) * alpha_n_1 + alpha_n_2;
        beta_n = 1.0 + 2.0 * n / (x * y) * beta_n_1 + beta_n_2;

        dn = dn * d1;

        alpha_n_2 = alpha_n_1;
        alpha_n_1 = alpha_n;

        beta_n_2 = beta_n_1;
        beta_n_1 = beta_n;

        n = n + 1;
    end

    if x < y
        val = alpha_n / (2.0 * beta_n) * exp(-(x - y) ^ 2 / 2.0);
    else
        val = 1.0 - (alpha_n / (2.0 * beta_n) * exp(-(x - y) ^ 2 / 2.0));
    end

end

