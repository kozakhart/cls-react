from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout, login, authenticate
from django.middleware.csrf import get_token
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from io import BytesIO
import io
import csv
import mysql.connector
# Create your views here.
from rest_framework import status, permissions, views
import os
from rest_framework import generics
import zipfile
import base64
from io import StringIO

from .models import Students, LASER_Queries, OPIc_Diagnostic_Grid_Languages
from .serializers import StudentSerializer, LASER_QueriesSerializer, ProgramSerializer, OPIcLanguageSerializer
from .serializers import UserSerializer
import api.filemaker_api as filemaker
import json
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.decorators import api_view, authentication_classes, permission_classes
import api.lti_api as lti
from datetime import datetime
import api.outlook_api as outlook
import api.box_api as box_api
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from axes.decorators import axes_dispatch
from axes.signals import user_login_failed
from axes.utils import reset

from datetime import datetime
import api.byu_api.byu_api as byu_api
from myapp.models import Languages, Reasons
import subprocess
from django.core.files import File
from dotenv import load_dotenv
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
load_dotenv()

MARIADB_HOST = os.getenv('MARIADB_HOST')
MARIADB_USER = os.getenv('MARIADB_USER')
MARIADB_PASSWORD = os.getenv('MARIADB_PASSWORD')
MARIADB_DATABASE = os.getenv('MARIADB_DATABASE')

def verify_user(request):
    username = request.user.username
    user = User.objects.filter(username=username).first()
    if user is not None and user.is_staff:
        return Response({'message': 'User is authenticated'}, status=200)
    else:
        return Response({'message': 'User is not authenticated'}, status=401)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def apiOverview(request):
    api_urls = {
        'Students': '/student-list/',
        'Filemaker': '/filemaker/',
        'LTI': '/lti/',
        'Example LTI': '/example-lti/',
        'Update Student': '/update/<str:student>/',
        'Delete Student': '/delete/<str:student>/',
        'Login': '/api/login/',
        'Generate CSRF Token': '/api/generate-csrf/',
        'Get Token': 'api/get-token/',
        'Check Authentication': 'api/check-authentication/',
        'Logout': 'api/logout/',
        'Need Approval Filemaker': 'api/need-approval-filemaker/',
        }
    return Response(api_urls)

@permission_classes([IsAuthenticated])
@api_view(['GET'])
def student_list(request):
    if request.user.is_staff or request.user.is_superuser:
        student_list = Students.objects.all()
        serializer = StudentSerializer(student_list, many=True)
        return Response(serializer.data)
    else:
        return Response({'message': 'User is not authenticated'}, status=401)

@permission_classes([IsAuthenticated])
@api_view(['POST'])
def student_update(request, student):
    if request.user.is_superuser:
        print('Student Record ID:', student)
        print(request.data)
    
        token = filemaker.login()
        if student == '0':
            # creates new record
            filemaker.create_record(scores=request.data['Scores'], testscheduled=request.data['TestScheduled'], approved=request.data['Approved'], entry_date=request.data['EntryDate'], entry_time=request.data['EntryTime'],
            firstname=request.data['FirstName'], lastname=request.data['LastName'], byuid=request.data['BYUID'], netid=request.data['NetID'], email=request.data['Email'],
            reason=request.data['Reason'], language=request.data['Language'], language_other=request.data['LanguageOther'],
            experience=request.data['PreviousExperience'],major=request.data['Major'],second_major=request.data['SecondMajor'],minor=request.data['Minor'],
            come_to_campus=request.data['ComeToCampus'],cannot_come=request.data['CannotCome'],testdate1=request.data['TestDate1'],testdate2=request.data['TestDate2'],time1=request.data['Time1'],time2=request.data['Time2']
            ,time3=request.data['Time3'],time4=request.data['Time4'], CertificateStatus=request.data['CertificateStatus'],phone=request.data['Phone'],email_sent=request.data['EmailSent'], lti_schedule=request.data['LTISchedule'],
            token=token
            )
        else:
            filemaker.edit_all_fields(scores=request.data['Scores'], testscheduled=request.data['TestScheduled'], agree=request.data['Approved'], entrydate=request.data['EntryDate'], entrytime=request.data['EntryTime'],
            firstname=request.data['FirstName'], lastname=request.data['LastName'], byuid=request.data['BYUID'], netid=request.data['NetID'], email=request.data['Email'], 
            reason=request.data['Reason'], language=request.data['Language'], languageother=request.data['LanguageOther'],
            previousexperience=request.data['PreviousExperience'],major=request.data['Major'],secondmajor=request.data['SecondMajor'],minor=request.data['Minor'],
            cometocampus=request.data['ComeToCampus'],cannotcome=request.data['CannotCome'],testdate1=request.data['TestDate1'],testdate2=request.data['TestDate2'],time1=request.data['Time1'],time2=request.data['Time2']
            ,time3=request.data['Time3'],time4=request.data['Time4'], CertificateStatus=request.data['CertificateStatus'],phone=request.data['Phone'],emailsent=request.data['EmailSent'], lti_schedule=request.data['LTISchedule'], 
            token=token, record_id=request.data['RecordID']
            )
        filemaker.logout(token)
        return Response(f'Student Record ID updated: {student}')
    else:
        return Response({'message': 'User is not authenticated'}, status=401)


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def student_delete(request, student):
    status= verify_user(request).status_code
    if status == 200:
        print('Student Record ID:', student)
        token = filemaker.login()
        filemaker.delete_record(record_id=student, token=token)
        filemaker.logout(token)
        return Response(f'Student Record ID deleted: {student}')

    else:
        return Response({'message': 'User is not authenticated'}, status=401)
        
