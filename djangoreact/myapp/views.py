from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import get_template
from datetime import *
from .forms import OPIForm_Forms
import myapp.filemaker_api.filemaker_api as filemaker
import myapp.byu_api.byu_api as byu_api
import json
import myapp.google_api.service_account as google_calendar
import myapp.slack_api.slack as slack_message
from django.contrib.auth.decorators import user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
import os
from django.views.decorators.csrf import requires_csrf_token, csrf_exempt
import time
import myapp.box_api.box_api as box_api
from myapp.box_api.box_api import *
from myapp.models import *

#this is for maintenance
def redirect_to_template(template_name):
    def decorator(view_func):
        def wrapped_view(request, *args, **kwargs):
            # Perform any checks or logic here if needed
            return render(request, template_name)
        return wrapped_view
    return decorator

@user_passes_test(lambda u: u.is_superuser)
def reports(request):        
    return render(request, 'reports.html')

def receipt(request):
    get_template('receipt.html')
    return render(request, 'receipt.html')

#@redirect_to_template('maintenance.html')
@staff_member_required
def index_data(request):
    #can you get rid of redunant context and renders?
    token = filemaker.login()
    persons = []
    individual = []
    data = []   
    form = OPIForm_Forms()
    languages = Languages.objects.all()
    reasons = Reasons.objects.all()
    experience = LanguageExperience.objects.all()
    come_to_campus_reason  = ComeToCampusReason.objects.all()
    if request.method == 'POST':
        if 'search' in request.POST:
            input_data = {}
            select1 = (request.POST.get('search_select1', False))
            input1 = (request.POST.get('search_input1', False))
            
            select2 = (request.POST.get('search_select2', False))
            input2 = (request.POST.get('search_input2', False))

            select3 = (request.POST.get('search_select3', False))
            input3 = (request.POST.get('search_input3', False))

            print(select1, input1, select2, input2, select3, input3)

            if len(input1) != 0:
                input_data[select1] = input1
            if len(input2) != 0:
                input_data[select2] = input2
            if len(input3) != 0:
                input_data[select3] = input3
            print(input_data)
            data = []
            data.append('all_students')
            
            token = filemaker.login()
            
            if select1 == 'record_id':
                get_record = filemaker.find_record_ID(token, input1)
                try:
                    total = get_record['response']['dataInfo']['returnedCount']
                except KeyError:
                    return render(request, 'data.html') 
            else:
                get_record = filemaker.adaptive_find_record(token, **input_data)
                try:
                    total = get_record[0]['response']['dataInfo']['returnedCount']
                except KeyError:
                    return render(request, 'data.html') 
            
            filemaker.logout(token)
                # for key, value in get_record['response']['data'][0]['fieldData'].items():
                #     value = str(value)
                #     #persons.append(key + ': \n' + value)
                #     persons.append(value)
           
            print("total=", total)
            for i in range(0, total):
                print('i=', i)
                if select1 == 'record_id':
                    record = get_record['response']['data'][i]['fieldData']
                else:
                    record = get_record[0]['response']['data'][i]['fieldData']
                print(record)
                for key, value in record.items():
                    value = str(value)
                    individual.append(value)
                persons.append(individual[:])
                individual.clear()   
                  
            context = {'form': form,
                'data':data, 
                    'person':persons, 
                    'languages': languages,
                        'reasons': reasons,
                            'experience': experience,
                            'come_to_campus_reason': come_to_campus_reason,
                    }   
            return render(request, 'data.html', context)
        if 'approval' in request.POST:
            #add something to check if 0 need approval
            data.append('all_students')
            get_record = filemaker.need_approval(token)
            if get_record['messages'][0]['code'] == '0':
                total = len(get_record['response']['data'])
                for i in range(total):
                    record = get_record['response']['data'][i]['fieldData']
                    for key, value in record.items():
                        value = str(value)
                        individual.append(value)
                    persons.append(individual[:])
                    individual.clear()                    
                context = {'form': form,
                    'data':data, 
                        'person':persons, 
                        'languages': languages,
                            'reasons': reasons,
                                'experience': experience,
                                'come_to_campus_reason': come_to_campus_reason,
                        }
                return render(request, 'data.html', context)
            return render(request, 'data.html')
            
        if 'update' in request.POST:
            list = []
            get_records = filemaker.get_all(token)
            total = len(get_records['response']['data'])
            print("total= " + str(total))

            for i in range(total):
                check_box = request.POST.get(f'check_box{i}', None)
                print(check_box) 
                if check_box == 'on':
                    print('checkbox on')
                    for j in range((i*29),29+(i*29)):
                        # print(request.POST.get(f'data{j}', None))
                        # print('data' + str(j))
                        if request.POST.get(f'data{j}', None) == "":
                            list.append('Empty')
                        else:
                            list.append(request.POST.get(f'data{j}', None))

                    print(list)
                    scores = list[0]
                    testscheduled = list[1]
                    agree = list[2]
                    entrydate = list[3]
                    entrytime = list[4]
                    firstname = list[5]
                    lastname = list[6]
                    byuid = list[7]
                    netid = list[8]
                    email = list[9]
                    reason = list[10]
                    language = list[11]
                    languageother = list[12]
                    previousexperience = list[13]
                    major = list[14]
                    secondmajor = list[15]
                    minor = list[16]
                    cometocampus = list[17]
                    cannotcome = list[18]
                    testdate1 = list[19]
                    testdate2 = list[20]
                    time1 = list[21]
                    time2 = list[22]
                    time3 = list[23]
                    time4 = list[24]
                    CertificateStatus = list[25]
                    phone = list[26]
                    emailsent = list[27]
                    lti_schedule = list[28]
                    query = filemaker.adaptive_find_record(token, BYUID=byuid, Language=language, EntryDate=entrydate, EntryTime=entrytime)
                    record_id = query[0]['response']['data'][0]['recordId']
                    filemaker.edit_all_fields(scores, testscheduled, agree, entrydate, entrytime, firstname, lastname, byuid, netid, email, reason, language, languageother,
                    previousexperience,major,secondmajor,minor,cometocampus,cannotcome,testdate1,testdate2,time1,time2,time3,time4, CertificateStatus,phone,emailsent, lti_schedule, token, record_id)
                    list.clear()
            #revoke token
            # 0-27
            #get value, update in database
            #reload entire page with data still pulled up
            #add select all
            # response = JsonResponse({"error": "Hello"})
            # response.status_code = 403
            #initial 0-27
            #case 2: 28-55
            #case 3: 56-83
            #case 4: 84-112
        if 'create_record' in request.POST:
            create_student_record(request, token)
        if 'delete' in request.POST:
            list = []
            get_records = filemaker.get_all(token)
            total = len(get_records['response']['data'])
            print("total= " + str(total))

            for i in range(total):
                check_box = request.POST.get(f'check_box{i}', None)
                print(check_box) 
                if check_box == 'on':
                    print('checkbox on')
                    for j in range((i*29),29+(i*29)):
                        # print(request.POST.get(f'data{j}', None))
                        # print('data' + str(j))
                        if request.POST.get(f'data{j}', None) == "":
                            list.append('Empty')
                        else:
                            list.append(request.POST.get(f'data{j}', None))

                    print(list)
                    #region
                    scores = list[0]
                    testscheduled = list[1]
                    agree = list[2]
                    entrydate = list[3]
                    entrytime = list[4]
                    firstname = list[5]
                    lastname = list[6]
                    byuid = list[7]
                    netid = list[8]
                    email = list[9]
                    reason = list[10]
                    language = list[11]
                    languageother = list[12]
                    previousexperience = list[13]
                    major = list[14]
                    secondmajor = list[15]
                    minor = list[16]
                    cometocampus = list[17]
                    cannotcome = list[18]
                    testdate1 = list[19]
                    testdate2 = list[20]
                    time1 = list[21]
                    time2 = list[22]
                    time3 = list[23]
                    time4 = list[24]
                    CertificateStatus = list[25]
                    phone = list[26]
                    emailsent = list[27]
                    lti_schedule = list[28]
                    #endregion
                    query = filemaker.adaptive_find_record(token, BYUID=byuid, Language=language, EntryDate=entrydate, EntryTime=entrytime)
                    record_id = query[0]['response']['data'][0]['recordId']
                    print(record_id)
                    delete_record = delete(request, record_id, token)
                    list.clear()
        data.append('all_students')
        get_record = filemaker.get_all(token)
        total = len(get_record['response']['data'])
        for i in range(total):
            record = get_record['response']['data'][i]['fieldData']
            for key, value in record.items():
                value = str(value)
                individual.append(value)
            persons.append(individual[:])
            individual.clear()      
        
        context = {'form': form,
        'data':data, 
            'person':persons, 
            'languages': languages,
                'reasons': reasons,
                    'experience': experience,
                    'come_to_campus_reason': come_to_campus_reason,
            }
        
        return render(request, 'data.html', context)
    else:
        data.append('all_students')
        get_record = filemaker.need_approval(token)
        if get_record['messages'][0]['code'] == '0':
            total = len(get_record['response']['data'])
            for i in range(total):
                record = get_record['response']['data'][i]['fieldData']
                for key, value in record.items():
                    value = str(value)
                    individual.append(value)
                persons.append(individual[:])
                individual.clear()                    

            context = {'form': form,
                'data':data, 
                    'person':persons, 
                    'languages': languages,
                        'reasons': reasons,
                            'experience': experience,
                            'come_to_campus_reason': come_to_campus_reason,
                    }
        
            return render(request, 'data.html', context)
        return render(request, 'data.html')

