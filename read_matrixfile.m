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
%load('/home/rm/Documents/master_thesis/data/vicon/wall_circ/okvis_output/ADELP_Aall_Dall_EP_EA.mat')

for c = 1:7
   ADELP_Aall_Dall_EP_EA(:,c) =  ADELP_Aall_Dall_EP_EA(:,c)/max(ADELP_Aall_Dall_EP_EA(:,c));
end
%ADELP_Aall_Dall_EP_EA(20:end,7) = ADELP_Aall_Dall_EP_EA(20:end,7) * 2e35;
%ADELP_Aall_Dall_EP_EA(:,6) = ADELP_Aall_Dall_EP_EA(:,6) - mean(ADELP_Aall_Dall_EP_EA(:,6));

a =[1 -1];b=[1];
int = filter(b,a,ADELP_Aall_Dall_EP_EA(:,6) - mean(ADELP_Aall_Dall_EP_EA(:,6)));

figure
% yyaxis left
plot(ADELP_Aall_Dall_EP_EA(:,1:6));
yyaxis right
plot(ADELP_Aall_Dall_EP_EA(:,7));
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

%%
figure
a = ADELP_Aall_Dall_EP_EA(:,8);
b = ADELP_Aall_Dall_EP_EA(:,6);
a = (a-mean(a))/std(a);
b = (b-mean(b))/std(b);
n = 1.2 * 20;
filt = fspecial('gaussian', [2*n ,1], n*2); %[24,2],8
filt((length(filt)/2+1):end) = 0;
filt = 2 * filt;
filt2 = [zeros(2*n,1); filt];
b_avg = conv(b,filt, 'same');
bf = conv(b, filt2, 'same');
corr = xcorr(a,bf);
l = length(a);
plot((-l+1):(l-1), corr/length(a));
title('xcorr trace error')
figure
plot(a)
hold on 
plot(b)
plot(bf)
plot(b_avg)
legend('position error', 'trace', 'trace filter lag', 'trace avg')

%%
clc; clear; close all;
load('/home/rm/Documents/master_thesis/data/vicon_leo/data_bag0-4.mat');

delta_t = t_0(1);
t_0 = t_0 - delta_t;
t_1 = t_1 - delta_t;
t_2 = t_2 - delta_t;
t_3 = t_3 - delta_t;
t_4 = t_4 - delta_t;

figure
subplot(3,1,1)
plot(t_0, ADELP_Aall_Dall_EP_EA_0(:,6));
hold on
plot(t_1, ADELP_Aall_Dall_EP_EA_1(:,6));
plot(t_2, ADELP_Aall_Dall_EP_EA_2(:,6));
plot(t_3, ADELP_Aall_Dall_EP_EA_3(:,6));
plot(t_4, ADELP_Aall_Dall_EP_EA_4(:,6));
title('trace all')

% subplot(3,1,2)
% plot(t_0, ADELP_Aall_Dall_EP_EA_0(:,7));
% hold on
% plot(t_1, ADELP_Aall_Dall_EP_EA_1(:,7));
% plot(t_2, ADELP_Aall_Dall_EP_EA_2(:,7));
% plot(t_3, ADELP_Aall_Dall_EP_EA_3(:,7));
% plot(t_4, ADELP_Aall_Dall_EP_EA_4(:,7));
% title('determinant all')
% ylim([0, 0.5e-244])

subplot(3,1,2)
plot(t_0, ADELP_Aall_Dall_EP_EA_0(:,8));
hold on
plot(t_1, ADELP_Aall_Dall_EP_EA_1(:,8));
plot(t_2, ADELP_Aall_Dall_EP_EA_2(:,8));
plot(t_3, ADELP_Aall_Dall_EP_EA_3(:,8));
plot(t_4, ADELP_Aall_Dall_EP_EA_4(:,8));
title('position error')

figure
subplot(5,1,1)
yyaxis left
plot(ADELP_Aall_Dall_EP_EA_0(:,8));
yyaxis right
plot(ADELP_Aall_Dall_EP_EA_0(:,6));
title('pos error vs trace')
xcorr(ADELP_Aall_Dall_EP_EA_0(:,8),ADELP_Aall_Dall_EP_EA_0(:,6));

subplot(5,1,2)
yyaxis left
plot(ADELP_Aall_Dall_EP_EA_1(:,8));
yyaxis right
plot(ADELP_Aall_Dall_EP_EA_1(:,6));

subplot(5,1,3)
yyaxis left
plot(ADELP_Aall_Dall_EP_EA_2(:,8));
yyaxis right
plot(ADELP_Aall_Dall_EP_EA_2(:,6));

subplot(5,1,4)
yyaxis left
plot(ADELP_Aall_Dall_EP_EA_3(:,8));
yyaxis right
plot(ADELP_Aall_Dall_EP_EA_3(:,6));

subplot(5,1,5)
yyaxis left
plot(ADELP_Aall_Dall_EP_EA_4(:,8));
yyaxis right
plot(ADELP_Aall_Dall_EP_EA_4(:,6));

figure
y = [550, 750];
subplot(5,1,1)
yyaxis left
plot(ADELP_Aall_Dall_EP_EA_0(:,8));
yyaxis right
plot(-log(ADELP_Aall_Dall_EP_EA_0(:,7)));
ylim(y)
title('pos error vs determinant')

