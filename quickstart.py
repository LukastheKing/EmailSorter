# Imports
# Imports the print_function from __future__
from __future__ import print_function

# Imports os.path
import os.path
# Imports pickle
import pickle

import pprint

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
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Defines main function 
def get_email_info():
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
            creds = flow.run_local_server(port=0,success_message='test')
        # Saves the credentials for the next run
        # Uses open to open the token.pickle file in write binary mode (wb) 
        with open('token.pickle', 'wb') as token:
            # Uses dump to save the credentials into the file
            pickle.dump(creds, token)
    
    # Creates an empty list fo the subjects
    email_info_list = []

    try:
        # Call the Gmail API
        # Builds access to the gmail api
        service = build('gmail', 'v1', credentials = creds)

        # Code for message functionality
        
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
                # Determines if the headers name is equal to the subject
                if header['name'] == 'Subject':
                    # Assigns the header value to subject
                    subject = header['value']
                    break
                elif header['name'] == 'From':
                    sender_info = header['value']
                    sender_name, sender_email = parse_sender_info(sender_info)
                
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

def parse_sender_info(sender_info):
    # Parse sender info in the format "Name <email>"
    sender_name, sender_email = sender_info.split('<')
    sender_name = sender_name.strip()
    sender_email = sender_email.replace('>', '').strip()
    return sender_name, sender_email

# Runs main function
if __name__ == '__main__':
    # Calls the main function
    email_info_list = get_email_info()
    print(email_info_list)