@user_passes_test(lambda u: u.is_superuser)
def delete(request, record_id, token):
    filemaker.delete_record(record_id, token)

@user_passes_test(lambda u: u.is_superuser)
def create_student_record(request, token):
    now = datetime.now()

    sqldb_entry_date = date.today()

    entry_date = datetime.strftime(sqldb_entry_date, '%m-%d-%Y')
    entry_time = now.strftime("%H:%M:%S")
    first_name = request.POST.get('first_name', None)
    last_name = request.POST.get('last_name', None)
    byuid = request.POST.get('byuid', None)
    netid = request.POST.get('netid', None)
    scores = None
    test_request = request.POST.get('test_request', None)
    approved = request.POST.get('approved', None)
    email_sent = request.POST.get('email_sent', None)
    reason_id = (request.POST.get('reason', False))
    reason = Reasons.objects.get(pk=reason_id)
    reason = str(reason)
    language_id = (request.POST.get('language', False))
    language = Languages.objects.get(pk=language_id)    
    language_other = request.POST.get('language_other', None)
    test_date1 = request.POST.get('test_date1', None)
    time1 = request.POST.get('time1', None)
    time2 = request.POST.get('time2', None)
    test_date2 = request.POST.get('test_date2', None)
    time3 = request.POST.get('time3', None)
    time4 = request.POST.get('time4', None)
    phone = request.POST.get('phone', None)
    experience_id = (request.POST.get('experience', False))
    experience = LanguageExperience.objects.get(pk=experience_id)
    experience = str(experience)
    major = request.POST.get('major', None)
    second_major = request.POST.get('second_major', None)
    minor = request.POST.get('minor', None)
    come_to_campus = (request.POST.get('come_to_campus', False))

    cannot_come_id = (request.POST.get('cannot_come', False))
    try:
        cannot_come = ComeToCampusReason.objects.get(pk=cannot_come_id)
        cannot_come = str(cannot_come)
    except:
        cannot_come = 'NA'
    email = netid + "@byu.edu"
    CertificateStatus = "None"
    scores = 'None'

    sqldb_testdate1 = (request.POST.get('test_date1'))
    format_testdate1 = datetime.strptime(sqldb_testdate1, '%Y-%m-%d').date()
    testdate1 = datetime.strftime(format_testdate1, '%m-%d-%Y')
    
    sqldb_testdate2 = (request.POST.get('test_date2'))
    format_testdate2 = datetime.strptime(sqldb_testdate2, '%Y-%m-%d').date()
    testdate2 = datetime.strftime(format_testdate2, '%m-%d-%Y')

    record_id = filemaker.create_record(scores=scores, approved=approved, entry_date=entry_date, entry_time=entry_time, firstname=first_name, lastname=last_name, byuid=byuid,
                netid=netid, email=email, reason=reason, language=language.abbreviation, language_other=language_other, experience=experience, major=major, second_major=second_major, minor=minor, come_to_campus=come_to_campus,
                cannot_come=cannot_come, testdate1=testdate1, testdate2=testdate2, time1=time1, time2=time2, time3=time3, time4=time4, CertificateStatus=CertificateStatus, phone=phone, token=token)

