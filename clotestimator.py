# Imports
import os
import tkinter as tk
from os import listdir
from os.path import isfile, join
from tkinter import filedialog
from PIL import Image
import cv2
from infoclass import Info
import numpy as np

info = Info("", 0, "")


# TODO: Have user click on region on image, remove ROI selection and instead make 50x50 square from user click
# TODO: Fix up thresholding to not remove light clots
# TODO: fix naming of output files to keep track of files better
# TODO: Check edge case scenarios with UI to minimize bugs

# Algo Functions
# Algo 1:
# Click on any pixel that is part of the clot, do a DFS for all pixels connected to that pixel
# Add a threshold for max size of clot
# Image thresholding to get rid of uneeded pixels that may interfere with DFS
# Algo 2:
# Select an ROI that contains the clot
# Create bounding boxes for all shapes
# Only return the clot we want - User selection
def clot_finder(framearray):
    im = Image.open(info.dirpath + '\\' + framearray[info.counter])
    # Save file as JPG
    name = str(info.pathtoframesfolder + framearray[info.counter]).rstrip(".tif")
    jpg = name + '.jpg'
    im.save(jpg, 'JPEG', quality=100)
    impath = jpg
    imjpg = cv2.imread(impath)
    imjpg = cv2.resize(imjpg, (800, 800))

    # cv2.selectROI("Frame", imtojpg, showCrosshair=True, fromCenter=False)
    # https://stackoverflow.com/questions/52212239/opencv-plot-contours-in-an-image
    # Grayscale image
    # imgtojpgbw = cv2.cvtColor(imjpg, cv2.COLOR_BGR2GRAY)
    # TODO: Change this to click rather than ROI
    # TODO: Need to allow for user to click multiple times on image
    # TODO: Create live rectangles to show where user clicked and what region will be scanned
    # TODO: Allow user to move an delete regions
    # TODO: Hough Transform OpenCV
    croppedareas = cv2.selectROIs(str(impath), imjpg, fromCenter=False)
    # If we don't have any clot, skip the frame altogether, but still count it
    if not croppedareas:
        cv2.destroyAllWindows()
        info.counter += 1
        return
    cropnum = 0
    for rect in croppedareas:
        print(rect)
        x1 = rect[0]
        y1 = rect[1]
        x2 = rect[2]
        y2 = rect[3]

        imgcropped = imjpg[y1:y1 + y2, x1:x1 + x2]
        cv2.imshow("crop " + str(cropnum), imgcropped)
        cv2.imwrite(str(info.pathtoframesfolder) + "crop" + str(cropnum) + ".jpg", imgcropped)
        cropnum += 1

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    thresh = None

    for i in range(0, cropnum):
        im = cv2.imread(info.pathtoframesfolder + "crop" + str(i) + ".jpg")
        imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        # Mess with the thresholding
        # TODO: Maybe denoise instead of bluring
        blur = cv2.GaussianBlur(imgray, (5, 5), 0)
        thresh = cv2.threshold(blur, 0, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C + cv2.THRESH_OTSU)[1]
        cnts, h = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for layer in zip(cnts, h[0]):
            contour = layer[0]
            cv2.drawContours(im, [contour], -1, (36, 255, 12), 2)

    cv2.imshow("Thresh", thresh)
    cv2.imshow("Image", im)
    cv2.imwrite(info.pathtoframesfolder + 'thresh' + str(info.counter) + '.jpg', thresh)
    cv2.imwrite(info.pathtoframesfolder + 'image' + str(info.counter) + '.jpg', im)
    cv2.waitKey(0)

    cv2.destroyAllWindows()


def select_tif():
    # Open Directory
    try:
        rep = filedialog.askdirectory(
            parent=app,
            title="Select TIFF Directory to Process",
            initialdir='/')
        info.dirpath = rep
        # last element in array placeholder, arr-2 needed for loop
        # TODO: Check to make sure only TIFF files are added into array
        arr = [f for f in listdir(info.dirpath) if isfile(join(info.dirpath, f))]
        info.listtiff = arr
        app.btn1.config(state='disabled')
    except FileNotFoundError:
        # Popup
        popupmsg(0)


def process_tiff():
    # Create folder to hold finalized jpg of found clots
    newpath = info.dirpath + '/tiffjpg/'
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    info.pathtoframesfolder = newpath
    app.btn2.config(state='disabled')
    clot_finder(info.listtiff)


def next_frame():
    # go to next frame in tiff file
    info.counter += 1
    app.lbl1.config(text="Current Frame: " + str(info.counter))
    if info.counter <= len(info.listtiff):
        clot_finder(info.listtiff)
    else:
        popupmsg(1)


def popupmsg(val):
    txt = ""
    if val == 1:
        txt = "No More Frames to Process"
        app.btn1.config(state='enabled')
        app.btn2.config(state='enabled')
        app.lbl1.config(text='')
    if val == 0:
        txt = "No Directory Chosen"
    popup = tk.Tk()
    popup.wm_title("!")
    label = tk.Label(popup, text=txt, font="Montserrat")
    label.config(bg="red")
    label.pack(side="top", fill="x", pady=10)


# lambda: allows the methods to be used on demand, not just when the application launches
# without lambda: in the command section of the button, the methods won't execute when we want
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.btn1 = tk.Button(self, text="Select Folder",
                              command=lambda: select_tif())
        self.btn1.pack(padx=120, pady=30)
        self.btn1.config(font=("Montserrat", 20))

        self.btn2 = tk.Button(self, text="Process TIFF Files",
                              command=lambda: process_tiff())
        self.btn2.pack(padx=120, pady=30)
        self.btn2.config(font=("Montserrat", 20))
        self.btn3 = tk.Button(self, text="Next TIFF File",
                              command=lambda: next_frame())
        self.btn3.pack(padx=120, pady=30)
        self.btn3.config(font=("Montserrat", 20))
        self.lbl1 = tk.Label(self, text="Current frame: " + str(info.counter))
        self.lbl1.config(font=("Montserrat", 20))
        self.lbl1.pack(padx=120, pady=30)
        self.lbl1.config(relief=tk.RAISED)


if __name__ == "__main__":
    app = App()
    app.title("Clot Estimator - Roman Wicky van Doyer 2021")
    app.mainloop()
