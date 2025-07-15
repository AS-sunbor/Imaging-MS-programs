import cv2
import numpy as np
import tkinter as tk
import tkinter.ttk as ttk
from data_struct import all_data
from PIL import Image, ImageTk
#import scipy.ndimage as scim
#from skimage.morphology import ball

def imread(filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
    try:
        n = np.fromfile(filename, dtype)
        img = cv2.imdecode(n, flags)
        return img
    except Exception as e:
        print(e)
        return None

class Tab_find_cell(tk.Frame):
    def canvas_update(self, data):
        self.img = imread(self.active_img, 0)
#        if data.gfp_rolling_tup[self.index] == 1:
#            print (data.gfp_ballsize_tup[self.index])
#            s = ball(data.gfp_ballsize_tup[self.index]) # Create 3D ball with radius of 50 and a diameter of 2*50+1
#            h = s.shape[1] // 2 + 1  # Take only the upper half of the ball
#            s = s[:h, :, :].sum(axis=0) # Flatten the 3D ball to a weighted 2D disc
#            s = (255 * (s - s.min())) / (s.max() - s.min()) # Rescale weights into 0-255
#            self.img = scim.white_tophat(self.img, structure=s) # Use im-opening(im,ball) (i.e. white tophat transform) (see original publication)
        ret, self.img = cv2.threshold(self.img, data.gfp_thr_tup[self.index], 255, cv2.THRESH_BINARY)
        self.img = cv2.resize(self.img, (1080,int(1080 / self.img.shape[1] * self.img.shape[0])))
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        self.img = Image.fromarray(self.img)
        self.img = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(540, 405, image=self.img)
    def Enter_pushed(self, event, data, val, tup, idx):
        tup[idx]=val.get()
        self.canvas_update(data=data)
    def Up_pushed(self, event, data, val, tup, idx):
        val.set(val.get()+1)
        tup[idx]=val.get()
        self.canvas_update(data=data)
    def Down_pushed(self, event, data, val, tup, idx):
        val.set(val.get()-1)
        tup[idx]=val.get()
        self.canvas_update(data=data)
    def Button_autothread_pushed(self, data=None):
        pass
    def Slct_img (self, event, data=None):
        if (self.Filebox.curselection()):
            self.index = self.Filebox.index(self.Filebox.curselection())
            self.active_img=data.gfp_files_tup[self.index]
            self.cur_threthold.set(data.gfp_thr_tup[self.index])
            self.cur_ballsize.set(data.gfp_ballsize_tup[self.index])
#            self.roll_list.current(data.gfp_rolling_tup[self.index])
            self.canvas_update(data=data)

    def select_rolllist(self, event, data=None):
#        data.gfp_rolling_tup[self.index]=self.roll_list.current()
        self.canvas_update(data=data)

    def __init__(self, master=None, data=None):
        self.tab = tk.Frame(master)
        master.add(self.tab, text='CellFinder', padding=3, state=tk.DISABLED) #, state=data.tab_find_cell_activity)
        self.active_img = None
        self.cur_threthold = tk.IntVar()
        self.cur_ballsize = tk.IntVar()
        self.spc1 = tk.Label(self.tab, text="", padx=125)
        self.spc1.grid(row=0,column=0, sticky=tk.W)
        self.button_autothread = tk.Button(self.tab, text="autothread", command=lambda: self.Button_autothread_pushed(data=data))
        self.button_autothread.grid(row=0,column=2, sticky=tk.W)
        self.label_curthrethold = tk.Label(self.tab, text="  threathold:")
        self.label_curthrethold.grid(row=0,column=3, sticky=tk.W)
        self.text_curthrethold = tk.Entry(self.tab, textvariable=self.cur_threthold, width=10)
        self.text_curthrethold.bind("<Up>"    , lambda event :   self.Up_pushed(self, val=self.cur_threthold, data=data, tup=data.gfp_thr_tup, idx=self.index))
        self.text_curthrethold.bind("<Down>"  , lambda event : self.Down_pushed(self, val=self.cur_threthold, data=data, tup=data.gfp_thr_tup, idx=self.index))
        self.text_curthrethold.bind("<Return>", lambda event :self.Enter_pushed(self, val=self.cur_threthold, data=data, tup=data.gfp_thr_tup, idx=self.index))
        self.text_curthrethold.bind("<Tab>"   , lambda event :self.Enter_pushed(self, val=self.cur_threthold, data=data, tup=data.gfp_thr_tup, idx=self.index))
        self.text_curthrethold.grid(row=0,column=4, sticky=tk.W)
#        self.roll_txt =  tk.Label(self.tab, text="Rolling ball :")
#        self.roll_txt.grid(row=0, column=5, sticky=tk.W)
#        self.roll_list = ttk.Combobox(self.tab, values=["OFF","ON"])
#        self.roll_list.current(0)
#        self.roll_list.grid(row=0, column=6, sticky=tk.W)
#        self.roll_list.bind('<<ComboboxSelected>>' , lambda event : self.select_rolllist(self, data=data))
#        self.label_ballsize = tk.Label(self.tab, text=" ballsize:")
#        self.label_ballsize.grid(row=0,column=7, sticky=tk.W)
#        self.text_ballsize = tk.Entry(self.tab, textvariable=self.cur_ballsize, width=10)
#        self.text_ballsize.bind("<Up>"    , lambda event :   self.Up_pushed(self, val=self.cur_ballsize, data=data, tup=data.gfp_ballsize_tup, idx=self.index))
#        self.text_ballsize.bind("<Down>"  , lambda event : self.Down_pushed(self, val=self.cur_ballsize, data=data, tup=data.gfp_ballsize_tup, idx=self.index))
#        self.text_ballsize.bind("<Return>", lambda event :self.Enter_pushed(self, val=self.cur_ballsize, data=data, tup=data.gfp_ballsize_tup, idx=self.index))
#        self.text_ballsize.bind("<Tab>"   , lambda event :self.Enter_pushed(self, val=self.cur_ballsize, data=data, tup=data.gfp_ballsize_tup, idx=self.index))
#        self.text_ballsize.grid(row=0,column=8, sticky=tk.W)
        self.spc2 = tk.Label(self.tab, text="", padx=125)
        self.spc2.grid(row=0,column=9, sticky=tk.W)
        self.img = Image.open('Unread_img.png')
        self.img = ImageTk.PhotoImage(self.img)
        self.canvas = tk.Canvas(self.tab, bg = "black", width=1081, height=811)
        self.canvas.grid(row=1, column=0, columnspan=10, rowspan=2)
        self.canvas.create_image(540, 405, image=self.img)
        self.Filebox = tk.Listbox(self.tab, listvariable=data.gfp_files, width=61, height=49, fg="black") # need scroll bar
        self.Filebox.grid(row=1, column=10, sticky=tk.S)
        self.yscrollbar = ttk.Scrollbar(self.tab,orient=tk.VERTICAL,command=self.Filebox.yview)
        self.Filebox['yscrollcommand'] = self.yscrollbar.set
        self.yscrollbar.grid(row=1, column=11, sticky=(tk.NS))
        self.xscrollbar = ttk.Scrollbar(self.tab,orient=tk.HORIZONTAL,command=self.Filebox.xview)
        self.Filebox['xscrollcommand'] = self.xscrollbar.set
        self.xscrollbar.grid(row=2, column=10, sticky=(tk.W,tk.E))
        self.Filebox.bind("<<ListboxSelect>>", lambda event:self.Slct_img(self, data=data))
