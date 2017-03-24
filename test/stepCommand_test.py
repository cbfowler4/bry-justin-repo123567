import Tkinter as tk

class MyApp:
    def __init__(self, parent):
        ## at the outset, we havent yet invoked any button handler
        self.myLastButtonInvoked = None
        
        self.myParent = parent #remember my parent, the root
        self.myContainer1 = tk.Frame(parent)
        self.myContainer1.pack()

        self.yellowButton = tk.Button(self.myContainer1)
        self.yellowButton.focus_force()
        self.yellowButton.configure(text = "Left", background = "yellow")
        self.yellowButton.bind("<Return>", self.button1Click)
        self.yellowButton.pack(side=tk.LEFT)

        self.redButton = tk.Button(self.myContainer1)
        self.redButton.focus_force()
        self.redButton.configure(text = "Close", background = "red")
        self.redButton.bind("<Return>", self.button2Click)
        self.redButton.pack(side=tk.LEFT)

    def button1Click(self, event):
        self.myLastButtonInvoked = 1
        print "go left", self.myLastButtonInvoked

        

    def button2Click(self, event):
        self.myParent.destroy()



print "\n"*100
print "starting..."
root = tk.Tk()
myapp = MyApp(root)
root.mainloop()
print "...Done!"
