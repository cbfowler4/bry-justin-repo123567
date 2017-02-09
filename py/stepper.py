#!/usr/bin/python
#Import required libraries

import sys
import time
import RPi.GPIO as gpio
import numpy as np
import argparse
import pdb

#angle = int(sys.argv[1])





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



def _stepper(stepDir, stepCounter, rate_ms_per_stp, seq, stepPins, dt_s):
    StepCount = len(seq)

    #Read wait time from command line
    rate = rate_ms_per_stp/float(1000)
    if (rate > 0): 
        for pin in range(0,4):
            xpin = stepPins[pin] #get gpio
            if seq[stepCounter][pin]!=0:
                gpio.output(xpin, True)
            else:
                gpio.output(xpin, False)

        stepCounter += stepDir

        #If we reach the end of the sequence start again
        if (stepCounter>=StepCount):
            stepCounter = 0
        if (stepCounter<0):
            stepCounter = StepCount+stepDir

        #wait before moving on
        time.sleep(rate)
    else:
        time.sleep(dt_s/20)
        
    return stepCounter



def _cleanupStepper(stepPins):
    for pin in range(0,4):
        xpin = stepPins[pin]
        gpio.output(xpin, False)


        
def _setupControl():
    q1 = 3
    q2 = 10

    return q1, q2




def _control(pos_curr, q1, q2):
    stepDir = int(np.sign(pos_curr))
    if (np.abs(pos_curr) < q1):
        rate = 0
    elif (np.abs(pos_curr) < q2): 
        rate = 50
    else:
        rate = 25

    return stepDir, rate



def _parseArgs():
    parser = argparse.ArgumentParser(description = "Enter in string of angle commands")

    parser.add_argument('movement', type = int, nargs = '+', help = 'enter in string of angles and wait times until next move')
    parser.add_argument('-s', type = int, help = 'movement speed between each step in ms, default is 10')

    args = parser.parse_args()

    return args



#args = _parseArgs()
#_stepper(args.movement, args.s)
[seq, stepPins] = _setupStepper()
[q1, q2] = _setupControl()
stepCounter = 0
dt_s = 3.0

pos_prev = 0
pos_curr = [11.0, -13.5, 1.0]

for x in xrange(3):
    start = time.time()
    [stepDir, rate] = _control(pos_curr[x], q1, q2)
    print stepDir
    print rate
    end = time.time()
    while (end - start)<(dt_s - .5):
        stepCounter = _stepper(stepDir, stepCounter, rate, seq, stepPins, dt_s)
        end = time.time()

    time.sleep(dt_s - (end-start))    

_cleanupStepper(stepPins)
