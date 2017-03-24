import Tkinter

root = Tkinter.Tk() #instance of the Tk class

myContainer1 = Tkinter.ACTIVEFrame(root) #creates a frame with parent of root
myContainer1.pack() #puts widget/container into frame

root.mainloop() #run until exited, event loop