subplot(5,1,2)
yyaxis left
plot(ADELP_Aall_Dall_EP_EA_1(:,8));
yyaxis right
plot(-log(ADELP_Aall_Dall_EP_EA_1(:,7)));
ylim(y)

subplot(5,1,3)
yyaxis left
plot(ADELP_Aall_Dall_EP_EA_2(:,8));
yyaxis right
plot(-log(ADELP_Aall_Dall_EP_EA_2(:,7)));
ylim(y)

subplot(5,1,4)
yyaxis left
plot(ADELP_Aall_Dall_EP_EA_3(:,8));
yyaxis right
plot(-log(ADELP_Aall_Dall_EP_EA_3(:,7)));
ylim(y)

subplot(5,1,5)
yyaxis left
plot(ADELP_Aall_Dall_EP_EA_4(:,8));
yyaxis right
plot(-log(ADELP_Aall_Dall_EP_EA_4(:,7)));
ylim(y)

figure
y = [-0.5, 0.5];
subplot(5,1,1)
a = ADELP_Aall_Dall_EP_EA_0(:,8);
b = ADELP_Aall_Dall_EP_EA_0(:,6);
a = (a-mean(a))/std(a);
b = (b-mean(b))/std(b);
corr = xcorr(a,b);
l = length(a);
plot((-l+1):(l-1), corr/length(a));
ylim(y)
hold on
title('xcorr trace pos error')

subplot(5,1,2)
a = ADELP_Aall_Dall_EP_EA_1(:,8);
b = ADELP_Aall_Dall_EP_EA_1(:,6);
a = (a-mean(a))/std(a);
b = (b-mean(b))/std(b);
corr = xcorr(a,b);
l = length(a);
plot((-l+1):(l-1), corr/length(a));
ylim(y)
hold on

subplot(5,1,3)
a = ADELP_Aall_Dall_EP_EA_2(:,8);
b = ADELP_Aall_Dall_EP_EA_2(:,6);
a = (a-mean(a))/std(a);
b = (b-mean(b))/std(b);
corr = xcorr(a,b);
l = length(a);
plot((-l+1):(l-1), corr/length(a));
ylim(y)
hold on

subplot(5,1,4)
a = ADELP_Aall_Dall_EP_EA_3(:,8);
b = ADELP_Aall_Dall_EP_EA_3(:,6);
a = (a-mean(a))/std(a);
b = (b-mean(b))/std(b);
corr = xcorr(a,b);
l = length(a);
plot((-l+1):(l-1), corr/length(a));
ylim(y)
hold on

subplot(5,1,5)
a = ADELP_Aall_Dall_EP_EA_4(:,8);
b = ADELP_Aall_Dall_EP_EA_4(:,6);
a = (a-mean(a))/std(a);
b = (b-mean(b))/std(b);
corr = xcorr(a,b);
l = length(a);
plot((-l+1):(l-1), corr/length(a));
ylim(y)
hold on

subplot(5,1,1)
a = ADELP_Aall_Dall_EP_EA_0(:,8);
b = log(ADELP_Aall_Dall_EP_EA_0(:,7));
a = (a-mean(a))/std(a);
b = (b-mean(b))/std(b);
corr = xcorr(a,b);
l = length(a);
plot((-l+1):(l-1), corr/length(a));
ylim(y)
legend('trace', 'determinant')
% title('xcorr determinant pos error')

subplot(5,1,2)
a = ADELP_Aall_Dall_EP_EA_1(:,8);
b = log(ADELP_Aall_Dall_EP_EA_1(:,7));
a = (a-mean(a))/std(a);
b = (b-mean(b))/std(b);
corr = xcorr(a,b);
l = length(a);
plot((-l+1):(l-1), corr/length(a));
ylim(y)

subplot(5,1,3)
a = ADELP_Aall_Dall_EP_EA_2(:,8);
b = log(ADELP_Aall_Dall_EP_EA_2(:,7));
a = (a-mean(a))/std(a);
b = (b-mean(b))/std(b);
corr = xcorr(a,b);
l = length(a);
plot((-l+1):(l-1), corr/length(a));
ylim(y)

subplot(5,1,4)
a = ADELP_Aall_Dall_EP_EA_3(:,8);
b = log(ADELP_Aall_Dall_EP_EA_3(:,7));
a = (a-mean(a))/std(a);
b = (b-mean(b))/std(b);
corr = xcorr(a,b);
l = length(a);
plot((-l+1):(l-1), corr/length(a));
ylim(y)

subplot(5,1,5)
a = ADELP_Aall_Dall_EP_EA_4(:,8);
b = log(ADELP_Aall_Dall_EP_EA_4(:,7));
a = (a-mean(a))/std(a);
b = (b-mean(b))/std(b);
corr = xcorr(a,b);
l = length(a);
plot((-l+1):(l-1), corr/length(a));
ylim(y)

%%
%load('/home/rm/Documents/master_thesis/data/vicon_leo/bag1/reconstructions/29-04-2017_08:57:48/T.mat')
T2=T;
T2(T2==0)=0.00001;
figure
imagesc(T2);

figure
plot([zeros(1,6), sum(T,2)']); %shift by two
hold on 
plot(sum(T,1));
legend('trace', 'temporal sum over one keyframe')













