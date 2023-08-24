# Imports
# Imports customkinter and its functions as ctk
import customtkinter as ctk
# Imports the get_email_subjects function from quick start
from quickstart import get_grouped_emails
# Import the get_label_info function from quickstart
from quickstart import get_label_info
# Imports the pprint function from pprint
from pprint import pprint

# Main code function
# Sets appearance and color for the window
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Code for subject functionality
grouped_emails = get_grouped_emails()
# 
label_info_list = get_label_info()
        
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
        # Sets up the grid configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.grid(row=0, column=0, padx=10, pady=(10,0), sticky="nsew")

        # Creates button and gives it text and sets functionality
        self.button = ctk.CTkButton(self.button_frame, text="Print out emails", command=self.button_callback)
        # Sets the padding on both the x and y axis to 20
        #self.button.pack(padx=20, pady=20)
        # Sets the button location based on the grid 
        self.button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.textbox_frame = ctk.CTkFrame(self)
        self.textbox_frame.grid(row=0, column=1, padx=(0,10), pady=(10,0), sticky="nsew")

        # Creates text box and gives it a width and a corner radius
        self.textbox = ctk.CTkTextbox(self.textbox_frame, width=1135, height=600, corner_radius=0)
        # Sets the padding on both the x and y axis to 20
        #self.textbox.pack(padx=20, pady=20)
        # Sets the textbox location based on the grid
        self.textbox.grid(row=1, column=0, padx=20, pady=20, sticky="ew")

    # Defines button_callback function with the paramaters of self to give functionality to the button
    def button_callback(self):
        # Button main functionality

        """
        # Prints out for testing
        for sender_email, emails in grouped_emails.items():
            # Prints senders name
            print(f"Sent by: {emails[0]['sender_name']} <{sender_email}> : \n")

            # Loops through the email info in emails
            for email_info in emails:
                # Assigns the value of subject as the subject from email info
                subject = email_info['subject']
                snippet = email_info['message']['snippet']
                
                # Printing the subject
                pprint(f"Subject: {subject}")
                pprint(f"Snippet: {snippet}")
                print("----------\n")

            # Divider
            print("----------")

        for label_info in label_info_list:
            label_name = label_info['label_name']
            pprint(f"Label: {label_name}")
            print("----------\n")
        """

        #"""
        # Loops through each sender and email in the grouped emails
        for sender_email, emails in grouped_emails.items():

            # Loops through the email info in emails
            for email_info in emails:
                # Assigns the value of subject as the subject from email info
                subject = email_info['subject']
                snippet = email_info['message']['snippet']
                
                # Inserts Subject into text box
                self.textbox.insert("0.0", "\t--------------------\n")
                self.textbox.insert("0.0", f"\t{snippet}\n")
                self.textbox.insert("0.0", f"\tSubject: {subject}\n")

            # Inserts Senders name and email into text box
            self.textbox.insert("0.0", "----------------------------------------\n")
            self.textbox.insert("0.0", f"Sent by: {emails[0]['sender_name']} <{sender_email}> : \n")
        #"""

# Creates app object based on the App class
app = App()
# Calls the window on startup
app.mainloop()