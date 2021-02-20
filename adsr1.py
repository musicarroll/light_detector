import sounddevice as sd
import numpy as np
import time


sample_rate = 44100
duration = 4.0
sustain_value = 0.3   # Release amplitude between 0 and  1

x = np.linspace(0, duration * 2 * np.pi, int(duration * sample_rate))

# Dividing x legnth value into three parts:- 1/10, 1/2, 4/10.
attack_length = len(x) // 10
decay_length = len(x) // 2
sustain_legnth = len(x) - (attack_length + decay_length)

# Setting array size and length.
attack = np.linspace(0, 1, num=attack_length)
decay = np.linspace(1, sustain_value, num=decay_length)
sustain = np.ones(sustain_legnth) * sustain_value
attack_decay_sustain = np.concatenate((attack, decay, sustain))

# Creating some waveform
wave_data = np.sin(220.0 * x)

# attack_decay_sustain will control the amplitudes of the waveform,
wave_data = wave_data * attack_decay_sustain

sd.play(wave_data, sample_rate)
time.sleep(duration)
sd.stop()
