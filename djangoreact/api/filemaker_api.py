from urllib import response
import requests
from requests.structures import CaseInsensitiveDict
import os
from dotenv import load_dotenv
load_dotenv()

# Notes:
# useful code for debugging:
#print(response_API.status_code)
# print(response_API.reason)
# print(response_API.text)
    
def login():
    LOGINAUTH = os.getenv('LOGINAUTH')
    DATABASE_NAME = os.getenv('DATABASE_NAME')
    DATABASE_USER = os.getenv('DATABASE_USER')
    DATABASE_PASS = os.getenv('DATABASE_PASS')

    
    url = 'https://clsfilemaker.byu.edu/fmi/data/vLatest/databases/opi/sessions'
    headers= CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = "Basic " + LOGINAUTH
    data=f"""
    {{ "fmDataSource":
    [ {{ "database": "{DATABASE_NAME}", "username":"{DATABASE_USER}", "password":"{DATABASE_PASS}" }} ]
    }}
    """

    response_API = requests.post(url, headers=headers, data=data).json()
    token = response_API['response']['token']
    print('Login successful')
    return token

def logout(token):
    url = f'https://clsfilemaker.byu.edu/fmi/data/vLatest/databases/opi/sessions/{token}'
    headers= CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    response_API = requests.delete(url, headers=headers).json()
    print('Logout successful')

def get_all_by_date(token):
    base_url = "https://clsfilemaker.byu.edu/fmi/data/"
    version = "vLatest"  # Replace with your desired version
    database_name = "opi"
    layout_name = "opi"

    url = f"{base_url}{version}/databases/{database_name}/layouts/{layout_name}/records?_limit=100000&_sort=[{{\"fieldName\":\"EntryDate\",\"sortOrder\":\"descend\"}}]"

    headers= CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = f"Bearer {token}"
    record_response = requests.get(url, headers=headers)
    
    print('filemaker: ', record_response.status_code)
    # print(record_response.json())
    record_response = record_response.json()
    return record_response

def get_all(token):
    url = 'https://clsfilemaker.byu.edu/fmi/data/vLatest/databases/opi/layouts/opi/records?_offset=1&_limit=10000'
    headers= CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = f"Bearer {token}"
    data="""
    { 
        "query": [
      {"FirstName": "="}]
    }
    """
    record_response = requests.get(url, headers=headers, data=data)
    
    print(record_response.status_code)
    record_response = record_response.json()

    #record_id = record_response['response']['data'][0]['recordId']
    print(record_response['response']['dataInfo'])
    #print(record_response)
    print('Records found')
    return record_response

def adaptive_find_record(token, **kwargs):
    url = 'https://clsfilemaker.byu.edu/fmi/data/vLatest/databases/opi/layouts/opi/_find'
    headers= CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = f"Bearer {token}"
    insert = [f""" "{key}": "{value}" """ for key, value in kwargs.items()]
    data="""{"query": [{}],"limit": "1000"}"""
    length = len(insert)
    iterator = 1
    for i in insert:
        #print(data)
        if iterator < length:
            data = data[:12] + ',' + i + data[12:]
            iterator += 1
        else:
            data = data[:12] + i + data[12:]
    #print(data)
    #print(length)
    record_response = requests.post(url, headers=headers, data=data)
    
    record_response = record_response.json()


    print(record_response)
    #print('Records found')
    return record_response

def edit_all_fields(scores, testscheduled, agree, entrydate, entrytime, firstname, lastname, byuid, netid, email, reason, language, languageother,
previousexperience,major,secondmajor,minor,cometocampus,cannotcome,testdate1,testdate2,time1,time2,time3,time4, CertificateStatus,phone,emailsent, lti_schedule, token, record_id):
    url = f'https://clsfilemaker.byu.edu/fmi/data/vLatest/databases/opi/layouts/opi/records/{record_id}'
    headers= CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = f"Bearer {token}"
    data=f"""
    {{ 
        "fieldData": 
      {{"Scores": "{scores}" ,"TestScheduled": "{testscheduled}",
      "Approved": "{agree}", "EntryDate": "{entrydate}",
      "EntryTime": "{entrytime}", "FirstName": "{firstname}",
      "LastName": "{lastname}", "BYUID": "{byuid}",
      "NetID": "{netid}", "Email": "{email}",
      "Reason": "{reason}", "Language": "{language}",
      "LanguageOther": "{languageother}", "PreviousExperience": "{previousexperience}",
      "Major": "{major}", "SecondMajor": "{secondmajor}",
      "Minor": "{minor}", "ComeToCampus": "{cometocampus}",
      "CannotCome": "{cannotcome}", "TestDate1": "{testdate1}",
      "TestDate2": "{testdate2}", "Time1": "{time1}",
      "Time2": "{time2}", "Time3": "{time3}",
      "Time4": "{time4}", "CertificateStatus": "{CertificateStatus}",
      "Phone": "{phone}", "EmailSent": "{emailsent}", "LTISchedule": "{lti_schedule}"
      }}
    }}
    """
    record_response = requests.patch(url, headers=headers, data=data)
    print(record_response.status_code)

    print('Record edited')

def delete_record(record_id, token):
    url = f'https://clsfilemaker.byu.edu/fmi/data/vLatest/databases/opi/layouts/opi/records/{record_id}'
    headers= CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = f"Bearer {token}"
    record_response = requests.delete(url, headers=headers)
    
    record_response = record_response.json()
    print(record_response)
    return record_response
    