load("noisyecg.mat");

%Filter 50 Hz
b_50Hz = [1, -2*cos(2*pi*50/500), 1];
a_50Hz = 1;
y1_50Hz = filter(b_50Hz, a_50Hz, ecg1);
y2_50Hz = filter(b_50Hz, a_50Hz, ecg2);
y3_50Hz = filter(b_50Hz, a_50Hz, ecg3);
%Filter 150 Hz
b_150Hz = [1, -2*cos(2*pi*150/500), 1];
a_150Hz = 1;
y1_150Hz = filter(b_150Hz, a_150Hz, y1_50Hz);
y2_150Hz = filter(b_150Hz, a_150Hz, y2_50Hz);
y3_150Hz = filter(b_150Hz, a_150Hz, y3_50Hz);
%Low pass and High pass 
h_low = firpm(50, [0, 0.20, 0.30, 1], [1, 1, 0, 0]);
h_high = firpm(50, [0, 0.004, 0.04, 1], [0, 0, 1, 1]);
y1_low = filter(h_low, 1, y1_150Hz);
y2_low = filter(h_low, 1, y2_150Hz);
y3_low = filter(h_low, 1, y3_150Hz);
y1_high = filter(h_high, 1, y1_low);
y2_high = filter(h_high, 1, y2_low);
y3_high = filter(h_high, 1, y3_low);
%Plot
subplot(3, 1, 1)
plot(y1_high)
title('ECG1')
xlim([100,1500])
subplot(3, 1, 2)
plot(y2_high)
title('ECG2')
xlim([100,1500])
subplot(3, 1, 3)
plot(y3_high)
title('ECG3')
xlim([100,2000])

