
from serial import *
from threading import Thread
import matplotlib
matplotlib.use('tkAgg')
import matplotlib.pyplot as plt
import time
fig=plt.figure()
plt.axis([0,256,0,1023])
plt.show(block=True)

def receiving(ser):
    global last_received
    buffer = ''
    li=[0]*256
    while True:
        buffer = buffer + ser.read(ser.inWaiting())
        if '\n' in buffer:
            lines = buffer.split('\n')
            last_received = lines[-2]
            buffer = lines[-1]
            li=li[1:256]
            li.append(float(last_received.rstrip('\r')))
            plt.plot(li)
            plt.draw()
            time.sleep(0.01)
            
if __name__ ==  '__main__':
    ser = Serial(
        port='COM7',
        baudrate=9600,
        bytesize=EIGHTBITS,
        parity=PARITY_NONE,
        stopbits=STOPBITS_ONE,
        timeout=0.1,
        xonxoff=0,
        rtscts=0,
        interCharTimeout=None
    )
    
Thread(target=receiving, args=(ser,)).start()
