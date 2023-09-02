# Imports
# Imports the print_function from __future__
from __future__ import print_function

# Imports os.path
import os.path
# Imports pickle
import pickle
# Imports the pprint function form pprint 
from pprint import pprint 

# Imports Request from google.auth.transprot.request 
from google.auth.transport.requests import Request
# Imports Credentials from google.oauth2.credentials
from google.oauth2.credentials import Credentials
# Imports InstalledAppFlow from google_auth_oauthlib.flow
from google_auth_oauthlib.flow import InstalledAppFlow
# Imports build from googleapiclient.discovery
from googleapiclient.discovery import build
# Imports HttpError from googleapiclient.errors
from googleapiclient.errors import HttpError

# Main code function 

# Sets the scope of the project to read only
# If modyfying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.labels', 'https://www.googleapis.com/auth/gmail.modify']

# Gets the authentication credits for the gmail api
def authenticate_gmail():
    # sets creds value to None
    creds = None

    # Creates the token.json file which stores the user's access and refresh tokens
    if os.path.exists('token.pickle'):
        # Uses open to open the token.pickle in read binary mode (rb) as the token
        with open('token.pickle', 'rb') as token:
            # sets creds value to that on the token file using pickle.load
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    # Checks if theres no valid credentials 
    if not creds or not creds.valid:
        # Refreshes the creds value using the Request
        if creds and creds.expired and creds.refresh_token:
            # Obtains valid credentials
            creds.refresh(Request())
        # Runs the program if theres valid credentials
        else:
            # Calls the credentials from credentials.json using the scopes already set using the App flow
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            # Opens a local server in port 0 and display the success message 'test'
            creds = flow.run_local_server(success_message='test')
        # Saves the credentials for the next run
        # Uses open to open the token.pickle file in write binary mode (wb) 
        with open('token.pickle', 'wb') as token:
            # Uses dump to save the credentials into the file
            pickle.dump(creds, token)
    return creds

# Gets all the email info: subject, sender and message
def get_email_info():
    # Gets the credits from the authentication function
    creds = authenticate_gmail()

    # Creates an empty list for the subjects
    email_info_list = []

    # Calls the Gmail API and tries to run the code
    try:
        # Builds access to the gmail api
        service = build('gmail', 'v1', credentials = creds)
        
        # Lists all messages in the user's inbox
        # Assigns the listed messages to results
        results = service.users().messages().list(userId='me').execute()
        # Gets the messages in results and assigns them to messages
        messages = results.get('messages', [])

        # Determines if theres no emails in the inbox
        if not messages:
            print('No messages found.')
            return email_info_list
        
        # Loops through each message and retrives its subject
        for message in messages:
            # Assigns the if from message to message_id
            message_id = message['id']
            # Gets the message based on the message_id and assigns it to msg
            msg = service.users().messages().get(userId='me', id=message_id).execute()

            # Assings the values of None to subject, sende email, sender name
            subject = None
            sender_email = None
            sender_name = None

            # Loops through each header or subject in msg
            for header in msg['payload']['headers']:
                # Determines if the emails headers name is equal to subject
                if header['name'] == 'Subject':
                    # Assigns the header value to subject
                    subject = header['value']
                    break
                # Deterines if the emails headers name is equal to From
                elif header['name'] == 'From':
                    # Assigns the header value to sender_info
                    sender_info = header['value']
                    # Sets the values of name and email to there own values 
                    sender_name, sender_email = parse_sender_info(sender_info)
                
            # Appends the subject, sender name and email, and message to the email_info list
            email_info_list.append({
                'subject': subject,
                'sender_name': sender_name,
                'sender_email': sender_email,
                'message':msg
            })

            """
            # Prints the subject of the message or a default message if no subject is found
            if subject:
                print(f"Subject: {subject} \n")
            else:
                print("No subject found.")
            print("------ \n")
            """

    # Uses HttpError to send an error if something fails
    except HttpError as error:
        #TODO(developer) - Handle errors form gmail API.
        print(f'An error ocurred:{error}')

    return email_info_list

