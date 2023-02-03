from PIL import Image
import customtkinter
import tkinter
import customtkinter
from PIL import ImageTk, Image
import test1
import os

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
                
        #app = customtkinter.CTk()  # create CTk window like you do with the Tk window
        self.geometry("450x240")
        self.title("DistApp")
        #self.resizable(False,False)

        def button_function():
            print("button pressed")
            df = test1.find_circ(15000)
            RegenImage.configure(state="normal")
        def RegenImage_function():
            df1 = test1.regen_image()
        def button2_function():
            value = self.Via_dia_min.get()
            labelViaDia.configure(text=int(value))
       
        def Via_dia_change(value):
            #value = Via_dia.get()
            labelViaDia.configure(text= 'from: ' + str(int(self.Via_dia_min.get())) + ' to: ' + str(int(self.Via_dia_max.get())))

 
 # load and create background image
        # self.bg_image = customtkinter.CTkImage(Image.open("AI_icon.png"),
        #                                        size=(self.winfo_width(), 240))
        # self.bg_image_label = customtkinter.CTkLabel(self,text="", image=self.bg_image)
        # self.bg_image_label.grid(row=0, column=0)
        my_image = customtkinter.CTkImage(light_image=Image.open('AI_icon.png'),
                                        dark_image=Image.open('AI_icon.png'),
                                        size=(30, 30))
        img_loading = customtkinter.CTkImage(light_image=Image.open('loading.gif'),
                                        dark_image=Image.open('loading.gif'),
                                        size=(100, 100))                                        
        self.label = customtkinter.CTkLabel(self, text="Via Dia", image=img_loading)
        self.label.place(relx=0.25, rely=0.5, anchor=tkinter.CENTER)
        self.frame_1 = customtkinter.CTkFrame(self,
                               width=200,
                               height=40,
                               corner_radius=5, border_width=2,border_color=['#bfb597','#bfb597'])
        self.frame_1.pack(fill="both", expand=False )
 


        button = customtkinter.CTkButton(self, text="Open Image" , image=my_image , command=button_function)
        button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        RegenImage = customtkinter.CTkButton(self, text="Regen Imnage", state="disabled"  , command=RegenImage_function)
        RegenImage.place(relx=0.7, rely=0.5, anchor=tkinter.W)

        button2 = customtkinter.CTkButton(self, text="Slider Value"  , command=button2_function)
        button2.place(relx=0.7, rely=0.7, anchor=tkinter.W)

        self.Via_dia_min = customtkinter.CTkSlider(self.frame_1, from_=0, to=100, command=Via_dia_change)
        self.Via_dia_min.place(relx=0.25, rely=0.5, anchor=tkinter.CENTER)

        self.Via_dia_max = customtkinter.CTkSlider(self.frame_1, from_=0, to=100, command=Via_dia_change)
        self.Via_dia_max.place(relx=0.7, rely=0.5, anchor=tkinter.CENTER)

        labelViaDia = customtkinter.CTkLabel(self, text='')
        labelViaDia.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)

        # create slider and progressbar frame
        # self.slider_progressbar_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        # self.slider_progressbar_frame.pack()
        # self.slider_progressbar_frame.grid(row=1, column=1, columnspan=2, padx=(20, 0), pady=(20, 0))
        # self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
        # self.slider_progressbar_frame.grid_rowconfigure(4, weight=1)
        # self.seg_button_1 = customtkinter.CTkSegmentedButton(self.slider_progressbar_frame)
        # self.seg_button_1.grid(row=0, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        # self.progressbar_1 = customtkinter.CTkProgressBar(self.slider_progressbar_frame)
        # self.progressbar_1.grid(row=1, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        # self.progressbar_2 = customtkinter.CTkProgressBar(self.slider_progressbar_frame)
        # self.progressbar_2.grid(row=2, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        # self.slider_1 = customtkinter.CTkSlider(self.slider_progressbar_frame, from_=0, to=1, number_of_steps=4)
        # self.slider_1.grid(row=3, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        # self.slider_2 = customtkinter.CTkSlider(self.slider_progressbar_frame, orientation="vertical")
        # self.slider_2.grid(row=0, column=1, rowspan=5, padx=(10, 10), pady=(10, 10), sticky="ns")
        # self.progressbar_3 = customtkinter.CTkProgressBar(self.slider_progressbar_frame, orientation="vertical")
        # self.progressbar_3.grid(row=0, column=2, rowspan=5, padx=(10, 20), pady=(10, 10), sticky="ns")

#img = ImageTk.PhotoImage(Image.open("AI_icon.png"))
#label = customtkinter.CTkLabel(master=app, Image=my_image)
#label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

if __name__ == "__main__":
    app = App()
    app.mainloop()