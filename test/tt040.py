import Tkinter

class MyApp:
    def __init__(self,myParent):
        self.myContainer1 = Tkinter.Frame(root)
        self.myContainer1.pack()

        self.button1 = Tkinter.Button(self.myContainer1) #create an instance of the class Button
        self.button1["text"] = "Hello, World!" #modify one of many attributes of the button class
        self.button1["background"] = "green"
        self.button1.pack() #pack into myContainer1

        self.button2 = Tkinter.Button(self.myContainer1)
        self.button2.configure(text="off to join the circus")
        self.button2.configure(background="tan")
        self.button2.pack()

        self.button3 = Tkinter.Button(self.myContainer1)
        self.button3.configure(text="join me?", background="cyan")
        self.button3.pack()

        self.button4 = Tkinter.Button(self.myContainer1, text = "goodbye", background="red")
        self.button4.pack()


root = Tkinter.Tk()
myapp = MyApp(root)
root.mainloop() #event loop, dont close until user closes
