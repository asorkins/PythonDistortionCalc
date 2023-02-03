from PIL import Image
import customtkinter
import tkinter
import customtkinter
from PIL import ImageTk, Image
import test1
import os
import math
import time
import pandas as pd
import numpy as np
from DistortionCalc import Distortion
import threading
from tkinter import filedialog
import pymsgbox

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

minsize = 0
maxsize = 100
mingray = 127
maxgray = 255
debug = True
df = pd.DataFrame()
busy_flag = True
file_path = ''

class App(customtkinter.CTk, Distortion):

    mydist = Distortion()

    def __init__(self):
        super().__init__()

        # configure window
        self.title("Distortion Calculator")
        self.geometry(f"{480}x{300}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(2, weight=1)
        #self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0,1), weight=1)

#########################             Layout

        self.slider_frame = customtkinter.CTkFrame(self , border_width=2, border_color=['#86878a','#86878a'])
        self.slider_frame.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="new")
        # Labels
        self.SliderLabel = customtkinter.CTkLabel(master=self.slider_frame, text='',  font=('aeral',14))
        self.SliderLabel.grid(row=0,column=0, padx=(70,50), pady=(15, 5) , sticky='e' )
        self.lblMinValue = customtkinter.CTkLabel(master=self.slider_frame, text='',  font=('aeral',14))
        self.lblMinValue.grid(row=0,column=0, padx=(10,80), pady=(15, 5) , sticky='e' )
        self.lblMaxValue = customtkinter.CTkLabel(master=self.slider_frame, text='',  font=('aeral',14))
        self.lblMaxValue.grid(row=0,column=0, padx=(120, 10), pady=(15, 5) , sticky='e' )
        self.lblMin = customtkinter.CTkLabel(master=self.slider_frame, text='min: ',  font=('aeral',14))
        self.lblMin.grid(row=1,column=0, padx=(10, 0), sticky='w' )
        self.lblMax = customtkinter.CTkLabel(master=self.slider_frame, text='max: ',  font=('aeral',14))
        self.lblMax.grid(row=2,column=0, padx=(10, 0), pady=(0, 5), sticky='w' )
        self.lblProgress = customtkinter.CTkLabel(master=self, text='',  font=('aeral',18), text_color='#fc0303')
        self.lblProgress.grid(row=3,column=0, padx=(10, 0), pady=(0, 5), sticky='we' )
        # Sliders
        self.slider_dia_min = customtkinter.CTkSlider(master=self.slider_frame, progress_color='#86878a', fg_color='#86878a', button_color='#86878a', state='disable',
            command=self.slider_min_event)
        self.slider_dia_min.grid(row=1, column=0, padx=(40, 10), pady=(7, 5), sticky="nw")
        self.slider_dia_max = customtkinter.CTkSlider(master=self.slider_frame, progress_color='#86878a', fg_color='#86878a', button_color='#86878a', state='disable',
            command=self.slider_max_event)
        self.slider_dia_max.grid(row=2, column=0, padx=(40, 10), pady=(7, 15), sticky="nw")
        self.chkSizeLimit = customtkinter.CTkCheckBox(master=self.slider_frame, text='Size Limit', command=self.chkbox_SizeLimit, state='disabled')
        self.chkSizeLimit.grid(row=0, column=0, pady=(20, 10), padx=(10,0), sticky="nw")
        # Buttons
        self.btn_LoadImage = customtkinter.CTkButton(master=self, text="Load Image", command=self.load_image)
        self.btn_LoadImage.grid(row=0,column=1, padx=10, pady=(40,0), sticky='n')
        self.btn_DetectViaas = customtkinter.CTkButton(master=self, text="Detect", command=self.detect_vias, state='disabled')
        self.btn_DetectViaas.grid(row=0,column=1, padx=10, pady=(100, 0), sticky='n')
        self.btn_Calculate = customtkinter.CTkButton(master=self, text="Calculate", command=self.calculate, state='disabled')
        self.btn_Calculate.grid(row=0,column=1, padx=10, pady=(160, 0) , sticky='n')
        self.btn_Submit = customtkinter.CTkButton(master=self, text="Submit", command=self.submit, state='disabled')

        self.btn_Submit.grid(row=0,column=1, padx=10, pady=(220, 0) , sticky='n')        

 # from web Example create checkbox and switch frame
        # self.checkbox_slider_frame = customtkinter.CTkFrame(self)
        # self.checkbox_slider_frame.grid(row=1, column=1, padx=(20, 20), pady=(20, 0), sticky="ew")

        # self.checkbox_2 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
        # self.checkbox_2.grid(row=2, column=0, pady=10, padx=20, sticky="n")
        # self.switch_1 = customtkinter.CTkSwitch(master=self.checkbox_slider_frame, command=lambda: print(f"switch {self.switch_1.get()} toggle"))
        # self.switch_1.grid(row=3, column=0, pady=10, padx=20, sticky="n")
        # self.switch_2 = customtkinter.CTkSwitch(master=self.checkbox_slider_frame)
        # self.switch_2.grid(row=4, column=0, pady=(10, 20), padx=20, sticky="n")

