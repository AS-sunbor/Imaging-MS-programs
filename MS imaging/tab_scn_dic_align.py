import cv2, re
import numpy as np
import tkinter as tk
import tkinter.ttk as ttk
from data_struct import all_data
from PIL import Image, ImageTk
from pyimzml.ImzMLParser import ImzMLParser


def imread(filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
    try:
        n = np.fromfile(filename, dtype)
        img = cv2.imdecode(n, flags)
        return img
    except Exception as e:
        print(e)
        return None

def img_position(image, xpad, ypad, xsiz, ysiz):
    if (xpad>0):
        img_add = np.zeros((image.shape[0],int(xpad), 3), np.uint8)
        image = cv2.hconcat([img_add, image])
    else:
        image = image[:,-1*xpad:]
    if (ypad>0):
        img_add = np.zeros((int(ypad), image.shape[1], 3), np.uint8)
        image = cv2.vconcat([img_add, image])
    else:
        image = image[-1*ypad:,:]
    if (xsiz>image.shape[1]):
        img_add = np.zeros((image.shape[0],int(xsiz-image.shape[1]), 3), np.uint8)
        image = cv2.hconcat([image, img_add])
    else:
        image = image[:,0:xsiz]
    if (ysiz>image.shape[0]):
        img_add = np.zeros((int(ysiz-image.shape[0]), image.shape[1], 3), np.uint8)
        image = cv2.vconcat([image, img_add])
    else:
        image = image[0:ysiz,:]
    return image


def set_to_display (image):
    xyohaku = 0
    yyohaku = 0
    if (image.shape[0]/1080 > image.shape[1]/810):
        bairitsu = 810/image.shape[0]
        image = cv2.resize(image, (int(image.shape[1]*bairitsu),810), interpolation=cv2.INTER_LANCZOS4)
        xyohaku = int((1080 - image.shape[1])/2)
    else:
        bairitsu = 1080/image.shape[1]
        image = cv2.resize(image, (1080,int(image.shape[0]*bairitsu)), interpolation=cv2.INTER_LANCZOS4)
        yyohaku = int((810 - image.shape[0])/2)
    return image, bairitsu, xyohaku, yyohaku

class Tab_scn_dic_align(tk.Frame):
    def canvas_update(self, data):
        img1 = imread(self.active_imgS)
        img2 = imread(self.active_imgD)
        msimg_imzml = ImzMLParser(self.active_imgM)
        heimsi = max([x for idx, (x,y,z) in enumerate(msimg_imzml.coordinates)])-min([x for idx, (x,y,z) in enumerate(msimg_imzml.coordinates)])+1
        widmsi = max([y for idx, (x,y,z) in enumerate(msimg_imzml.coordinates)])-min([y for idx, (x,y,z) in enumerate(msimg_imzml.coordinates)])+1
        heimsi = int(heimsi*data.msi_res.get()/data.gfp_res.get())
        widmsi = int(widmsi*data.msi_res.get()/data.gfp_res.get())
        img1 = cv2.resize(img1, dsize=None, fx=data.scn_res.get()/data.gfp_res.get(), fy=data.scn_res.get()/data.gfp_res.get())
        h, w = img2.shape[:2]
        angle_rad = data.scn_rotat_tup[self.index]*np.pi/180.0
        w_rot = int(np.round(h*np.absolute(np.sin(angle_rad))+w*np.absolute(np.cos(angle_rad))))
        h_rot = int(np.round(h*np.absolute(np.cos(angle_rad))+w*np.absolute(np.sin(angle_rad))))
        size_rot = (w_rot, h_rot)
        center = (w/2, h/2)
        rotation_matrix = cv2.getRotationMatrix2D(center, data.scn_rotat_tup[self.index] , 1)
        affine_matrix = rotation_matrix.copy()
        affine_matrix[0][2] = affine_matrix[0][2] -w/2 + w_rot/2
        affine_matrix[1][2] = affine_matrix[1][2] -h/2 + h_rot/2
        img2 = cv2.warpAffine(img2, affine_matrix, size_rot, flags=cv2.INTER_CUBIC)
        if (data.scn_ymove_tup[self.index] > 0):
            img_add = np.zeros((int(data.scn_ymove_tup[self.index]), img2.shape[1], 3), np.uint8)
            img2 = cv2.vconcat([img_add, img2])
        else:
            img2 = img2[int(-1*data.scn_ymove_tup[self.index]):img2.shape[0],:]
        if (data.scn_xmove_tup[self.index] > 0):
            img_add = np.zeros((img2.shape[0],int(data.scn_xmove_tup[self.index]), 3), np.uint8)
            img2 = cv2.hconcat([img_add, img2])
        else:
            img2 = img2[:, -1*int(data.scn_xmove_tup[self.index]):img2.shape[1]]
        if (img2.shape[0] < img1.shape[0]):
            img_add = np.zeros((img1.shape[0]-img2.shape[0], img2.shape[1], 3), np.uint8)
            img2 = cv2.vconcat([img2, img_add])
        else:
            img2 = img2[0:img1.shape[0],:]
        if (img2.shape[1] < img1.shape[1]):
            img_add = np.zeros((img2.shape[0],img1.shape[1]-img2.shape[1], 3), np.uint8)
            img2 = cv2.hconcat([img2, img_add])
        else:
            img2 = img2[:,0:img1.shape[1]]
        img1 = cv2.bitwise_not(img1)
        img1[:, :, (0,1)] = 0;
        self.img = cv2.addWeighted(img1, 1, img2, 1, 0)
        self.img, bairitsu, xyohaku, yyohaku = set_to_display(self.img)
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        self.img = Image.fromarray(self.img)
        self.img = ImageTk.PhotoImage(self.img)
        self.marge_canvas.delete("all")
        self.marge_canvas.create_image(540, 405, image=self.img)
        self.marge_canvas.create_rectangle((data.ms_xleft_tup[self.index]*bairitsu)+xyohaku,
                                           (data.ms_ytop_tup[self.index]*bairitsu)+yyohaku,
                                           ((data.ms_xleft_tup[self.index]+heimsi-1)*bairitsu)+xyohaku,
                                           ((data.ms_ytop_tup[self.index]+widmsi-1)*bairitsu)+yyohaku,
                                           outline="green")
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
    def Button_automarge_pushed(self, data=None):
        pass
    def Slct_img (self, event, data=None):
        if (self.Filebox.curselection()):
            self.index = self.Filebox.index(self.Filebox.curselection())
            self.active_imgS=data.scn_files_tup[self.index]
            self.active_imgD=data.dic_files_tup[self.index]
            self.active_imgM=data.msi_files_tup[self.index]
            self.cur_x.set(data.scn_xmove_tup[self.index])
            self.cur_y.set(data.scn_ymove_tup[self.index])
            self.cur_r.set(data.scn_rotat_tup[self.index])
            self.cur_msxleft.set(data.ms_xleft_tup[self.index])
            self.cur_msytop.set(data.ms_ytop_tup[self.index])
            self.canvas_update(data=data)
    def __init__(self, master=None, data=None):
        self.tab = tk.Frame(master)
        master.add(self.tab, text='Align', padding=3, state=tk.DISABLED) #, state=data.tab_scn_dic_align_activity)
        self.index = None
        self.active_imgS = None
        self.active_imgD = None
        self.active_imgM = None
        self.cur_x = tk.DoubleVar()
        self.cur_y = tk.DoubleVar()
        self.cur_r = tk.DoubleVar()
        self.cur_msxleft = tk.DoubleVar()
        self.cur_msytop = tk.DoubleVar()
        self.spc1 = tk.Label(self.tab, text="", padx=125)
        self.spc1.grid(row=0,column=0, sticky=tk.W)
        self.button_marge = tk.Button(self.tab, text="automarge", command=lambda: self.Button_automarge_pushed(data=data))
        self.button_marge.grid(row=0,column=1, sticky=tk.W)
        self.label_curx = tk.Label(self.tab, text="  x:")
        self.label_curx.grid(row=0,column=2, sticky=tk.W)
        self.text_curx = tk.Entry(self.tab, textvariable=self.cur_x, width=10)
        self.text_curx.bind("<Up>"    , lambda event :   self.Up_pushed(self, val=self.cur_x, data=data, tup=data.scn_xmove_tup, idx=self.index))
        self.text_curx.bind("<Down>"  , lambda event : self.Down_pushed(self, val=self.cur_x, data=data, tup=data.scn_xmove_tup, idx=self.index))
        self.text_curx.bind("<Return>", lambda event :self.Enter_pushed(self, val=self.cur_x, data=data, tup=data.scn_xmove_tup, idx=self.index))
        self.text_curx.bind("<Tab>"   , lambda event :self.Enter_pushed(self, val=self.cur_x, data=data, tup=data.scn_xmove_tup, idx=self.index))
        self.text_curx.grid(row=0,column=3, sticky=tk.W)
        self.label_cury = tk.Label(self.tab, text="  y:")
        self.label_cury.grid(row=0,column=4, sticky=tk.W)
        self.text_cury = tk.Entry(self.tab, textvariable=self.cur_y, width=10)
        self.text_cury.bind("<Up>"   ,  lambda event :   self.Up_pushed(self, val=self.cur_y, data=data, tup=data.scn_ymove_tup, idx=self.index))
        self.text_cury.bind("<Down>" ,  lambda event : self.Down_pushed(self, val=self.cur_y, data=data, tup=data.scn_ymove_tup, idx=self.index))
        self.text_cury.bind("<Return>", lambda event :self.Enter_pushed(self, val=self.cur_y, data=data, tup=data.scn_ymove_tup, idx=self.index))
        self.text_cury.bind("<Tab>"  ,  lambda event :self.Enter_pushed(self, val=self.cur_y, data=data, tup=data.scn_ymove_tup, idx=self.index))
        self.text_cury.grid(row=0,column=5, sticky=tk.W)
        self.label_curr = tk.Label(self.tab, text="  rotate:")
        self.label_curr.grid(row=0,column=6, sticky=tk.W)
        self.text_curr = tk.Entry(self.tab, textvariable=self.cur_r, width=10)
        self.text_curr.bind("<Up>",     lambda event :   self.Up_pushed(self, val=self.cur_r, data=data, tup=data.scn_rotat_tup, idx=self.index))
        self.text_curr.bind("<Down>",   lambda event : self.Down_pushed(self, val=self.cur_r, data=data, tup=data.scn_rotat_tup, idx=self.index))
        self.text_curr.bind("<Return>", lambda event :self.Enter_pushed(self, val=self.cur_r, data=data, tup=data.scn_rotat_tup, idx=self.index))
        self.text_curr.bind("<Tab>"   , lambda event :self.Enter_pushed(self, val=self.cur_r, data=data, tup=data.scn_rotat_tup, idx=self.index))
        self.text_curr.grid(row=0,column=7, sticky=tk.W)
        self.label_msxleft = tk.Label(self.tab, text="  x for imaging start:")
        self.label_msxleft.grid(row=0,column=8, sticky=tk.W)
        self.text_msxleft = tk.Entry(self.tab, textvariable=self.cur_msxleft, width=10)
        self.text_msxleft.bind("<Up>"    , lambda event :   self.Up_pushed(self, val=self.cur_msxleft, data=data, tup=data.ms_xleft_tup, idx=self.index))
        self.text_msxleft.bind("<Down>"  , lambda event : self.Down_pushed(self, val=self.cur_msxleft, data=data, tup=data.ms_xleft_tup, idx=self.index))
        self.text_msxleft.bind("<Return>", lambda event :self.Enter_pushed(self, val=self.cur_msxleft, data=data, tup=data.ms_xleft_tup, idx=self.index))
        self.text_msxleft.bind("<Tab>"   , lambda event :self.Enter_pushed(self, val=self.cur_msxleft, data=data, tup=data.ms_xleft_tup, idx=self.index))
        self.text_msxleft.grid(row=0,column=9, sticky=tk.W)
        self.label_msytop = tk.Label(self.tab, text="  y for imaging start:")
        self.label_msytop.grid(row=0,column=10, sticky=tk.W)
        self.text_msytop = tk.Entry(self.tab, textvariable=self.cur_msytop, width=10)
        self.text_msytop.bind("<Up>"   ,  lambda event :   self.Up_pushed(self, val=self.cur_msytop, data=data, tup=data.ms_ytop_tup, idx=self.index))
        self.text_msytop.bind("<Down>" ,  lambda event : self.Down_pushed(self, val=self.cur_msytop, data=data, tup=data.ms_ytop_tup, idx=self.index))
        self.text_msytop.bind("<Return>", lambda event :self.Enter_pushed(self, val=self.cur_msytop, data=data, tup=data.ms_ytop_tup, idx=self.index))
        self.text_msytop.bind("<Tab>"  ,  lambda event :self.Enter_pushed(self, val=self.cur_msytop, data=data, tup=data.ms_ytop_tup, idx=self.index))
        self.text_msytop.grid(row=0,column=11, sticky=tk.W)
        self.spc2 = tk.Label(self.tab, text="", padx=125)
        self.spc2.grid(row=0,column=12, sticky=tk.W)
        self.img = Image.open('Unread_img.png')
        self.img = ImageTk.PhotoImage(self.img)
        self.marge_canvas = tk.Canvas(self.tab, bg = "black", width=1081, height=811)
        self.marge_canvas.grid(row=1, column=0, columnspan=12, rowspan=2)
        self.marge_canvas.create_image(540, 405, image=self.img)
        self.Filebox = tk.Listbox(self.tab, listvariable=data.scn_files, width=61, height=49, fg="black") # need scroll bar
        self.Filebox.grid(row=1, column=12, sticky=tk.S)
        self.yscrollbar = ttk.Scrollbar(self.tab,orient=tk.VERTICAL,command=self.Filebox.yview)
        self.Filebox['yscrollcommand'] = self.yscrollbar.set
        self.yscrollbar.grid(row=1, column=13, sticky=(tk.NS))
        self.xscrollbar = ttk.Scrollbar(self.tab,orient=tk.HORIZONTAL,command=self.Filebox.xview)
        self.Filebox['xscrollcommand'] = self.xscrollbar.set
        self.xscrollbar.grid(row=2, column=12, sticky=(tk.W,tk.E))
        self.Filebox.bind("<<ListboxSelect>>", lambda event:self.Slct_img(self, data=data))
        self.Filebox.bind("<Control-a>", lambda event:self.Slct_img(self, data=data))
