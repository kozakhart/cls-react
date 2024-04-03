from datetime import datetime
from boxsdk import Client, CCGAuth
from django.core.files.storage import FileSystemStorage
import os
from dotenv import load_dotenv
import csv
# test
load_dotenv()

BOX_CLIENT_SECRET = os.getenv('BOX_CLIENT_SECRET')
BOX_CLIENT_ID = os.getenv('BOX_CLIENT_ID')
BOX_ENTERPRISE_ID = os.getenv('BOX_ENTERPRISE_ID')

def create_client():
    auth = CCGAuth(
        client_id=BOX_CLIENT_ID,
        client_secret=BOX_CLIENT_SECRET,
        enterprise_id=BOX_ENTERPRISE_ID
        )
    client = Client(auth)
    return client

from requests.structures import CaseInsensitiveDict
import requests

def get_folder(token, client):
    url = f'https://api.box.com/2.0/folders/185240535599'
    headers= CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = f"Bearer {token}"
    response_API = requests.post(url, headers=headers, verify=False)
    response_json = response_API.json()
    subfolder = client.folder('0').create_subfolder('My Stuff')
    print(response_API.status_code)
    print(response_json)

    return token


slat_folder = '185240535599'
file_id = '1084898659538'

def create_folder(client, student_name, slat_folder):
    student_folder = client.folder(slat_folder).create_subfolder(student_name)
    print('folder created')

def upload_files(client, student_name, language, files, folder):
    title = student_name + " " + language
    student_folder = client.folder(folder).create_subfolder(title)
    all_items = client.folder(folder).get_items()
    for item in all_items:
        if title in item.name:
            folder_id = item.id
            print(folder_id)
    for f in files:
        new_file = client.folder(folder_id).upload(f)
        print('files uploaded')

# files = [r'C:\Users\kozak\opi_render\OPI_Signup\myapp\database_scripts\lti.py', r'C:\Users\kozak\opi_render\OPI_Signup\myapp\database_scripts\make_pdf.py']
# client = create_client()
# upload_files(client, 'Peter', files)

#imports hidden
from os import access
import os
from PyPDF2 import PdfWriter, PdfReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import *
from django.core.files.storage import FileSystemStorage

def create_pdf(full_name, byu_id, language, thesis):
    current_month = str(datetime.now().month)
    current_year = str(datetime.now().year)
    current_day = str(datetime.now().day)

    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFillColorRGB(0, 0, 0)
    can.setFont("Times-Roman", 16)
    # full_name = 'Peter Hart'
    # byu_id = '0987654321'
    # language = 'Russian'
    # thesis = '01-01-2000'
    today = current_month + '-' + current_day + '-' + current_year

    can.drawString(250, 650, full_name)
    can.drawString(250, 595, byu_id)
    can.drawString(250, 540, language)
    can.drawString(250, 485, thesis)
    can.drawString(250, 430, today)
    can.save()

    #move to the beginning of the StringIO buffer
    packet.seek(0)

    # create a new PDF with Reportlab
    new_pdf = PdfReader(packet)
    # read your existing PDF
    pdf_path = os.path.abspath("myapp/box_api/SLaT_PDF_Template.pdf")
    existing_pdf = PdfReader(open(pdf_path, "rb"))
    output = PdfWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.pages[0]
    page.merge_page(new_pdf.pages[0])
    output.add_page(page)
    # finally, write "output" to a real file
    outputStream = open(f"{full_name} Information.pdf", "wb+")
    output.write(outputStream)
    FileSystemStorage(location="/tmp").save(f"{full_name} Information.pdf", outputStream)
    outputStream.close()

    if os.path.exists(f"{full_name} Information.pdf"):
        os.remove(f"{full_name} Information.pdf")
    else:
        print('failed to create student information pdf')

cert_folder = '190685933673'

def create_folder_cert(client, student_name, cert_folder):
    student_folder = client.folder(cert_folder).create_subfolder(student_name)
    print('folder created')

def upload_files_cert(client, student_name, files, cert_folder):
    student_folder = client.folder(cert_folder).create_subfolder(student_name)
    all_items = client.folder(cert_folder).get_items()
    for item in all_items:
        if student_name in item.name:
            folder_id = item.id
            print(folder_id)
    for f in files:
        new_file = client.folder(folder_id).upload(f)
        print('files uploaded')

#create_mapl_application(firstname='Peter', middlename='Russell', lastname='Hart', email='kozakhart@gmail.com', byuid='123456789', phone='623-414-1835', major='Russian', heard_about='Friend', semester_of_entry='20235', academic_status='Senior', gpa='3.6', opi_score='Advanced High', opi_date='05/23/23', wpt_score='IH', wpt_date='05/23/23', alt_score='AL', alt_date='05/23/23', art_score='Superior', art_date='05/23/23', other_test_name='Important Test', other_test_score='Some other rating', other_test_date='05/23/23', institution_name='UVU', institution_location='Utah', institution_from_date='05/23/23', institution_to_date='05/23/23', degree='BA', graduation_date='05/23/23', recommender_name_1='John', recommender_title_1='Mr', recommender_institution_1='UVU', recommender_email_1='asdf@gmail.com', recommender_phone_1='123-123-1234', recommender_name_2='Samantha', recommender_title_2='Mrs', recommender_institution_2='UVU', recommender_email_2='asdf@gmail.com', recommender_phone_2='1231231234', student_signature='Peter Hart', signature_date='05/23/23', location_of_experience='This is my experience. There is more. I need to make this super long. This is my experience. There is more. I need to make this super long. This is my experience. There is more. I need to make this super long. This is my experience. There is more. I need to make this super long.')

