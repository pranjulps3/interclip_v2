from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


SCOPES = ['https://www.googleapis.com/auth/drive.appdata']

class Drive:
    def __init__(self):
        self.creds = None
        if os.path.exists('drive.token.pickle'):
            with open('drive.token.pickle', 'rb') as token:
                print("Loading Credentials....", end='')
                self.creds = pickle.load(token)
                print("done.")
        if not self.creds or not self.creds.valid:
            print("Invalid/No credentials found.")
            if self.creds and self.creds.expired and self.creds.refresh_token:
                print("Refreshing expired credentials....", end='')
                self.creds.refresh(Request())
                print("done.")
            else:
                print("Authorizing for Credentials....", end='')
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                self.creds = flow.run_local_server()
                print("done.")
            with open('drive.token.pickle', 'wb') as token:
                print("Saving Credentials....", end='')
                pickle.dump(self.creds, token)
                print("done.")
        self.service = build('drive', 'v3', credentials=self.creds)
    
    def listItems(self):
        res = self.service.files().list().execute()
        items = res.get('files', [])
        if not items:
            print('No files found.')
        else:
            print('Files:')
            for item in items:
                print(u'{0} ({1})'.format(item['name'], item['id']))

if __name__ == '__main__':
    drive = Drive()
    drive.listItems()