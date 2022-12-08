import wave
import scipy.signal as sig
import sys
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
import matplotlib.colors as colors
import numpy as np

wf = wave.open(sys.argv[1], 'rb')
rate, data = wav.read(sys.argv[1])
fs = wf.getframerate()

f,t_spec,s = sig.spectrogram(data, fs, nperseg = 1024, scaling = "spectrum")
plt.pcolormesh(t_spec,f,s, norm=colors.LogNorm(vmin=s.min(), vmax = s.max()), shading='auto')
plt.title(" Spectrogram")
plt.ylabel('Frequency (Hz)')
plt.xlabel("Time (s)")
plt.show()

# walking speed should be keep in frequencies below 500Hz
stopband = 500 #Hz
for i in range(len(f)):
    if f[i] < stopband:
        continue
    stopband_index = i
    print(stopband_index)
    break

# noise floor measurement
high_f_bands = np.log10(s[-stopband_index:,:])
noise_floor = np.mean(high_f_bands)

# peak mag tracker
peak_mag = np.zeros(len(t_spec))
for i in range(len(t_spec)):
    peak_mag[i] = np.log10(np.max(s[:stopband_index, i]))


n_frames = 20
padding_frames = np.ones(n_frames) * noise_floor
analyzing_frames = np.append(padding_frames, peak_mag)
minus_avg_s = np.zeros(len(peak_mag))
for i in range(len(analyzing_frames)):
    averaged_window = np.mean(analyzing_frames[ i - n_frames:i])
    if i >= n_frames:
        minus_avg_s[i-n_frames] = analyzing_frames[i] - averaged_window
   



    # freq_bin_mags = []
    # for j in range(stopband_index):

    #     if minus_avg_s[j, i] < 0:
    #     peak_mag_log_minus_s[i] = np.min(minus_avg_s[:stopband_index, i])
    # else:
    #     peak_mag_log_minus_s[i] = np.max(minus_avg_s[:stopband_index, i])
# trendline
# chunks_per_sec = 43
# window = np.ones(chunks_per_sec) * noise_floor +0.1
# poly_coeff = np.zeros((2,len(peak_mag)))
# trend_detection_time = np.linspace(-0.5, 0.5, chunks_per_sec, endpoint = True)
# for i in range(len(peak_mag)):
#     window = np.append(window, peak_mag[i]+0.000001)
#     window = window[1:]
    
#     coeff = np.polyfit(trend_detection_time, np.log10(window), deg = 1)
#     poly_coeff[0][i] = coeff[0]
#     poly_coeff[1][i] = coeff[1]


fig, ax = plt.subplots(3,1)
ax[0].plot(t_spec, peak_mag)
ax[2].plot(t_spec, minus_avg_s)
ax[2].set_ylim(-1,1)
plt.show()