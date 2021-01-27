# pendulum_counter.py:  reads serial data from phptoresistor and counts pendulum light breaks
import serial
import datetime
import re
import numpy as np
import time

# Set up lists for parsing loop:
num_lights = 2
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
first_time = True
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

while(True):
    try:
        record = {}
        bytedata = ser.readline()
        current_read_timestamp = float(time.time())
        bytestr = str(bytedata)
        fpraw.write(bytestr)
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
            
            for i in range(num_lights):
                if  myvals[0,i] < Thresholds[i] and prev_vals[0,i]>=Thresholds[i]: 
                    counters[0,i] += 1
                    if first_time:
                        delta_t = 0.0
                        delta_val = 0.0
                        ravg = nominal_halfperiod
                        first_time = False
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

