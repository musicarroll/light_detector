import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
import time
plt.style.use('dark_background')


# a skeleton function to stuff full of meaty sawtooth values.
# play with phase at your leisure, phase arg is optional.

def a_wave(x, freq, phase=0):
    return np.sin((freq * x) + phase) * 0.2

# build up ya reverse sawtooth


def make_wave_2(x):
    wave0 = a_wave(x, 220.0)
    wave1 = a_wave(x, 440.0)/2
    wave2 = a_wave(x, 660.0)/3
    wave3 = a_wave(x, 880.0)/4
    wave4 = a_wave(x, 1100.0)/5
    wave5 = a_wave(x, 1320.0)/6
    wave6 = a_wave(x, 1540.0)/7
    wave7 = a_wave(x, 1760.0)/8

    return wave0 + wave1 + wave2 + wave3 + wave4 + wave5 + wave6 + wave7


# see what it looks like
def plotting():
    y = make_wave_2(x)
    y_plot = y[: 500]

    fig, ax = plt.subplots()
    ax.plot(y_plot)

    plt.xlabel('Sample Number')
    plt.title('Reverse Sawtooth')
    plt.show()


# hear what it sounds like
def hearing():
    waveform = make_wave_2(x)
    atten_waveform = waveform * 0.8
    sd.play(atten_waveform, sample_rate)
    time.sleep(duration)
    sd.stop()


sample_rate = 44100
duration = 3.0
x = np.linspace(0, duration  * 2 * np.pi, int(duration * sample_rate))
hearing()
plotting()
    