#@redirect_to_template('maintenance.html')
def opi_form(request):
    if request.method == 'POST':
        form = OPIForm_Forms(request.POST)

        google_calendar.main()

        valid = True
        now = datetime.now()

        #region contains all request values
        sqldb_entry_date = date.today()
        entry_date = datetime.strftime(sqldb_entry_date, '%m-%d-%Y')

        entry_time = now.strftime("%H:%M:%S")
        agree = bool(request.POST.get('agree'))
        firstname = (request.POST.get('firstname', False))
        lastname = (request.POST.get('lastname', False))
        byuid = (request.POST.get('byuid', False))
        print(f'Student {byuid} has attempted to to submit a test request.')
        netid = (request.POST.get('netid', False))
        netid = netid.replace(' ', '')
        
        email = (request.POST.get('email', False))

        reason_id = (request.POST.get('reason', False))
        reason = Reasons.objects.get(pk=reason_id)
        reason = str(reason)

        reason_other= (request.POST.get('reason_other', False))

        language_id = (request.POST.get('language', False))
        language = Languages.objects.get(pk=language_id)

        language_other = (request.POST.get('language_other', False))

        experience_id = (request.POST.get('experience', False))
        experience = LanguageExperience.objects.get(pk=experience_id)
        experience = str(experience)

        major = (request.POST.get('major', False))
        second_major= (request.POST.get('second_major', False))
        minor = (request.POST.get('minor', False))
        scores = 'None'
        come_to_campus = (request.POST.get('come_to_campus', False))

        cannot_come_id = (request.POST.get('cannot_come', False))
        try:
            cannot_come = ComeToCampusReason.objects.get(pk=cannot_come_id)
            cannot_come = str(cannot_come)
        except:
            cannot_come = 'NA'

        time1 = (request.POST.get('time1'))
        time_object1 = datetime.strptime(time1, "%H:%M").time()
        time2 = (request.POST.get('time2'))
        time_object2 = datetime.strptime(time2, "%H:%M").time()
        time3 = (request.POST.get('time3'))
        time_object3 = datetime.strptime(time3, "%H:%M").time()
        time4 = (request.POST.get('time4'))
        time_object4 = datetime.strptime(time4, "%H:%M").time()
        CertificateStatus = (request.POST.get('CertificateStatus', False))
        phone = (request.POST.get('phone', False))
        
        finished_date = datetime.strptime(request.POST['testdate1'], '%Y-%m-%d')

        sqldb_testdate1 = (request.POST.get('testdate1'))
        format_testdate1 = datetime.strptime(sqldb_testdate1, '%Y-%m-%d').date()
        testdate1 = datetime.strftime(format_testdate1, '%m-%d-%Y')
        
        finished_date_2 = datetime.strptime(request.POST['testdate2'], '%Y-%m-%d')

        sqldb_testdate2 = (request.POST.get('testdate2'))
        format_testdate2 = datetime.strptime(sqldb_testdate2, '%Y-%m-%d').date()
        testdate2 = datetime.strftime(format_testdate2, '%m-%d-%Y')
        if finished_date.weekday() == 1:
            if (time_object1.hour == 8 or time_object1.hour == 9 or time_object1.hour == 10 or time_object1.hour == 11) and (time_object2.hour > 11 or (time_object2.hour == 11 and time_object2.minute > 0)):
                response = JsonResponse({"error": "You cannot schedule during a devotional."})
                response.status_code = 403
                return response
            if time2 == '11:00':
                time2 = '10:30'
        if finished_date_2.weekday() == 1:
            if (time_object3.hour == 8 or time_object3.hour == 9 or time_object3.hour == 10 or time_object3.hour == 11) and (time_object4.hour > 11 or (time_object4.hour == 11 and time_object4.minute > 0)):
                response = JsonResponse({"error": "You cannot schedule during a devotional."})
                response.status_code = 403
                return response
            if time4 == '11:00':
                time4 = '10:30'
        #endregion
        f = open(os.path.abspath("myapp/google_api/events.json"))
        data = json.load(f)
        k = 0
        for i in data:
            if testdate1 == data[k]['Date']:
                print(testdate1, i, 'first')
                response = JsonResponse({"error": "The testing center is closed on " + data[k]['Date'] + '. Please schedule for a different day.'})
                response.status_code = 403
                valid == False
                return response
            if testdate2 == data[k]['Date']:
                print(testdate2, i, 'second')
                response = JsonResponse({"error": "The testing center is closed on " + data[k]['Date'] + '. Please schedule for a different day.'})
                response.status_code = 403
                valid == False
                return response
            k += 1

        byu_token = byu_api.login()
        valid_student = byu_api.get_byuid(byu_token, byuid, netid, valid)

        try:
            filemaker_token = filemaker.login()
            test = filemaker.find_record('BYUID', byuid, filemaker_token)
            print(test['response']['data'][0]['fieldData']['Language'])
            if test['messages'][0]['code'] == '0':
                if test['response']['data'][0]['fieldData']['Language'] in language.abbreviation and test['response']['data'][0]['fieldData']['EmailSent'] == 'No':
                    response = JsonResponse({"error": "You have already submitted a test request for your requested language. If you would like to rescedule, please call or email the Center for Language Studies."})
                    response.status_code = 403
                    return response
        except KeyError:
            #this student is clear to submit a test request
            pass
        if language.full_language != "Other":
            print(type(language.abbreviation))
            print(byuid, language.abbreviation, reason, valid)
            valid_classes = byu_api.get_classes(byu_token, byuid, language.abbreviation, valid, reason)
        logout = byu_api.logout(byu_token)
        if (language.full_language == "Other" and valid_student == True) or (valid_student == True and valid == True and valid_classes == True):

            email = netid + '@byu.edu'
            CertificateStatus = 'None'
            success = 'Sent for ' + firstname
            approved = 'Waiting'

            #send slack message if applicable
            if reason == 'Individual Request' or \
            'FLAS' in reason or \
            'Study Abroad' in reason or \
            'CLS_Instructor' in reason or \
            'LASER' in reason or \
            'MAPL' in reason or \
            'Research' in reason or \
            'Dual Immersion' in reason or \
            'Program Applicant' in reason or \
            'SLaT' in reason or \
            'LSR' in reason or \
            'Research' in reason or \
            'Study Abroad' in reason or \
            language.full_language == 'Other': 
                approved='No'
                record_id = filemaker.create_record(scores, approved, entry_date, entry_time, firstname, lastname, byuid,
                    netid, email, reason, language.abbreviation, language_other, experience, major, second_major, minor, come_to_campus,
                    cannot_come, testdate1, testdate2, time1, time2, time3, time4, CertificateStatus, phone, filemaker_token)
                if firstname == 'test' or firstname == 'Test' or lastname == 'Person' or lastname == 'person':
                    pass
                elif language.full_language == 'Other':
                    slack_str = f'A student requires your assistance. \nReason: Other Language \nRecord ID: {record_id} '
                    slack_message.send_slack_message(slack_str)  
                elif ('Research' in reason) or ('Individual Request' in reason) or ('Study Abroad' in reason) or ('LASER' in reason) or ('SLaT' in reason):
                    slack_str = f'A student requires your assistance. \nReason: {reason} \nRecord ID: {record_id} '
                    slack_message.send_slack_message(slack_str)          
                elif come_to_campus == 'No':
                    slack_str = f'A student cannot come to campus to take their OPI test and requires your attention. \nReason: {cannot_come} \nRecord ID: {record_id} '
                    slack_message.send_slack_message(slack_str)
                else:
                    slack_str = f'A student has sent in an OPI request that requires your attention. \nReason: {reason} \nRecord ID: {record_id} '
                    slack_message.send_slack_message(slack_str)

            else:
                record_id = filemaker.create_record(scores, approved, entry_date, entry_time, firstname, lastname, byuid,
                    netid, email, reason, language.abbreviation, language_other, experience, major, second_major, minor, come_to_campus,
                    cannot_come, testdate1, testdate2, time1, time2, time3, time4, CertificateStatus, phone, filemaker_token)
            filemaker.logout(filemaker_token)
            return HttpResponse(success)
        else:
            print('it faileeeedddd')
            response = JsonResponse({"error":"There was an error submitting your request."})
            if not valid_student:
                response = JsonResponse({"error": "Your BYU student information is incorrect. Please verify your BYU ID and NET ID and make sure that there is not a space at the end of your NET ID."})
            if not valid_classes:
                response = JsonResponse({"error": "You have not yet completed the required language courses to qualify for the OPI. Please verify your course selection. Additionally, students often put the incorrect reason for taking the test. For example, sometimes students enter 'Language Certificate', when really they should be putting their seminar class as the reason for taking the OPI test."})
            response.status_code = 403
            return response
        
    else:
        form = OPIForm_Forms()
        languages = Languages.objects.all()
        reasons = Reasons.objects.all()
        experience = LanguageExperience.objects.all()
        come_to_campus_reason  = ComeToCampusReason.objects.all()

        ### start of testing block
        # byu_id = "052163478"
        # language_abbre = "RUSS"
        # if language_abbre != "None":
        #     byu_token = byu_api.login()
        #     valid_type_language_courses = Courses.objects.filter(language_abbreviation=language_abbre, type_language=True).values('byu_course_key')
        #     valid_type_culture_courses = Courses.objects.filter(language_abbreviation=language_abbre, type_civilization_culture=True).values('byu_course_key')
        #     valid_type_literature_courses = Courses.objects.filter(language_abbreviation=language_abbre, type_literature=True).values('byu_course_key')
        #     reason = "Language Certificate"
        #     seminar_filter = Reasons.objects.filter(reason=reason).first()

        #     byu_api.test2(byu_token, valid_type_language_courses, valid_type_culture_courses, valid_type_literature_courses, seminar_filter, byu_id, language_abbre, reason)
        #     byu_api.logout(byu_token)

        ### end of testing block
        context = {'form': form, 
                   'languages': languages,
                     'reasons': reasons,
                        'experience': experience,
                        'come_to_campus_reason': come_to_campus_reason,
                
                }
    
        return render(request, 'opi_form.html', context)

