# Imports
# Imports customkinter and its functions as ctk
import customtkinter as ctk
# Imports the get_email_subjects function from quick start
from quickstart import get_email_info

# Main code function
# Sets appearance and color for the window
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Code for subject functionality
email_info_list = get_email_info()

# Creates the new window class with its properties and its "Widgets"
class App(ctk.CTk):
    # Defines init function 
    def __init__(self):
        # Super init
        super().__init__()
        # Sets title of the window to "Easy Email Sorter" 
        self.title("Easy Email Sorter")
        # Maximizes the window on open
        self.attributes('-zoomed', True)
        # Sets the default floating window size to "400x150"
        self.geometry("400x150")

        # Creates button and gives it text and sets functionality
        self.button = ctk.CTkButton(self, text="my button", command=self.button_callback)
        # Sets the padding on both the x and y axis to 20
        self.button.pack(padx=20, pady=20)

        # Creates text box and gives it a width and a corner radius
        self.textbox = ctk.CTkTextbox(self, width=1000, height=600, corner_radius=0)
        # Sets the padding on both the x and y axis to 20
        self.textbox.pack(padx=20, pady=20)

    # Defines button_callback function with the paramaters of self to give functionality to the button
    def button_callback(self):
        # Button main functionality
        #self.textbox.insert("0.0","PP \n") # Testing code

        # Loops through each email in emails_subjects
        for email_info in email_info_list:
            # Prints out for testing
            #print(f"Sender: {email_info['sender_name']} <{email_info['sender_email']}>")
            #print(f"Subject: {email_info['subject']}") 
            #print("------")

            # Inserts the subjects into the textbox
            self.textbox.insert("0.0", "----------\n")
            self.textbox.insert("0.0", f"Subject: {email_info['subject']}\n")
            self.textbox.insert("0.0", f"Sender: {email_info['sender_name']} <{email_info['sender_email']}>\n")
# Creates app object based on the App class
app = App()
# Calls the window on startup
app.mainloop()