# pendulum_counter.py:  reads serial data from phptoresistor and counts pendulum light breaks
import serial
import datetime
import re
import numpy as np


# Regular Expression for parsing byte string from USB:
p = re.compile(r'Light\d\=\d+')

# Calibration initialization:
Threshold0 = 190  # Nominal values;  exact values determined by calibration
Threshold1 = 190
first_time = True
calibrate = True
num_cal_samples = 500
cal_array = np.zeros((1,num_cal_samples))
cal_count = 0

# Read USB port for data coming from Arduino:
ser = serial.Serial(port="/dev/ttyACM0",baudrate=38400, timeout=1)

# Counters to keep track of number of good records read:
counter0 = 0
counter1 = 0

while(True):
    try:
        record = {}
        bytedata = ser.readline()
        print('raw: ',bytedata)
        bytestr = str(bytedata)
        if 'Light0' in bytestr and 'Light1' in bytestr:
            m=p.findall(bytestr)
            kv=m[0].split('=')
            k0=kv[0]
            v0=int(kv[1])
            kv=m[1].split('=')
            k1=kv[0]
            v1=int(kv[1])
            if first_time:
                first_time = False
                prev_v0 = v0
                prev_v1 = v1
        else:
            raise(ValueError)

    except ValueError:
        print("ValueError\n")
        continue
    except IndexError:
        print("IndexError\n")
        continue
    except KeyboardInterrupt:
        fp.write('End data stream\n*****\n')
        fp.close()
        quit()
    else:
        if calibrate:         # Only executed upon startup
            cal_array[0,cal_count] = v0
            cal_count += 1
            if cal_count == num_cal_samples:
                calibrate = False
                calmax = np.max(cal_array)
                calmin = np.min(cal_array)
                Threshold0 = calmin + 2.0
                print('Calibration Complete: Threshold=',Threshold0,'\n')
                print('Cal max= ',calmax)
                startans = input('Start? (y/n)')
                if startans != 'y':
                    quit()
                else:
                    # open file to write data:
                    fp=open('pendcount.csv',mode='at')
                    fp.write('*****\nRestart: '+datetime.datetime.now().isoformat()+\
                                '\nThreshold0='+str(Threshold0)+'\tThreshold1='+str(Threshold1)+'\n\n')

        else:
            if  v0 < Threshold0 and prev_v0>=Threshold0:
                counter0 += 1
                prev_v0 = v0
            if  v1 < Threshold1:
                counter1 += 1
            sep = '\t'
            record = datetime.datetime.now().isoformat() + '\t' + sep.join([str(v0),str(counter0),\
                        str(v1), str(counter1)])
            print(record)
            fp.write(record+'\n')
            prev_v0 = v0
            prev_v1 = v1

