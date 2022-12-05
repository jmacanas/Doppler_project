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

f,t_spec,s = sig.spectrogram(data, fs, nperseg = 2048)
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
    break

#peak mag tracker
peak_mag = np.zeros(len(t_spec))
for i in range(len(t_spec)):
    peak_mag[i] = np.max(s[:stopband_index, i]) #scans up to stopband and collects max amp for every time slice

plt.plot(t_spec,np.log10(peak_mag))
plt.show()
print(t_spec[1])
