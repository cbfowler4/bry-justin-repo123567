import Tkinter as tk

class MyApp:
    def __init__(self, parent):
        self.myParent = parent #remember my parent, the root
        self.myContainer1 = tk.Frame(parent)
        self.myContainer1.pack()

        self.button1 = tk.Button(self.myContainer1)
        self.button1.configure(text="OK", background = "green")
        self.button1.pack(side=tk.LEFT)
        self.button1.bind("<Button-1>", self.button1Click)

        self.button2 = tk.Button(self.myContainer1)
        self.button2.configure(text="cancel", background = "red")
        self.button2.pack(side=tk.RIGHT)
        self.button2.bind("<Button-1>", self.button2Click)

    def button1Click(self, event):
        if self.button1["background"] == "green":
            self.button1["background"] = "yellow"
        else:
            self.button1["background"] = "green"
        print "hello"


    def button2Click(self, event):
        self.myParent.destroy()

root = tk.Tk()
myapp = MyApp(root)
root.mainloop()
