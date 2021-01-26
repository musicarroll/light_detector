import serial
ser = serial.Serial('/dev/ttyACM0', 19200, timeout=1)
#x = ser.read()          # read one byte
#s = ser.read(10)        # read up to ten bytes (timeout)
#line = ser.readline()   # read a '\n' terminated line

while True:
    try:
        line = ser.readline()
        print(str(line))
    except KeyboardInterrupt:
        quit()
