import Tkinter as tk

global value

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
        self.yellowButton.bind("<Button-1>", self.button1Click)

        self.redButton = tk.Button(self.myContainer1, command=self.redButtonClick)
        self.redButton.configure(text = "RED", background = "red")
        self.redButton.pack(side=tk.LEFT)


        
        
    def redButtonClick(self):
        print "hello"
        

    def yellowButtonClick(self):
        value = 2
        print value

    def button1Click(self, event):
        value = 1
        print value


print "\n"*100
print "starting..."
root = tk.Tk()
myapp = MyApp(root)
root.mainloop()
print "...Done!"
