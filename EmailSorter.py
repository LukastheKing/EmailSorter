# Imports
# Imports the get_email_subjects function from quick start
from quickstart import get_grouped_emails
# Imports the get_label_info function from quick start
from quickstart import get_label_info
# Imports the get_email_labels function from quickstart
from quickstart import get_email_labels
# Imports the pprint function from pprint
from pprint import pprint

# Main code function

# Code for subject functionality
grouped_emails = get_grouped_emails()
# Code for label functionality
label_info_list = get_label_info()
        
# Loops through email in the grouped emails 
for sender_email, emails in grouped_emails.items():
    # Prints senders name
    print(f"Sent by: {emails[0]['sender_name']} <{sender_email}> : \n")

    # Loops through the email info in emails
    for email_info in emails:
        # Gets the email subject
        subject = email_info['subject']
        # Gets the email snippet
        snippet = email_info['message']['snippet']
        # Gets the message ID
        message_id = email_info['message']['id']
        # Gets the email labels
        email_labels = get_email_labels(message_id)
                
        # Printing the subject
        print(f"Subject: {subject} \n")
        pprint(f"Snippet: {snippet}")

        if email_labels:
            print(f"\nLabels: {', '.join(email_labels)} \n")
        else:
            print("No labels found for this email. \n")

        print("----------\n")

    # Divider
    print("----------")


# Loops through the label infor in the list
for label_info in label_info_list:
    # Assigns the value of label_name as the one in the label info
    label_name = label_info['label_name']
    # Prints out the label
    pprint(f"Label: {label_name}")
    print("----------\n")
