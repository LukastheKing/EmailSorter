# Imports
# Imports the get_email_subjects function from quickstart
from quickstart import get_grouped_emails
# Imports the get_label_info function from quickstart
from quickstart import get_label_info
# Imports the get_email_labels function from quickstart
from quickstart import get_email_labels
# Imports the check label existance for sender from quickstar
from quickstart import check_label_existance_for_sender
# Imports the add label to email from quickstart
from quickstart import add_label_to_email
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
        # Gets the sender to check
        sender_email_to_check = email_info['sender_email']
        # Sets the label name to be checked to the value as the sender email
        label_name_to_check = sender_email_to_check

        # Gets the email subject
        subject = email_info['subject']
        # Gets the email snippet
        snippet = email_info['message']['snippet']
        # Gets the message ID
        message_id = email_info['message']['id']
        # Gets the email labels
        email_labels = get_email_labels(message_id)

        # Checks if label exist based on the senders email and label name
        label_exists = check_label_existance_for_sender(sender_email_to_check, label_name_to_check)
                
        # Printing the subject
        print(f"Subject: {subject} \n")
        pprint(f"Snippet: {snippet}")

        if label_exists:
            print(f"The label '{label_name_to_check}' exists for this email.")
        else:
            print(f"The label '{label_name_to_check}' does not exist for this email")

            add_label_to_email(message_id, sender_email_to_check)
            print(f"Label '{sender_email_to_check}' added to email.")
        
        if email_labels:
            print(f"\nLabels: {', '.join(email_labels)} \n")
        else:
            print("No labels found for this email. \n")

        print("----------\n")

    # Divider
    print("----------")


"""
# Loops through the label infor in the list
for label_info in label_info_list:
    # Assigns the value of label_name as the one in the label info
    label_name = label_info['label_name']
    # Prints out the label
    pprint(f"Label: {label_name}")
    print("----------\n")
"""