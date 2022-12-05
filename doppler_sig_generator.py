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

gain = 1000 #arbituary amount of power gain for radar
target_rcs = 10 #arbituary rcs value for target

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
    phase = 2 * np.pi * integrate.cumtrapz(f_doppler, t, initial= 0)
    doppler_IF = doppler_mag * np.sin(phase)
    return doppler_IF


# sig 1: target starting near and then moving away at 1 m/s
sig1_pos_t = np.zeros(len(t))
sig1_pos_t0 = 0.1 #m away from radar
sig1_v = 1 #m/s moving away from sensor

for i in range(len(sig1_pos_t)):
    sig1_pos_t[i] = sig1_pos_t0 + t[i] * sig1_v

sig1_v_t = calc_velocity(t, sig1_pos_t)
sig1_IF = gen_doppler(t, sig1_pos_t, sig1_v_t)

wav.write("sig1_target_moving_away.wav", SAMPLING_RATE, sig1_IF.astype(np.int16))


# sig 2: target starting far then moving closer to the sensor
sig2_pos_t = np.zeros(len(t))
sig2_pos_t0 = 6 #m away from radar
sig2_v = -1 #m/s moving away from sensor

for i in range(len(sig2_pos_t)):
    sig2_pos_t[i] = sig2_pos_t0 + t[i] * sig2_v

sig2_v_t = calc_velocity(t, sig2_pos_t)
sig2_IF = gen_doppler(t, sig2_pos_t, sig2_v_t)
wav.write("sig2_target_moving_closer.wav", SAMPLING_RATE, sig2_IF.astype(np.int16))