import sys
import tty
import termios

orig_set = termios.tcgetattr(sys.stdin)
tty.setraw(sys.stdin)

x = 0
while x != chr(120):
    x = sys.stdin.read(1)[0]
    print x
    
termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_set)
