import Tkinter as tk

class MyApp:
    def __init__(self, parent):

        ## at the outset, we havent yet invoked any button handler
        self.myLastButtonInvoked = None
        
        self.myParent = parent #remember my parent, the root
        self.myContainer1 = tk.Frame(parent)
        self.myContainer1.pack()

        self.yellowButton = tk.Button(self.myContainer1, command=self.yellowButtonClick)
        self.yellowButton.configure(text = "YELLOW", background = "yellow")
        self.yellowButton.pack(side=tk.LEFT)

        self.redButton = tk.Button(self.myContainer1, command=self.redButtonClick)
        self.redButton.configure(text = "RED", background = "red")
        self.redButton.pack(side=tk.LEFT)

        self.whiteButton = tk.Button(self.myContainer1, command=self.whiteButtonClick)
        self.whiteButton.configure(text = "WHITE", background = "white")
        self.whiteButton.pack(side=tk.LEFT)
        
        
    def redButtonClick(self):
        print "red button clicked. Previous button invoked was", self.myLastButtonInvoked
        self.myLastButtonInvoked = "WHITE"

    def yellowButtonClick(self):
        print "yellow button clicked. Previous button invoked was", self.myLastButtonInvoked
        self.myLastButtonInvoked = "WHITE"

    def whiteButtonClick(self):
        print "white button clicked. Previous button invoked was", self.myLastButtonInvoked
        self.myLastButtonInvoked = "WHITE"

print "\n"*100
print "starting..."
root = tk.Tk()
myapp = MyApp(root)
root.mainloop()
print "...Done!"
