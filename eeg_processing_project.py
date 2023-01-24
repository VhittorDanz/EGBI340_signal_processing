import os
import numpy as np
import matplotlib.pyplot as plt
import mne
from scipy import signal
from matplotlib import mlab
from matplotlib.widgets import Slider, Button
import matplotlib.gridspec as gridspec

def selection_EEG(channel, time_range):
    start_stop_seconds = np.array(time_range)
    start_sample, stop_sample = (start_stop_seconds * sampling_freq).astype(int)
    channel_names = channel  
    eeg_selection = eeg_chan[channel_names, start_sample:stop_sample]
    return eeg_selection

def plotTimeDomain(eeg):
    x = eeg[1]
    y = eeg[0].T
    axs[2].plot(x, y)
    axs[2].margins(x=0)
    axs[2].set_ylim([-5e-5,20e-5])
    axs[2].set_title('EEG in Time Domain')
    axs[2].set_xlabel('Time (s)')
    axs[2].set_ylabel('Amplitude')

def plotFrequencyDomain(eeg):
    w = np.hamming(len(eeg[0][0]))
    X = np.fft.fft(eeg[0][0]*w)
    N = len(X)

    axs[1].plot(np.linspace(0, sampling_freq * (N - 1)/N, N), np.abs(X))
    axs[1].set_xlim([0, 20])
    axs[1].set_ylim([0, 0.1])
    axs[1].set_title('EEG in Frequency Domain')
    axs[1].set_xlabel('Frequency (Hz)')
    axs[1].set_ylabel('Amplitude')

def plotSpec(eeg):
    Pxx, freqs, bins, im = axs[0].specgram(eeg[0][0], 
                            Fs=sampling_freq, NFFT=140, cmap='jet')
    axs[0].set_ylim([0, 10])
    axs[0].set_title('EEG in Spectrogram')
    axs[0].set_xlabel('Time (s)')
    axs[0].set_ylabel('Frequency (Hz)')
    return im

#Create figure
fig = plt.figure()
gs = fig.add_gridspec(3, 4, width_ratios=[5, 5, 5, 0.2], wspace=0.1, hspace=0.75)
ax1 = fig.add_subplot(gs[0, :3])
ax2 = fig.add_subplot(gs[1, :3])
ax3 = fig.add_subplot(gs[2, :3])
ax4 = fig.add_subplot(gs[0, 3])
axs = [ax1, ax2, ax3, ax4]
#fig.tight_layout()
fig.subplots_adjust(bottom=0.18)

#Import dataset
sample_data_folder = mne.datasets.sample.data_path()
sample_data_raw_file = os.path.join(sample_data_folder, 'MEG', 'sample',
                                    'sample_audvis_raw.fif')
raw = mne.io.read_raw_fif(sample_data_raw_file, preload=True, verbose=False)
raw.crop(tmax=60).load_data() #crop range of time

#Declare variables
n_time_samps = raw.n_times
time_secs = raw.times
ch_names = raw.ch_names
sampling_freq = raw.info['sfreq']
n_chan = len(ch_names)

#Access EEG from data
eeg = raw.copy().pick_types(meg=False, eeg=True, eog=False) #select type of signal
ssp_projectors = eeg.info['projs']
eeg.del_proj()
eeg.apply_hilbert()
eeg_chan = eeg.copy().pick_channels(['EEG 001', 'EEG 002', 'EEG 003']) #select channels
channel_renaming_dict = {name: name.replace(' ', '_') for name in eeg_chan.ch_names}
eeg_chan.rename_channels(channel_renaming_dict)

#Access time range and channel 
channel_names = ['EEG_003']   
eeg_selection = selection_EEG(channel_names, [0, 3])

#events = mne.find_events(raw, stim_channel='STI 014')
#eeg_chan.plot(events=events, start=0, duration=3, color='black',
#         event_color={1: 'r', 2: 'g', 3: 'b', 4: 'm', 5: 'y', 32: 'k'})

#Plot time series
plotTimeDomain(eeg_selection)

#Fourier transform
plotFrequencyDomain(eeg_selection)

#Spectrogram
im = plotSpec(eeg_selection)
cbar = plt.colorbar(im, cax=axs[3])
cbar.set_label('Amplitude (dB)')

#Slider
axfreq = fig.add_axes([0.15, 0.075, 0.7, 0.03])
time_slider = Slider(
    ax=axfreq,
    label='Time(s)',
    valmin=0,
    valmax=57,
    valinit=0,
)

def update(val):
    axs[0].clear()
    axs[1].clear()
    axs[2].clear()
    eeg_selection = selection_EEG(channel_names, 
                    [time_slider.val, time_slider.val+3])
    plotTimeDomain(eeg_selection)
    plotFrequencyDomain(eeg_selection)
    plotSpec(eeg_selection)
    fig.canvas.draw_idle()
time_slider.on_changed(update)

plt.show()