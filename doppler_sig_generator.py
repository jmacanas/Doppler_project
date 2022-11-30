import numpy as np
import scipy.io.wavfile as wav
import scipy.signal as sig
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import struct
from scipy import integrate

SAMPLING_RATE = 44100
DURATION = 5 #sec

c = 3e8 #m/s

f_radar = 10.5e9 #Hz

bits = 16
t = np.linspace(0, DURATION, SAMPLING_RATE*DURATION)

max_int16 = 2**15 -1

gain = 100 #arbituary amount of power gain for radar
target_rcs = 1 #arbituary rcs value for target

def calc_velocity(t, position_t):
    # position_t = position of target with respect to time
    # t = array of time points
    v = np.zeros(len(position_t))
    del_t = t[1] - t[0]
    for i in range(len(position_t)):
        if i == 0:
            continue # assumes target is not moving at t=0
        v[i] = (position_t[i] - position_t[i-1])/del_t
    
    return v

def gen_doppler(t, position_t, velocity_t):
    # t = array of time points
    # position_t = position of target with respect to time
    # velocity_t = velocity of target with respect to time
    f_doppler = 2 * velocity_t * f_radar/c
    doppler_mag = np.sqrt(target_rcs * gain)/(position_t**2)
    phase = 2 * np.pi * integrate.cumtrapz(f_doppler, t)
    doppler_IF = doppler_mag * np.sin(phase)
    return doppler_IF

