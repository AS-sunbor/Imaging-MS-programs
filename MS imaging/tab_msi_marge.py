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
        img_add = np.zeros((image.shape[0],int(xsiz)-image.shape[1], 3), np.uint8)
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
        xyohaku = (1080 - image.shape[1])/2
    else:
        bairitsu = 1080/image.shape[1]
        image = cv2.resize(image, (1080,int(image.shape[0]*bairitsu)), interpolation=cv2.INTER_LANCZOS4)
        yyohaku = (810 - image.shape[0])/2
    return image, bairitsu, xyohaku, yyohaku

class Tab_msi_marge(tk.Frame):
    def Slct_img(self, event, data=None):
        if (self.Filebox.curselection()):
            self.index = self.Filebox.index(self.Filebox.curselection())
            self.Update_img(data=data)

    def Slct_mpz(self, event, data=None):
        index = self.mpzbox.index(self.mpzbox.curselection())
        if (self.RGB.get() == "R"):
            self.maxr.set(100.0)
            self.mzminr.set(data.mz_values_tup[index][0])
            self.mzmaxr.set(data.mz_values_tup[index][1])
        if (self.RGB.get() == "G"):
            self.maxg.set(100.0)
            self.mzming.set(data.mz_values_tup[index][0])
            self.mzmaxg.set(data.mz_values_tup[index][1])
        if (self.RGB.get() == "B"):
            self.maxb.set(100.0)
            self.mzminb.set(data.mz_values_tup[index][0])
            self.mzmaxb.set(data.mz_values_tup[index][1])
        if (self.Filebox.curselection()):
            self.Update_img(data=data)

    def Update_img(self, data=None):
        scn_img = imread(data.scn_files_tup[self.index])
        msimg_imzml = ImzMLParser(data.msi_files_tup[self.index])
        minx = min([x for idx, (x,y,z) in enumerate(msimg_imzml.coordinates)])
        miny = min([y for idx, (x,y,z) in enumerate(msimg_imzml.coordinates)])
        maxx = max([x for idx, (x,y,z) in enumerate(msimg_imzml.coordinates)])
        maxy = max([y for idx, (x,y,z) in enumerate(msimg_imzml.coordinates)])
        msimg_floatr = np.zeros((maxx+1-minx,maxy-miny+1))
        msimg_floatg = np.zeros((maxx+1-minx,maxy-miny+1))
        msimg_floatb = np.zeros((maxx+1-minx,maxy-miny+1))
        ranger = []
        rangeg = []
        rangeb = []
        for idx, (x,y,z) in enumerate(msimg_imzml.coordinates):
            mzs, intensities = msimg_imzml.getspectrum(idx)
            ranger = [i for i, v in enumerate(mzs) if self.mzminr.get()<=v<=self.mzmaxr.get()]
            rangeg = [i for i, v in enumerate(mzs) if self.mzming.get()<=v<=self.mzmaxg.get()]
            rangeb = [i for i, v in enumerate(mzs) if self.mzminb.get()<=v<=self.mzmaxb.get()]
            break
        for idx, (x,y,z) in enumerate(msimg_imzml.coordinates):
            mzs, intensities = msimg_imzml.getspectrum(idx)
            msimg_floatr[x-minx,y-miny] = max([intensities[i] for i in ranger])
            msimg_floatg[x-minx,y-miny] = max([intensities[i] for i in rangeg])
            msimg_floatb[x-minx,y-miny] = max([intensities[i] for i in rangeb])
        msimg_floatr[msimg_floatr < 0] = 0
        msimg_floatg[msimg_floatg < 0] = 0
        msimg_floatb[msimg_floatb < 0] = 0
        msimg_floatr[msimg_floatr > self.maxr.get()] = self.maxr.get()
        msimg_floatg[msimg_floatg > self.maxg.get()] = self.maxg.get()
        msimg_floatb[msimg_floatb > self.maxb.get()] = self.maxb.get()
        msimg_intr = np.array(msimg_floatr*255/self.maxr.get(), np.uint8)
        msimg_intg = np.array(msimg_floatg*255/self.maxg.get(), np.uint8)
        msimg_intb = np.array(msimg_floatb*255/self.maxb.get(), np.uint8)
        self.img = np.dstack([msimg_intb.T, msimg_intg.T, msimg_intr.T])
        if (self.interpolation_list.get() == "None"):
            self.img = cv2.resize(self.img, (int((maxx+1-minx)*data.msi_res.get()/data.gfp_res.get()),int((maxy+1-miny)*data.msi_res.get()/data.gfp_res.get())), interpolation=cv2.INTER_NEAREST)
        elif (self.interpolation_list.get() == "linear"):
            self.img = cv2.resize(self.img, (int((maxx+1-minx)*data.msi_res.get()/data.gfp_res.get()),int((maxy+1-miny)*data.msi_res.get()/data.gfp_res.get())), interpolation=cv2.INTER_LINEAR)
        elif (self.interpolation_list.get() == "cubic"):
            self.img = cv2.resize(self.img, (int((maxx+1-minx)*data.msi_res.get()/data.gfp_res.get()),int((maxy+1-miny)*data.msi_res.get()/data.gfp_res.get())), interpolation=cv2.INTER_CUBIC)
        elif (self.interpolation_list.get() == "Lanczos"):
            self.img = cv2.resize(self.img, (int((maxx+1-minx)*data.msi_res.get()/data.gfp_res.get()),int((maxy+1-miny)*data.msi_res.get()/data.gfp_res.get())), interpolation=cv2.INTER_LANCZOS4)
        self.img = img_position(self.img, int(data.ms_xleft_tup[self.index]), int(data.ms_ytop_tup[self.index]), int(scn_img.shape[1]*data.scn_res.get()/data.gfp_res.get()), int(scn_img.shape[0]*data.scn_res.get()/data.gfp_res.get()))
        if (self.filter_list.get() == "by cell region"):
            gfp_img = imread(data.gfp_files_tup[self.index])
            h, w = gfp_img.shape[:2]
            angle_rad = data.scn_rotat_tup[self.index]*np.pi/180.0
            w_rot = int(np.round(h*np.absolute(np.sin(angle_rad))+w*np.absolute(np.cos(angle_rad))))
            h_rot = int(np.round(h*np.absolute(np.cos(angle_rad))+w*np.absolute(np.sin(angle_rad))))
            size_rot = (w_rot, h_rot)
            center = (w/2, h/2)
            rotation_matrix = cv2.getRotationMatrix2D(center, data.scn_rotat_tup[self.index] , 1)
            affine_matrix = rotation_matrix.copy()
            affine_matrix[0][2] = affine_matrix[0][2] -w/2 + w_rot/2
            affine_matrix[1][2] = affine_matrix[1][2] -h/2 + h_rot/2
            gfp_img = cv2.warpAffine(gfp_img, affine_matrix, size_rot, flags=cv2.INTER_CUBIC)
            gfp_img = img_position(gfp_img, data.scn_xmove_tup[self.index], data.scn_ymove_tup[self.index], int(scn_img.shape[1]*data.scn_res.get()/data.gfp_res.get()), int(scn_img.shape[0]*data.scn_res.get()/data.gfp_res.get()))
            gfp_img = cv2.cvtColor(gfp_img, cv2.COLOR_BGR2GRAY)
            ret, gfp_img = cv2.threshold(gfp_img, data.gfp_thr_tup[self.index], 255, cv2.THRESH_BINARY)
            gfp_img = gfp_img/255
            gfp_img = gfp_img.astype(np.uint8)
            gfp_img = np.dstack([gfp_img, gfp_img, gfp_img])
            self.img = self.img * gfp_img
        if (self.marge_check1.get()=='1'):
            dic_img = imread(data.dic_files_tup[self.index])
            h, w = dic_img.shape[:2]
            angle_rad = -1*data.scn_rotat_tup[self.index]*np.pi/180.0
            w_rot = int(np.round(h*np.absolute(np.sin(angle_rad))+w*np.absolute(np.cos(angle_rad))))
            h_rot = int(np.round(h*np.absolute(np.cos(angle_rad))+w*np.absolute(np.sin(angle_rad))))
            size_rot = (w_rot, h_rot)
            center = (w/2, h/2)
            rotation_matrix = cv2.getRotationMatrix2D(center, data.scn_rotat_tup[self.index] , 1)
            affine_matrix = rotation_matrix.copy()
            affine_matrix[0][2] = affine_matrix[0][2] -w/2 + w_rot/2
            affine_matrix[1][2] = affine_matrix[1][2] -h/2 + h_rot/2
            dic_img = cv2.warpAffine(dic_img, affine_matrix, size_rot, flags=cv2.INTER_CUBIC)
            dic_img = img_position(dic_img, data.scn_xmove_tup[self.index], data.scn_ymove_tup[self.index], int(scn_img.shape[1]*data.scn_res.get()/data.gfp_res.get()), int(scn_img.shape[0]*data.scn_res.get()/data.gfp_res.get()))
            self.img = cv2.add(dic_img,self.img)
        if (self.marge_check2.get()=='1'):
            scn_img = cv2.resize(scn_img, (int(scn_img.shape[1]*data.scn_res.get()/data.gfp_res.get()), int(scn_img.shape[0]*data.scn_res.get()/data.gfp_res.get())), interpolation=cv2.INTER_LANCZOS4)
            self.img = cv2.add(scn_img,self.img)

        self.img, bairitsu, xyohaku, yyohaku = set_to_display(self.img)
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        self.img = Image.fromarray(self.img)
        self.img = ImageTk.PhotoImage(self.img)
        self.marge_canvas.create_image(540, 405, image=self.img)

    def Edit_Pushed(self, data, mpzbox=None):
        self.newWindow = tk.Toplevel(self.tab)
        self.lay.append(self.newWindow)
        self.newWindow.geometry("300x300")
        label = tk.Label(self.newWindow, text = "m/z list")
        txt = tk.Text(self.newWindow)
        buttonimporttxt = tk.Button(self.newWindow, text = "Import m/z list from text", command=lambda: self.get_mpz(text_widget=txt))
        buttonimportimzml = tk.Button(self.newWindow, text = "Import m/z list from imzml", command=lambda: self.get_mpz2(text_widget=txt))
        buttonback = tk.Button(self.newWindow, text = "save and exit", command=lambda: self.save(text_widget=txt, data=data, mpzbox=mpzbox))
        buttonimporttxt.pack()
        buttonimportimzml.pack()
        buttonback.pack()
        label.pack()
        txt.pack()

    def get_mpz(self, text_widget=None):
        path = tk.filedialog.askopenfilename(filetypes = [("","*")])
        with open (path, mode='r') as f:
            s = f.read()
            text_widget.delete('1.0', 'end')
            text_widget.insert('1.0', s)

    def get_mpz(self, text_widget=None):
        path = tk.filedialog.askopenfilename(filetypes = [("","*")])
        with open (path, mode='r') as f:
            s = f.read()
            text_widget.delete('1.0', 'end')
            text_widget.insert('1.0', s)

    def save(self, text_widget=None, data=None, mpzbox=None):
        s = text_widget.get('1.0', 'end')
        s = s.replace(',','±')
        s = re.sub('\n+$','', s)
        l1 = s.split(sep='\n')
        l2 = [l1[i].split(sep='±') for i in range(len(l1))]
        data.mz_values.set(l1)
        data.mz_values_tup = [[float(l2[i][0])-float(l2[i][1]),float(l2[i][0])+float(l2[i][1])] for i in range(len(l2))]
        self.newWindow.destroy()

    def select_cb(self, event, data=None):
        #if (self.Filebox.curselection()):
        self.Update_img(data=data)

    def marge1_pushed(self, data=None):
        if (self.marge_check1=='1'):
            self.marge_check2.set('0')
        self.Update_img(data=data)
    def marge2_pushed(self, data=None):
        if (self.marge_check2=='1'):
            self.marge_check1.set('0')
        self.Update_img(data=data)

    def __init__(self, master=None, data=None):
        self.tab = tk.Frame(master)
        self.lay = []
        self.index = 0
        master.add(self.tab, text='Marge', padding=3, state=tk.DISABLED) #, state=data.tab_msi_marge_activity)
        self.interpolation_txt =  tk.Label(self.tab, text="Interpolation method :", width=17)
        self.interpolation_txt.grid(row=0, column=0)
        self.interpolation_list = ttk.Combobox(self.tab, values=["None","linear","cubic","Lanczos"])
        self.interpolation_list.current(0)
        self.interpolation_list.grid(row=0, column=1)
        self.interpolation_list.bind('<<ComboboxSelected>>' , lambda event : self.select_cb(self, data=data))
        self.filter_txt =  tk.Label(self.tab, text="Filter method :", width=10)
        self.filter_txt.grid(row=0, column=2)
        self.filter_list = ttk.Combobox(self.tab, values=["None","by cell region", "single value / single cell"])
        self.filter_list.current(0)
        self.filter_list.grid(row=0, column=3)
        self.filter_list.bind('<<ComboboxSelected>>' , lambda event : self.select_cb(self, data=data))
        self.free_txt =  tk.Label(self.tab, text="", width=40)
        self.free_txt.grid(row=0, column=5)
        self.marge_check1 = tk.StringVar()
        self.marge_check1.set('0')
        self.marge = tk.Checkbutton(self.tab, text='marge DIC', onvalue='1', offvalue='0', variable=self.marge_check1, command=lambda :self.marge1_pushed(data=data))
        self.marge.grid(row=0, column=5)
        self.marge_check2 = tk.StringVar()
        self.marge_check2.set('0')
        self.marge2 = tk.Checkbutton(self.tab, text='marge scan', onvalue='1', offvalue='0', variable=self.marge_check2, command=lambda :self.marge2_pushed(data=data))
        self.marge2.grid(row=0, column=6)
        self.img = Image.open('Unread_img.png')
        self.img = ImageTk.PhotoImage(self.img)
        self.marge_canvas = tk.Canvas(self.tab, bg = "black", width=1081, height=811)
        self.marge_canvas.grid(row=1, column=0, columnspan=7, rowspan=8)
        self.marge_canvas.create_image(540, 405, image=self.img)
        self.Fileboxtxt = tk.Label(self.tab, text="Files", width=10)
        self.Fileboxtxt.grid(row=1, column=7, sticky=tk.S)
        self.Filebox = tk.Listbox(self.tab, listvariable=data.msi_files, width=30, height=48, fg="black") # need scroll bar
        self.Filebox.grid(row=2, column=7, rowspan=5, sticky=tk.S)
        self.yscrollbar = ttk.Scrollbar(self.tab,orient=tk.VERTICAL,command=self.Filebox.yview)
        self.Filebox['yscrollcommand'] = self.yscrollbar.set
        self.yscrollbar.grid(row=2, column=8, rowspan=5, sticky=(tk.NS))
        self.xscrollbar = ttk.Scrollbar(self.tab,orient=tk.HORIZONTAL,command=self.Filebox.xview)
        self.Filebox['xscrollcommand'] = self.xscrollbar.set
        self.xscrollbar.grid(row=7, column=7, sticky=(tk.W,tk.E))
        self.Filebox.bind("<<ListboxSelect>>", lambda event : self.Slct_img(self, data=data))
        self.mpzboxtxt = tk.Label(self.tab, text="m/z", width=10)
        self.mpzboxtxt.grid(row=1, column=9, columnspan=2, sticky=tk.S)
        self.Labelframe = tk.Label(self.tab, text="Color", width=4)
        self.Labelframe.grid(row=2,column=9)
        self.RGB = tk.StringVar()
        rbr = ttk.Radiobutton(self.tab,text='R',value='R',variable=self.RGB)
        rbg = ttk.Radiobutton(self.tab,text='G',value='G',variable=self.RGB)
        rbb = ttk.Radiobutton(self.tab,text='B',value='B',variable=self.RGB)
        rbr.grid(row=3,column=9)
        rbg.grid(row=4,column=9)
        rbb.grid(row=5,column=9)
        self.max_intensitytxt = tk.Label(self.tab, text="max", width=6)
        self.max_intensitytxt.grid(row=2,column=10)
        self.maxr = tk.DoubleVar()
        self.maxrbox = tk.Entry(self.tab, textvariable=self.maxr, width=6)
        self.maxrbox.grid(row=3,column=10)
        self.maxg = tk.DoubleVar()
        self.maxgbox = tk.Entry(self.tab, textvariable=self.maxg, width=6)
        self.maxgbox.grid(row=4,column=10)
        self.maxb = tk.DoubleVar()
        self.maxbbox = tk.Entry(self.tab, textvariable=self.maxb, width=6)
        self.maxbbox.grid(row=5,column=10)
        self.mzmintxt = tk.Label(self.tab, text="m/z", width=6)
        self.mzmintxt.grid(row=2,column=11,columnspan=3)
        self.mzminr = tk.DoubleVar()
        self.mzminrbox = tk.Entry(self.tab, textvariable=self.mzminr, width=6)
        self.mzminrbox.grid(row=3,column=11)
        self.mzming = tk.DoubleVar()
        self.mzmingbox = tk.Entry(self.tab, textvariable=self.mzming, width=6)
        self.mzmingbox.grid(row=4,column=11)
        self.mzminb = tk.DoubleVar()
        self.mzminbbox = tk.Entry(self.tab, textvariable=self.mzminb, width=6)
        self.mzminbbox.grid(row=5,column=11)
        self.minustxt1 = tk.Label(self.tab, text="-")
        self.minustxt1.grid(row=3,column=12)
        self.minustxt2 = tk.Label(self.tab, text="-")
        self.minustxt2.grid(row=4,column=12)
        self.minustxt3 = tk.Label(self.tab, text="-")
        self.minustxt3.grid(row=5,column=12)
        self.mzmaxr = tk.DoubleVar()
        self.mzmaxrbox = tk.Entry(self.tab, textvariable=self.mzmaxr, width=6)
        self.mzmaxrbox.grid(row=3,column=13)
        self.mzmaxg = tk.DoubleVar()
        self.mzmaxgbox = tk.Entry(self.tab, textvariable=self.mzmaxg, width=6)
        self.mzmaxgbox.grid(row=4,column=13)
        self.mzmaxb = tk.DoubleVar()
        self.mzmaxbbox = tk.Entry(self.tab, textvariable=self.mzmaxb, width=6)
        self.mzmaxbbox.grid(row=5,column=13)
        self.mpzbox = tk.Listbox(self.tab, width=30, height=42, listvariable=data.mz_values, fg="black") # need scroll bar
        self.mpzbox.grid(row=6, column=9, columnspan=5, sticky=tk.S)
        self.yscrollbarmpz = ttk.Scrollbar(self.tab,orient=tk.VERTICAL,command=self.mpzbox.yview)
        self.mpzbox['yscrollcommand'] = self.yscrollbarmpz.set
        self.yscrollbarmpz.grid(row=6, column=14, sticky=(tk.NS))
        self.xscrollbarmpz = ttk.Scrollbar(self.tab,orient=tk.HORIZONTAL,command=self.mpzbox.xview)
        self.mpzbox['xscrollcommand'] = self.xscrollbarmpz.set
        self.xscrollbarmpz.grid(row=7, column=9, columnspan=5, sticky=(tk.W,tk.E))
        self.mpzbox.bind("<<ListboxSelect>>", lambda event: self.Slct_mpz(self, data=data))
        self.mpzeditbutton = tk.Button(self.tab, text="edit list", command=lambda: self.Edit_Pushed(data=data, mpzbox=self.mpzbox))
        self.mpzeditbutton.grid(row=1, column=11, columnspan=2, sticky=tk.S)
        self.button_update = tk.Button(self.tab, text="update", command=lambda :self.Update_img(data=data))
        self.button_update.grid(row=0, column=4)
        
        #ここからデバッグ終了時に消すところ#
        self.maxr.set(437.5)
        self.maxg.set(68.2)
        self.maxb.set(86.6)
        self.mzminr.set(1006.41236)
        self.mzming.set(1149.47096)
        self.mzminb.set(1158.53829)
        self.mzmaxr.set(1006.81236)
        self.mzmaxg.set(1149.87096)
        self.mzmaxb.set(1158.93829)
        #ここまでデバッグ終了時に消すところ#

