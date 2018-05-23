import DeviceBot
#python imports
import string
import random
import signal
import os
import sys
import strings
from time import sleep

SD = 4
TOA = 3
GET = 2
SELL = 1

deviceid = 'TA92908B8P'
app_package = 'com.com2us.smon.normal.freefull.google.kr.android.common'

def getItem():
    print "Clicking on OK or GET button if exists"
    if DeviceBot.tap_image(strings.ok_button):
        pass
    else:
        DeviceBot.tap_image(strings.get_button)

def sellItem():
    print 'Selling Item'
    if DeviceBot.tap_image(strings.sell_button):
        sleep(2)
        DeviceBot.tap_image(strings.yes_button)
        sleep(2)   
        return True
    else:
        return False

def openStash(): 
    print "Stage ended. Clicking on middle to open the stash."
    DeviceBot.tap_middle()
    sleep(1)
    DeviceBot.tap_middle()
    sleep(1)      

def verifyEndGame():
    while not DeviceBot.tap_image(strings.screen_victory):                    
        print "Waiting for victory or lose screen..."
        if DeviceBot.tap_image(strings.screen_defeated):
            DeviceBot.tap_image(strings.no_stage_button)
            sleep(2)               
            break
        sleep(5)
    return

def verifyEnd10Stage():
    while not DeviceBot.tap_image(strings.screen_clear):                    
        print "Waiting for 10 stage clear..."
        sleep(5)
    return

def start_stage(action):
    level = 0
    while not DeviceBot.tap_image(strings.energy_empty):
        if level == 0:
            # Clicking on Start
            print "Starting stage..."
            DeviceBot.tap_image(strings.start_button)
            level = 1
        elif level == 1:
            # Verifying if game ended
            if action == SD:
                verifyEnd10Stage()
            else:
                verifyEndGame()
            openStash()
            level = 2

        elif level == 2:
            if action == SELL:
                if not sellItem():
                    getItem()        
            else:   
                getItem()
            
            level = 3
            sleep(1)
        elif level == 3:
            if action == TOA:
                print 'Clicking on Next Stage Button'
                DeviceBot.tap_image(strings.next_button)
            else :
                print "Clicking on Replay button"
                DeviceBot.tap_image(strings.replay_button)
            
            level = 0
            sleep(2)
    DeviceBot.close_application(app_package)

def main():
    start_stage(input(strings.bot_action))
        
def exitGracefully(self, signum, frame):
    signal.signal(signal.SIGINT, signal.getsignal(signal.SIGINT))
    sys.exit(1)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, exitGracefully)
    DeviceBot.initialize()
    main()