@api_view(['GET'])
@ensure_csrf_cookie
def get_csrf_token(request):
    # Function to get CSRF token (replace this with your implementation)
    csrf_token = get_token(request)
    
    response = JsonResponse({"message": "Set CSRF cookie"})
    
    # Set the CSRF token as an HTTP-only cookie for same-origin requests
    response.set_cookie(key='csrftoken', value=csrf_token, httponly=True)
    
    return response

@permission_classes([IsAuthenticated])
@api_view(['GET'])
def filemaker_view(request):
    if request.user.is_staff or request.user.is_superuser:
        print('Filemaker API Used')
        token = filemaker.login()
        students = filemaker.get_all(token)
        filemaker.logout(token)
        print(request)
        return JsonResponse(students, safe=False)
    return JsonResponse({'message': 'User is not authenticated'}, status=401)

@permission_classes([IsAuthenticated])
@api_view(['GET'])
def example_lti_view(request):
    if request.user.is_staff or request.user.is_superuser:
        browser = lti.get_browser()
        score_type = 'OPI'
        from_date = '10/01/2023'
        to_date = '10/30/2023'
        selected_data = ['firstname', 'lastname', 'byuid', 'language', 'score', 'test_type', 'test_date']
        byuid = None
        language = None
        print(selected_data)
        kwargs = {data: None for data in selected_data}

        data = lti.get_data(browser, fromdate=from_date, todate=to_date, 
            byuid=byuid, language=language,
            test_type=score_type, kwargs=kwargs)

        lti.close_browser(browser)
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'message': 'User is not authenticated'}, status=401)

