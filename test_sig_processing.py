import wave
import scipy.signal as sig
import sys

wf = wave.open(sys.argv[1], 'rb')
data = wf.readframs(wf.getnframes())
print(wf.getparams())