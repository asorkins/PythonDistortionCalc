import tkinter
import tkinter.messagebox
import customtkinter

customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    minsize = 0
    maxsize = 100
    mingray = 127
    maxgray = 255
    def __init__(self):
        super().__init__()

        # configure window
        self.title("CustomTkinter complex_example.py")
        self.geometry(f"{400}x{380}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(2, weight=1)
        #self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0,1), weight=1)


        self.slider_frame = customtkinter.CTkFrame(self , border_width=2, border_color=['#86878a','#86878a'])
        self.slider_frame.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="new")
        # Labels
        self.SliderLabel = customtkinter.CTkLabel(master=self.slider_frame, text='-->',  font=('aeral',14))
        self.SliderLabel.grid(row=0,column=0, padx=(70,50), pady=(15, 5) , sticky='e' )
        self.lblMinValue = customtkinter.CTkLabel(master=self.slider_frame, text='44',  font=('aeral',14))
        self.lblMinValue.grid(row=0,column=0, padx=(10,80), pady=(15, 5) , sticky='e' )
        self.lblMaxValue = customtkinter.CTkLabel(master=self.slider_frame, text='123',  font=('aeral',14))
        self.lblMaxValue.grid(row=0,column=0, padx=(120, 10), pady=(15, 5) , sticky='e' )
        self.lblMin = customtkinter.CTkLabel(master=self.slider_frame, text='min: ',  font=('aeral',14))
        self.lblMin.grid(row=1,column=0, padx=(10, 0), sticky='w' )
        self.lblMax = customtkinter.CTkLabel(master=self.slider_frame, text='max: ',  font=('aeral',14))
        self.lblMax.grid(row=2,column=0, padx=(10, 0), pady=(0, 5), sticky='w' )
        # Sliders
        self.slider_dia_min = customtkinter.CTkSlider(master=self.slider_frame, progress_color='#86878a', fg_color='#86878a', button_color='#86878a', state='disable',
            command=self.slider_min_event)
        self.slider_dia_min.grid(row=1, column=0, padx=(40, 10), pady=(7, 5), sticky="nw")
        self.slider_dia_max = customtkinter.CTkSlider(master=self.slider_frame, progress_color='#86878a', fg_color='#86878a', button_color='#86878a', state='disable',
            command=self.slider_max_event)
        self.slider_dia_max.grid(row=2, column=0, padx=(40, 10), pady=(7, 15), sticky="nw")
        self.chkSizeLimit = customtkinter.CTkCheckBox(master=self.slider_frame, text='Size Limit', command=self.chkbox_SizeLimit)
        self.chkSizeLimit.grid(row=0, column=0, pady=(20, 10), padx=(10,0), sticky="nw")
        self.LoadImage = customtkinter.CTkButton(master = self)
        self.LoadImage.pack(row=1,column=0, padx=10, pady=40, text="Load Image")
 # from web Example create checkbox and switch frame
        # self.checkbox_slider_frame = customtkinter.CTkFrame(self)
        # self.checkbox_slider_frame.grid(row=1, column=1, padx=(20, 20), pady=(20, 0), sticky="ew")

        # self.checkbox_2 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
        # self.checkbox_2.grid(row=2, column=0, pady=10, padx=20, sticky="n")
        # self.switch_1 = customtkinter.CTkSwitch(master=self.checkbox_slider_frame, command=lambda: print(f"switch {self.switch_1.get()} toggle"))
        # self.switch_1.grid(row=3, column=0, pady=10, padx=20, sticky="n")
        # self.switch_2 = customtkinter.CTkSwitch(master=self.checkbox_slider_frame)
        # self.switch_2.grid(row=4, column=0, pady=(10, 20), padx=20, sticky="n")



    def slider_min_event(self, slidervalue):
        self.lblMinValue.configure(text=slidervalue)
    
    def slider_max_event(self, slidervalue):
        self.lblMaxValue.configure(text=slidervalue)

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