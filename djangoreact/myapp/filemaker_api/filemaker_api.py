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

def create_record(scores, approved, entry_date, entry_time, firstname, lastname, byuid,
    netid, email, reason, language, language_other, experience, major, second_major, minor, come_to_campus,
    cannot_come, testdate1, testdate2, time1, time2, time3, time4, CertificateStatus, phone, token):
    url = 'https://clsfilemaker.byu.edu/fmi/data/vLatest/databases/opi/layouts/opi/records'
    headers= CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = f"Bearer {token}"
    data=f"""
    {{ "fieldData":
     {{ "Scores": "{scores}", "TestScheduled":"No", "EmailSent":"No", "Approved":"{approved}", "EntryTime": "{entry_time}", 
        "EntryDate":"{entry_date}", "FirstName":"{firstname}", "Lastname":"{lastname}", "BYUID":"{byuid}",
        "NetID": "{netid}", "Email":"{email}", "Reason":"{reason}", "Language":"{language}",
        "LanguageOther": "{language_other}", "PreviousExperience":"{experience}", "Major":"{major}", "SecondMajor":"{second_major}",
        "Minor": "{minor}", "ComeToCampus":"{come_to_campus}", "CannotCome":"{cannot_come}", "TestDate1":"{testdate1}", 
        "TestDate2": "{testdate2}", "Time1":"{time1}", "Time2":"{time2}", "Time3":"{time3}",
        "Time4": "{time4}", "CertificateStatus":"{CertificateStatus}", "Phone":"{phone}", "LTISchedule":"None"
        }}
    }}
    """
    response_API = requests.post(url, headers=headers, data=data)
    response_API = response_API.json()
    print(response_API)
    print('Record Created Successfully')
    record_id = response_API['response']['recordId']
    print(record_id)
    return record_id
#create_record()

def find_record(field_name, data, token):
    url = 'https://clsfilemaker.byu.edu/fmi/data/vLatest/databases/opi/layouts/opi/_find'
    headers= CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = f"Bearer {token}"
    data=f"""
    {{ 
        "query": [
      {{"{field_name}": "{data}"}}],
      "limit": "10"
    }}
    """
    record_response = requests.post(url, headers=headers, data=data)
    
    record_response = record_response.json()

    record_id = record_response['response']['data'][0]['recordId']

    print(record_response)
    print('Records found')
    return record_response

def find_first_last_name(first='', last='', token=None):
    url = 'https://clsfilemaker.byu.edu/fmi/data/vLatest/databases/opi/layouts/opi/_find'
    headers= CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = f"Bearer {token}"
    data=f"""
    {{"query": [{{"FirstName": "{first}"}},
    {{"LastName": "{last}"}}],
      "limit": "100"
    }}
    """ 

    record_response = requests.post(url, headers=headers, data=data)
    
    record_response = record_response.json()

   # record_id = record_response['response']['data'][0]['recordId']

    print(record_response)
    print('Records found')
    return record_response


def find_record_ID(token, id):
    url = f'https://clsfilemaker.byu.edu/fmi/data/vLatest/databases/opi/layouts/opi/records/{id}'
    headers= CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = f"Bearer {token}"

    record_response = requests.get(url, headers=headers)
    print(record_response)    
    record_response = record_response.json()

  
    #print(record_id)
    print(record_response)
    print('Records found')
    return record_response

def edit_record(field_name, data, token, record_id):
    url = f'https://clsfilemaker.byu.edu/fmi/data/vLatest/databases/opi/layouts/opi/records/{record_id}'
    print(url)
    headers= CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = f"Bearer {token}"
    data=f"""
    {{ 
        "fieldData": 
      {{"{field_name}": "{data}"}}
    }}
    """
    record_response = requests.patch(url, headers=headers, data=data)
    print(record_id)
    print(record_response.status_code)

    print('Record edited')

def logout(token):
    url = f'https://clsfilemaker.byu.edu/fmi/data/vLatest/databases/opi/sessions/{token}'
    headers= CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    response_API = requests.delete(url, headers=headers).json()
    print('Logout successful')
