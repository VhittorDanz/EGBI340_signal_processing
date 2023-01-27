load("noisyecg.mat");
h_low = firpm(50, [0, 0.004, 0.04, 1], [0, 0, 1, 1]);
y1_low = filter(h_low, 1, ecg1);
y2_low = filter(h_low, 1, ecg2);
y3_low = filter(h_low, 1, ecg3);
pecg1 = pwelch(ecg1);
pecg2 = pwelch(ecg2);
pecg3 = pwelch(ecg3);
py1_low = pwelch(y1_low);
py2_low = pwelch(y2_low);
py3_low = pwelch(y3_low);
subplot(3,2,1);
semilogy(pecg1)
subplot(3,2,3);
semilogy(pecg2)
subplot(3,2,5);
semilogy(pecg3)
subplot(3,2,2);
semilogy(py1_low)
subplot(3,2,4);
semilogy(py2_low)
subplot(3,2,6);
semilogy(py3_low)
