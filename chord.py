import numpy as np
import sounddevice as sd
import time


def sine(f):
    y = np.sin(f * x) * 0.2
    return y


def triangle(f1, f2):
    y = 2 / np.pi * np.arcsin(np.sin(f1 * x + ramp_1 * sine(f2))) * 0.2
    return y


def triangle2(f):
    y = 2 / np.pi * np.arcsin(np.sin(f * x)) * 0.2
    return y


def triangle_mod(f):
    y = 2 / np.pi * np.arcsin(np.sin(A4 * x + ramp_0 * np.sin(f * x))) * 0.2
    return y


def lfo():
    y = np.sin(lfo_f * x)
    y = (y * lf0_amount / 2 + (1 - lf0_amount / 2))
    return y


sample_rate = 44100
duration = 20.0
freq1 = 400.0
freq2 = 300.0
A1 = 55.0
A4 = 440.0
Bb5 = 932.3275
Bb6 = 1864.655
Eb5 = 622.2540
E2 = 82.40689
lfo_f = 10.0
lf0_amount = 0.1

x = np.linspace(0, duration * 2 * np.pi, int(duration * sample_rate))

ramp_0 = np.logspace(0, 1, int(duration * sample_rate)) * 4
ramp_1 = np.logspace(1, 0, int(duration * sample_rate)) * 5

wave_data = ((triangle_mod(freq1) + sine(freq2) + triangle(Bb6, Eb5)
                + triangle2(Bb5) + sine(E2) + sine(A1)) * lfo()) * 0.2

sd.play(wave_data, sample_rate)
time.sleep(duration)
sd.stop()
