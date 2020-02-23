# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 08:16:43 2020

@author: josep
"""

from __future__ import print_function

from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2 import service_account

import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
SAMPLE_RANGE_NAME = 'Class Data!A2:E'

def main():
    global service
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            creds = service_account.Credentials.from_service_account_file('sheets_api.json')
            
            #InstalledAppFlow.from_client_secrets_file(
            #    'sheets_api.json', SCOPES)
            #creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        #with open('token.pickle', 'wb') as token:
        #    pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print('Name, Major:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print('%s, %s' % (row[0], row[4]))

#Appending column

def insertOneRecord(sheetId, value):
    global service
    data = {
     "requests": [
       {
         "appendCells": {
           "sheetId": sheetId,
           "rows": [  {"values": [
               {"userEnteredValue": {"stringValue": 'a'}},
               {"userEnteredValue": {"stringValue": 'b'}}
              ]}],
           "fields" : "userEnteredValue"
         }
       }]}
    response = service.spreadsheets().batchUpdate(spreadsheetId = sheetId,body = data).execute()

def send_request():
    requests = []
    # Change the spreadsheet's title.
    requests.append({
        'updateSpreadsheetProperties': {
            'properties': {
                'title': 'Sandwich'
            },
            'fields': 'title'
        }
    })
    
    # Add additional requests (operations) ...
    
    body = {
        'requests': requests
    }
    response = service.spreadsheets().batchUpdate(
        spreadsheetId='1FkPIMQlI7_wMYGP_0jdq62lCF3p65VaeZmr576XdTso',
        body=body).execute()
    find_replace_response = response.get('replies')[1].get('findReplace')
    print('{0} replacements made.'.format(
        find_replace_response.get('occurrencesChanged')))
    return 

if __name__ == '__main__':
    ssid = '1FkPIMQlI7_wMYGP_0jdq62lCF3p65VaeZmr576XdTso'
    service = 'a'
    main()
    insertOneRecord(ssid, ['hello', 'hi'])
