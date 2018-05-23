import cv2
import numpy as np
import os
import string
import random
from PIL import Image
import subprocess as sp
from time import sleep
from threading import Thread

device_name = ''
screen_width = 0
screen_height = 0
#-------------- USABLE METHODS -------------------------
def tap_middle():
    cmd = "adb shell input tap %s %s" % (screen_width/2, screen_height/2)
    os.system(cmd)

def tap_screen(x,y):
    cmd = "adb shell input tap %s %s" % (x,y)
    os.system(cmd)

def tap_image(query_image,width_modifier=1, height_modifier=1, retries=1):
    retries_left = retries
    rect = None
    while retries_left > 0 and not rect:
        rect = find_image(query_image)
        retries_left = retries_left - 1

    if not rect:
        return False
    else:
        image_name = os.path.split(query_image)[1]
        x = int((rect[0]+rect[2])*0.5*width_modifier)
        y = int((rect[1]+rect[3])*0.5*height_modifier)
        cmd = "adb shell input tap %s %s" % (x,y)
        os.system(cmd)
        return True

def find_image(queryimage_file, screenshot_match=None):
    #self.log.append('Trying to find %s in current screen' % queryimage_file)
    try:
        queryimage_file = queryimage_file.replace('#', device_name)
        screenshot_name=randomword(5)
        screenshot_match="%s\%s.png" % ('screenshots', screenshot_name)
        screenshot(screenshot_name, path='screenshots')
        return find_template(queryimage_file, screenshot_match)
    finally:
        os.remove(screenshot_match)
        os.system('adb shell rm -f /sdcard/' + screenshot_name + '.png')

def close_application(package_name):
    os.system('adb shell am force-stop ' + package_name)

#--------------------- FILE METHODS --------------------------

def find_template(queryimage,screenshot_match):
    img = cv2.imread(screenshot_match,0)
    template = cv2.imread(queryimage,0)
    w, h = template.shape[::-1]

    # Apply template Matching
    res = cv2.matchTemplate(img,template,cv2.TM_CCOEFF_NORMED)
    threshold = 0.9
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        print 'Template found'
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        return (top_left[0],top_left[1],bottom_right[0],bottom_right[1])
    print 'Nothing found'
    return None

def screenshot(name, path=None):
    full_path='%s/%s.png' % (path,name)
    os.system('adb shell screencap -p /sdcard/'+ name +'.png')
    os.system('cd '+ path +' && adb pull /sdcard/'+ name +'.png')

    im = Image.open(full_path)
    width, height = im.size

    if(height > width):
        os.system('sips -r 270 %s >/dev/null 2&>1' % full_path)

def get_screen():
    size = sp.check_output(['adb', 'shell', 'wm', 'size'])
    size = size.replace('x', ' ')
    size_in_number = [int(s) for s in size.split() if s.isdigit()]
    global screen_width
    global screen_height 
    screen_width, screen_height = size_in_number
    print 'Screen sizes got:', screen_width, 'x', screen_height

def get_device_name():
    global device_name
    device_name = sp.check_output(['adb', 'shell', 'getprop', 'ro.product.name'])
    device_name = ''.join(device_name.split())
    print 'Device name got:', device_name

def randomword(length):
    s=string.lowercase+string.digits
    return ''.join(random.sample(s,length))

def start_server():
    os.system("adb start-server")

def initialize():
    print 'Starting...'
    server = Thread(target = start_server, args = ())
    server.start()
    server.join()
    print 'ADB Server started.'
    print 'Getting device info...'
    get_screen()
    get_device_name()

if __name__ == '__main__':
    initialize()
