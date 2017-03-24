import Tkinter

root = Tkinter.Tk()

myContainer1 = Tkinter.Frame(root)
myContainer1.pack()

button1 = Tkinter.Button(myContainer1) #create an instance of the class Button
button1["text"] = "Hello, World!" #modify one of many attributes of the button class
button1["background"] = "green"
button1.pack() #pack into myContainer1

root.mainloop() #event loop, dont close until user closes
