# Imports
# Imports the get_email_subjects function from quick start
from quickstart import get_grouped_emails
# Import the get_label_info function from quickstart
from quickstart import get_label_info
# Imports the pprint function from pprint
from pprint import pprint

# Main code function

# Code for subject functionality
grouped_emails = get_grouped_emails()
# Code for label functionality
label_info_list = get_label_info()
        
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
