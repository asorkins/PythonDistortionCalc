from tkinter import filedialog
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import pymsgbox
from numpy.polynomial import polynomial as P
import math


#VAriable
debug = True
via_dia = 0
cnt_vias_in_row = 0 


def regen_image(minArea=15000, maxArea=25000):
    global via_dia, thresh, img
    # Find contours in the image
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    areas =[]
    cx =[]
    cy = []
    df = pd.DataFrame()
    # Convert thresh image into RGB to display with contours draws
    disp_image = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
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
    via_dia = 2*np.sqrt(avrg_dia/np.pi)
    if debug:
        show_image(disp_image,1024*4)
        print(via_dia)
    return df

def find_min_max_size(graymin=127, graymax=255):
    global via_dia, thresh, img
    file_path = filedialog.askopenfilename()
    if file_path=="":
        return
    img = cv2.imread(file_path)
# Convert the image to grayscale
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# Threshold the image to convert it to binary
    ret, thresh = cv2.threshold(gray_image, graymin, graymax, cv2.THRESH_BINARY)
#r Apply Gaussian Blur Filter
    #thresh = cv2.GaussianBlur(thresh, (15, 15), 0)
# Find contours in the image
    # contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    areas =[]
    cx =[]
    cy = []
    df = pd.DataFrame()

    disp_image = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
# Iterate through the contours
    for cnt in contours:
# Find the area of the contour
        area = cv2.contourArea(cnt)
        if area > 100:
            areas.append(area)
    return math.ceil(np.min(areas)), math.ceil(np.mean(areas)), math.ceil(np.max(areas))


def find_circ(minArea):
    global via_dia, thresh, img
    file_path = filedialog.askopenfilename()
    if file_path=="":
        return
    img = cv2.imread(file_path)
# Convert the image to grayscale
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# Threshold the image to convert it to binary
    ret, thresh = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)
#r Apply Gaussian Blur Filter
    #thresh = cv2.GaussianBlur(thresh, (15, 15), 0)

# Find contours in the image
    # contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    areas =[]
    cx =[]
    cy = []
    df = pd.DataFrame()

    disp_image = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
# Iterate through the contours
    for cnt in contours:
# Find the area of the contour
        area = cv2.contourArea(cnt)
        
# Check if the contour has a round shape
        if area > minArea:
            areas.append(area)
# Draw the contour on the image
            cv2.drawContours(disp_image, [cnt], 0, (255, 0, 0), 2)
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
    via_dia = 2*np.sqrt(avrg_dia/np.pi)
    if debug:
        show_image(img,1024*4)
        show_image(disp_image,1024*4)
        print(via_dia)

    return df

def show_image(image,resize):
    ratio = resize / image.shape[1]
    dimension = (resize, int(image.shape[0] * ratio))
    # resize the original image
    resizedImage = cv2.resize(image, dimension, interpolation=cv2.INTER_AREA)
    im_pil = Image.fromarray(resizedImage)
    im_pil.show()

def df_plot(df, plotType='scatter'):
    # df.plot(kind=plotType,x="X",y="Y",title='Vias Centers')
    plt.scatter(df['X'],df['Y'])
    plt.show()

def data_process(df):
    df_list = []
    list_df_len = []
    row_end_indexes = []
#--- Sort the DF
    df.sort_values(['Y','X'],ascending = [False,True],ignore_index=True,inplace=True)
#--- Find Delta Y for adjacent vias    
    yDelta = df['Y'] - df['Y'].shift(1)
    df['yDelta'] = yDelta
#--- Find end of row and collect its index into array 'ii' and then move to list row_end_ind
    yDelta = np.where(yDelta < -(via_dia), 10101, yDelta)
    end_index = np.where(yDelta == 10101)[0]
    row_end_indexes = end_index.tolist()
#--- Add the very last index
    row_end_indexes.append(len(df))
    if debug:
        print(row_end_indexes)
        #return
        pass
#--- Generate separate DF for each row using revious index array 
#       and add them into df_list and return    
    previ_index=0
    for i in row_end_indexes:
        new_df = df[previ_index:i].copy()
        previ_index = i
        tempdf = new_df.sort_values('X', ascending = True, ignore_index=True)
        df_list.append(tempdf[tempdf.columns[0:3]])
        list_df_len.append(len(tempdf))
#--- Check lenghts of each row
    row_vias_count = {i:list_df_len.count(i) for i in list_df_len}
    if debug:
        pass
        print(row_vias_count)
        print(row_vias_count.keys())
        #print(df_list[(len(df_list)-1)])
    return df_list, row_vias_count

######################### Distortion Calculation  ################################
def dist_calc(df):
    new_df = pd.DataFrame()
    X_Diff = df['X'] - df['X'].shift(1)
    avrg = X_Diff.mean()
    rowStart = df['X'][0]
    df['ind'] = df.index
    dist = df['X'] - avrg*df['ind'] - rowStart
    new_df['X'] = df['X']
    new_df['Dist'] = dist
    return new_df
##########################  Plot Distortion for each vias row ##################
def plot_distortions(list_of_rows):
    i=0
    fig = plt.figure(figsize=(12, 6))
    for df in list_of_rows:
        if len(df) == cnt_vias_in_row:
            #--- Calculate and add distortion series
            dist_df = dist_calc(df)
            plt.plot(dist_df['X'], dist_df['Dist'], label=f'row-{i}')
            i+=1
    x= dist_df['X']
    y= dist_df['Dist']
    #--- Add TrendLine and calculate coefficinet
    #calculate equation for trendline
    z = np.polyfit(x, y, 6)
    p = np.poly1d(z)
    c, stats = P.polyfit(x,y,6,full=True)
    #add trendline to plot
    trdln = plt.plot(x, p(x), 'b--', label='Trendline')
    plt.setp(trdln, color='b', linewidth=2.5,)
    # Subtract trendline from last dist row
    corrected_dist = y - p(x)
    correctln = plt.plot(x, corrected_dist, label='Corrected')
    plt.setp(correctln, color='g', linewidth=2.5)
 
    #--- Prepare Plot
    
    plt.xlabel('X Coord [px]')
    plt.ylabel('Distortion [px]')
    plt.title('Distortion Chart')
    # Add a note
    plt.figtext(0.8, 0.9, str(c), ha="center", fontsize=7, bbox={"facecolor":"orange", "alpha":0.5, "pad":5})
    plt.legend()
    plt.show()
    return c

def main():
    global cnt_vias_in_row
    mymin,mymean,mymax = find_min_max_size()
    print(str(mymin) + " ; " + str(mymean) + " ; " + str(mymax))
    df2 = regen_image(mymax*0.8,mymax)
    print(df2)
    # return
    # df2 = find_circ(15000)
    #return
    #pd.set_option('display.max_rows', 500)
    rows_list, rows_vias_cnt = data_process(df2)
    cnt_vias_in_row = max(rows_vias_cnt.keys())
#--- Check if there is different vias count in the rows and choose the largest vias count
    if len(rows_vias_cnt)>1:
        #cnt_vias_in_row = max(rows_vias_cnt, key=rows_vias_cnt.get)
        pymsgbox.alert(f'There are rows with diferent vias counts! \n vias_num:rows_count {rows_vias_cnt}' +
        '\n Only rows with largest vias count will be selected', 'Title')
    poly_args = plot_distortions(rows_list)
    
    #return
    if debug:
        pass
        # print(rows_list[5])
        # print(rows_vias_cnt)
        # print(max(rows_vias_cnt, key=rows_vias_cnt.get))
        # print(len(rows_vias_cnt))
        print(poly_args)
        # df_plot(df2)

if __name__ == "__main__":
    main()