#@redirect_to_template('maintenance.html')
def email_confirmation(request, encoded_string):
    import base64
    decoded_string = base64.b64decode(encoded_string).decode('utf-8')
    print(decoded_string)

    split_values = decoded_string.split('&')
    byuid = split_values[0]
    language = split_values[1]
    entrydate = split_values[2]

    #try except block for entrytime because entrytime was instituted 9/20
    try:
        entrytime = split_values[3]
    except:
        entrytime = None

    token = filemaker.login()

    if entrytime == None:
        query = filemaker.adaptive_find_record(token, BYUID=byuid, Language=language, EntryDate=entrydate)
    else:
        query = filemaker.adaptive_find_record(token, BYUID=byuid, Language=language, EntryDate=entrydate, EntryTime=entrytime)

    record_id = query[0]['response']['data'][0]['recordId']
    first_name = query[0]['response']['data'][0]['fieldData']['FirstName']
    last_name = query[0]['response']['data'][0]['fieldData']['LastName']
    approved = query[0]['response']['data'][0]['fieldData']['Approved']
    full_name = first_name + " " + last_name
    if approved == 'Yes':
        pass
    else:
        filemaker.edit_record('Approved', 'Yes', token, record_id)
        slack_str = f'A student has confirmed their testing date. \nRecord ID: {record_id} '
        slack_message.send_slack_message(slack_str) 
    filemaker.logout(token)
    return render(request, 'email_confirmation.html', context={'fullname': full_name})

