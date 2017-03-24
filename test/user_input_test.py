import sys
import select
import time
import curses
import multiprocessing
import subprocess

def heardEnter():
    i,o,e = select.select([sys.stdin],[],[],.1)
    for s in i:
        if s == sys.stdin:
            input = sys.stdin.readline()
            return True
        return False

#while True:
    #a = heardEnter()
    #print a

def input_char(message):
    try:
        win = curses.initscr()
        win.addstr(0,0,(message))
        while True:
            ch = win.getch()
            if ch in range(32,127): break
            time.sleep(.1)
    except: raise
    finally:
        curses.endwin()
    return chr(ch)

#c = input_char('Press s or n to continue:')
#if c.upper() == 'S':
#    print 'YES'

#while True:
#    win = curses.initscr()
#    ch = win.getch()
#    time.sleep(1)
#    win.erase()


import tty
import termios
##
##orig_set = termios.tcgetattr(sys.stdin)
##
##tty.setraw(sys.stdin)
##
##x = 0
##while x != chr(120):
##    x = sys.stdin.read(1)[0]
##    print x
##    
##
##termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_set)

def _getUinput():
    orig_set = termios.tcgetattr(sys.stdin)
    tty.setraw(sys.stdin)
    x = 0
    while x != chr(120):
        x = sys.stdin.read(1)[0]
        print x
    
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_set)

def _test():
    x=0
    while True:
        print x
        x = x+1
        time.sleep(3)


                           
#subprocess.Popen(executable = _getUinput(), shell=True)

#_getUinput()

#Puinput = multiprocessing.Process(target = _getUinput())

#Puinput.start()
#Puinput.join()

import shlex
process = subprocess.Popen(shlex.split("""x-terminal-emulator -e 'bash -c "test.py"'"""), stdout=subprocess.PIPE)
time.sleep(10)
process.wait()
print(process.returncode)