#logout()
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

def return_all_for_student(byuid, token):
    url = 'https://clsfilemaker.byu.edu/fmi/data/vLatest/databases/opi/layouts/opi/_find'
    headers= CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = f"Bearer {token}"
    data=f"""
    {{"query": [{{{"BYUID": "{byuid}"}
    }}],
      "limit": "100"
    }}
    """ 
    # data=f"""
    # {{"query": [{{"FirstName": "{first}",
    # "LastName": "{last}"
    # }}],
    #   "limit": "1"
    # }}
    # """
    record_response = requests.post(url, headers=headers, data=data)
    
    record_response = record_response.json()

    return record_response

def need_approval(token):
    url = 'https://clsfilemaker.byu.edu/fmi/data/vLatest/databases/opi/layouts/opi/_find'
    headers= CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = f"Bearer {token}"
    data="""
    {"query": [{"Approved": "Waiting"}, 
            {"Approved": "Pending"},
            {"Approved": "No"}
    ],
      "limit": "1000"
    }
    """ 
    record_response = requests.post(url, headers=headers, data=data)
    
    record_response = record_response.json()
    print(record_response)
    return record_response

def needs_scheduling(token):
    url = 'https://clsfilemaker.byu.edu/fmi/data/vLatest/databases/opi/layouts/opi/_find'
    headers= CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = f"Bearer {token}"
    data="""
    {
        "query": [
      {"Approved": "Yes",
      "TestScheduled": "No"}
      ],
      "limit": "1"
    }
    """
    record_response = requests.post(url, headers=headers, data=data)

    record_response = record_response.json()

    status_code = record_response['messages'][0]['code']
    print(record_response)
    if status_code == '0':
        print('Records found')
        valid = True
    else:
        valid = False
    return record_response, valid

def delete_record(record_id, token):
    url = f'https://clsfilemaker.byu.edu/fmi/data/vLatest/databases/opi/layouts/opi/records/{record_id}'
    headers= CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = f"Bearer {token}"
    record_response = requests.delete(url, headers=headers)
    
    record_response = record_response.json()
    print(record_response)
    return record_response

def adaptive_find_record(token, **kwargs):
    headers= CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = f"Bearer {token}"
    insert = [f""" "{key}": "{value}" """ for key, value in kwargs.items()]
    data="""{"query": [{}]}"""
    length = len(insert)
    iterator = 1
    for i in insert:
        if iterator < length:
            data = data[:12] + ',' + i + data[12:]
            iterator += 1
        else:
            data = data[:12] + i + data[12:]
    print(data)

    for key, value in kwargs.items():
        if key == 'FirstName' and value == '=':
            url = 'https://clsfilemaker.byu.edu/fmi/data/vLatest/databases/opi/layouts/opi/records?_offset=1&_limit=10000'
            record_response = requests.get(url, headers=headers, data=data)

            break
        else:
            url = 'https://clsfilemaker.byu.edu/fmi/data/vLatest/databases/opi/layouts/opi/_find'
            record_response = requests.post(url, headers=headers, data=data)
    
    record_response = record_response.json()

    try:
        record_id = record_response['response']['data'][0]['recordId']
    except KeyError:
        pass

    print(record_response)

    status_code = record_response['messages'][0]['code']
    if status_code == '0':
        print('Records found')
        valid = True
    else:
        valid = False
    return record_response, valid

# import csv

# # Assuming you have already retrieved the data
# token = login()
# all_data = get_all(token)
# logout(token)

# from datetime import datetime

# now = datetime.now()

# print("Today's date and time:", now)

# formatted_date_time = now.strftime("%Y-%m-%d %H-%M-%S")
# print("Formatted date and time:", formatted_date_time)

