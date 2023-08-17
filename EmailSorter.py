import customtkinter as ctk
import quickstart
from quickstart import main

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

if __name__ == '__main__':
    label_names = main()

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Easy Email Sorter")
        #self.attributes('-zoomed', True)
        self.geometry("400x150")

        self.button = ctk.CTkButton(self, text="my button", command=self.button_callback)
        self.button.pack(padx=20, pady=20)

        self.textbox = ctk.CTkTextbox(self, width=800, corner_radius=0)
        self.textbox.pack(padx=20, pady=20)

    def button_callback(self):
        self.textbox.insert("0.0", f"{label_names} \n")

app = App()
app.mainloop()