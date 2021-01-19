# Imports
import os
import tkinter as tk
from os import listdir
from os.path import isfile, join
from tkinter import filedialog
from PIL import Image
import cv2
import numpy as np
from matplotlib import pyplot as plt


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
    # Create folder to hold finalized jpg of found clots
    newpath = path + '/tiffjpg/'
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    info.pathtoframesfolder = newpath
    im = Image.open(path + '\\' + arr[0])

    # Save file as JPG
    name = str(newpath + arr[0]).rstrip(".tif")
    jpg = name + '.jpg'
    im.save(jpg, 'JPEG', quality=100)
    impath = jpg
    imjpg = cv2.imread(impath)
    imjpg = cv2.resize(imjpg, (800, 800))

    # cv2.selectROI("Frame", imtojpg, showCrosshair=True, fromCenter=False)
    # https://stackoverflow.com/questions/52212239/opencv-plot-contours-in-an-image
    # Grayscale image
    # imgtojpgbw = cv2.cvtColor(imjpg, cv2.COLOR_BGR2GRAY)
    croppedareas = cv2.selectROIs("Select Rois", imjpg, fromCenter=False)
    cropnum = 0
    for rect in croppedareas:
        print(rect)
        x1 = rect[0]
        y1 = rect[1]
        x2 = rect[2]
        y2 = rect[3]

        imgcropped = imjpg[y1:y1+y2, x1:x1+x2]
        cv2.imshow("crop " + str(cropnum), imgcropped)
        cv2.imwrite(str(info.pathtoframesfolder) + "crop"+str(cropnum) + ".jpeg", imgcropped)
        cropnum += 1

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print("Got here")



    # Contour the crops
    # Open to Show Confirmation

    # Then, add all the cropped contours into the original picture
    # https://stackoverflow.com/questions/36533540/how-to-copy-a-cropped-image-onto-the-original-one-given-the-coordinates-of-the
    # Use this link to add cropped back into original picture

    # Save the now contoured image as a JPG
    # Show picture for confirmation


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


def next_frame():
    # go to next frame in tiff file
    info.counter += 1
    app.lbl.config(text="Current Frame: " + str(info.counter))


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