@permission_classes([IsAuthenticated])
@api_view(['POST'])
def get_certificate_data(request):
    if request.user.is_staff or request.user.is_superuser:
        data = request.data

        byuid = data.get('byuidValue')
        language = data.get('languageValue')
        print(byuid, language)
        if byuid == "None":
            byuid = ''
        if language == "None":
            language = ''
        print(byuid, language)
        record_date_str = data.get('recordDate')
        record_date = datetime.strptime(record_date_str, '%m/%d/%Y')
        formatted_record_date = record_date.strftime('%m/%d/%Y')

        semester_date_str = data.get('semesterDate')
        semester_date = datetime.strptime(semester_date_str, '%m/%d/%Y')
        formatted_semester_date = semester_date.strftime('%m/%d/%Y')

        today = datetime.now()
        today = today.strftime("%m/%d/%Y")
        browser = lti.get_browser()
        try:
            lti.get_data(browser, formatted_record_date, todate=today, test_type='OPI', byuid=byuid, language=language, kwargs={'firstname':None, 'score': None, 'major': None})
            lti.get_data(browser, formatted_record_date, todate=today, test_type='WPT', byuid=byuid, language=language, kwargs={'firstname':None, 'score': None, 'major': None})
            lti.get_data(browser, formatted_record_date, todate=today, test_type='OPIc', byuid=byuid, language=language, kwargs={'firstname':None, 'score': None, 'major': None})
        except Exception as e:
            print(e)
        #lti.get_all_data(browser, formatted_record_date, formatted_semester_date, byuid=byuid, language=language, kwargs={'firstname':None, 'score': None, 'major': None})
        lti.close_browser(browser)
        data = lti.start_search(formatted_record_date, formatted_semester_date)

        score_df = {"NL": "Novice Low", "NM": "Novice Mid", "NH": "Novice High", 
                "IL": "Intermediate Low", "IM": "Intermediate Mid", "IH": "Intermediate High", 
                "AL": "Advanced Low", "AM": "Advanced Mid", "AH": "Advanced High", 
                "S": "Superior", "D": "Distinguished"}
        
        level_df = {"Advanced": "(Intermediate High, Advanced Low, Advanced Mid) 1", "Mastery": "(Advanced High) 2", "Professional": "(Superior) 3"}
        level_values = list(level_df.values())

        for student_df in data:
            try:
                if student_df['opiScore'] in score_df:
                    student_df['opiScore'] = {student_df['opiScore']: score_df[student_df['opiScore']]}
                if student_df['wptScore'] in score_df:
                    student_df['wptScore'] = {student_df['wptScore']: score_df[student_df['wptScore']]}
                if student_df['opicScore'] in score_df:
                    student_df['opicScore'] = {student_df['opicScore']: score_df[student_df['opicScore']]}
            
                opi_score_values = list(student_df['opiScore'].values())
                wpt_score_values = list(student_df['wptScore'].values())
                #print(opi_score_values, wpt_score_values)

                if (opi_score_values[0] in level_values[2]) or (wpt_score_values[0] in level_values[2]):
                    level = "Professional"
                elif (opi_score_values[0] in level_values[1]) or (wpt_score_values[0] in level_values[1]):
                    level = "Mastery"
                elif (opi_score_values[0] in level_values[0]) or (wpt_score_values[0] in level_values[0]):
                    level = "Advanced"
                    if opi_score_values[0] == "Intermediate High":
                        level = 'Undetermined'
                else:
                    level = "Undetermined"
                student_df['level'] = level
            except Exception as e:
                print(e)

        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'message': 'User is not authenticated'}, status=401)


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def award_certificate(request):
    if request.user.is_superuser:
        if request.data['type'] == 'award_all':
            box_client = box_api.create_client()
            filemaker_token = filemaker.login()
            byu_token = byu_api.login()
            token = outlook.get_token()

            current_date = datetime.now()       
            month = datetime.now().strftime("%B")
            month_num =current_date.month
            year = datetime.now().strftime("%Y")  

            if month_num >= 1 and month_num <= 4:
                yearterm = '1'
            elif month_num >= 5 and month_num <= 6:
                yearterm = '3'
            elif month_num >= 7 and month_num <= 8:
                yearterm = '4'
            elif month_num >= 9 and month_num <= 12:
                yearterm = '5'
            else:
                yearterm = '0'
            yearterm = year + yearterm       
            
            filtered_students = [student for student in request.data['students'] if student['recordId'] in request.data['recordids']]

            for student in filtered_students:
                full_name = student['firstname'] + ' ' + student['lastname']
                byuid = student['byuid']
                netid = student['netid']
                language = student['language'].values()
                language = list(language)[0]
                level = student['level']
                opi_score = student['opiScore'].values()
                opi_score = list(opi_score)[0]
                wpt_score = student['wptScore'].values()
                wpt_score = list(wpt_score)[0]
                record_id = student['recordId']
                formatted_date = current_date.strftime("%m/%d/%Y")
                cert_type = "False"

                file_id = box_api.create_pdf_cert(box_client, record_id, full_name, language.upper(), level.upper(), opi_score, wpt_score, formatted_date, cert_type)
                shareable_link = box_api.generate_shareable_link(box_client, file_id)
                data = {
                "subject": f'Language Certificate for {full_name}',
                "importance":"High",
                "body":{
                    "contentType":"HTML",
                    "content":"""
                    <BODY><p style="color:black;font-weight:normal;">{full_name},<br><br>
                    
                    Congratulations on earning your language certificate! Please see the attached certificate.<br><br>

                    <a href="{shareable_link}">{shareable_link}</a><br><br>
                    
                    Best,<br><br>

                    Center for Language Studies<br> 
                    cls.byu.edu<br> 
                    </p></BODY></HTML>
                    """.format(
                    full_name=full_name,
                    shareable_link=shareable_link,
                    )
                    },
                            
                "toRecipients":[
                    {
                        "emailAddress":{
                            "address": netid + "@byu.edu"
                        }
                    }
                ]
            }
                # "address": netid + "@byu.edu"

                
                message = outlook.create_message(token, data)
                outlook.send_message(token, message)

                data = {
                    "subject": f'Language Certificate for {full_name}',
                    "importance":"High",
                    "body":{
                        "contentType":"HTML",
                        "content":"""
                        <BODY><p style="color:black;font-weight:normal;">BYU Enrollment Services,<br><br>
                        
                        {full_name} has earned their BYU Language Certificate and requires a notation on their transcript. Thank you for your assistance.<br><br>

                        Name: {full_name}<br>
                        BYUID: {byuid}<br>
                        Language: {language}<br>
                        Level: {level}<br>
                        Month: {month}<br>
                        Year: {year}<br>
                        Yearterm: {yearterm}<br><br>
                        
                        Best,<br><br>

                        Mariah Nix<br>
                        Language Assessment Coordinator<br>
                        Center for Language Studies<br> 
                        cls.byu.edu<br> 
                        </p></BODY></HTML>
                        """.format(
                                full_name=full_name,
                                language=language,
                                level=level,
                                byuid=byuid,
                                month=month,
                                year=year,
                                yearterm=yearterm,
                            )
                                },
                    "toRecipients":[
                        {
                            "emailAddress":{
                                "address": "graduation@byu.edu"
                            }
                        }
                    ]
                }
                #"address": "graduation@byu.edu"

                message = outlook.create_message(token, data)
                outlook.send_message(token, message)
                programs = byu_api.get_programs(byu_token, byuid)
                major_count = 1
                minor_count = 1
                major1 = ','
                major2 = ','
                major3 = ','
                minor1 = ','
                minor2 = ','
                minor3 = ','

                for program in programs:
                    if 'MAJOR' in program:
                        if major_count == 1:
                            major1 = program['MAJOR']
                        elif major_count == 2:
                            major2 = program['MAJOR']
                        elif major_count == 3:
                            major3 = program['MAJOR']
                        major_count += 1
                    elif 'MINOR' in program:
                        if minor_count == 1:
                            minor1 = program['MINOR']
                        elif minor_count == 2:
                            minor2 = program['MINOR']
                        elif minor_count == 3:
                            minor3 = program['MINOR']
                        minor_count += 1

                course1 = ','
                course2 = ','
                course3 = ','
                other_courses = ''
                find_lang_abbreviation = Languages.objects.filter(full_language=language).first()
                lang_abbreviation = find_lang_abbreviation.abbreviation
                courses = byu_api.get_classes(byu_token, byuid, lang_abbreviation, 'Language Certificate', valid=True)
                course_count = 1
                print('courses', courses)
                for index, course in enumerate(courses):
                    if course_count == 1:
                        course1 = course
                    elif course_count == 2:
                        course2 = course
                    elif course_count == 3:
                        course3 = course
                    else:
                        other_courses += " " + course

                    course_count += 1
                print(course1, course2, course3, other_courses)
                box_api.append_to_fulton_report(box_client, {"Last Name":full_name.split(' ')[1], "First Name":full_name.split(' ')[0], "RouteY ID":"", 
                "BYUID":byuid, "Major 1":major1, "Major 2":major2 ,"Major 3":major3,"Minor 1":minor1,"Minor 2":minor2,"Minor 3":minor3,"Language":language, 
                "OPI Rating":opi_score, "WPT Rating":wpt_score, "Semester Finished":yearterm, "Course 1":course1, "Course 2":course2, "Course 3":course3, "Other Courses":other_courses})
                filemaker.edit_record('CertificateStatus', 'Awarded', filemaker_token, record_id)
            filemaker.logout(filemaker_token)
            byu_api.logout(byu_token)
            return JsonResponse({'message': 'All certificates awarded'})
        else: 
            full_name = request.data['dataToSend']['FullName']
            byuid = request.data['dataToSend']['BYUID']
            netid = request.data['dataToSend']['NetID']
            language = request.data['dataToSend']['Language']
            level = request.data['dataToSend']['Level']
            opi_score = request.data['dataToSend']['OPIScore']
            wpt_score = request.data['dataToSend']['WPTScore']
            formatted_date = request.data['dataToSend']['TodaysDate']
            cert_type = str(request.data['dataToSend']['CertificateType'])
            if cert_type == 'True':
                wpt_score = 'N/A'
                
            record_id = request.data['dataToSend']['RecordID']

            box_client = box_api.create_client()
            file_id = box_api.create_pdf_cert(box_client, record_id, full_name, language.upper(), level.upper(), opi_score, wpt_score, formatted_date, cert_type)
            shareable_link = box_api.generate_shareable_link(box_client, file_id)

            data = {
                "subject": f'Language Certificate for {full_name}',
                "importance":"High",
                "body":{
                    "contentType":"HTML",
                    "content":"""
                    <BODY><p style="color:black;font-weight:normal;">{full_name},<br><br>
                    
                    Congratulations on earning your language certificate! Please see the attached certificate.<br><br>

                    <a href="{shareable_link}">{shareable_link}</a><br><br>
                    
                    Best,<br><br>

                    Center for Language Studies<br> 
                    cls.byu.edu<br> 
                    </p></BODY></HTML>
                    """.format(
                    full_name=full_name,
                    shareable_link=shareable_link,
                    )
                    },
                            
                "toRecipients":[
                    {
                        "emailAddress":{
                            "address": netid + "@byu.edu"
                        }
                    }
                ]
            }
            # "address": netid + "@byu.edu"
            token = outlook.get_token()
            message = outlook.create_message(token, data)
            outlook.send_message(token, message)

            date_obj = datetime.strptime(formatted_date, "%m/%d/%Y")

            month = date_obj.strftime("%B")
            year = date_obj.strftime("%Y")
            month_num = date_obj.month

            if month_num >= 1 and month_num <= 4:
                yearterm = '1'
            elif month_num >= 5 and month_num <= 6:
                yearterm = '3'
            elif month_num >= 7 and month_num <= 8:
                yearterm = '4'
            elif month_num >= 9 and month_num <= 12:
                yearterm = '5'
            else:
                yearterm = '0'
            yearterm = year + yearterm

            data = {
                "subject": f'Language Certificate for {full_name}',
                "importance":"High",
                "body":{
                    "contentType":"HTML",
                    "content":"""
                    <BODY><p style="color:black;font-weight:normal;">BYU Enrollment Services,<br><br>
                    
                    {full_name} has earned their BYU Language Certificate and requires a notation on their transcript. Thank you for your assistance.<br><br>

                    Name: {full_name}<br>
                    BYUID: {byuid}<br>
                    Language: {language}<br>
                    Level: {level}<br>
                    Month: {month}<br>
                    Year: {year}<br>
                    Yearterm: {yearterm}<br><br>
                    
                    Best,<br><br>

                    Mariah Nix<br>
                    Language Assessment Coordinator<br>
                    Center for Language Studies<br> 
                    cls.byu.edu<br> 
                    </p></BODY></HTML>
                    """.format(
                            full_name=full_name,
                            language=language,
                            level=level,
                            byuid=byuid,
                            month=month,
                            year=year,
                            yearterm=yearterm,
                        )
                            },
                "toRecipients":[
                    {
                        "emailAddress":{
                            "address": "graduation@byu.edu"
                        }
                    }
                ]
            }
            #"address": "graduation@byu.edu"

            message = outlook.create_message(token, data)
            outlook.send_message(token, message)
            byu_token = byu_api.login()
            programs = byu_api.get_programs(byu_token, byuid)
            major_count = 1
            minor_count = 1
            major1 = ','
            major2 = ','
            major3 = ','
            minor1 = ','
            minor2 = ','
            minor3 = ','

            for program in programs:
                if 'MAJOR' in program:
                    if major_count == 1:
                        major1 = program['MAJOR']
                    elif major_count == 2:
                        major2 = program['MAJOR']
                    elif major_count == 3:
                        major3 = program['MAJOR']
                    major_count += 1
                elif 'MINOR' in program:
                    if minor_count == 1:
                        minor1 = program['MINOR']
                    elif minor_count == 2:
                        minor2 = program['MINOR']
                    elif minor_count == 3:
                        minor3 = program['MINOR']
                    minor_count += 1

            course1 = ','
            course2 = ','
            course3 = ','
            other_courses = ''
            find_lang_abbreviation = Languages.objects.filter(full_language=language).first()
            lang_abbreviation = find_lang_abbreviation.abbreviation
            courses = byu_api.get_classes(byu_token, byuid, lang_abbreviation, 'Language Certificate', valid=True)
            byu_api.logout(byu_token)
            course_count = 1
            for index, course in enumerate(courses):
                if course_count == 1:
                    course1 = course
                elif course_count == 2:
                    course2 = course
                elif course_count == 3:
                    course3 = course
                else:
                    other_courses += " " + course

                course_count += 1

            box_api.append_to_fulton_report(box_client, {"Last Name":full_name.split(' ')[1], "First Name":full_name.split(' ')[0], "RouteY ID":"", 
            "BYUID":byuid, "Major 1":major1, "Major 2":major2 ,"Major 3":major3,"Minor 1":minor1,"Minor 2":minor2,"Minor 3":minor3,"Language":language, 
            "OPI Rating":opi_score, "WPT Rating":wpt_score, "Semester Finished":yearterm, "Course 1":course1, "Course 2":course2, "Course 3":course3, "Other Courses":other_courses})
            filemaker_token = filemaker.login()
            filemaker.edit_record('CertificateStatus', 'Awarded', filemaker_token, record_id)
            filemaker.logout(filemaker_token)
            return JsonResponse({'message': 'Certificate awarded'})
    else:
        return JsonResponse({'message': 'User is not authenticated'}, status=401)


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def lti_view(request):
    if request.user.is_staff or request.user.is_superuser:
        # token = request.COOKIES['token']
        # token, username = token.split(':')
        # user = User.objects.filter(username=username).first()
        # if user is not None and user.is_staff:
        browser = lti.get_browser()
        score_type = request.data.get('scoreType')
        from_date = request.data.get('fromDate')
        to_date = request.data.get('toDate')
        selected_data = request.data.get('selectedData')
        byuid = None
        language = None
        print(selected_data)
        kwargs = {data: None for data in selected_data}

        data = lti.get_data(browser, fromdate=from_date, todate=to_date, byuid=byuid, language=language, test_type=score_type, kwargs=kwargs)
        # print(data)

        lti.close_browser(browser)
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'message': 'User is not authenticated'}, status=401)