def create_pdf_cert(box_client, record_id, full_name, language, level, opi_score, wpt_score, today, cert_type):
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfbase import pdfmetrics

    pdfmetrics.registerFont(TTFont('TimesNewRoman', 'myapp/box_api/times_new_roman.ttf'))

    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFillColorRGB(0, 0, 0)

    if cert_type == 'False':
        can.setFont('TimesNewRoman', 31)
        can.drawCentredString(390, 320, full_name)

        can.setFont("TimesNewRoman", 22)
        can.drawCentredString(246, 221, opi_score)
        can.drawCentredString(526, 221, wpt_score)

        can.setFont("TimesNewRoman", 18)
        can.drawCentredString(570, 121, today)

        can.setFont("TimesNewRoman", 20)
        can.drawCentredString(390, 440, language + ' LANGUAGE CERTIFICATE')

        can.setFont("TimesNewRoman", 24)
        can.drawCentredString(390, 395, level + ' LEVEL')
        can.save()

        #move to the beginning of the StringIO buffer
        packet.seek(0)

        # create a new PDF with Reportlab
        new_pdf = PdfReader(packet)
        # read your existing PDF
        pdf_path = os.path.abspath("myapp/box_api/cert_template.pdf")
        print(pdf_path)
        existing_pdf = PdfReader(open(pdf_path, "rb"))
        output = PdfWriter()
        # add the "watermark" (which is the new pdf) on the existing page
        page = existing_pdf.pages[0]
        page.merge_page(new_pdf.pages[0])
        output.add_page(page)
    elif cert_type == 'True':
        can.setFont('TimesNewRoman', 31)
        #320
        can.drawCentredString(390, 310, full_name)

        can.setFont("TimesNewRoman", 22)
        can.drawCentredString(390, 214, opi_score)

        can.setFont("TimesNewRoman", 18)
        can.drawCentredString(570, 110, today)

        can.setFont("TimesNewRoman", 20)
        can.drawCentredString(390, 430, language + ' LANGUAGE CERTIFICATE')

        can.setFont("TimesNewRoman", 24)
        can.drawCentredString(390, 385, level + ' LEVEL')
        can.save()

        packet.seek(0)

        new_pdf = PdfReader(packet)

        pdf_path = os.path.abspath("myapp/box_api/cert_template_opi_only.pdf")
        print(pdf_path)
        existing_pdf = PdfReader(open(pdf_path, "rb"))
        output = PdfWriter()

        page = existing_pdf.pages[0]
        page.merge_page(new_pdf.pages[0])
        output.add_page(page)

    outputStream = open(f"{record_id} {full_name} {language.capitalize()} Language Certificate.pdf", "wb")
    output.write(outputStream)
    #FileSystemStorage(location="/tmp").save(f"{full_name} Language Certificate.pdf", outputStream)
    outputStream.close()
    box_folder_id = '190685933673'
    new_file = box_client.folder(box_folder_id).upload(f"{record_id} {full_name} {language.capitalize()} Language Certificate.pdf")


    if os.path.exists(f"{record_id} {full_name} {language.capitalize()} Language Certificate.pdf"):
        os.remove(f"{record_id} {full_name} {language.capitalize()} Language Certificate.pdf")
    else:
        print('failed to create student information pdf')
    return new_file.id

def generate_shareable_link(client, file_id):
    #file_id = '1259828991808'
    url = client.file(file_id).get_shared_link(access='open', allow_download=True, allow_edit=False)
    print(url)
    return url

def append_to_fulton_report(client, userdata):
    # {"Last Name":full_name.split(' ')[1], "First Name":full_name.split(' ')[0], "RouteY ID":"",
    #     "BYUID":byuid, "Major1":major1, "Major2":major2 ,"Major3":major3,"Minor1":minor1,"Minor2":minor2,"Minor3":minor3,"Language":language,
    #     "OPI Rating":opi_score, "WPT Rating":wpt_score, "Semester Finished":str(year + yearterm), "Course1":course1, "Course2":course2, "Course3">    last_name = userdata['Last Name']
    last_name = userdata['Last Name']
    first_name = userdata['First Name']
    byuid = userdata['BYUID']
    routeY = userdata['RouteY ID']
    major1 = userdata['Major 1']
    major2 = userdata['Major 2']
    major3 = userdata['Major 3']
    minor1 = userdata['Minor 1']
    minor2 = userdata['Minor 2']
    minor3 = userdata['Minor 3']
    language = userdata['Language']
    opi_score = userdata['OPI Rating']
    wpt_score = userdata['WPT Rating']
    yearterm = userdata['Semester Finished']
    course1 = userdata['Course 1']
    course2 = userdata['Course 2']
    course3 = userdata['Course 3']
    other_courses = userdata['Other Courses']

    folder_id = "240958742190"
    all_items = client.folder(folder_id).get_items()
    for item in all_items:
        if 'Fulton Report' in item.name:
            file_id = item.id
            print(file_id)
    open_file = 'Fulton Report Data.csv'
    with open(open_file, 'wb') as download_file:
        client.file(file_id).download_to(download_file)
        download_file.close()

    with open(open_file, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([last_name, first_name, routeY, byuid, major1, major2, major3, minor1, minor2, minor3, language, opi_score, wpt_score, yearterm, course1, course2, course3, other_courses])
    client.file(file_id).delete()
    new_file = client.folder(folder_id).upload('Fulton Report Data.csv')
    if os.path.exists('Fulton Report Data.csv'):
        os.remove('Fulton Report Data.csv')
    else:
        print('failed to create student information pdf')