#@redirect_to_template('maintenance.html')
@staff_member_required
def certificates(request):
    if request.method == 'POST':
        record_id = list(request.POST.keys())[1]
        context = {'record_id': record_id}
        return redirect(f'certificates/review-certificate/record-id={record_id}')
    else:
        token = filemaker.login()
        try:
            query = filemaker.find_record('CertificateStatus', 'Qualified', token)
        except KeyError:
            return render(request, 'certificates.html')
        students = []
        for student in query['response']['data']:
            student_data = []
            student_data.append(student['fieldData']['FirstName'])
            student_data.append(student['fieldData']['LastName'])
            language = Languages.objects.filter(abbreviation=student['fieldData']['Language']).values()
            print(language[0]['full_language'])
            student_data.append(language[0]['full_language'])
            scores = student['fieldData']['Scores'].split('/')
            print(scores)
            try:
                opi_score = scores[0]
            except:
                opi_score = scores[1]
            wpt_score = scores[2]

            score_df = {"NL": "Novice Low", "NM": "Novice Mid", "NH": "Novice High", 
                        "IL": "Intermediate Low", "IM": "Intermediate Mid", "IH": "Intermediate High", 
                        "AL": "Advanced Low", "AM": "Advanced Mid", "AH": "Advanced High", 
                        "S": "Superior", 
                        "D": "Distinguished"}
            
            for key, value in score_df.items():
                if key == opi_score:
                    opi_score = value
                    break
            for key, value in score_df.items():
                if key == wpt_score:
                    wpt_score = value
                    break
            student_data.append(opi_score)
            student_data.append(wpt_score)
            student_data.append(student['recordId'])
            students.append(student_data)

        context = {'query': students}
        get_template('certificates.html')
        filemaker.logout(token)
        return render(request, 'certificates.html', context)

