import sys
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# print('********')
# print(sys.argv)
# print('********')

filename = sys.argv[1]
#filename = '/home/mcarroll/Documents/python/light_detector/test.csv'
df = pd.read_csv(filename, delimiter='\t')
df['timestamp'] = df['timestamp']-df['timestamp'][0]


if sys.argv[2]!='all':
        light_num = int(sys.argv[2])
        light_list = [light_num]
else:
        light_list = [0,1,2,3]

plt.style.use('seaborn')
plt.figure(1)

for light_num in light_list:

        filvar = (df['light']==light_num)
        myrows = (df[filvar].head(5000))


        ax0 = plt.subplot(4,2,2*light_num+1)
        plt.plot(myrows['timestamp'],myrows['value'])
        if light_num < len(light_list)-1 and len(light_list)>1:
                plt.setp(ax0.get_xticklabels(), visible=False)
        if light_num==0:
                plt.title('Light Values')
 
        mymean = myrows['value'].mean()
        mystd =  myrows['value'].std()
        # print(mymean)
        # print(mystd)
        lowfilter = (myrows['value']<mymean-3.0*mystd)
        lowpoints = myrows[lowfilter]

#       print('\n')
        minfilter = [True]
        i=0
        #print(lowpoints)
        minfilter = (lowpoints['value']==lowpoints['value'])

        for rowidx,row in lowpoints.iterrows():
#                print(rowidx,row['value'])
                if i>0:
                        if abs(rowidx-last_rowidx)==4:
                                if row['value']<last_row_value:
                                        minfilter[last_rowidx] = False
                                        minfilter[rowidx] = True
                                else:
                                        minfilter[rowidx] = False
                                        minfilter[last_rowidx] = True
                        else:
                                minfilter[rowidx] = True
                else:
                        minfilter[rowidx] = False
                i += 1
                last_rowidx = rowidx
                last_row_value = row['value']
        minfilt = minfilter
        # print(minfilt)
        local_minima = lowpoints[minfilt]
        # print('\n Local Minima:\n')
        # print(local_minima)
        # print(local_minima.size)

        lowpoint = local_minima['value'].min()
        lowpoint_index = local_minima['value'].idxmin()
        print('***********************************\nLight: ',light_num,\
                ' Min Value: ',lowpoint,' at index: ',lowpoint_index, ' at time: ',\
                df.iloc[lowpoint_index]['timestamp'],' num stds: ', (mymean-lowpoint)/mystd)

        times = np.zeros((local_minima.index.size,1))
        times = local_minima['timestamp']
        delta_times = np.diff(times)
        print('Mean Delta Time: ',delta_times.mean(),' Stdev: ',delta_times.std())
        print('Delta Times between Local Minima: \n ')
        print(delta_times)
        # print(delta_times)
        # print(delta_times.mean())

        ax0 = plt.subplot(4,2,2*light_num+2)
        # if light_num < len(light_list)-1 and len(light_list)>1:
        #         plt.setp(ax0.get_xticklabels(), visible=False)
        if light_num==0:
                plt.title('Local Minima: Delta Times for Light Crossings')
        plt.plot(times[0:local_minima.index.size-1],delta_times)


plt.show()


plt.style.use('seaborn')
plt.figure(2)

for light_num in light_list:
        filvar = (df['light']==light_num)
        myrows = (df[filvar].head(5000))
        alltimes = np.zeros((myrows.index.size,1))
        alltimes = myrows['timestamp']
        allvalues = np.zeros((myrows.index.size,1))
        allvalues = myrows['value']
        all_delta_times = np.diff(alltimes[100:])
        print(all_delta_times.shape)
        print('Mean Time Delta for Light ',light_num,': ',np.mean(all_delta_times))
        print('Stdev Time Delta for Light ',light_num,': ',np.std(all_delta_times))

        ax0 = plt.subplot(4,2,2*light_num+1)
        plt.plot(alltimes[100:myrows.index.size-1],all_delta_times)
        ax0 = plt.subplot(4,2,2*light_num+2)
        plt.plot(alltimes,allvalues)

plt.show()