@permission_classes([IsAuthenticated])
@api_view(['GET'])
def need_approval_filemaker(request):
    username = request.user.username
    user = User.objects.filter(username=username).first()
    if user is not None and user.is_staff:
        print('Filemaker API Used')
        token = filemaker.login()
        students = filemaker.adaptive_find_record(token, Approved='No')
        filemaker.logout(token)
        return JsonResponse(students, safe=False)
    else:
        return JsonResponse({'message': 'User is not authenticated'}, status=401)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    username = request.user.username
    user = User.objects.filter(username=username).first()

    if user is None:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    user_groups = user.groups.all()
    group_names = [group.name for group in user_groups]

    return Response({
        'user': UserSerializer(user, context={'request': request}).data,
        'groups': group_names
    })



    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_student_grades(request):
    byu_id = request.GET.get('byuid')
    language = request.GET.get('language')
    reason = request.GET.get('reason')
    print(byu_id, language, reason)

    if request.user.is_staff or request.user.is_superuser:
        username = request.user.username
        user = User.objects.filter(username=username).first()
        if user is not None and user.is_staff:
            token = byu_api.login()
            grades = byu_api.get_classes(token, byu_id, language, reason, valid=True)
            byu_api.logout(token)
            #grades = 'A'
            return JsonResponse(grades, safe=False)
        else:
            return JsonResponse({'message': 'User is not authenticated'}, status=401)
    else:
        return JsonResponse({'message': 'User is not authenticated'}, status=401)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def edit_records(request):
    username = request.user.username
    recordids = request.data.get('recordids')

    user = User.objects.filter(username=username).first()
    if user is not None and user.is_staff:
        token = filemaker.login()
        for record in recordids:
            filemaker.edit_record('Approved', 'Waiting', token, record)
        filemaker.logout(token)
        return JsonResponse({'message': 'Record updated'}, status=200)
    else:
        return JsonResponse({'message': 'User is not authenticated'}, status=401)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def qualtrics_reports(request):
    if request.method == 'POST' and request.FILES.getlist('files'):
        if request.user.is_staff or request.user.is_superuser:
            try:
                args = []
                report_type = ''
                qualtrics_token = request.data.get('qualtricsToken')
                args.append(qualtrics_token)

                files = request.FILES.getlist('files')
                for file in files:
                    if 'OPIc' in file.name:
                        args.append(file.read())
                        report_type = 'opic_report.pdf'
                        files.remove(file)
                    elif 'OPI' in file.name:
                        args.append(file.read())
                        report_type = 'opi_report.pdf'
                        files.remove(file)
                    elif 'WPT' in file.name:
                        args.append(file.read())
                        report_type = 'wpt_report.pdf'
                        files.remove(file)
                for file in files:
                    args.append(file.read())
                
                print(args)
                folder_path = '/home/clsdeveloper/laser-ltiscores-autoreports'
                file_name = "Reports.R"
                file_path = os.path.join(folder_path, file_name)

                # Activate renv environment
                activate_command = f'Rscript -e "renv::activate(\'{folder_path}\')"'
                result_activate = subprocess.run(activate_command, shell=True, capture_output=True, text=True)

                # Check if activation was successful
                if result_activate.returncode == 0:
                    print("renv is activated.")
                    # install_tinytex_command = 'Rscript -e "if (!requireNamespace(\'tinytex\', quietly = TRUE)) install.packages(\'tinytex\')"'
                    # result_install_tinytex = subprocess.run(install_tinytex_command, shell=True, capture_output=True, text=True)

                    
                    # snapshot_command = 'Rscript -e "renv::snapshot()"'
                    # result_snapshot = subprocess.run(snapshot_command, shell=True, capture_output=True, text=True)
                    # # Generate lockfile
                    # # Now, restore the packages and execute the R script with arguments
                    # install_command = 'Rscript -e "renv::restore()"'
                    # result_install = subprocess.run(install_command, shell=True, capture_output=True, text=True)

                    # if result_install.returncode == 0:
                    if result_activate.returncode == 0:
                        print("Packages installed successfully.")

                            # Now, execute the R script with arguments
                        execute_command = ['Rscript', file_path] + args
                        result_execute = subprocess.run(execute_command, capture_output=True, text=True)

                            # Check if execution was successful
                        if result_execute.returncode == 0:
                                # Print the standard output
                            print(f"Output of {file_path}:\n{result_execute.stdout}")
                        else:
                                # Print the error message if execution fails
                            print(f"Error executing {file_path}:\n{result_execute.stderr}")
                    else:
                        print("Error installing packages:")
                        #print(result_install.stderr)
                        print(result_activate.stderr)
                else:
                    print("Error activating renv:")
                    print(result_activate.stderr)

                file_path = os.path.join(folder_path, report_type)

                with open(file_path, 'rb') as file:
                    django_file = File(file)
                    file_content = django_file.read()

                zip_buffer = BytesIO()
    
    # List all files in the directory with .csv extension
                csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

                with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                    zip_file.writestr(os.path.basename(file_path), file_content)
                    for csv_file in csv_files:
                        csv_file_path = os.path.join(folder_path, csv_file)
                        with open(csv_file_path, 'rb') as file:
                            file_content = file.read()
                        zip_file.writestr(os.path.basename(csv_file_path), file_content)
                        os.remove(csv_file_path)
                        
                zip_buffer.seek(0)

                response = HttpResponse(zip_buffer.read(), content_type='application/zip')
                response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}.zip"'

                return response
            except Exception as e:
                print(e)
                return Response({'message': 'Error generating report'}, status=400)

        else:
            return JsonResponse({'message': 'User is not authenticated'}, status=401)
    else:
        return JsonResponse({'error': 'Invalid request'})
    
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def laser_data(request):
    if request.method == 'POST':
        if request.user.is_staff or request.user.is_superuser:
            recordids = request.data.get('recordids')
            username = request.user.username
            user = User.objects.filter(username=username).first()
            if user is not None and user.is_staff:
                data = request.data
                sql_query = data['sqlQuery'].replace('\n', ' ')
                connection = mysql.connector.connect(
                    host=MARIADB_HOST,
                    user=MARIADB_USER,
                    password=MARIADB_PASSWORD,
                    database=MARIADB_DATABASE
                )
                
                cursor = connection.cursor()
                cursor.execute(sql_query)
                
                # Fetch all rows
                rows = cursor.fetchall()
                
                # Create a CSV string
                csv_output = io.StringIO()
                csv_writer = csv.writer(csv_output)
                csv_writer.writerow([i[0] for i in cursor.description])  # Write headers
                csv_writer.writerows(rows)  # Write rows
                
                # Close database connection
                cursor.close()
                connection.close()
                # sample_data = [
                #     [sql_query, 'Age', 'City'],
                #     ['John', 25, 'New York'],
                #     ['Alice', 30, 'Los Angeles'],
                #     ['Bob', 28, 'Chicago']
                # ]

                # # Create a CSV string
                # csv_output = io.StringIO()
                # csv_writer = csv.writer(csv_output)
                # csv_writer.writerows(sample_data)

                # Return CSV response
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="result.csv"'
                response.write(csv_output.getvalue())
                return response
            else:
                return JsonResponse({'message': 'User is not authenticated'}, status=401)
        else:
            return JsonResponse({'message': 'User is not authenticated'}, status=401)
    else:
        return JsonResponse({'error': 'Invalid request'})

