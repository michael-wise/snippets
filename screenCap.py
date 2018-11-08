from PIL import ImageGrab
import os
import time
 
def screenGrab():
    box = ()
    im = ImageGrab.grab(box)
    im.save(os.getcwd() + '\\full_snap__' + str(int(time.time())) +
'.png', 'PNG')

def boxGrab():
    box = (157,346,796,825)
    im = ImageGrab.grab(box)
    im.save(os.getcwd() + '\\box_snap__' + str(int(time.time())) +
'.png', 'PNG')

def main():
    screenGrab()
    boxGrab()

if __name__ == '__main__':
    main()
