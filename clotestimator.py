# Imports
import tkinter as tk
import cv2
import os
import numpy as np
from tkinter import filedialog


# Algo Functions
# Algo 1:
# Click on any pixel that is part of the clot, do a DFS for all pixels connected to that pixel
# Add a threshold for max size of clot
# Image thresholding to get rid of uneeded pixels that may interfere with DFS
# Algo 2:
# Select an ROI that contains the clot
# Create bounding boxes for all shapes
# Only return the clot we want - User selection
def clot_dfs():
    print("D")


# App Section
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.btn = tk.Button(self, text="Select TIFF File",
                             command=self.select_tiff())
        self.btn.pack(padx=120, pady=30)
        self.btn = tk.Button(self, text="Process TIFF File",
                             command=self.process_tiff())
        self.btn.pack(padx=120, pady=30)
        self.btn = tk.Button(self, text="Next Frame",
                             command=self.next_frame())
        self.btn.pack(padx=120, pady=30)

    def select_tiff(self):
        # Open File
        print("A")
    def process_tiff(self):
        # open tiff file, go through each frame
        print("B")
    def next_frame(self):
        # go to next frame in tiff file
        print("C")


if __name__ == "__main__":
    app = App()
    app.title("Clot Estimator - Roman Wicky van Doyer 2021")
    app.mainloop()
