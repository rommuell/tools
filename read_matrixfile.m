close all
clearvars
clc

%% 

opt = 4;

if opt == 3
    load('/home/rm/Documents/master_thesis/data/okvis_output/Jacobian_i3.mat');
    load('/home/rm/Documents/master_thesis/data/okvis_output/H_i3.mat');
    load('/home/rm/Documents/master_thesis/data/okvis_output/cov_i3.mat');
elseif opt == 4
    % after bugfix
    load('/home/rm/Documents/master_thesis/data/okvis_output/Jacobian_i4.mat');
    load('/home/rm/Documents/master_thesis/data/okvis_output/H_i4.mat');
    load('/home/rm/Documents/master_thesis/data/okvis_output/cov_i4.mat');
elseif opt == 15
    load('/home/rm/Documents/master_thesis/data/okvis_output/Jacobian_i15.mat');
    load('/home/rm/Documents/master_thesis/data/okvis_output/H_i15.mat');
    load('/home/rm/Documents/master_thesis/data/okvis_output/cov_i15.mat');
end


figure
imagesc(J_egm);
title('J_{egm}')

figure 
imagesc(H_egm)
title('H_{egm}')

H_matl = J_egm' * J_egm;
H_diff = H_matl - H_egm;
figure
imagesc(H_diff)
title('(J_{egm}*J_{egm})_{matl} - H_{egm}')

figure
imagesc(C_egm)
title('C_{egm}')

C_matl = inv(H_egm);
figure
imagesc(C_matl)
title('(H_{egm}^{-1})_{matl}')

C_matl_matl = inv(H_matl);
figure
imagesc(C_matl_matl)
title('((J_{egm}*J_{egm})_{matl}^{-1})_{matl}')

%% 
load('/home/rm/Documents/master_thesis/data/okvis_output/covariances_i6to9.mat')

figure
subplot(2,2,1)
imagesc(C6)
title('C6')

subplot(2,2,2)
imagesc(C7)
title('C7')

subplot(2,2,3)
imagesc(C8)
title('C8')

subplot(2,2,4)
imagesc(C9)
title('C9')

%% ADELP Plot

load('/home/rm/Documents/master_thesis/data/okvis_output/ADELP.mat');
plot(ADELP(:,1:5));
title('covariance criteria');
legend('trace', 'determinant', 'max(eig)', 'sum(eig²)', 'P(eig)')

%diff = ADELP(:,1)-ADELP(:,4);
%% AD_EP_EA plot
figure
yyaxis left
plot(AD_EP_EA(:,1:2));

yyaxis right
plot(AD_EP_EA(:,3:4));
title('covariance criteria');
legend('trace', 'determinant', 'e_{pos}', 'e_{angle}');

figure

yyaxis left
plot(AD_EP_EA(:,1));

yyaxis right
plot(AD_EP_EA(:,2));
title('covariance criteria');
legend('trace', 'determinant');

%% ADELP_EP_EA plot

load('/home/rm/Documents/master_thesis/data/vicon/v1/okvis_output/ADELP_EP_EA.mat')

for c = 1:5
   ADELP_EP_EA(:,c) =  ADELP_EP_EA(:,c)/max(ADELP_EP_EA(:,c));
end

figure
plot(ADELP_EP_EA(:,1:5));
title('covariance criteria');
legend('trace', 'determinant', 'max(eig)', 'sum(eig²)', 'P(eig)');

figure
yyaxis left
plot(ADELP_EP_EA(:,1));

yyaxis right
plot(ADELP_EP_EA(:,2));
title('covariance criteria');
legend('trace', 'determinant');

figure
yyaxis left
plot(ADELP_EP_EA(:,1:2));

yyaxis right
plot(ADELP_EP_EA(:,6:7));
title('covariance criteria');
legend('trace', 'determinant', 'e_{pos}', 'e_{angle}');


%% ADELP_Aall_Dall_EP_EA plot
%clc, clear all, close all
load('/home/rm/Documents/master_thesis/data/vicon/wall_circ/okvis_output/ADELP_Aall_Dall_EP_EA.mat')

for c = 1:7
   ADELP_Aall_Dall_EP_EA(:,c) =  ADELP_Aall_Dall_EP_EA(:,c)/max(ADELP_Aall_Dall_EP_EA(:,c));
end
%ADELP_Aall_Dall_EP_EA(20:end,7) = ADELP_Aall_Dall_EP_EA(20:end,7) * 2e35;
%ADELP_Aall_Dall_EP_EA(:,6) = ADELP_Aall_Dall_EP_EA(:,6) - mean(ADELP_Aall_Dall_EP_EA(:,6));

a =[1 -1];b=[1];
int = filter(b,a,ADELP_Aall_Dall_EP_EA(:,6) - mean(ADELP_Aall_Dall_EP_EA(:,6)));

figure
plot(ADELP_Aall_Dall_EP_EA(:,1:7));
title('covariance criteria');
legend('trace', 'determinant', 'max(eig)', 'sum(eig²)', 'P(eig)', 'trace all', 'determinant all');

figure
yyaxis left
plot(ADELP_Aall_Dall_EP_EA(:,1));

yyaxis right
plot(ADELP_Aall_Dall_EP_EA(:,2));
title('covariance criteria');
legend('trace', 'determinant');

figure
yyaxis left
plot(ADELP_Aall_Dall_EP_EA(:,6));

yyaxis right
plot(ADELP_Aall_Dall_EP_EA(:,7));
title('covariance criteria full matrix');
legend('trace all', 'determinant all');

figure
yyaxis left
plot(ADELP_Aall_Dall_EP_EA(:,1:2));

yyaxis right
plot(ADELP_Aall_Dall_EP_EA(:,8:9));
title('covariance criteria');
legend('trace', 'determinant', 'e_{pos}', 'e_{angle}');

figure
yyaxis left
plot([ADELP_Aall_Dall_EP_EA(:,6), int]);
ylim([0,0.5]);


yyaxis right
plot(ADELP_Aall_Dall_EP_EA(:,8:9));
title('covariance criteria');
legend('trace all', 'int', 'e_{pos}', 'e_{angle}');






