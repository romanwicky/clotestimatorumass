# Imports
import os
import tkinter as tk
from os import listdir
from os.path import isfile, join
from tkinter import filedialog
from PIL import Image


class Info:
    def __init__(self, dirpath, counter, pathtoframesfolder):
        self.dirpath = dirpath
        self.counter = counter
        self.pathtoframesfolder = pathtoframesfolder
        self.listtiff = []


info = Info("", 0, "")


# Algo Functions
# Algo 1:
# Click on any pixel that is part of the clot, do a DFS for all pixels connected to that pixel
# Add a threshold for max size of clot
# Image thresholding to get rid of uneeded pixels that may interfere with DFS
# Algo 2:
# Select an ROI that contains the clot
# Create bounding boxes for all shapes
# Only return the clot we want - User selection
def clot_dfs(path, arr):
    newpath = path + '/tiffjpg/'
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    info.pathtoframesfolder = newpath
    im = Image.open(path + '\\' + arr[0])

    # Save file as JPG
    name = str(newpath + arr[0]).rstrip(".tif")
    im.save(name + '.jpg', 'JPEG')
    # im.dtype is uint8 and not uint16 as desired.
    # specifying dtype as uint16 does not correct this
    # regions = cv2.selectROIs("Select Regions Of Interest", img, fromCenter=False)
    #"http://creativemorphometrics.co.vu/blog/2014/08/05/automated-outlines-with-opencv-in-python/"
    # Link on how to threshold images to get bounding boxes, should help make clots more clear
    # output as png
    # img = cv2.imread(path)
    # cv2.normalize(img, dst=None, alpha=0, beta=65535, norm_type=cv2.NORM_MINMAX)
    # cv2.imshow("IMG", img)
    return 0
    # Notes
    # cv2.selectRois() = multiple ROIs if needed from one image
    # Enter with no ROI = no clot found

def select_tif():
    # Open File
    filelog_ext = ".tif"
    rep = filedialog.askdirectory(
        parent=app,
        title="Select TIFF Directory to Process",
        initialdir='/')
    info.dirpath = rep
    # last element in array placeholder, arr-2 needed for loop
    arr = [f for f in listdir(info.dirpath) if isfile(join(info.dirpath, f))]
    info.listtiff = arr


def process_tiff():
    clot_dfs(info.dirpath, info.listtiff)
    info.counter += 1
    app.lbl.config(text="Current Frame: " + str(info.counter))
    print(info.listtiff)



def next_frame():
    # go to next frame in tiff file
    print("hey")


# lambda: allows the methods to be used on demand, not just when the application launches
# without lambda: in the command section of the button, the methods won't execute when we want
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.btn = tk.Button(self, text="Select Folder",
                             command=lambda: select_tif())
        self.btn.pack(padx=120, pady=30)
        self.btn.config(font=("Montserrat", 20))

        self.btn = tk.Button(self, text="Process TIFF Files",
                             command=lambda: process_tiff())
        self.btn.pack(padx=120, pady=30)
        self.btn.config(font=("Montserrat", 20))
        self.btn = tk.Button(self, text="Next TIFF File",
                             command=lambda: next_frame())
        self.btn.pack(padx=120, pady=30)
        self.btn.config(font=("Montserrat", 20))
        self.lbl = tk.Label(self, text="Current frame: " + str(info.counter))
        self.lbl.config(font=("Montserrat", 20))
        self.lbl.pack(padx=120, pady=30)
        self.lbl.config(relief=tk.RAISED)


if __name__ == "__main__":
    app = App()
    app.title("Clot Estimator - Roman Wicky van Doyer 2021")
    app.mainloop()
