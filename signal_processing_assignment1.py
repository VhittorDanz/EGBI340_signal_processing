import numpy as np
import IPython.display as ipd
from scipy.io import wavfile
import librosa
import librosa.display
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, filtfilt
import soundfile as sf

def butter_lowpass_filter(data, low_cut, fs, order):
    b, a = butter(order, low_cut, fs=fs, btype='low', analog=False)
    y = lfilter(b, a, data)
    return y

plt.rcParams["figure.figsize"] = [12, 8]
plt.rcParams.update({"font.size": 16})

#Import recordings
fs1, x1 = wavfile.read("Apple.wav")
fs2, x2 = wavfile.read("Banana.wav")

# Filter requirements.
order = 10
low_cut = 200

#Filter data
#x1_filter = butter_lowpass_filter(x1, cutoff, fs1, order)
x1_filter = butter_lowpass_filter(x1, low_cut, fs1, order)
x2_filter = butter_lowpass_filter(x2, low_cut, fs2, order)

#Generate fourier transform from a recording 
w1 = np.hamming(len(x1_filter))
X1 = np.fft.fft(x1_filter * w1)
N1 = len(X1)
w2 = np.hamming(len(x2_filter))
X2 = np.fft.fft(x2_filter * w2)
N2 = len(X2)

#Create spectrogram
n_fft1 =  fs1 * 0.1
hop_len1 = fs1 * 0.01
stft1 = librosa.stft(x1_filter / x1_filter.max(), n_fft=int(n_fft1), hop_length=int(hop_len1))
D1 = librosa.amplitude_to_db(stft1, ref=np.max)
stft1 = np.abs(stft1)
n_fft2 =  fs2 * 0.1
hop_len2 = fs2 * 0.01
stft2 = librosa.stft(x2_filter / x2_filter.max(), n_fft=int(n_fft2), hop_length=int(hop_len2))
D2 = librosa.amplitude_to_db(stft2, ref=np.max)
stft2 = np.abs(stft2)
#plot graph and spectrogram

librosa.display.specshow(
    D2, y_axis='linear', x_axis='time', sr=fs2,
    fmax=1000  
)
plt.xlim([0.5, 4])
plt.ylim([0, 1000])

'''
plt.plot(np.linspace(0, fs1 * (N1 - 1)/N1, N1), np.abs(X1))
plt.xlabel("Frequency (Hz)")
plt.ylabel("Amplitude")
plt.xlim([0, 1000])
'''
#plt.plot(np.linspace(0, (len(x2_filter) / fs2), len(x2_filter)), x2_filter)
#plt.plot(np.linspace(0, (len(x2) / fs2), len(x2)), x2)
plt.xlabel("Time (s)")
plt.ylabel("Frequency (Hz)")
plt.title("Apple")
plt.show()

sf.write('Apples.filtered.wav', x1_filter, 48000, 'PCM_24')
sf.write('Banana.filtered.wav', x2_filter, 48000, 'PCM_24')

