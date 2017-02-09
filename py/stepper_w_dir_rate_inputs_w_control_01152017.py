#!/usr/bin/python
#Import required libraries

#import different libraries so commands from libraries can be used throughout the program
import sys
import time
import RPi.GPIO as gpio
import numpy as np
import argparse
import pdb



def _setupStepper():
#This function defines the connection of the physical pins on the pi board. It defines the pins to be output pins. 
#It defines the drive sequence of the stepper motor

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
#This function takes the step direction, the current step number (1-4), the rate, the drive sequence, 
#the defined step pin numbers and the discrete time interval. The function takes a step in the stepper motor.
#Returns the current step.

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
#This function turns off all of the output pins. It is used after the user is finished moving the stepper motor. 

    for pin in range(0,4):
        xpin = stepPins[pin]
        gpio.output(xpin, False)


        
def _setupControl():
#This function sets up the control. Two quadrants are defined in the control: q1 and q2.  

    q1 = 3
    q2 = 10

    return q1, q2




def _control(pos_curr, q1, q2):
#This function takes the current position of the object it is tracking and the control quadrants. It decides
#if the current position is within a certain quadrant then returns a direction and a rate for the stepper motor.
#units of rate is ms, and specifies the time to wait between each step, higher rate = SLOWER MOVEMENT

    stepDir = int(np.sign(pos_curr))
    if (np.abs(pos_curr) < q1):
        rate = 0
    elif (np.abs(pos_curr) < q2): 
        rate = 50
    else:
        rate = 25

    return stepDir, rate



def _parseArgs():
#Not used. This function is designed to parse the command line for user input and feed into the stepper script. 

    parser = argparse.ArgumentParser(description = "Enter in string of angle commands")

    parser.add_argument('movement', type = int, nargs = '+', help = 'enter in string of angles and wait times until next move')
    parser.add_argument('-s', type = int, help = 'movement speed between each step in ms, default is 10')

    args = parser.parse_args()

    return args




################################################################################
#execute when python script is called.
################################################################################

#args = _parseArgs()
#_stepper(args.movement, args.s)

[seq, stepPins] = _setupStepper() 
[q1, q2] = _setupControl()
stepCounter = 0
dt_s = 3.0

pos_curr = [11.0, -13.5, 1.0] #used to test, position vector for control to track to

for x in xrange(3): #defined 3 dt's for stepper motor to go through
    start = time.time() #start timer
    [stepDir, rate] = _control(pos_curr[x], q1, q2) #run control 
    print stepDir
    print rate
    end = time.time() #check time
    while (end - start)<(dt_s - .5): #while time elapsed is less than the total dT time minus some extra time take steps
        stepCounter = _stepper(stepDir, stepCounter, rate, seq, stepPins, dt_s) #take a step
        end = time.time() #check time
 
    time.sleep(dt_s - (end-start))  #wait for rest of dT

_cleanupStepper(stepPins) #cleanup
