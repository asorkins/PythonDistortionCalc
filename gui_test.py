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
        self.geometry("400x240")
        self.title("DistApp")
        #self.resizable(False,False)

        def button_function():
            print("button pressed")
            df = test1.find_circ(15000)
            RegenImage.configure(state="normal")
        def RegenImage():
            df1 = test1.regen_image()
        def button2_function():
            value = Via_dia.get()
            label.configure(text=int(value))
        def Via_dia_function(value):
            #value = Via_dia.get()
            label.configure(text=int(value))

 
 # load and create background image
        # self.bg_image = customtkinter.CTkImage(Image.open("AI_icon.png"),
        #                                        size=(self.winfo_width(), 240))
        # self.bg_image_label = customtkinter.CTkLabel(self,text="", image=self.bg_image)
        # self.bg_image_label.grid(row=0, column=0)


       
 
        my_image = customtkinter.CTkImage(light_image=Image.open('AI_icon.png'),
                                        dark_image=Image.open('AI_icon.png'),
                                        size=(30, 30))

        button = customtkinter.CTkButton(self, text="Open Image" , image=my_image , command=button_function)
        button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        RegenImage = customtkinter.CTkButton(self, text="Regen Imnage", state="disabled"  , command=RegenImage)
        RegenImage.place(relx=0.7, rely=0.5, anchor=tkinter.W)

        button2 = customtkinter.CTkButton(self, text="Slider Value"  , command=button2_function)
        button2.place(relx=0.7, rely=0.7, anchor=tkinter.W)

        Via_dia = customtkinter.CTkSlider(self, from_=0, to=100, command=Via_dia_function)
        Via_dia.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

        label = customtkinter.CTkLabel(self, text=str(int(Via_dia.get())))
        label.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)

#img = ImageTk.PhotoImage(Image.open("AI_icon.png"))
#label = customtkinter.CTkLabel(master=app, Image=my_image)
#label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

if __name__ == "__main__":
    app = App()
    app.mainloop()