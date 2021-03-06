import numpy as np
import sounddevice as sd
import random
import time

tones = {'E4':329.6276,'F#4':369.9944,'A4':440.0,'B4':493.8833,'C#5':554.3653,'E5':659.2551, 'F#5':739.9888,'A5':880.00}
#tones = {'E4':329.6276,'A4':440.0,'C#5':554.3653,'E5':659.2551}
tlist = list(tones.keys())
sample_rate = 44100
duration = 0.5
attenuation = 0.3

x = np.linspace(0, duration * 2 * np.pi, int(duration * sample_rate))
random.shuffle(tlist)
sw_data_hash = {}
sinewave_data = np.zeros(len(x))
for tone in tlist:
    frequency = tones[tone]
    sinewave_data += np.sin(frequency * x)
# best to attenuate it before playing, they can get very loud
    sinewave_data = sinewave_data * attenuation
    sw_data_hash[tone]=sinewave_data


for tone in tlist:
    sinewave_data = sw_data_hash[tone]
    sd.play(sw_data_hash[tone], sample_rate)
    time.sleep(duration)

random.shuffle(tlist)

for tone in tlist:
    sinewave_data = sw_data_hash[tone]
    sd.play(sw_data_hash[tone], sample_rate)
    time.sleep(duration)


#        sd.stop()
#        time.sleep(0.01)

x = np.linspace(0, duration * 4 * np.pi, int(2*duration * sample_rate))

sinewave_data1 = np.sin(tones['E5'] * x[:int(len(x)/2-1)])
sinewave_data2 = np.sin(tones['A4'] * x[int(len(x)/2):])
sinewave_data = np.hstack((sinewave_data1,sinewave_data2))

# best to attenuate it before playing, they can get very loud
sinewave_data = sinewave_data * attenuation


sd.play(sinewave_data, sample_rate)
time.sleep(2.0)
sd.stop()


