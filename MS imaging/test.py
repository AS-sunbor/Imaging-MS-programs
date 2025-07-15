import tkinter as tk

class Application (tk.Frame):
    def up_pushed(self, event, val):
        val.set(val.get()+1)
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets(master=master)
    def create_widgets(self, master=None):
        self.sz1 = tk.DoubleVar()
        self.sz2 = tk.DoubleVar()
        self.sz3 = tk.DoubleVar()
        self.sz1.set(1.0)
        self.text_size1 = tk.Entry(self, textvariable=self.sz1, font=24,width=20)
        self.text_size2 = tk.Entry(self, textvariable=self.sz2, font=24,width=20)
        self.text_size3 = tk.Entry(self, textvariable=self.sz3, font=24,width=20)
        self.text_size1.bind("<Up>", lambda event :self.up_pushed(self, val=self.sz1))
        self.text_size1.pack()
        self.text_size2.pack()
        self.text_size3.pack()

root = tk.Tk()
root.title("MS imaging")
#root.geometry("1280x960")
root.resizable(0,0)
app = Application(master=root)
app.mainloop()
root.destroy()
