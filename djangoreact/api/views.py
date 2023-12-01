from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout, login, authenticate
from django.middleware.csrf import get_token
from django.http import HttpResponse
from django.contrib.auth.models import User
from knox.models import AuthToken
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.
from rest_framework import status
from rest_framework import generics

from .models import Students
from .serializers import StudentSerializer
from .serializers import UserSerializer
import api.filemaker_api as filemaker
import json
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from knox.auth import TokenAuthentication
from knox.views import LogoutView
import api.lti_api as lti
from datetime import datetime
import api.outlook_api as outlook
import api.box_api as box_api
from django.contrib.auth import authenticate
from django.utils import timezone
from knox.models import AuthToken
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from axes.decorators import axes_dispatch
from axes.signals import user_login_failed
from axes.utils import reset

from datetime import datetime
from django.utils import timezone
        
@api_view(['GET'])
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


@api_view(['GET'])
def student_list(request):
    student_list = Students.objects.all()
    serializer = StudentSerializer(student_list, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def student_update(request, student):
    token = request.COOKIES['token']
    token, username = token.split(' : ')
    user = User.objects.filter(username=username).first()
    if user is not None and user.is_superuser:
        print('Student Record ID:', student)
        print(request.data)
    
        token = filemaker.login()
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

@api_view(['POST'])
def student_delete(request, student):
    token = request.COOKIES['token']
    token, username = token.split(' : ')
    user = User.objects.filter(username=username).first()
    if user is not None and user.is_superuser:
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
    response = Response({"message": "Set CSRF cookie"})
    response["X-CSRFToken"] = get_token(request)
    return response

@api_view(['GET'])
def filemaker_view(request):
    token = request.COOKIES['token']
    token, username = token.split(':')
    user = User.objects.filter(username=username).first()
    if user is not None and user.is_staff:
            
        print('Filemaker API Used')
        token = filemaker.login()
        students = filemaker.get_all(token)
        filemaker.logout(token)
        print(request)
        return JsonResponse(students, safe=False)
    return JsonResponse({'message': 'User is not authenticated'}, status=401)

@api_view(['GET'])
def example_lti_view(request):
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

@api_view(['POST'])
def get_certificate_data(request):
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

    lti.close_browser(browser)
    data = lti.start_search(formatted_record_date, formatted_semester_date)

    score_df = {"NL": "Novice Low", "NM": "Novice Mid", "NH": "Novice High", 
            "IL": "Intermediate Low", "IM": "Intermediate Mid", "IH": "Intermediate High", 
            "AL": "Advanced Low", "AM": "Advanced Mid", "AH": "Advanced High", 
            "S": "Superior", "D": "Distinguished"}
    
    level_df = {"Advanced": "(Advanced Low, Advanced Mid) 1", "Mastery": "(Advanced High) 2", "Superior": "(Superior) 3"}
    level_values = list(level_df.values())

    for student_df in data:
        if student_df['opiScore'] in score_df:
            student_df['opiScore'] = {student_df['opiScore']: score_df[student_df['opiScore']]}
        if student_df['wptScore'] in score_df:
            student_df['wptScore'] = {student_df['wptScore']: score_df[student_df['wptScore']]}
        if student_df['opicScore'] in score_df:
            student_df['opicScore'] = {student_df['opicScore']: score_df[student_df['opicScore']]}
    
        opi_score_values = list(student_df['opiScore'].values())
        wpt_score_values = list(student_df['wptScore'].values())
        print(opi_score_values, wpt_score_values)

        if (opi_score_values[0] in level_values[2]) or (wpt_score_values[0] in level_values[2]):
            level = "Superior"
        elif (opi_score_values[0] in level_values[1]) or (wpt_score_values[0] in level_values[1]):
            level = "Mastery"
        elif (opi_score_values[0] in level_values[0]) or (wpt_score_values[0] in level_values[0]):
            level = "Advanced"
        else:
            level = "Undetermined"
        student_df['level'] = level

    return JsonResponse(data, safe=False)

@api_view(['POST'])
def award_certificate(request):
    print(request.data)
    #{'dataToSend': {'NetID': 'phart4'}}
    netid = request.data['dataToSend']['NetID']
    box_client = box_api.create_client()
    file_id = box_api.create_pdf_cert(box_client, record_id, full_name, language.upper(), level.upper(), opi_score, wpt_score, formatted_date)
    shareable_link = box_api.create_shared_link(box_client, file_id)
    #add box link to emaild
    data = {
        "subject": f'Language Certificate',
        "importance":"High",
        "body":{
            "contentType":"HTML",
            "content":"""
            <BODY><p style="color:black;font-weight:normal;">{Name},<br><br>
            
            Congratulations on earning your language certificate! Please see the attached certificate.<br><br>
            
            Best,<br><br>

            Center for Language Studies<br> 
            cls.byu.edu<br> 
            </p></BODY></HTML>
            """
                    },
        "toRecipients":[
            {
                "emailAddress":{
                    "address": netid + "@byu.edu"
                }
            }
        ]
    }
    # token = outlook.get_token()
    # message = outlook.create_message(token, data)
    # outlook.send_message(token, message)
    data = {
        "subject": f'Language Certificate for [Name]',
        "importance":"High",
        "body":{
            "contentType":"HTML",
            "content":"""
            <BODY><p style="color:black;font-weight:normal;">BYU Enrollment Services,<br><br>
            
            [Name] has earned their BYU Language Certificate and requires a notation on their transcript. Thank you for your assistance.<br><br>

            Name: [Name]<br>
            BYUID:[BYUID]<br>
            Language:[Language]<br>
            Level:[Level]<br>
            Month:[Month]<br>
            Year:[Year]<br>
            Yearterm:[Yearterm]<br>
            
            Best,<br><br>

            Center for Language Studies<br> 
            cls.byu.edu<br> 
            </p></BODY></HTML>
            """
                    },
        "toRecipients":[
            {
                "emailAddress":{
                    "address": "graduation@byu.edu"
                }
            }
        ]
    }
    # message = outlook.create_message(token, data)
    # outlook.send_message(token, message)

    return JsonResponse({'message': 'Certificate awarded'})


@api_view(['POST'])
def lti_view(request):
    # token = request.COOKIES['token']
    # token, username = token.split(' : ')
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


@api_view(['GET'])
def need_approval_filemaker(request):
    token = request.COOKIES['token']
    token, username = token.split(':')
    user = User.objects.filter(username=username).first()
    if user is not None and user.is_staff:
        print('Filemaker API Used')
        token = filemaker.login()
        students = filemaker.adaptive_find_record(token, Approved='No')
        filemaker.logout(token)
        return JsonResponse(students, safe=False)
    else:
        return JsonResponse({'message': 'User is not authenticated'}, status=401)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def logout_view(request):
    # logout(request)
    # LogoutView().post(request)
    response = JsonResponse({
    "user": 'None',
    })
    response.set_cookie('token', expires='Thu, 01 Jan 1970 00:00:00 GMT', httponly=True)

    return response

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def get_user_info(request):
    try:
        token = request.COOKIES['token']
        token_parts = token.split(':')

        if len(token_parts) != 2:
            return Response({'error': 'Invalid token format'}, status=status.HTTP_400_BAD_REQUEST)

        token, username = token_parts
        user = User.objects.filter(username=username).first()

        if user is None:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        user_groups = user.groups.all()
        group_names = [group.name for group in user_groups]

        return Response({
            'user': UserSerializer(user, context={'request': request}).data,
            'groups': group_names
        })
    except KeyError:
        return Response({'error': 'Token not found'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@axes_dispatch
@api_view(['POST'])
def login_knox(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(request, username=username, password=password)  # Authenticate user

    if user is None:
        # If the login failed, dispatch user_login_failed signal for Axes
        user_login_failed.send(
            sender=__name__,
            credentials={'username': username},
            request=request
        )

        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        # If the login succeeded, reset failed attempts for the user
        reset(username=username)
        try:
            # Verify if a token exists and is valid
            token = request.COOKIES.get('token')
            auth_token = None

            if token:
                token_parts = token.split(':')
                if len(token_parts) == 2:
                    token, username = token_parts
                    auth_token = AuthToken.objects.get(token_key=token, user__username=username)
                    #auth_token = AuthToken.objects.get(digest=token)

            if auth_token and auth_token.expiry > timezone.now():
                print(auth_token, 'Token is valid and no new token created')
                return Response({'message': 'Token is valid'})
            else:
                # Token is expired or doesn't exist, create a new token
                if auth_token:
                    auth_token.delete()  # Delete expired token

                new_token_tuple = AuthToken.objects.create(user=user)

                # Unpack the tuple returned by AuthToken.objects.create()
                new_token, created = new_token_tuple

                response = JsonResponse({
                    "user": UserSerializer(user, context={'request': request}).data,
                })
                response.set_cookie(key='token', value=f'{new_token.token_key}:{user.username}', httponly=True, secure=True)
                print(new_token.token_key, 'Token created')  # Access the token_key attribute
                return response
        except AuthToken.DoesNotExist:
            # No token exists for the user, create a new one
            new_token_tuple = AuthToken.objects.create(user=user)

            # Unpack the tuple returned by AuthToken.objects.create()
            new_token, created = new_token_tuple

            response = JsonResponse({
                "user": UserSerializer(user, context={'request': request}).data,
            })
            response.set_cookie(key='token', value=f'{new_token.token_key}:{user.username}', httponly=True, secure=True)
            print(new_token.token_key, 'Token created')  # Access the token_key attribute
            return response
        except Exception as e:
            print(e)
            return HttpResponse('Token authentication error', status=status.HTTP_401_UNAUTHORIZED)

    
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def verify_token_knox(request):
    try:
        token = request.COOKIES['token']  # Get the token from the cookie
        token, username = token.split(':')

        print('token:', token)
    except:
        return HttpResponse('Token is not provided', status=status.HTTP_401_UNAUTHORIZED)
    if token is None:
        return HttpResponse('Token is not provided', status=status.HTTP_401_UNAUTHORIZED)

    try:
        auth_token = AuthToken.objects.get(token_key=token, user__username=username)
        if auth_token is not None and auth_token.user.username == username and auth_token.expiry > timezone.now():
            print(auth_token, 'worked')
            return HttpResponse('Token is valid', status=status.HTTP_200_OK)
        else:
            print(auth_token, 'did not work')
            return HttpResponse('Token is invalid', status=status.HTTP_401_UNAUTHORIZED)
    except:
        print('huh')
        return HttpResponse('Token authentication error', status=status.HTTP_401_UNAUTHORIZED)


