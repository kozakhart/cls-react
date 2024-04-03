from datetime import datetime
from boxsdk import Client, CCGAuth
from django.core.files.storage import FileSystemStorage
import os
from dotenv import load_dotenv

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

def upload_files(client, student_name, files, slat_folder):
    student_folder = client.folder(slat_folder).create_subfolder(student_name)
    all_items = client.folder(slat_folder).get_items()
    for item in all_items:
        if student_name in item.name:
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



def create_mapl_application(firstname, middlename, lastname, email, byuid, phone, major, heard_about, semester_of_entry, 
                            academic_status, gpa, opi_score, opi_date, wpt_score, wpt_date, alt_score, alt_date, 
                            art_score, art_date, other_test_name, other_test_score, other_test_date, 
                            institution_name, institution_location, institution_from_date, institution_to_date, 
                            degree, graduation_date, recommender_name_1, recommender_title_1, recommender_institution_1, 
                            recommender_email_1, recommender_phone_1, recommender_name_2, recommender_title_2, recommender_institution_2, 
                            recommender_email_2, recommender_phone_2, student_signature, signature_date, location_of_experience):
    
    def wrap_text(canvas, text, x, y, max_width, max_height, font_name, font_size):
        text_object = canvas.beginText(x, y)
        text_object.setFont(font_name, font_size)
        lines = text.splitlines()
        y_offset = 0

        for line in lines:
            words = line.split(' ')
            current_line = ""
            for word in words:
                if canvas.stringWidth(current_line + word, font_name, font_size) <= max_width:
                    current_line += word + " "
                else:
                    text_object.textLine(current_line)
                    y_offset += font_size
                    if y_offset >= max_height:
                        break
                    current_line = word + " "
            if current_line:
                text_object.textLine(current_line)
                y_offset += font_size
                if y_offset >= max_height:
                    break

        canvas.drawText(text_object)

    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfbase import pdfmetrics

    #font_path = os.path.abspath(r"C:\Users\kozak\Code\cls-opi-aws\myapp\box_api\times_new_roman.ttf")
    #pdfmetrics.registerFont(TTFont('TimesNewRoman', font_path))

    pdfmetrics.registerFont(TTFont('TimesNewRoman', 'myapp/box_api/times_new_roman.ttf'))


    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFillColorRGB(0, 0, 0)
    can.setFont('TimesNewRoman', 14)
    can.drawString(210, 644, firstname)
    can.drawString(210, 618, middlename)
    can.drawString(210, 590, lastname)

    can.drawString(210, 563, email)
    can.drawString(210, 536, byuid)
    can.drawString(210, 510, phone)
    can.drawString(210, 483, major)
    can.drawString(210, 423, heard_about)
    can.drawString(210, 380, semester_of_entry)
    can.drawString(210, 337, academic_status)
    can.drawString(210, 308, gpa)
    can.drawString(210, 281, opi_score)
    can.drawString(210, 255, opi_date)
    can.drawString(210, 228, wpt_score)
    can.drawString(210, 201, wpt_date)
    can.drawString(210, 174, alt_score)
    can.drawString(210, 147, alt_date)
    can.drawString(210, 120, art_score)
    can.drawString(210, 93, art_date)

    can.save()
    packet.seek(0)
    page_1 = PdfReader(packet)


    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFillColorRGB(0, 0, 0)
    can.setFont('TimesNewRoman', 13.5)
    can.drawString(113, 700, "Other Test")
    can.drawString(210, 700, other_test_name)

    can.drawString(210, 657, other_test_score)
    can.drawString(210, 629, other_test_date)
    can.drawString(210, 586, institution_name)
    can.drawString(210, 559, institution_location)
    can.drawString(210, 531, institution_from_date)
    can.drawString(210, 505, institution_to_date)
    can.drawString(210, 477, degree)
    can.drawString(210, 434, graduation_date)
    can.drawString(210, 390, recommender_name_1)
    can.drawString(210, 363, recommender_title_1)
    can.drawString(210, 336, recommender_institution_1)
    can.drawString(210, 308, recommender_email_1)
    can.drawString(210, 281, recommender_phone_1)
    can.drawString(210, 238, recommender_name_2)
    can.drawString(210, 210, recommender_title_2)
    can.drawString(210, 184, recommender_institution_2)   
    can.drawString(210, 157, recommender_email_2)
    can.drawString(210, 130, recommender_phone_2)
    can.drawString(210, 103, student_signature)
    can.drawString(210, 76, signature_date)
    can.save()
    packet.seek(0)
    page_2 = PdfReader(packet)


    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFillColorRGB(0, 0, 0)
    can.setFont('TimesNewRoman', 14)

    # Define the wrapping area
    x = 100
    y = 650
    max_width = 450
    max_height = 800

    wrap_text(can, location_of_experience, x, y, max_width, max_height, "Times-Roman", 12)

    can.save()
    packet.seek(0)
    page_3 = PdfReader(packet)

    # read your existing PDF
    pdf_path = os.path.abspath("myapp/box_api/MAPL_Application_Template.pdf")
    #pdf_path = os.path.abspath(r"C:\Users\kozak\Code\cls-opi-aws\myapp\box_api\MAPL_Application_Template.pdf")

    print(pdf_path)
    existing_pdf = PdfReader(open(pdf_path, "rb"))
    output = PdfWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.pages[0]
    page.merge_page(page_1.pages[0])
    output.add_page(page)

    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.pages[1]
    page.merge_page(page_2.pages[0])
    output.add_page(page)

    page = existing_pdf.pages[2]
    page.merge_page(page_3.pages[0])
    output.add_page(page)
    # finally, write "output" to a real file
    #outputStream = open(f"{full_name} Language Certificate.pdf", "wb+")
    outputStream = open(f"{firstname} MAPL Application.pdf", "wb+")
    output.write(outputStream)

    FileSystemStorage(location="/tmp").save(f"{firstname} {lastname} MAPL Application.pdf", outputStream)
    outputStream.close()


    if os.path.exists(f"{firstname} {lastname} MAPL Application.pdf"):
        os.remove(f"{firstname} {lastname} MAPL Application.pdf")
        pass
    else:
        print('failed to create student application pdf')

