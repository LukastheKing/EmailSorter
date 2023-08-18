# Imports
# Imports the print_function from __future__
from __future__ import print_function

# Imports os.path
import os.path
# Imports pickle
import pickle

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
""" 
    Shows basic usage of the gmail API.
    Lists the user's Gmail labels.
"""

# Sets the scope of the project to read only
# If modyfying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Defines main function 
def main():
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
    
    try:
        # Call the Gmail API
        # Builds access to the gmail api
        service = build('gmail', 'v1', credentials = creds)

        # Code for message functionality
        results = service.users().messages().list(userId='me').execute()
        messages = results.get('messages', [])

        if not messages:
            print('No messages found.')
            return
        
        for message in messages:
            message_id = message['id']
            msg = service.users().messages().get(userId='me', id=message_id).execute()

            subject = None
            for header in msg['payload']['headers']:
                if header['name'] == 'Subject':
                    subject = header['value']
                    break

            if subject:
                print(f"Subject: {subject}")
            else:
                print("No subject found.")
            print("------")

        # Code for label functionality
        """
            results = service.users().labels().list(userId='me').execute()
            labels = results.get('labels',[])

            label_names = []

            if not labels:
                print('No labels found.')
                return
            #print('Labels:')
            for label in labels:
                label_names.append(label['name'])  # Append each label name to the list

            #print('Labels saved:', label_names)
            return label_names
        """
    
    # Uses HttpError to send an error if something fails
    except HttpError as error:
        #TODO(developer) - Handle errors form gmail API.
        print(f'An error ocurred:{error}')

# Runs main function
if __name__ == '__main__':
    # Calls the main function
    main()