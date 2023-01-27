import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import librosa
import librosa.display

df = pd.read_csv('mitbih_train.csv', header=None)
df0 = np.array(df.iloc[100:102,:187]).flatten()
df1 = np.array(df.iloc[72805:72807,:187]).flatten()
df2 = np.array(df.iloc[75650:75652,:187]).flatten()
df3 = np.array(df.iloc[80580:80582,:187]).flatten()
df4 = np.array(df.iloc[83813:83815,:187]).flatten()

fs = 125 #Hz

#Spectrogram
n_fft1 =  fs * 0.1
hop_len1 = fs * 0.01
stft1 = librosa.stft(df4 / df4.max(), n_fft=int(n_fft1), hop_length=int(hop_len1))
D1 = librosa.amplitude_to_db(stft1, ref=np.max)
stft1 = np.abs(stft1)

librosa.display.specshow(
    D1, y_axis='linear', x_axis='time', sr=fs,
    fmax=1000  
)
#plt.xlim([0.5, 4])
#plt.ylim([0, 500])

#plt.plot(df4)
#plt.title('Non-ecotic (Normal) ECG')
#plt.title('Supraventricular-ectopic ECG')
#plt.title('Ventricular-ectopic ECG')
#plt.title('Fusion ECG')
plt.title('Unknown ECG')
plt.xlabel("Time (s)")
plt.ylabel("Frequency (Hz)")
plt.show()