# Parses the sender info into name and email 
def parse_sender_info(sender_info):
    # Parse sender info in the format "Name <email>"
    if '<' in sender_info and '>' in sender_info:
        sender_name, sender_email = sender_info.split('<')
        sender_name = sender_name.strip()
        sender_email = sender_email.replace('>', '').strip()
    else:
        # Set default values if sender information is not in expected format
        sender_name = "Unknown"
        sender_email = "unknown@example.com"
    
    # Returns senders name and email 
    return sender_name, sender_email

# Groups emails by senders
def get_grouped_emails():
    # Groups up emails by sender 

    # Creates a variable with the value of the function get_email_info
    email_info_list = get_email_info()

    # Makes an empty dictionary for grouping
    grouped_emails = {}

    # Loops through the email info in the email info list
    for email_info in email_info_list:
        # Gets the email sender from sender_email
        sender_email = email_info['sender_email']
        # Determines if the sender has not been grouped in the dictionary
        if sender_email not in grouped_emails:
            # Adds the email into the dictionary
            grouped_emails[sender_email] = []
        # appends the email info 
        grouped_emails[sender_email].append(email_info)

    # Returns the grouped emails
    return grouped_emails

# Gets the labels
def get_label_info():
    # Gets the credits from the authentication function
    creds = authenticate_gmail()

    # Creates empty list for the labels
    label_info_list = []

    # Calls Gmail API and tries to run the code
    try:
        # Builds access to the gmail 
        service = build('gmail', 'v1', credentials=creds)

        # List all labels from the user
        # Assigns the listed labels to results
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])

        if not labels:
            print("No labels found")
            return label_info_list
        
        for label in labels:
            label_name = label['name']
            label_id = label['id']
            label_info = {
                'label_name': label_name,
                'label_id': label_id
            }

            if 'sender_name' in label:
                label_info['sender_name'] = label['sender_name']

            label_info_list.append(label_info)

    except HttpError as error:
        #TODO(developer) - Handle errors from Gmail API
        print(f'An error ocurred:{error}')

    return label_info_list

# Gets the labels of all the emails in the inbox
def get_email_labels(message_id):
    # Gets the credits from the authentication function
    creds = authenticate_gmail()

    # Creates an empty lis for the email labels
    email_labels = []

    try:
        # Builds service for the gmail API
        service = build('gmail', 'v1', credentials=creds)

        msg = service.users().messages().get(userId='me', id=message_id, format='metadata', metadataHeaders=['labelsIds']).execute()
        label_ids = msg.get('labelIds', [])

        existing_labels = get_label_info()

        for label_id in label_ids:
            #email_labels.append(label_id)
            label_name = next((label['label_name'] for label in existing_labels if label['label_id'] == label_id), None)
            if label_name:
                email_labels.append(label_name)

    except HttpError as error:
        print(f'An error ocurred: {error}')

    return email_labels

# Checks the existence of certain labels 
def check_label_existance_for_sender(sender_name, label_name_to_check):
    # Gets the label info from the function get label info
    label_info_list = get_label_info()

    # Loops throught the label info in the list
    for label_info in label_info_list:
        # Checks if the label name is the same as the variables value
        if label_info['label_name'] == label_name_to_check:
            if 'sender_name' in label_info and label_info.get('sender_name') == sender_name:
                return True
        
    return False

def add_label_to_email(message_id, label_name, sender_name):
    creds = authenticate_gmail()

    try:
        service = build('gmail', 'v1', credentials=creds)

        existing_labels = get_label_info()
        existing_label_names = [label['label_name'] for label in existing_labels]

        if label_name not in existing_label_names:
            # Create a new label with the name provided
            label = {'name': label_name, 'sender_name': sender_name}
            label = service.users().labels().create(userId='me', body=label).execute()
            label_id = label['id']
        else:
            label_id = existing_labels[existing_label_names.index(label_name)]['label_id']
        
        msg = service.users().messages().modify(userId='me', id=message_id, body={'addLabelIds':[label_id]}).execute()
        print(f"\nLabel '{label_name}' added to email with ID {message_id}")
    
    except HttpError as error:
        print(f'An error ocurred: {error}')

# Runs main function
if __name__ == '__main__':
    # Printing funciton
    print('')