@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_db_schema(request):
# Construct the relative path using BASE_DIR
    if request.user.is_staff or request.user.is_superuser:
        csv_file_path = settings.BASE_DIR / 'api' / 'schemas' / 'db_key.csv'

        with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
            # Read the file content
            file_content = csv_file.read()
            
            # Create an HttpResponse object with the CSV content
            response = HttpResponse(file_content, content_type='text/csv')
            # Add the Content-Disposition header to prompt a download in the browser
            response['Content-Disposition'] = 'attachment; filename="db_schema.csv"'
            
            return response
    else:
        return JsonResponse({'message': 'User is not authenticated'}, status=401)
    
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_grid_schema(request):
    if request.user.is_staff or request.user.is_superuser:
        pdf_file_path = settings.BASE_DIR / 'api' / 'schemas' / 'grid_schema.pdf'


        
        with open(pdf_file_path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="grid_schema.pdf"'
            return response

    else:
        return JsonResponse({'message': 'User is not authenticated'}, status=401)
    
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_grid_example_search_csv(request):
    if request.user.is_staff or request.user.is_superuser:
        csv_file_path = settings.BASE_DIR / 'api' / 'schemas' / 'example_search.csv'
        
        with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
            file_content = csv_file.read()
            response = HttpResponse(file_content, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="example_search.csv"'
            return response
    else:
        return JsonResponse({'message': 'User is not authorized'}, status=401)
    
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login
@ensure_csrf_cookie
@permission_classes([AllowAny])
@api_view(['POST'])
def login_view(request):
    # add axes login/logout counter and reset
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(request, username=username, password=password)

    if user is None:
        user_login_failed.send(sender=__name__, credentials={'username': username}, request=request)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

    login(request, user)
    return Response({"user": UserSerializer(user, context={'request': request}).data})

# logout
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response({"message": "User logged out"})

@permission_classes([IsAuthenticated])
@api_view(['GET'])
def verify_session(request):
    username = request.user.username
    user = User.objects.filter(username=username).first()
    if user is not None and user.is_staff:
        return Response({"message": "User is authenticated"})

    else:
        return Response({"message": "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
    


#LASER Queries
#@permission_classes([IsAuthenticated])
@api_view(['GET', 'POST'])
def get_post_laser_queries(request):
    if request.user.is_staff or request.user.is_superuser:
        if request.method == "GET":
            queries = LASER_Queries.objects.all()
            query_serializer = LASER_QueriesSerializer(queries, many=True)
            return JsonResponse(query_serializer.data, safe=False)
        if request.method == "POST":
            data = request.data
            query_serializer = LASER_QueriesSerializer(data=data)
            if query_serializer.is_valid():
                query_serializer.save()
                return JsonResponse(query_serializer.data, status=201)
            return JsonResponse(query_serializer.errors, status=400)
        
        return JsonResponse({'message': 'No Valid Method'}, status=400)
        
    else:
        return JsonResponse({'message': 'User is not authenticated'}, status=401)
        
@permission_classes([IsAuthenticated])
@api_view(['POST', 'DELETE'])
def delete_laser_queries(request, pk):
    if request.user.is_staff or request.user.is_superuser:
        if request.method == "DELETE":
            query = LASER_Queries.objects.get(id=pk)
            query.delete()
            return JsonResponse({'message': 'Query deleted successfully!'}, status=204)
        else:
            return JsonResponse({'message': 'User is not authenticated'}, status=401)
    else:
        return JsonResponse({'message': 'User is not authenticated'}, status=401)


from .lti_grid_api import get_opic_diagnostic_grids, get_opi_comments

@permission_classes([IsAuthenticated])
@api_view(['POST', 'GET'])
def get_post_diagnostic_grid(request):
    if request.user.is_staff or request.user.is_superuser:
        if request.method == "GET":
            all_languages = OPIc_Diagnostic_Grid_Languages.objects.all()
            all_languages_serializer = OPIcLanguageSerializer(all_languages, many=True)
            all_programs = Reasons.objects.all()
            all_programs_serializer = ProgramSerializer(all_programs, many=True)
            return JsonResponse({'languages': all_languages_serializer.data, 'programs': all_programs_serializer.data}, status=200)
        if request.method == "POST":
            data = request.data
            language = data.get('language')
            from_date = data.get('fromDate')
            to_date = data.get('toDate')
            csv_file = data.get('files')
            test_type = data.get('testType')
            
            if test_type == 'OPIc':
                nl_intermediate_grid_results, nm_intermediate_grid_results, nh_intermediate_grid_results, il_advanced_grid_results, im_advanced_grid_results, ih_advanced_grid_results, al_advanced_grid_results, am_superior_grid_results, ah_superior_grid_results, nl_insight_counters, nm_insight_counters, nh_insight_counters, il_insight_counters, im_insight_counters, ih_insight_counters, al_insight_counters, am_insight_counters, ah_insight_counters, total_results, s_counter, missing_candidates = get_opic_diagnostic_grids(from_date, to_date, language, csv_file)

                data = {
                        'nl_intermediate_grid_results': nl_intermediate_grid_results,
                        'nm_intermediate_grid_results': nm_intermediate_grid_results,
                        'nh_intermediate_grid_results': nh_intermediate_grid_results,
                        'il_advanced_grid_results': il_advanced_grid_results,
                        'im_advanced_grid_results': im_advanced_grid_results,
                        'ih_advanced_grid_results': ih_advanced_grid_results,
                        'al_advanced_grid_results': al_advanced_grid_results,
                        'am_superior_grid_results': am_superior_grid_results,
                        'ah_superior_grid_results': ah_superior_grid_results,
                        'nl_insight_details': nl_insight_counters,
                        'nm_insight_details': nm_insight_counters,
                        'nh_insight_details': nh_insight_counters,
                        'il_insight_details': il_insight_counters,
                        'im_insight_details': im_insight_counters,
                        'ih_insight_details': ih_insight_counters,
                        'al_insight_details': al_insight_counters,
                        'am_insight_details': am_insight_counters,
                        'ah_insight_details': ah_insight_counters,
                        'total_results': total_results,
                        'superior_count': s_counter,
                    }
                
            if test_type == 'OPI':
                nl_intermediate_grid_results, nm_intermediate_grid_results, nh_intermediate_grid_results, il_advanced_grid_results, im_advanced_grid_results, ih_advanced_grid_results, al_advanced_grid_results, am_superior_grid_results, ah_superior_grid_results, nl_insight_counters, nm_insight_counters, nh_insight_counters, il_insight_counters, im_insight_counters, ih_insight_counters, al_insight_counters, am_insight_counters, ah_insight_counters, total_results, s_counter, missing_candidates = get_opi_comments(from_date, to_date, language, csv_file)

                data = {
                        'nl_intermediate_grid_results': nl_intermediate_grid_results,
                        'nm_intermediate_grid_results': nm_intermediate_grid_results,
                        'nh_intermediate_grid_results': nh_intermediate_grid_results,
                        'il_advanced_grid_results': il_advanced_grid_results,
                        'im_advanced_grid_results': im_advanced_grid_results,
                        'ih_advanced_grid_results': ih_advanced_grid_results,
                        'al_advanced_grid_results': al_advanced_grid_results,
                        'am_superior_grid_results': am_superior_grid_results,
                        'ah_superior_grid_results': ah_superior_grid_results,
                        'nl_insight_details': nl_insight_counters,
                        'nm_insight_details': nm_insight_counters,
                        'nh_insight_details': nh_insight_counters,
                        'il_insight_details': il_insight_counters,
                        'im_insight_details': im_insight_counters,
                        'ih_insight_details': ih_insight_counters,
                        'al_insight_details': al_insight_counters,
                        'am_insight_details': am_insight_counters,
                        'ah_insight_details': ah_insight_counters,
                        'total_results': total_results,
                        'superior_count': s_counter,
                    }
                
            if len(missing_candidates) != 0:
                csv_output = StringIO()
                writer = csv.writer(csv_output)
                
                # Write header for CSV (optional)
                writer.writerow(['Missing Candidates'])
                
                # Write each candidate to a new row in the CSV
                for candidate in missing_candidates:
                    writer.writerow([candidate])
                
                # Step 2: Encode the CSV content as base64
                csv_output.seek(0)  # Move to the start of the StringIO buffer
                csv_base64 = base64.b64encode(csv_output.getvalue().encode('utf-8')).decode('utf-8')

                # Step 3: Return the base64-encoded CSV content in the response
                data['csv_file'] = csv_base64

            return JsonResponse(data, status=201)
        return JsonResponse({'message': 'No Valid Method'}, status=400)
    else:
        return JsonResponse({'message': 'User is not authenticated'}, status=401)