# field_names = [
#     'RecordId', 'Scores', 'TestScheduled', 'Approved', 'EntryDate', 'EntryTime',
#     'FirstName', 'LastName', 'BYUID', 'NetID', 'Email', 'Reason',
#     'Language', 'LanguageOther', 'PreviousExperience', 'Major', 'SecondMajor',
#     'Minor', 'ComeToCampus', 'CannotCome', 'TestDate1', 'TestDate2',
#     'Time1', 'Time2', 'Time3', 'Time4', 'CertificateStatus', 'Phone',
#     'EmailSent', 'LTISchedule'
# ]
# file_name = formatted_date_time + ".csv"
# # Open a CSV file for writing
# with open(file_name, 'w', newline='') as csv_file:
#     writer = csv.DictWriter(csv_file, fieldnames=field_names)
    
#     # Write the header row to the CSV file
#     writer.writeheader()
    
#     # Write data for each student to the CSV file
#     for student in all_data['response']['data']:
#         student_data = {
#             'RecordId': student['recordId'],
#             'Scores': student['fieldData']['Scores'],
#             'TestScheduled': student['fieldData']['TestScheduled'],
#             'Approved': student['fieldData']['Approved'],
#             'EntryDate': student['fieldData']['EntryDate'],
#             'EntryTime': student['fieldData']['EntryTime'],
#             'FirstName': student['fieldData']['FirstName'],
#             'LastName': student['fieldData']['LastName'],
#             'BYUID': student['fieldData']['BYUID'],
#             'NetID': student['fieldData']['NetID'],
#             'Email': student['fieldData']['Email'],
#             'Reason': student['fieldData']['Reason'],
#             'Language': student['fieldData']['Language'],
#             'LanguageOther': student['fieldData']['LanguageOther'],
#             'PreviousExperience': student['fieldData']['PreviousExperience'],
#             'Major': student['fieldData']['Major'],
#             'SecondMajor': student['fieldData']['SecondMajor'],
#             'Minor': student['fieldData']['Minor'],
#             'ComeToCampus': student['fieldData']['ComeToCampus'],
#             'CannotCome': student['fieldData']['CannotCome'],
#             'TestDate1': student['fieldData']['TestDate1'],
#             'TestDate2': student['fieldData']['TestDate2'],
#             'Time1': student['fieldData']['Time1'],
#             'Time2': student['fieldData']['Time2'],
#             'Time3': student['fieldData']['Time3'],
#             'Time4': student['fieldData']['Time4'],
#             'CertificateStatus': student['fieldData']['CertificateStatus'],
#             'Phone': student['fieldData']['Phone'],
#             'EmailSent': student['fieldData']['EmailSent'],
#             'LTISchedule': student['fieldData']['LTISchedule'],
#         }
        
#         # Write the student's data to the CSV file
#         writer.writerow(student_data)

# print("Data has been written to student_data.csv")


# logout(token)

# #adaptive_find_record(token, FirstName="Kayla")
# # create_record(scores='AH/IH', approved='No', entry_date='01/01/22', entry_time='00:00:12', firstname='Test', lastname='Person', byuid='052163478',
# # netid='phart4', email='a', reason='a', language='a', language_other='a', experience='a', major='a', second_major='a', minor='a', come_to_campus='a',
# # cannot_come='a', testdate1='01/01/22', testdate2='01/01/22', time1='11:00', time2='11:00', time3='11:00', time4='11:00', CertificateStatus='s', phone='123-122-1234', token=token)
# # needs_scheduling(token)

# # response_ = get_all(token)
# # for i in response_['response']['data']:
# #     if i['fieldData']['NetID'] == 'asdf':
# #         record_id = i['recordId']
# #         delete_record(record_id, token)

        
# #find_record('BYUID', '052163478', token)
# # test = find_first_last_name('Peter', '', token)
# # print(test['messages'][0]['code'])

# # try:
# #     test = find_record('BYUID', '357065560', token)
# #     print(test['response']['data'][0]['fieldData']['Language'])
# #     print('hi')
# #     if test['messages'][0]['code'] == '0':
# #         if test['response']['data'][0]['fieldData']['Language'] in 'CHIN':
# #             print('cant make another one')
# # except KeyError:
# #     print('does not exist')
# logout(token)