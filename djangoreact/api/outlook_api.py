import requests
from requests.structures import CaseInsensitiveDict
import os
from dotenv import load_dotenv
load_dotenv()


def get_token():
    OUTLOOK_TENANT_ID = os.getenv('OUTLOOK_TENANT_ID')
    url = f'https://login.microsoftonline.com/{OUTLOOK_TENANT_ID}/oauth2/token'
    #url = "https://login.microsoftonline.com/byu.onmicrosoft.com/oauth2/token"

    headers= CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    # headers["Authorization"] = f"Bearer {token}"
    headers = {

    "client_id": os.getenv('OUTLOOK_CLIENT_ID'),

    "client_secret": os.getenv('OUTLOOK_VALUE'),

    "grant_type": "password",

    "username": os.getenv("OUTLOOK_USERNAME"),

    "password": os.getenv('OUTLOOK_PASSWORD'),

    "resource": 'https://graph.microsoft.com/',

    "scope": "Mail.ReadWrite Mail.Send"

}

    record_response = requests.post(url, data=headers)
    print("Get access token status:", record_response.status_code)

    record_response = record_response.json()
    return record_response['access_token']

def get_mailbox(access_token):
    #url = "https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messages"
    url = 'https://graph.microsoft.com/v1.0/me/mailFolders/?$top=100'
    headers= CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = f"Bearer {access_token}"
    response = requests.get(url, headers=headers)
    #print(response.text)

def get_folder(access_token, folder_id):
    url = f'https://graph.microsoft.com/v1.0/me/mailFolders/{folder_id}/messages'
    headers= CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = f"Bearer {access_token}"
    response = requests.get(url, headers=headers)
    #print(response.text)
    response = response.json()
    return response['value']

def create_message(access_token, data):
    url = "https://graph.microsoft.com/v1.0/me/messages"
    headers= CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = f"Bearer {access_token}"
    
    response = requests.post(url, headers=headers, json=data)
    print("Message created status:", response.status_code)
    response = response.json()
    return response['id']

def send_message(access_token, message_id):
    url = f"https://graph.microsoft.com/v1.0/me/messages/{message_id}/send"
    headers= CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = f"Bearer {access_token}"
    response = requests.post(url, headers=headers)
    print("Message sent status:", response.status_code)

def move_message(access_token, message_id, folder_id):
    url = f"https://graph.microsoft.com/v1.0/me/messages/{message_id}/move"
    headers= CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = f"Bearer {access_token}"
    data = {
        "destinationId": folder_id
    }
    response = requests.post(url, headers=headers, json=data)
    print("Message moved status:", response.status_code)
