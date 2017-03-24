import Tkinter

class MyApp:
    def __init__(self,myParent):
        self.myContainer1 = Tkinter.Frame(root)
        self.myContainer1.pack()

        self.button1 = Tkinter.Button(self.myContainer1) #create an instance of the class Button
        self.button1["text"] = "Hello, World!" #modify one of many attributes of the button class
        self.button1["background"] = "green"
        self.button1.pack() #pack into myContainer1se


root = Tkinter.Tk()
myapp = MyApp(root)
root.mainloop() #event loop, dont close until user closes
