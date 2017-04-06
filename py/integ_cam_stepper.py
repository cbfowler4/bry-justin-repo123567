#!/usr/bin/python
#Import required libraries

#import different libraries so commands from libraries can be used throughout the program
import sys
import time
import RPi.GPIO as gpio
import numpy as np
import argparse
import pdb
import multiprocessing
import cv2



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


def _stepProcess(stepDir, stepCounter, rate, seq, stepPins):
    a = 1
    while a>0:
        rate_int = rate.value #read shared memory object
        stepDir_int = stepDir.value #read shared memory object
        stepCounter = _stepper(stepDir_int, stepCounter, rate_int, seq, stepPins, dt_s) #take a step

def _controlProcess(pos_curr, q1, q2, rate, stepDir, dt_s):
    a = 1
    x = 0
    while a>0: 
        start = time.time()
        if x >= (len(pos_curr)-1): #resets the position count so it can go on forever
            x = 0
        else:
            x=x+1
        print x    
        [stepDir_int, rate_int] = _control(pos_curr[x], q1, q2)
        stepDir.value = stepDir_int #set shared memory object
        rate.value = rate_int #set shared memory object
        end = time.time()
        time.sleep(dt_s-(end-start))



def camera():
  face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
  cap = cv2.VideoCapture(0)

  while True:
      ret, img = cap.read()
      gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
      faces = face_cascade.detectMultiScale(gray, 1.3, 5)
      for (x,y,w,h) in faces:
          cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
          eoi_gray = gray[y:y+h, x:x+w]
          roi_color = img[y:y+h, x:x+w]
          xval = x + w/2
          yval = y+ h/2
          print xval
       
      cv2.imshow('img', img)
    

      k = cv2.waitKey(5) & 0xFF
      if k == 1048603:
          break

  cv2.destroyAllWindows()
  cap.release()

################################################################################
#execute when python script is called.
################################################################################

#args = _parseArgs()
#_stepper(args.movement, args.s)



if __name__ == "__main__":
    [seq, stepPins] = _setupStepper() 
    [q1, q2] = _setupControl()
    stepCounter = 0
    dt_s = 2.0

    pos_curr = [11.0, -13.5, 15.0, -15.0, 15.0] #used to test, position vector for control to track to

    rate = multiprocessing.Value('d', 0.0) #creates a shared memory object called rate
    stepDir = multiprocessing.Value('i', 1)#creates a shared memory object called stepDir

    Pstep = multiprocessing.Process(target= _stepProcess, args=(stepDir, stepCounter, rate, seq, stepPins))
    Pcontrol = multiprocessing.Process(target = _controlProcess, args = (pos_curr, q1, q2, rate, stepDir, dt_s))
    Pcamera = multiprocessing.Process(target = camera, args = ())
    
    Pstep.start()
    Pcontrol.start()
    Pcamera.start()
 
    Pstep.join()
    Pcontrol.join()
    Pcamera.join()
        
                                        
_cleanupStepper(stepPins) #cleanup
