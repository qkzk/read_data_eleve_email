import json
import os.path
import pickle
from pprint import pprint

# google api
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# spreadsheet id
from spreadsheet_id import SAMPLE_SPREADSHEET_ID

# If modifying these scopes, delete the file token_sheet.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_RANGE_NAME = 'Tr1!A2:E'


def create_service():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token_sheet.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token_sheet.pickle'):
        with open('token_sheet.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials_sheets.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token_sheet.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)
    return service


def write_data_sheet(service, dict_msg):
    # Call the Sheets API
    sheet = service.spreadsheets()
    values = [[value["name"], value["from"], value["body"]]
              for key, value in dict_msg.items()]
    body = {'values': values}
    result = service.spreadsheets().values().update(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        range=SAMPLE_RANGE_NAME,
        valueInputOption="USER_ENTERED",
        body=body
    ).execute()
    print('{0} cells updated.'.format(result.get('updatedCells')))


if __name__ == '__main__':
    with open("dict_msg.json", "r", encoding='utf-8') as f:
        dict_msg = json.load(f)

    service = create_service()
    main(service, dict_msg)
