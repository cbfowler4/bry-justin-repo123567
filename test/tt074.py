import Tkinter as tk

class MyApp:
    def __init__(self, parent):
        self.myParent = parent #remember my parent, the root
        self.myContainer1 = tk.Frame(parent)
        self.myContainer1.pack()

        self.button1 = tk.Button(self.myContainer1, command=self.button1Click)
        self.button1.configure(text="OK", background = "green")
        self.button1.pack(side=tk.LEFT)
        self.button1.focus_force()
        
        self.button2 = tk.Button(self.myContainer1, command=self.button2Click)
        self.button2.configure(text="cancel", background = "red")
        self.button2.pack(side=tk.RIGHT)
        
        
    def button1Click(self):
        print "button1Click event handler"
        if self.button1["background"] == "green":
            self.button1["background"] = "yellow"
        else:
            self.button1["background"] = "green"

    def button2Click(self):
        print "button2Click event handler"
        self.myParent.destroy()


    
root = tk.Tk()
myapp = MyApp(root)
root.mainloop()

