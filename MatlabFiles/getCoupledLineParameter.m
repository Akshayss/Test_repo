function [Z0eDZ0o,Z_0e,Z_0o,epsilon_eo,epsilon_ee,Z_0,Z_0S] = getCoupledLineParameter(epsilon_r,w,s,h)
% getCoupledLineParameter- 
% author: Michael Steer (2013)
%
% Calculate the parameters of a microstrip line and a pair of
% coupled microstrip lines of equal width
%
% Uses the analysis of Hammerstad and Jensen described in
% Section 8.7 of
% Microwave and RF Design: A Systems Approach, Second Editio
% by Michael Steer

% INPUT:
%       espilon_r relative permittivity of substrate
%       w = width of line(s)
%       h = height of substrate
%       s = separation of line(s)
% OUTPUT:
%      Z_0 characteristic impedance of a single line
%      espilon_e effective relative permittivity of a single
%                line
%      Z_0e characteristic impedance of even mode
%      Z_0e characteristic impedance of odd mode
%      espilon_ee effective relative permittivity of even mode
%      espilon_eo effective relative permittivity of odd mode

% Generates different coupled line parametrs for a
%set of different normalized width (u) and normalized spacing (g) of a
%given epsilon r.



% Trial Parameters
    u = w/h;
    g = s/h;
    mu = g.*exp(-g)+u*(20+g.^2)./(10+g.^2);
    m = 0.2175 + (4.113+(20.36./g).^6).^-0.251 + log(g.^10./(1+(g./13.8).^10))./323;
    alpha = 0.5.*exp(-g);
    psi = 1+(g./1.45)+(g.^2.09)./3.95;
    varphi = 0.8645*u^0.1472;
    phi_e = varphi./(psi.*(alpha.*u.^m+(1-alpha).*u.^-m));
    b = 0.564*((epsilon_r-0.9)/(epsilon_r+3))^0.053;
    a = 1+log((u^4 + (u/52)^2)/(u^4+0.432))/49+log(1+(u/18.1)^3)/18.7;
    epsilon_e = (epsilon_r+1)/2 + ((epsilon_r-1).*(1+10./u).^(-(a*b)))/2;
    F_1 = 6+(2*pi-6)*exp(-(30.999./u).^0.7528);
    Z_01 = 60*log(F_1./u+sqrt(1+(2./u).^2));
    Z_0 = Z_01./sqrt(epsilon_e);
% Now calculate coupled line parameters.
    F_e = (1+10./mu).^(-(a*b));
    epsilon_ee = (epsilon_r+1)/2 + (epsilon_r-1).*F_e./2;
    Z_01e = Z_01./(1-Z_01.*phi_e/377);
    Z_0e = Z_01e./sqrt(epsilon_ee);
    q = exp(-1.366-g);
    r = 1+0.15*(1-exp(1-(epsilon_r-1)^2/8.2)./(1+g.^(-6)));
    f_o1 = 1-exp(-0.179*g.^0.15-(0.328*g.^r)./log(exp(1)+(g./7).^2.8));
    p = exp(-0.745*g.^0.295)./cosh(g.^0.68);
    f_o = f_o1.*exp(p.*log(u)+q.*sin(pi*log(u)/log(10)));
    n =(1/17.7 + exp(-6.424-0.76*log(g)-(g/0.23).^5)).*log((10+68.3*g.^2)./(1+32.5*g.^3.093));
    beta = 0.2306+log((g.^10)./(1+(g/3.73).^10))/301.8 + log(1+0.646*g.^1.175)/5.3;
    theta = 1.729 + 1.175*log(1+(0.627)./(g+0.327*g.^2.17));
    phi_o = phi_e - theta.*exp(beta.*u.^(n)*log(u))./psi;
    F_o = f_o.*(1+10/u)^(-a*b);
    epsilon_eo = (epsilon_r + 1)/2 + F_o.*(epsilon_r-1)/2;
    Z_01o = Z_01./(1-Z_01.*phi_o/377);
    Z_0o = Z_01o./sqrt(epsilon_eo);
    Z0eDZ0o = Z_0e/Z_0o;
    Z_0S = sqrt(Z_0e*Z_0o);
 %
    eeoee = epsilon_eo/epsilon_e;
    eeeee = epsilon_ee/epsilon_e;


end

