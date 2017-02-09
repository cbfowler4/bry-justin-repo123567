#!/usr/bin/python
#Import required libraries

import sys
import time
import RPi.GPIO as gpio
import numpy as np
import argparse
import pdb

#angle = int(sys.argv[1])


#pdb.set_trace()


def _setupStepper():
    #Use BCM GPIO references instead of physical pin numbers
    gpio.setmode(gpio.BCM)

    #Define gpio signals to use physical pins 11, 15, 16, 18
    #GPIO17, GPIO22, GPIO23, GPIO24
    StepPins = [17, 18, 27, 22]

    #set all pins as output
    for pin in StepPins:
        print "Setup pins"
        gpio.setup(pin,gpio.OUT)
        gpio.output(pin, False)

    #Define advanced sequence as shown in manufacturers datasheet
    #half step
    #seq = [[1, 0, 0, 1],       [1, 0, 0, 0],       [1, 1, 0, 0],       [0, 1, 0, 0],       [0, 1, 1, 0],       [0, 0, 1, 0],       [0, 0, 1, 1],       [0, 0, 0, 1]]
    
    #wave drive
    seq = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]

    #full step
    #seq = [[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 1], [1, 0, 0, 1]]

    return seq, StepPins



def _stepper(angle, rate_ms_per_stp, seq, stepPins):
    StepCount = len(seq)
    StepDir = np.sign(angle) # set to 1 or 2 for clockwise, set to -1 or -2 for anti-clockwise

    #Read wait time from command line
    rate = rate_ms_per_stp/float(1000)

    #Initialize variables
    StepCounter = 0

    #calculate number of steps based on input angle
    stepsPerRev = 2048
    totSteps = stepsPerRev/360*abs(angle)

    #Start main loop
    for stepNum in xrange(totSteps):

        print StepCounter,
        print seq[StepCounter]

        for pin in range(0,4):
            xpin = stepPins[pin] #get gpio
            if seq[StepCounter][pin]!=0:
                print "Enabled GPIO %i" %(xpin)
                gpio.output(xpin, True)
            else:
                gpio.output(xpin, False)

        StepCounter += StepDir

        #If we reach the end of the sequence start again
        if (StepCounter>=StepCount):
            StepCounter = 0
        if (StepCounter<0):
            StepCounter = StepCount+StepDir

        #wait before moving on
        time.sleep(rate)



def _cleanupStepper(stepPins):
    for pin in range(0,4):
        xpin = stepPins[pin]
        gpio.output(xpin, False)
        



def _parseArgs():
    parser = argparse.ArgumentParser(description = "Enter in string of angle commands")

    parser.add_argument('movement', type = int, nargs = '+', help = 'enter in string of angles and wait times until next move')
    parser.add_argument('-s', type = int, help = 'movement speed between each step in ms, default is 10')

    args = parser.parse_args()

    return args



#args = _parseArgs()
#_stepper(args.movement, args.s)
[seq, stepPins] = _setupStepper()

for x in xrange(3):
    start = time.time()
    _stepper(10, 20, seq, stepPins)
    end = time.time()
    stepTime = end-start
    dt_s = 3
    time.sleep(dt_s)    

_cleanupStepper(stepPins)
