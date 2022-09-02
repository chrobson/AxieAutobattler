from ppadb.client import Client
from cv2 import cv2, waitKey
import numpy as np
from mss import mss
from PIL import ImageGrab
from PIL import Image
import time
 

 #const
#D:\download\platform-tools_r31.0.3-windows\platform-tools>adb shell wm size 720x1480

#D:\download\platform-tools_r31.0.3-windows\platform-tools>adb shell wm size 1080x2220


adb = Client(host='localhost', port=5037)


devices = adb.devices()
device = devices[0]

if len(devices) == 0:
    print( "No devices found")
    
print("Connected devices:",devices)
print(devices)

while True:
    image = device.screencap()
    img_np = cv2.imdecode(np.frombuffer(image, np.uint8), -1)
    img_gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)

    # Read the template
    template = cv2.imread(r'D:\Projekty\Axie\card1en.png',0)
    #0energy temp
    energy0 = cv2.imread(r'D:\Projekty\Axie\0energy.png',0)
    endturn = cv2.imread(r'D:\Projekty\Axie\end.png',0)
    victory = cv2.imread(r'D:\Projekty\Axie\victory.png',0)
    # Perform match operations.
    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
    res1 = cv2.matchTemplate(img_gray,energy0,cv2.TM_CCOEFF_NORMED)
    vic1 = cv2.matchTemplate(img_gray,victory,cv2.TM_CCOEFF_NORMED)
    # Specify a threshold
    threshold = 0.85

    # Store the coordinates of matched area in a numpy array
    loc = np.where( res >= threshold)
    en0 = np.where( res1 >= threshold)
    vict = np.where(vic1 >= threshold)


    if vict[0].size >0 :
        for x in range(6):
            time.sleep(3)
            device.shell(f'input touchscreen tap 994 613')
            print('Victory')
    # Draw a rectangle around the matched region.
    if loc[0].size == 0:
        res2 = cv2.matchTemplate(img_gray,endturn,cv2.TM_CCOEFF_NORMED)
        end0 = np.where( res2 >= threshold)
        if end0[0].size >0 :
            device.shell(f'input touchscreen tap 1395 495')
            print('tap no cards')
    if en0[0].size == 1:
        res2 = cv2.matchTemplate(img_gray,endturn,cv2.TM_CCOEFF_NORMED)
        end0 = np.where( res2 >= threshold)
        if end0[0].size > 0:
            device.shell(f'input touchscreen tap 1395 495')
            print('tap no energy')
    for pt in zip(*loc[::-1]):
        print(f'y{pt[0]} x{pt[1]}')
        # x1 = 38
        # y1 = 561
        # x2 = 38
        # y2 = 451
        # if pt[0].size > 0:
        if en0[0].size == 0:
            device.shell(f'input touchscreen swipe {pt[0]} {pt[1]} {pt[0]} {pt[1]-100}')
            #time.sleep(1)
        #cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,255,255), 2)