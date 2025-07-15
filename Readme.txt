                     ** Imaging MS progmram Read me**


This program is written in python and run on the windows 10, 11 or later. Please install Anaconda for Windows including python 3.9.

In the Anaconda power shell, type 'python main.py', then packages which should be installed are shown. Please install them. 

Generally, the following steps will be needed to run the program.
("\Users\admin" will be changed depending on the user environment). 

(base) C:\Users\admin conda install open cv
↓
Please enter "y"
↓
(base) C:\Users\admin conda install -c bioconda wheezy.template
↓
(base) C:\Users\admin pip install pyimzml
↓
(base) C:\Users\admin pip install opencv-rolling-ball
↓
Please change path in the file "tab_sort_files.py" in the "MS imaging" folder  depending on your environment.
↓
(base) C:\Users\admin python main.py



Please store images of DIC, GFP, scan in the imaging MS, and imzML data in each folder. 

If you encountered any errors in the Git version, please try an alternative download at https://zenodo.org/records/7297174.
