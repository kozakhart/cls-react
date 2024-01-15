from datetime import datetime, timedelta
import json
import random
import string
from io import IOBase
from typing import Optional, Union, Callable, TYPE_CHECKING, Any
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
import jwt #PyJWT
from boxsdk import Client
from django.core.files.storage import FileSystemStorage
import os
from dotenv import load_dotenv

load_dotenv()

BOX_USER_ID = os.getenv('BOX_USER_ID')
BOX_JWT = os.getenv('BOX_JWT')
BOX_CLIENT_SECRET = os.getenv('BOX_CLIENT_SECRET')
BOX_CLIENT_ID = os.getenv('BOX_CLIENT_ID')
BOX_ENTERPRISE_ID = os.getenv('BOX_ENTERPRISE_ID')
BOX_ACCESS_TOKEN = os.getenv('BOX_ACCESS_TOKEN')
BOX_RSA_PRIVATE_PASSPHRASE = os.getenv('BOX_RSA_PRIVATE_PASSPHRASE')
BOX_RSA_PRIVATE_KEY = os.getenv('BOX_RSA_PRIVATE_KEY')

from boxsdk.auth.server_auth import ServerAuth

if TYPE_CHECKING:
    from boxsdk.network.network_interface import Network
    from boxsdk.object.user import User


