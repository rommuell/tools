% kf_id kf_number timestamp A_all_crit A_angle_crit A_crit A_pos_crit 
% D_all_crit D_crit E_crit L_crit P_crit okvisOut_e_abs_pos okvis_e_angle 
% okvis_e_angle_pitch okvis_e_angle_roll okvis_e_angle_yaw okvis_e_pos 
% okvis_e_pos_x okvis_e_pos_y okvis_e_pos_z turn_rate reopt1_e_abs_pos 
% reopt1_e_angle reopt1_e_angle_pitch reopt1_e_angle_roll 
% reopt1_e_angle_yaw reopt1_e_pos reopt1_e_pos_x reopt1_e_pos_y

clear all, close all, clc
load('/media/rm/9480CE0280CDEB36/experiments_1/criterion/laborit2_l2/CL.mat')
load('/media/rm/9480CE0280CDEB36/experiments_1/criterion/HG_13/CL.mat')

C = CL2_1;
C = CHG13_1;

% figure
% yyaxis left
% plot(CL2_5(20:end-10,4));
% yyaxis right
% plot(CL2_5(:,18));
% legend('A_all', 'e_pos_5')

figure
yyaxis left
plot(C(20:end-10,6)); %A
yyaxis right
plot(C(20:end-10,18)); 
legend('A', 'e_pos_1')
title('against single trace')

figure
yyaxis left
plot(C(20:end-10,4));
yyaxis right
plot(C(20:end-10,18));
legend('A_all', 'e_pos_1')
title('against full trace')

figure
yyaxis left
c = real(log(C(20:end-10,8)));
plot(c);
yyaxis right
plot(C(20:end-10,18));
legend('D_all', 'e_pos_1')
title('against log(det)')

figure
y = [-1, 1];
subplot(5,1,1)
a = C(20:end-10,4); % A_all
b = C(20:end-10,18);
a = (a-mean(a))/std(a);
b = (b-mean(b))/std(b);
corr = xcorr(a,b);
l = length(a);
plot((-l+1):(l-1), corr/length(a));
ylim(y)
hold on
title('xcorr A_all -rel error')

subplot(5,1,2)
a = C(20:end-10,6); % A
b = C(20:end-10,18); % pos error
a = (a-mean(a))/std(a);
b = (b-mean(b))/std(b);
corr = xcorr(a,b);
l = length(a);
plot((-l+1):(l-1), corr/length(a));
ylim(y)
hold on
title('xcorr A -rel error')

subplot(5,1,3)
c(c==-Inf) = 0
a = c; % A
b = C(20:end-10,18); % pos error
a = (a-mean(a))/std(a);
b = (b-mean(b))/std(b);
corr = xcorr(a,b);
l = length(a);
plot((-l+1):(l-1), corr/length(a));
ylim(y)
hold on
title('xcorr A -rel error')