from SimpleLoggerV1 import SimpleLoggerV1
import time

sl = SimpleLoggerV1(method='rtu',serialPort='/dev/ttyACM0')

while(1):
    # time.sleep()
    print(sl.readA12A13())