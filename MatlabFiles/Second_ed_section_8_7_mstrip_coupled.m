
% author: Akshay Sawant
%
% General file calling functions created out of matlab code given in
% resource for section 8.7 and 6.63
%


% Created  table out of methods provided for section 8.7
    clear all
    clc
    spacing= 0.1:0.1:10;
    width= 0.1:0.01:2;
    epsilon_r = 5.5;
    height=1;
    
    Z0_ratio= zeros (length(spacing), length(width));
    Z_0e= zeros (length(spacing), length(width));
    Z_0o= zeros (length(spacing), length(width));
    eps_e= zeros (length(spacing), length(width));
    eps_o=zeros (length(spacing), length(width));
    Z0_sys= zeros (length(spacing), length(width));
    Z0_char= zeros (length(spacing), length(width));
    
    for s_iter=1:length(spacing)
        for w_iter= 1:length(width);
            [z0_ratio,z0e,z0o,eeo,eee,z0,z0s]= getCoupledLineParameter(epsilon_r,width(w_iter),spacing(s_iter),height);
            Z0_ratio(s_iter,w_iter)= z0_ratio;
            Z_0e(s_iter,w_iter)= z0e; 
            Z_0o(s_iter,w_iter)= z0o;
            eps_e(s_iter,w_iter)= eee;
            eps_o(s_iter,w_iter)= eeo;
            Z0_sys(s_iter,w_iter)= z0s;
            Z0_char(s_iter,w_iter)= z0;
        end
    end
    
    
    % Create to generate nomalized width values based on section 6.6.3
    microstripWidth= 0:1e-6:1.27e-3;
    subHeight=635e-6;
    Z0_micro= zeros(1,length(microstripWidth));
    E_eff= zeros(1,length(microstripWidth));
    
    for width_iter=1:length(microstripWidth)
        [z0_char,eff]= getMicrostripParameter(epsilon_r,microstripWidth(width_iter),subHeight);
        Z0_micro(1,width_iter)=z0_char;
        E_eff(1,width_iter)=eff;
    end
    
   