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
import csv
# test
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
        """Extends baseclass method.
        Must pass exactly one of either `rsa_private_key_file_sys_path` or
        `rsa_private_key_data`.
        If both `enterprise_id` and `user` are non-`None`, the `user` takes
        precedence when `refresh()` is called. This can be overruled with a
        call to `authenticate_instance()`.
        :param client_id:
            Box API key used for identifying the application the user is authenticating with.
        :param client_secret:
            Box API secret used for making OAuth2 requests.
        :param enterprise_id:
            The ID of the Box Developer Edition enterprise.
            May be `None`, if the caller knows that it will not be
            authenticating as an enterprise instance / service account.
            If `user` is passed, this value is not used, unless
            `authenticate_instance()` is called to clear the user and
            authenticate as the enterprise instance.
        :param jwt_key_id:
            Key ID for the JWT assertion.
        :param rsa_private_key_file_sys_path:
            (optional) Path to an RSA private key file, used for signing the JWT assertion.
        :param rsa_private_key_passphrase:
            Passphrase used to unlock the private key. Do not pass a unicode string - this must be bytes.
        :param user:
            (optional) The user to authenticate, expressed as a Box User ID or
            as a :class:`User` instance.
            This value is not required. But if it is provided, then the user
            will be auto-authenticated at the time of the first API call or
            when calling `authenticate_user()` without any arguments.
            Should be `None` if the intention is to authenticate as the
            enterprise instance / service account. If both `enterprise_id` and
            `user` are non-`None`, the `user` takes precedense when `refresh()`
            is called.
            May be one of this application's created App User. Depending on the
            configured User Access Level, may also be any other App User or
            Managed User in the enterprise.
            <https://developer.box.com/en/guides/applications/>
            <https://developer.box.com/en/guides/authentication/select/>
        :param store_tokens:
            Optional callback to get access to tokens and store them. Callback method should take two
             paramaters - access_token: str and refresh_token: str - and it is not expected to return anything.
        :param box_device_id:
            Optional unique ID of this device. Used for applications that want to support device-pinning.
        :param box_device_name:
            Optional human-readable name for this device.
        :param access_token:
            Access token to use for auth until it expires.
        :param session:
            If specified, use it to make network requests. If not, the default session will be used.
        :param jwt_algorithm:
            Which algorithm to use for signing the JWT assertion. Must be one of 'RS256', 'RS384', 'RS512'.
        :param rsa_private_key_data:
            (optional) Contents of RSA private key, used for signing the JWT assertion. Do not pass a
            unicode string. Can pass a byte string, or a file-like object that returns bytes, or an
            already-loaded `RSAPrivateKey` object.
        """
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
        """
        Construct the claims used for JWT auth and send a request to get a JWT.
        Pass an enterprise ID to get an enterprise token (which can be used to provision/deprovision users),
        or a user ID to get a user token.
        :param subject_id:
            The enterprise ID or user ID to auth.
        :param subject_type:
            Either 'enterprise' or 'user'
        :param now_time:
            Optional. The current UTC time is needed in order to construct the expiration time of the JWT claim.
            If None, `datetime.utcnow()` will be used.
        :return:
            The access token for the enterprise or app user.
        """
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