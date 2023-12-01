#from django.test import TestCase
# Create your tests here.

import base64
import filemaker_api.filemaker_api as filemaker


token = filemaker.login()

data = filemaker.adaptive_find_record(token, FirstName="Test", LastName='Person')

byuid = data[0]['response']['data'][0]['fieldData']['BYUID']
language = data[0]['response']['data'][0]['fieldData']['Language']
entrydate = data[0]['response']['data'][0]['fieldData']['EntryDate']

final = byuid + '&' + language + '&' +entrydate
filemaker.logout(token)

encoded_string = base64.b64encode(final.encode('utf-8')).decode('utf-8')

print(encoded_string)

decoded_string = base64.b64decode(encoded_string).decode('utf-8')

print(decoded_string)

   





