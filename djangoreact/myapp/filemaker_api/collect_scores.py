import filemaker_api as filemaker
import lti_api as lti 
import openpyxl

token = filemaker.login()
students = filemaker.adaptive_find_record(token=token, FirstName='=')
filemaker.logout(token=token)

browser = lti.get_browser()
score_type = 'OPI Test'
from_date = '10/01/2023'
to_date = '10/30/2023'
# selected_data = request.data.get('selectedData')
selected_data = ['firstname', 'lastname', 'byuid', 'score']
print(selected_data)
kwargs = {data: None for data in selected_data}

lti_data = lti.get_data(browser, fromdate=from_date, todate=to_date, test_type=score_type, kwargs=kwargs)

student_list = []
for student in students[0]['response']['data']:
    print(student['fieldData']['FirstName'], student['fieldData']['LastName'], student['fieldData']['BYUID'])
    byuid = student['fieldData']['BYUID']
    student_list.append([byuid])
workbook = openpyxl.load_workbook('lti_data.xlsx')

sheet = workbook.active

for desired_byuid in student_list:
    matching_rows = []

    for row in sheet.iter_rows(min_row=2, values_only=True):
        candidateid = row[2]  # Assuming byuid is in the third column (0-based index)
        candidateid = candidateid.strip("'")
        print(candidateid, 'no quotes')
        if candidateid == desired_byuid:
            matching_rows.append(row)

# Print or process matching rows
for row in matching_rows:
    print("Found Row:", row)

# Close the workbook when done
workbook.close()

# print(data)

lti.close_browser(browser)

