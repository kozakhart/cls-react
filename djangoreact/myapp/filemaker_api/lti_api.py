import mechanicalsoup
from dotenv import load_dotenv
import os
import openpyxl

def get_browser():
    load_dotenv()
    LTI_USER = os.getenv('LTI_USER')
    LTI_PASS = os.getenv('LTI_PASS')
    browser = mechanicalsoup.StatefulBrowser()

    login_url = "https://tms.languagetesting.com/Clientsite/login.aspx"  # Replace with the actual login page URL
    print(browser.open(login_url))
    browser.select_form('form[id="form1"]')  # Replace with the actual form name or attributes
    browser["txtLoginID"] = LTI_USER  # Replace with your username
    browser["txtPassword"] = LTI_PASS  # Replace with your password
    browser.submit_selected()
    return browser

def get_data(browser, fromdate, todate, test_type, kwargs):
    if test_type == 'WPT':
        test_type = 'WPT Test (no grid)'
    if test_type == 'OPI':
        test_type = 'OPI Test'
    if test_type == 'OPIc':
        test_type = 'OPIc Test'
        
    download_url = "https://tms.languagetesting.com/clientsite/DownloadRatingsV2.aspx"
    print(browser.open(download_url))
    browser.select_form('form[id="form1"]')
    browser['ctl00$cphMain$txtFromDate'] = fromdate
    browser['ctl00$cphMain$txtToDate'] = todate
    browser['ctl00$cphMain$ddlTestOptions'] = test_type

    response = browser.submit_selected()
    print(response.status_code)
    response.raise_for_status()

    file_path = 'lti_data.xlsx'

    if os.path.exists(file_path):
        os.remove(file_path)
        
    with open(file_path, 'wb') as outf:
        outf.write(response.content)

    xlsx_file = openpyxl.load_workbook(file_path, data_only=True)

    sheet = xlsx_file.active

    firstname_index = 0
    lastname_index = 1
    byuid_index = 2
    BYU_ON_LINE_index = 3
    language_index = 4
    test_type_index = 5
    test_date_index = 6
    score_index = 7
    note_index = 8
    self_assessment_index = 9
    form_name_index = 10
    aappl_index = 11
    language_background_index = 12
    unit_index = 13
    major_index = 14
    minor_index = 15
    major2_index = 16
    minor2_index = 17
    special_instructions_index = 18
    testing_date_index = 19

    variable_mapping = {}
    for key, value in kwargs.items():
        if key in ['firstname', 'lastname', 'byuid', 'BYU_ON_LINE', 'language', 'test_type',
                   'test_date', 'score', 'note', 'self_assessment', 'form_name', 'aappl',
                   'language_background', 'unit', 'major', 'minor', 'major2', 'minor2',
                   'special_instructions', 'testing_date']:
            variable_mapping[key] = locals()[f'{key}_index']

    data_list = []
    for row in sheet.iter_rows(min_row=2, values_only=True):
        data = {}
        for variable_name, column_index in variable_mapping.items():
            cell_value = row[column_index]
            if cell_value is not None and isinstance(cell_value, str):
                cell_value = cell_value.strip()
            data[variable_name] = cell_value
        data_list.append(data)

    # if os.path.exists(file_path):
    #     os.remove(file_path)
    return data_list
    
def close_browser(browser):
    browser.close()



