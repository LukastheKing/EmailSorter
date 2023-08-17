import customtkinter as ctk
import quickstart

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Easy Email Sorter")
        self.attributes('-zoomed', True)
        self.geometry("400x150")

        self.button = ctk.CTkButton(self, text="my button", command=self.button_callback)
        self.button.pack(padx=20, pady=20)

    def button_callback(self):
        print("button clicked")

app = App()
app.mainloop()