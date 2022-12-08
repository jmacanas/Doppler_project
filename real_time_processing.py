import pyaudio
import wave
from array import array
from struct import pack
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.fft import fft, fftfreq
from scipy.signal.windows import tukey

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5

chunks_per_second = int(RATE/CHUNK)
# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(2,1)
fft_bins = list(fftfreq(CHUNK, d = 1/RATE))
# ax.set_ylim((-5,5))
xs = np.linspace(0,5,chunks_per_second*5)
ys = np.zeros(len(xs))

print("len of xs:", len(xs))
stopband = 500 #Hz
for i in range(len(fft_bins)):
    if fft_bins[i] < stopband:
        continue
    stopband_index = i
    print(stopband_index)
    break

window = tukey(CHUNK, alpha = 0.25, sym = False)
p = pyaudio.PyAudio()
# open stream object as input
stream = p.open(format = FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = True,
                frames_per_buffer = CHUNK)
print("*recording")

# This function is called periodically from FuncAnimation
def animate(i):
    global ys
    global window
    
    data = list(array("h",stream.read(CHUNK)))
    window_data = data * window
    # runs fft on chunk
    log_fft = np.log10(abs(fft(window_data))+0.000001)

    # noise floor measurement
    high_f_bands = np.log10(log_fft[-stopband_index:])
    noise_floor = np.mean(high_f_bands)

    max_band = np.max(log_fft[:stopband_index])
    ys = np.append(ys,max_band)
    ys = ys[1:]

    n_frames = 20
    averaging_frames = ys[-(n_frames+1):-1]
    averaged_value = np.mean(averaging_frames)
    ys1= averaging_frames[i] - averaged_value
   


    # Draw x and y lists
    ax.clear()
    # ax.set_ylim((0,5))
    ax[0].plot(xs, ys) # max mag plot
    ax[1].plot(xs, ys1) # difference to moving average
    

ani = animation.FuncAnimation(fig, animate,interval=0)
plt.show()



# peak mag tracker
peak_mag = np.zeros(len(t_spec))
for i in range(len(t_spec)):
    peak_mag[i] = np.log10(np.max(s[:stopband_index, i]))


