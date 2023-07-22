# imports
from pprint import pprint

# Created class for the emails
class email:
    def __init__(self, email_address, email_subject, email_content):
        self.email_address = email_address
        self.email_subject = email_subject
        self.email_content = email_content

# Created received email list
emails = []

#Adding emails to list
emails.append(email("tomgo@gmail.com","About that game","Hey that game that you told me about..."))
emails.append(email("JakeWork@gmail.com","You broke the database again","You did it again, the whole app is down.."))

# Printing out the contents

for obj in emails:
    print("")
    # Call the vars() on Object
    obj_vars = vars(obj)

    # Print the properties
    pprint(obj_vars)
    
    print("")