@user_passes_test(lambda u: u.is_superuser)
def review_certificate(request, encoded_string):
    token = filemaker.login()
    if request.method == 'POST':
        full_name = request.POST['full_name']
        language = request.POST['language']
        level = request.POST['level']
        opi_score = request.POST['opi_score']
        wpt_score = request.POST['wpt_score']
        formatted_date = request.POST['date']
        print(full_name, language, level, opi_score, wpt_score, formatted_date)
        #filemaker.edit_record('Approved', 'Yes', token, encoded_string)
        box_api.create_pdf_cert(encoded_string, full_name, language.upper(), level.upper(), opi_score, wpt_score, formatted_date)
        filemaker.logout(token)
        return redirect('certificates')
    else:
        student = filemaker.find_record_ID(token, encoded_string)
        filemaker.logout(token)

        abbreviated_language = student['response']['data'][0]['fieldData']['Language']
        language = Languages.objects.filter(abbreviation=abbreviated_language).values()
        language = language[0]['full_language']

        first_name = student['response']['data'][0]['fieldData']['FirstName']
        last_name = student['response']['data'][0]['fieldData']['LastName']
        full_name = first_name + " " + last_name

        scores = student['response']['data'][0]['fieldData']['Scores'].split('/')

        try:
            opi_score = scores[0]
        except:
            opi_score = scores[1]
        wpt_score = scores[2]

        score_df = {"NL": "Novice Low", "NM": "Novice Mid", "NH": "Novice High", 
                    "IL": "Intermediate Low", "IM": "Intermediate Mid", "IH": "Intermediate High", 
                    "AL": "Advanced Low", "AM": "Advanced Mid", "AH": "Advanced High", 
                    "S": "Superior", 
                    "D": "Distinguished"}
        
        for key, value in score_df.items():
            if key == opi_score:
                opi_score = value
                break
        for key, value in score_df.items():
            if key == wpt_score:
                wpt_score = value
                break
        
        level_df = {"Advanced": "(Advanced Low, Advanced Mid) 1", "Mastery": "(Advanced High) 2", "Superior": "(Superior) 3"}

        level_values = list(level_df.values())
        if opi_score in level_values[2] or wpt_score in level_values[2]:
            level = "Superior"
        elif opi_score in level_values[1] or wpt_score in level_values[1]:
            level = "Mastery"
        elif opi_score in level_values[0] or wpt_score in level_values[0]:
            level = "Advanced"
        else:
            level = "Undetermined"

        todays_date = date.today()
        formatted_date = todays_date.strftime("%m/%d/%Y")

        context = {'language': language,
                    'full_name': full_name,
                    'level': level,
                    'opi_score': opi_score,
                    'wpt_score': wpt_score,
                    'date': formatted_date,
                    }
        return render(request, 'review_certificate.html', context)
    