#########################             Control
    def background_img_loading(self):
        global busy_flag
        mymin,mymean,mymax = self.mydist.find_min_max_size(file_path)
        print(mymin, mymax)
        busy_flag = False
        self.lblProgress.configure(text='')
        self.update_detect_labels(mymin, mymax)

    def background_detect_vias(self):
        global df
        dia = self.slider_dia_min.get()
        minarea = math.pi * dia * dia / 4
        dia = self.slider_dia_max.get()
        maxarea = math.pi * dia * dia / 4
        df, img = self.mydist.regen_image(minarea, maxarea)
        self.mydist.show_image(img,2048)
        self.toggle_element_state(self.btn_Calculate,True)    
        self.toggle_element_state(self.btn_Submit,False)   
        self.toggle_element_state(self.btn_LoadImage,True)
                             
        self.lblProgress.configure(text='')

    def update_detect_labels(self,mymin,mymax):
            minsize = math.ceil(math.sqrt(4*mymin/math.pi))
            minsize = minsize*0.9 # reduce 10%
            maxsize = math.ceil(math.sqrt(4*mymax/math.pi))
            maxsize = maxsize*1.1 # increase 10%
            avgsize = (minsize + int(maxsize*0.1))/2
            self.slider_dia_min.configure(from_=minsize)
            self.slider_dia_min.configure(to=maxsize)
            self.slider_dia_min.set(avgsize)
            self.lblMinValue.configure(text=int(self.slider_dia_min.get()))
            self.slider_dia_max.configure(from_=minsize)
            self.slider_dia_max.configure(to=maxsize)
            self.slider_dia_max.set(maxsize)
            self.lblMaxValue.configure(text=int(self.slider_dia_max.get()))  
            self.SliderLabel.configure(text='-->')      
        # Activate UI elements
            self.chkSizeLimit.configure(state='normal')
            self.toggle_element_state(self.btn_Calculate,False)       
            self.toggle_element_state(self.btn_Submit,False)   
            self.toggle_element_state(self.btn_DetectViaas,True)              
  
    def calculate(self):
        #rows_list = []    
        rows_list, rows_vias_cnt = self.mydist.data_process(df)
        cnt_vias_in_row = max(rows_vias_cnt.keys())
    #--- Check if there is different vias count in the rows and choose the largest vias count
        if len(rows_vias_cnt)>1:
            #cnt_vias_in_row = max(rows_vias_cnt, key=rows_vias_cnt.get)
            pymsgbox.alert(f'There are rows with diferent vias counts! \n vias_num:rows_count {rows_vias_cnt}' +
            '\n Only rows with largest vias count will be selected', 'Title')
        poly_args = self.mydist.plot_distortions(rows_list)    
        print(poly_args)
        self.toggle_element_state(self.btn_Submit,True)
            

    def submit(self):
        # Use External Class function
        pass
        self.toggle_element_state(self.btn_LoadImage)
        

    def toggle_element_state(self, element, IsEnabled=True):
        if IsEnabled:
            element.configure(state='normal')

        else:
            element.configure(state='disabled')


    def detect_vias(self):
        self.lblProgress.configure(text='Wait as vias detecting ... ')
        self.toggle_element_state(self.btn_Calculate,False)       
        self.toggle_element_state(self.btn_Submit,False)   
        self.toggle_element_state(self.btn_LoadImage,False)             
        thread = threading.Thread(target=self.background_detect_vias)
        thread.start()
        if (debug):
            print(df)

    def load_image(self):
        global busy_flag, file_path
        self.toggle_element_state(self.btn_DetectViaas,False)
        self.toggle_element_state(self.btn_Calculate,False)       
        self.toggle_element_state(self.btn_Submit,False)
        file_path = filedialog.askopenfilename()
        self.lblProgress.configure(text='Wait as image is loading ... ')
        thread = threading.Thread(target=self.background_img_loading)
        thread.start()       
        print('Thread Start') 
        mymin,mymean,mymax = 0, 0, 0
        # self.show_waiting()
        # thread1 = threading.Thread(target=self.show_waiting)
        # thread1.start()   
        # time.sleep(1)          
        # thread.join()  
        print('Thread Joined') 

        # mymin,mymean,mymax = self.mydist.find_min_max_size()
        busy_flag = False
        if((mymin!=0) & (mymax!=0)):
            minsize = math.ceil(math.sqrt(4*mymin/math.pi))
            minsize = minsize*0.9 # reduce 10%
            maxsize = math.ceil(math.sqrt(4*mymax/math.pi))
            maxsize = maxsize*1.1 # increase 10%
            avgsize = (minsize + int(maxsize*0.1))/2
            self.slider_dia_min.configure(from_=minsize)
            self.slider_dia_min.configure(to=maxsize)
            self.slider_dia_min.set(avgsize)
            self.lblMinValue.configure(text=int(self.slider_dia_min.get()))
            self.slider_dia_max.configure(from_=minsize)
            self.slider_dia_max.configure(to=maxsize)
            self.slider_dia_max.set(maxsize)
            self.lblMaxValue.configure(text=int(self.slider_dia_max.get()))  
            self.SliderLabel.configure(text='-->')      
        # Activate UI elements
            self.chkSizeLimit.configure(state='normal')
            self.btn_DetectViaas.configure(state='normal')

    def slider_min_event(self, slidervalue):
        self.lblMinValue.configure(text=int(slidervalue))
    
    def slider_max_event(self, slidervalue):
        self.lblMaxValue.configure(text=int(slidervalue))

    def chkbox_SizeLimit(self):
        if self.chkSizeLimit.get():
            self.slider_dia_max.configure(state='normal')
            self.slider_dia_max.configure(progress_color='#288f06', fg_color='#e30918', button_color='#020bfa', button_hover_color='#02e1fa')
            self.slider_dia_min.configure(state='normal')
            self.slider_dia_min.configure(fg_color='#288f06', progress_color='#e30918', button_color='#020bfa', button_hover_color='#02e1fa')
            self.slider_frame.configure(border_color=['#09800f','#09800f'])
        else:
            self.slider_dia_min.configure(state='disable')
            self.slider_dia_min.configure(progress_color='#86878a', fg_color='#86878a', button_color='#86878a')
            self.slider_dia_max.configure(state='disable')
            self.slider_dia_max.configure(progress_color='#86878a', fg_color='#86878a', button_color='#86878a')
            self.slider_frame.configure(border_color=['#86878a','#86878a'])

if __name__ == "__main__":
    app = App()
    app.mainloop()