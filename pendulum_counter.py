# pendulum_counter.py:  reads serial data from phptoresistor and counts pendulum light breaks
import serial
import datetime
import re
ser = serial.Serial(port="/dev/ttyACM0",timeout=1)
counter0 = 0
counter1 = 0
Threshold0 = 0.25  # Using percentage light drop off
Threshold1 = 0.25
first_time = True
# open file to write data:
fp=open('pendcount.csv',mode='at')
fp.write('*****\nRestart: '+datetime.datetime.now().isoformat()+\
            '\nThreshold0='+str(Threshold0)+'\tThreshold1='+str(Threshold1)+'\n\n')
while(True):
    try:
        record = {}
        bytedata = ser.readline()
        print('raw: ',bytedata)
        bytestr = str(bytedata)
        p = re.compile(r'Light\d\=\d+')
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
        if (prev_v0-v0)/prev_v0< -Threshold0:
            counter0 += 1
        if (prev_v1-v1)/prev_v1< -Threshold1:
            counter1 += 1
        sep = '\t'
        record = datetime.datetime.now().isoformat() + '\t' + sep.join([str(v0),str(counter0),\
                    str(v1), str(counter1)])
        print(record)
        fp.write(record+'\n')
        prev_v0 = v0
        prev_v1 = v1