class JWTAuth(ServerAuth):
    """
    Responsible for handling JWT Auth for Box Developer Edition. Can authenticate enterprise instances or app users.
    """
    _GRANT_TYPE = 'urn:ietf:params:oauth:grant-type:jwt-bearer'
    test = 0
    def __init__(
            self,
            rsa_private_key_file_sys_path: Optional[str] = None,
            #rsa_private_key_passphrase: Optional[Union[str, bytes]] = None,
            store_tokens: Optional[Callable[[str, str], None]] = None,
            user: Optional[Union[str, 'User']] = BOX_USER_ID,
            jwt_key_id: str = BOX_JWT,
            client_secret: str = BOX_CLIENT_SECRET,
            client_id: str = BOX_CLIENT_ID,
            enterprise_id: Optional[str] = BOX_ENTERPRISE_ID,
            box_device_id: str = '0',
            box_device_name: str = '',
            access_token: str = BOX_ACCESS_TOKEN,
            session: Optional['Network'] = None,
            jwt_algorithm: str = 'RS256',
            rsa_private_key_passphrase: Optional[Union[str, bytes]] = BOX_RSA_PRIVATE_PASSPHRASE,
            rsa_private_key_data: Union[bytes, IOBase, RSAPrivateKey] = BOX_RSA_PRIVATE_KEY,
            **kwargs
    ):
        rsa_private_key = self._normalize_rsa_private_key(
            file_sys_path=rsa_private_key_file_sys_path,
            data=rsa_private_key_data,
            passphrase=rsa_private_key_passphrase,
        )
        del rsa_private_key_data
        del rsa_private_key_file_sys_path
        super().__init__(
            client_id=client_id,
            client_secret=client_secret,
            enterprise_id=enterprise_id,
            user=user,
            store_tokens=store_tokens,
            box_device_id=box_device_id,
            box_device_name=box_device_name,
            access_token=access_token,
            refresh_token=None,
            session=session,
            **kwargs
        )
        self._rsa_private_key = rsa_private_key
        self._jwt_algorithm = jwt_algorithm
        self._jwt_key_id = jwt_key_id

    def _fetch_access_token(self, subject_id: str, subject_type: str, now_time: Optional[datetime] = None) -> str:
        system_random = random.SystemRandom()
        jti_length = system_random.randint(16, 128)
        ascii_alphabet = string.ascii_letters + string.digits
        ascii_len = len(ascii_alphabet)
        jti = ''.join(ascii_alphabet[int(system_random.random() * ascii_len)] for _ in range(jti_length))
        if now_time is None:
            now_time = datetime.utcnow()
        now_plus_30 = now_time + timedelta(seconds=30)
        assertion = jwt.encode(
            {
                'iss': self._client_id,
                'sub': subject_id,
                'box_sub_type': subject_type,
                'aud': 'https://api.box.com/oauth2/token',
                'jti': jti,
                'exp': int((now_plus_30 - datetime(1970, 1, 1)).total_seconds()),
            },
            self._rsa_private_key,
            algorithm=self._jwt_algorithm,
            headers={
                'kid': self._jwt_key_id,
            },
        )
        data = {
            'grant_type': self._GRANT_TYPE,
            'client_id': self._client_id,
            'client_secret': self._client_secret,
            'assertion': assertion,
        }
        if self._box_device_id:
            data['box_device_id'] = self._box_device_id
        if self._box_device_name:
            data['box_device_name'] = self._box_device_name
        return self.send_token_request(data, access_token=None, expect_refresh_token=False)[0]

    @classmethod
    def _normalize_rsa_private_key(
            cls,
            file_sys_path: str,
            data: Union[bytes, IOBase, RSAPrivateKey],
            passphrase: Optional[Union[str, bytes]] = None
    ) -> Any:
        if len(list(filter(None, [file_sys_path, data]))) != 1:
            raise TypeError("must pass exactly one of either rsa_private_key_file_sys_path or rsa_private_key_data")
        if file_sys_path:
            with open(file_sys_path, 'rb') as key_file:
                data = key_file.read()
        if hasattr(data, 'read') and callable(data.read):
            data = data.read()
        if isinstance(data, str):
            try:
                data = data.encode('ascii')
            except UnicodeError as unicode_error:
                raise TypeError(
                    "rsa_private_key_data must contain binary data (bytes/str), not a text/unicode string"
                ) from unicode_error

        if isinstance(data, bytes):
            passphrase = cls._normalize_rsa_private_key_passphrase(passphrase)
            return serialization.load_pem_private_key(
                data,
                password=passphrase,
                backend=default_backend(),
            )
        if isinstance(data, RSAPrivateKey):
            return data
        raise TypeError(
            'rsa_private_key_data must be binary data (bytes/str), '
            'a file-like object with a read() method, '
            'or an instance of RSAPrivateKey, '
            f'but got {data.__class__.__name__!r}'
        )
    @staticmethod
    def _normalize_rsa_private_key_passphrase(passphrase: Any):
        if isinstance(passphrase, str):
            try:
                return passphrase.encode('ascii')
            except UnicodeError as unicode_error:
                raise TypeError(
                    "rsa_private_key_passphrase must contain binary data (bytes/str), not a text/unicode string"
                ) from unicode_error

        if not isinstance(passphrase, (bytes, type(None))):
            raise TypeError(
                f"rsa_private_key_passphrase must contain binary data (bytes/str), "
                f"got {passphrase.__class__.__name__!r}"
            )
        return passphrase

    @classmethod
    def from_settings_dictionary(cls, settings_dictionary: dict, **kwargs: Any) -> 'JWTAuth':
        """
        Create an auth instance as defined by the given settings dictionary.
        The dictionary should have the structure of the JSON file downloaded from the Box Developer Console.
        :param settings_dictionary:       Dictionary containing settings for configuring app auth.
        :return:                        Auth instance configured as specified by the config dictionary.
        """
        if 'boxAppSettings' not in settings_dictionary:
            raise ValueError('boxAppSettings not present in configuration')
        return cls(
            client_id=settings_dictionary['boxAppSettings']['clientID'],
            client_secret=settings_dictionary['boxAppSettings']['clientSecret'],
            enterprise_id=settings_dictionary.get('enterpriseID', None),
            jwt_key_id=settings_dictionary['boxAppSettings']['appAuth'].get('publicKeyID', None),
            rsa_private_key_data=settings_dictionary['boxAppSettings']['appAuth'].get('privateKey', None),
            rsa_private_key_passphrase=settings_dictionary['boxAppSettings']['appAuth'].get('passphrase', None),
            **kwargs
        )
    @classmethod
    def from_settings_file(cls, settings_file_sys_path: str, **kwargs: Any) -> 'JWTAuth':
        """
        Create an auth instance as defined by a JSON file downloaded from the Box Developer Console.
        See https://developer.box.com/en/guides/authentication/jwt/ for more information.
        :param settings_file_sys_path:    Path to the JSON file containing the configuration.
        :return:                        Auth instance configured as specified by the JSON file.
        """
        with open(settings_file_sys_path, encoding='utf-8') as config_file:
            config_dictionary = json.load(config_file)
            return cls.from_settings_dictionary(config_dictionary, **kwargs)



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

def create_client():
    config = JWTAuth()
    token = config._fetch_access_token(BOX_USER_ID, 'user')
    client = Client(config)
    print('client created')
    return client

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

#create_mapl_application(firstname='Peter', middlename='Russell', lastname='Hart', email='kozakhart@gmail.com', byuid='123456789', phone='623-414-1>




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