#create_mapl_application(firstname='Peter', middlename='Russell', lastname='Hart', email='kozakhart@gmail.com', byuid='123456789', phone='623-414-1835', major='Russian', heard_about='Friend', semester_of_entry='20235', academic_status='Senior', gpa='3.6', opi_score='Advanced High', opi_date='05/23/23', wpt_score='IH', wpt_date='05/23/23', alt_score='AL', alt_date='05/23/23', art_score='Superior', art_date='05/23/23', other_test_name='Important Test', other_test_score='Some other rating', other_test_date='05/23/23', institution_name='UVU', institution_location='Utah', institution_from_date='05/23/23', institution_to_date='05/23/23', degree='BA', graduation_date='05/23/23', recommender_name_1='John', recommender_title_1='Mr', recommender_institution_1='UVU', recommender_email_1='asdf@gmail.com', recommender_phone_1='123-123-1234', recommender_name_2='Samantha', recommender_title_2='Mrs', recommender_institution_2='UVU', recommender_email_2='asdf@gmail.com', recommender_phone_2='1231231234', student_signature='Peter Hart', signature_date='05/23/23', location_of_experience='This is my experience. There is more. I need to make this super long. This is my experience. There is more. I need to make this super long. This is my experience. There is more. I need to make this super long. This is my experience. There is more. I need to make this super long.')




def create_pdf_cert(record_id, full_name, language, level, opi_score, wpt_score, today):
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfbase import pdfmetrics

    pdfmetrics.registerFont(TTFont('TimesNewRoman', 'myapp/box_api/times_new_roman.ttf'))

    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFillColorRGB(0, 0, 0)

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
    # finally, write "output" to a real file
    #outputStream = open(f"{full_name} Language Certificate.pdf", "wb+")
    outputStream = open(f"{record_id} {full_name} {language.capitalize()} Language Certificate.pdf", "wb")
    output.write(outputStream)
    #FileSystemStorage(location="/tmp").save(f"{full_name} Language Certificate.pdf", outputStream)
    outputStream.close()

    box_client = create_client()
    box_folder_id = '190685933673'
    new_file = box_client.folder(box_folder_id).upload(f"{record_id} {full_name} {language.capitalize()} Language Certificate.pdf")

    
    if os.path.exists(f"{record_id} {full_name} {language.capitalize()} Language Certificate.pdf"):
        os.remove(f"{record_id} {full_name} {language.capitalize()} Language Certificate.pdf")
    else:
        print('failed to create student information pdf')

#create_pdf_cert('1000', 'Mariah Joshephine Nixonstien', 'HAITIAN-CREOLE', 'PROFESSIONAL', "Intermediate High", "Intermediate High", "07/04/2023")
