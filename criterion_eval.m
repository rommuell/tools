%% plotting of different criteria

% OKVIS run l2 of Labortit away 2 dataset with rel. error window size of 1 (in egm.yaml)

clear all, close all, clc
load('/media/rm/9480CE0280CDEB36/experiments_1/criterion/laborit2_l2/CL.mat')

% matrix colums (criteriaList.txt):
% 7 kf_id kf_number timestamp A_all_crit A_angle_crit A_crit A_pos_crit 
% 7 D_all_crit D_crit E_all_crit E_crit L_crit okvisOut_e_abs_pos okvis_e_angle
% 4 okvis_e_angle_pitch okvis_e_angle_roll okvis_e_angle_yaw okvis_e_pos
% 5 okvis_e_pos_x okvis_e_pos_y okvis_e_pos_z turn_rate reopt1_e_abs_pos 
% 3 reopt1_e_angle reopt1_e_angle_pitch reopt1_e_angle_roll
% 4 reopt1_e_angle_yaw reopt1_e_pos reopt1_e_pos_x reopt1_e_pos_y 
% 3 reopt1_e_pos_z reopt1_optWind reoptWindows

C = CL2_1;

figure
ax1 = subplot(7,1,1);
yyaxis left
plot(C(20:end-10,6), 'linewidth', 1.5); %A
ylim([1.5e-8, 3.5e-8])
yyaxis right
plot(C(20:end-10,18), 'linewidth', 1.5); 
legend('A_{pose}', 'e_{rel\_p}', 'Location', 'northwest')
title('trace of pose')
ylim([0, 0.5])
ylabel('m')

ax2 = subplot(6,1,2);
yyaxis left
plot(C(20:end-10,9), 'linewidth', 1.5);
% ylim([-680, -553])
yyaxis right
plot(C(20:end-10,18), 'linewidth', 1.5);
legend('D_{pose}', 'e_{rel\_p}', 'Location', 'northwest')
title('determinant of one pose')
ylim([0, 0.5])
% xlabel('keyframes')
ylabel('m')

ax3 = subplot(6,1,3);
yyaxis left
plot(C(20:end-10,11), 'linewidth', 1.5);
% ylim([-680, -553])
yyaxis right
plot(C(20:end-10,18), 'linewidth', 1.5);
legend('max(e_{pose}))', 'e_{rel\_p}', 'Location', 'northwest')
title('max eigenvalue of pose')
ylim([0, 0.5])
% xlabel('keyframes')
ylabel('m')

ax4 = subplot(6,1,4);
yyaxis left
plot(C(20:end-10,4), 'linewidth', 1.5);
ylim([0, 1.1e-4])
yyaxis right
plot(C(20:end-10,18), 'linewidth', 1.5);
legend('A_{window}', 'e_{rel\_p}', 'Location', 'northwest')
title('trace of full window')
ylim([0, 0.5])
ylabel('m')

ax5 = subplot(6,1,5);
yyaxis left
plot(C(20:end-10,8), 'linewidth', 1.5);
ylim([-0.1e-252, 1.6e-252])
yyaxis right
plot(C(20:end-10,18), 'linewidth', 1.5);
legend('D_{window}', 'e_{rel\_p}', 'Location', 'northwest')
title('determinant of full window')
ylim([0, 0.5])
ylabel('m')

ax6 = subplot(6,1,6);
yyaxis left
plot(C(20:end-10,10), 'linewidth', 1.5);
% ylim([-680, -553])
yyaxis right
plot(C(20:end-10,18), 'linewidth', 1.5);
legend('max(eig_{window})', 'e_{rel\_p}', 'Location', 'northwest')
title('maximal eigenvalue full window')
ylim([0, 0.5])
xlabel('keyframes')
ylabel('m')



% ax5 = subplot(7,1,5);
% yyaxis left
% c = real(log(C(20:end-10,8)));
% plot(c, 'linewidth', 1.5);
% ylim([-680, -553])
% yyaxis right
% plot(C(20:end-10,18), 'linewidth', 1.5);
% legend('log(D_{window})', 'e_{rel\_p}', 'Location', 'northwest')
% title('logarithm of determinant of full window')
% ylim([0, 0.5])
% xlabel('keyframes')
% ylabel('m')

linkaxes([ax1,ax2,ax3, ax4, ax5, ax6],'x')
xlim([2,86])

%%
figure
yyaxis left
hold on
plot(C(20:end-10,6)); %A
plot(C(20:end-10,4)); %A_all
area(C(20:end-10,8)*1e250); %D_all
ylim([0, 14e-5])

% c = real(log(C(20:end-10,8)));
% plot(c); %log(det)

yyaxis right
plot(C(20:end-10,18));
legend('A_{pose}', 'A_{window}', 'D_{window}', 'relative position error', 'Location', 'northwest')
title('Relative position error vs. criteria')


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
title('xcorr A_{all} -rel error')

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
c(c==-Inf) = -630;
a = c; % log det
b = C(20:end-10,18); % pos error
a = (a-mean(a))/std(a);
b = (b-mean(b))/std(b);
corr = xcorr(a,b);
l = length(a);
plot((-l+1):(l-1), corr/length(a));
ylim(y)
hold on
title('xcorr log(det) -rel error')

