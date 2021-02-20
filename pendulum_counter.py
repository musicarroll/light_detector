# pendulum_counter.py:  reads serial data from phptoresistor and counts pendulum light breaks
import serial
import datetime
import re
import numpy as np
import time
import sounddevice as sd
import random

# Set up lists for parsing loop:
data_dump = True
num_lights = 4
light_strings = []
Thresholds = np.ones((1,num_lights))*1000 # Starting value
counters = np.zeros((1,num_lights))
read_timestamps = np.zeros((1,num_lights))
prev_timestamps = np.zeros((1,num_lights))
# Counters to keep track of number of good records read:

for i in range(num_lights):
    light_strings.append('Light' + str(i))

# Regular Expression for parsing byte string from USB:
p = re.compile(r'Light\d\=\d+')

# Calibration initialization:
nominal_halfperiod = 0.0036
first_time = []
for i in range(num_lights):
    first_time.append(True)
calibrate = True
num_cal_samples = 200
cal_array = np.zeros((num_lights,num_cal_samples))
cal_count = 0

sep ='\t'

# Read USB port for data coming from Arduino:
ser = serial.Serial(port="/dev/ttyACM0",baudrate=57600, timeout=1)

myvals = np.zeros((1,num_lights))
prev_vals = np.zeros((1,num_lights))

timestamp = datetime.datetime.now().isoformat()
fpraw = open('pcountraw-'+timestamp+'.txt',mode='wt')

# Tone generation:
tones = {'E4':329.6276,'F#4':369.9944,'A4':440.0,'B4':493.8833,'C#5':554.3653,'E5':659.2551, 'F#5':739.9888,'A5':880.00}
tlist = list(tones.keys())
random.shuffle(tlist)
tlist = tlist[:num_lights]
sample_rate = 44100
duration = 0.10
attenuation = 0.5

x = np.linspace(0, duration * 2 * np.pi, int(duration * sample_rate))
random.shuffle(tlist)
sw_data_hash = {}
for tone in tlist:
    frequency = tones[tone]
    sinewave_data = np.sin(frequency * x)

# best to attenuate it before playing, they can get very loud
    sinewave_data = sinewave_data * attenuation
    sw_data_hash[tone]=sinewave_data



while(True):
    try:
        record = {}
        bytedata = ser.readline()
        current_read_timestamp = float(time.time())
        bytestr = str(bytedata)
        fpraw.write(bytestr+'\n')
        if 'Light' in bytestr:
            matches=p.findall(bytestr)  # Use regex to find key/value pairs
            if len(matches) != num_lights:
                raise ValueError
            for i in range(num_lights):
                kv=matches[i].split('=')
#                mykey=kv[0]
                myvals[0,i] = int(kv[1])
                read_timestamps[0,i] = current_read_timestamp
        else:
            raise(ValueError)
    except ValueError:
        print("ValueError\n")
        continue
    except IndexError:
        print("IndexError\n")
        continue
    except KeyboardInterrupt:
        if data_dump:
            dd.close()
        else:
            if fp!=[]:
                for i in range(num_lights):
    #                fp[i].write('End data stream\n*****\n')
                    fp[i].close()
            fpraw.close()

        quit()
    else:
        if calibrate:         # Only executed upon startup
            for i in range(num_lights):
                cal_array[i,cal_count] = myvals[0,i]
                print('Calibration value: ',cal_count,myvals[0,i])
            cal_count += 1
            if cal_count >= num_cal_samples:
                calibrate = False
                calmax = np.max(cal_array, axis=1)
                calmin = np.min(cal_array,axis=1)
                Thresholds = calmin + 2.0
                print('Calibration Complete: Threshold=',Thresholds,'\n')
                print('Cal max= ',calmax)
                startans = input('Start? (y/n): ')

                if startans != 'y':
                    fpraw.close()
                    quit()
                else:
                    # open file to write data:
                    if data_dump:
                        dd = open('dd'+timestamp +'.csv',mode='wt')
                        dd.write('light\ttimestamp\tvalue\n')
                    else:
                        fp = []
                        metafp = []
                        for i in range(num_lights):
                            metafp.append(open('pendcount'+str(i)+'-'+ timestamp +'.txt',mode='wt'))
                            fp.append(open('pendcount'+str(i)+'-'+ timestamp + '.csv',mode='wt'))
                        for i in range(num_lights):
                            fp[i].write(sep.join(\
                                ['Time','Time Delta','Run Avg','Light Value','Delta Value','Count'])+'\n')
                            metafp[i].write('*****\nRestart: '+datetime.datetime.now().isoformat()+'\n')
                            metafp[i].write('Threshold = '+str(Thresholds[i])+'\n')
                            metafp[i].close()

        else:  # Not calibrate:
            if data_dump:
                for i in range(num_lights):
                    record = sep.join([str(i),str(read_timestamps[0,i]),\
                        str(myvals[0,i])])
                    dd.write(record+'\n')
                    print(record)

            else:
            
                for i in range(num_lights):
                    if  myvals[0,i] < Thresholds[i] and prev_vals[0,i]>=Thresholds[i]: 
                        sd.play(sw_data_hash[tlist[i]], sample_rate)
                        time.sleep(duration)
    #                    sd.stop()

                        counters[0,i] += 1
                        if first_time[i]:
                            delta_t = 0.0
                            delta_val = 0.0
                            ravg = nominal_halfperiod
                            first_time[i] = False
                        else:
                            delta_t = read_timestamps[0,i] - prev_timestamps[0,i]
                            delta_val = myvals[0,i] - prev_vals[0,i]
                            ravg = ravg + 1/counters[0,i] * (delta_t - ravg)

                        record = sep.join([str(read_timestamps[0,i]),str(delta_t),str(ravg),\
                            str(myvals[0,i]),str(delta_val),str(counters[0,i])])
    #                    print(record)
                        fp[i].write(record+'\n')
                        print('Records written to ',str(i),str(counters[0,i]))
                    prev_timestamps[0,i] = read_timestamps[0,i]
                    prev_vals[0,i] = myvals[0,i]

