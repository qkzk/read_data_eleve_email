import json
import email
import base64
import pickle
import os.path
from pprint import pprint

# google api
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def create_service():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service


def get_nsi_msg_list(service):
    # Call the Gmail API
    results_list_msg = service.users().messages().list(userId='me',
                                                       labelIds=["INBOX"],
                                                       q='"subject:NSI"'
                                                       ).execute()
    nsi_msg = results_list_msg['messages']

    dict_info = {}
    for message in nsi_msg:
        id = message["id"]
        result_msg = service.users().messages().get(userId='me',
                                                    id=id).execute()

        # extract the payload of the msg
        list_payload = result_msg['payload']['headers']
        # find the subject payload
        for message_payload in list_payload:
            # find the subject dict
            if message_payload['name'] == 'Subject':
                message_subject = message_payload['value']
                if not "Repl.it" in message_subject:
                    dict_info[id] = result_msg['payload']
                    # print(message_subject)

    return dict_info


def GetMimeMessage(service, user_id, msg_id):
    """Get a Message and use it to create a MIME Message.

    Args:
      service: Authorized Gmail API service instance.
      user_id: User's email address. The special value "me"
      can be used to indicate the authenticated user.
      msg_id: The ID of the Message required.

    Returns:
      A MIME Message, consisting of data from Message.
    """
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id,
                                                 format='full').execute()
        # format = 'raw').execute()

        list_payload = message['payload']['headers']
        # find the subject payload
        for message_payload in list_payload:
            # find the subject dict
            if message_payload['name'] == 'Subject':
                message_subject = message_payload['value']
                # find the author dict
            if message_payload['name'] == 'Return-Path':
                message_from = message_payload['value']

        dict_msg = {"from": message_from,
                    "body": message['snippet'].replace("&#39;", "'"),
                    "subject": message_subject}

        return dict_msg
    except Exception as e:
        print('An error occurred')
        print(e)
        raise


def scrap_from(from_msg):
    splitted = from_msg[1:-1].split('@')[0].split('.')
    return splitted[1]+'_'+splitted[0]


def scrap_email(from_msg):
    return from_msg[1:-1]


def scrap_name(from_msg):
    return from_msg.replace("_", " ")


if __name__ == '__main__':

    service = create_service()
    dict_info = get_nsi_msg_list(service)

    print(len(dict_info))

    dict_nsi_msg = {}
    for id in dict_info.keys():
        dict_msg = GetMimeMessage(service, 'me', id)
        author = scrap_from(dict_msg["from"])
        email_addr = scrap_email(dict_msg["from"])
        name = scrap_name(author)
        dict_msg['from'] = email_addr
        dict_msg['name'] = name
        dict_nsi_msg[author] = dict_msg

    with open("dict_msg.json", "w", encoding='utf-8') as f:
        json.dump(dict_nsi_msg, f, ensure_ascii=False, indent=4, sort_keys=True)
