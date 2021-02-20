# sdtest2.py
import numpy as np
import sounddevice as sd
import random
import time

tones = {'E4':329.6276,'F#4':369.9944,'A4':440.0,'B4':493.8833,'C#5':554.3653,'E5':659.2551, 'F#5':739.9888,'A5':880.00}

tlist = list(tones.keys())
sample_rate = 44100
duration = 0.5
attenuation = 0.3

x = np.linspace(0, duration * 2 * np.pi, int(duration * sample_rate))
random.shuffle(tlist)
sw_data_hash = {}
dlen = len(x)
print('dlen=',dlen)

sinewave_data = np.zeros(dlen)
alen = int(dlen*0.0)
attack_mask = np.ones(dlen)
for i in range(alen):
    attack_mask[i] = float(i)/40
tone = 'E4'
frequency = tones[tone]
sinewave_data += np.sin(frequency * x)
lasttone = tone
# best to attenuate it before playing, they can get very loud
sinewave_data = sinewave_data * attenuation

while True:
    try:
        sinewave_data *= attack_mask
        sd.play(sinewave_data,sample_rate)
        time.sleep(duration)
        frequency = tones[lasttone]
        sinewave_data = np.zeros(len(x))
        tone1 = random.choice(tlist)
        tone2 = random.choice(tlist)
        frequency1 = tones[tone1]
        frequency2 = tones[tone2]
        sinewave_data += np.sin(frequency1 * x)
        sinewave_data += np.sin(frequency2 * x)
        sinewave_data = sinewave_data * attenuation
        sd.sleep(15) # pause 15 ms
    except KeyboardInterrupt:
        sd.stop()
        quit()

