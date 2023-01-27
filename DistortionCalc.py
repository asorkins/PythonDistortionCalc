from tkinter import filedialog
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import pymsgbox
from numpy.polynomial import polynomial as P
import math

class Distortion:
    # Class Variables:
    threshImg = None
    via_dia = 0

    # Constructor

    # Instance Methods
    #region Find Min Max Areas
    def find_min_max_size(self, graymin=127, graymax=255):
    #global via_dia, thresh, img
        file_path = filedialog.askopenfilename()
        if file_path=="":
            return
        img = cv2.imread(file_path)
    # Convert the image to grayscale
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Threshold the image to convert it to binary
        ret, Distortion.threshImg = cv2.threshold(gray_image, graymin, graymax, cv2.THRESH_BINARY)
    #r Apply Gaussian Blur Filter
        #thresh = cv2.GaussianBlur(thresh, (15, 15), 0)
    # Find contours in the image
        # contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours, _ = cv2.findContours(Distortion.threshImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        areas =[]
        cx =[]
        cy = []
        df = pd.DataFrame()

        disp_image = cv2.cvtColor(Distortion.threshImg, cv2.COLOR_GRAY2BGR)
    # Iterate through the contours
        for cnt in contours:
    # Find the area of the contour
            area = cv2.contourArea(cnt)
            if area > 100:
                areas.append(area)
        return math.ceil(np.min(areas)), math.ceil(np.mean(areas)), math.ceil(np.max(areas))
    #endregion

    def show_image(self,image,resize):
        ratio = resize / image.shape[1]
        dimension = (resize, int(image.shape[0] * ratio))
        # resize the original image
        resizedImage = cv2.resize(image, dimension, interpolation=cv2.INTER_AREA)
        im_pil = Image.fromarray(resizedImage)
        im_pil.show()

    def regen_image(self,minArea=15000, maxArea=25000):
        # global via_dia, thresh, img
        # Find contours in the image
        contours, _ = cv2.findContours(Distortion.threshImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        areas =[]
        cx =[]
        cy = []
        df = pd.DataFrame()
        # Convert thresh image into RGB to display with contours draws
        disp_image = cv2.cvtColor(Distortion.threshImg, cv2.COLOR_GRAY2BGR)
    # Iterate through the contours
        for cnt in contours:
    # Find the area of the contour
            area = cv2.contourArea(cnt)       
    # Check if the contour has a round shape
            if ((area >= minArea) & (area < maxArea)):
                areas.append(area)
    # Draw the contour on the image
                cv2.drawContours(disp_image, [cnt], 0, (255, 0, 0), 12)
                M = cv2.moments(cnt)
                #print( M )
                cx.append(int(M['m10']/M['m00']))
                cy.append(int(M['m01']/M['m00']))
                #print(f"center is at {cx} and {cy}")
        df['Areas'] = areas
        df['X'] = cx
        df['Y'] = cy
    #--- Find average via dia
        avrg_dia = np.mean(areas)
        Distortion.via_dia = 2*np.sqrt(avrg_dia/np.pi)
        # if debug:
        #     show_image(disp_image,1024*4)
        #     print(via_dia)
        return df, disp_image