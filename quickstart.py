# Imports
# Imports the print_function from __future__
from __future__ import print_function

# Imports os.path
import os.path
# Imports pickle
import pickle

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
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.labels']

# Gets the authentication credits for the gmail api
def authenticate_gmail():
    # sets creds value to None
    creds = None
    
    """
        The file token.json stores the user's access and refresh tokens, and is 
        created automatically when the authorization flow completes for the first time.
    """

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
    sender_name, sender_email = sender_info.split('<')
    sender_name = sender_name.strip()
    sender_email = sender_email.replace('>', '').strip()
    
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
            label_info = {
                'label_name': label_name
            }
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
        label_ids = msg['labelIds']

        for label_id in label_ids:
            email_labels.append(label_id)

    except HttpError as error:
        print(f'An error ocurred: {error}')

    return email_labels

def check_label_existance(label_name_to_check):
    label_info_list = get_label_info()

    for label_info in label_info_list:
        if label_info['label_name'] == label_name_to_check:
            return True
        
    return False

# Runs main function
if __name__ == '__main__':
    # Calls the email function
    #grouped_emails = get_grouped_emails()
    #pprint(grouped_emails)

    # Calls the label function
    #label_info_list = get_label_info()
    #pprint(label_info_list)

    # Calls the message label function
    label_name_to_check = "IMPORTANT"
    label_exist = check_label_existance(label_name_to_check)
    if label_exist:
        print(f"The label '{label_name_to_check}' exists.")
    else:
        print(f"The label '{label_name_to_check}' does not exist.")

    # Just so it works
    print('')