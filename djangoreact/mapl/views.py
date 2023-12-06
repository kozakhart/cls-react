from django.shortcuts import render
from .models import *
from .forms import *
from datetime import datetime, date
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
import mapl.box_api.box_api as box_api

# Create your views here.
def mapl_form(request):
    if request.method == 'POST':
        form = MAPLForm_Forms(request.POST)

        now = datetime.now()

        sqldb_entry_date = date.today()
        entry_date = datetime.strftime(sqldb_entry_date, '%m-%d-%Y')
        entry_time = now.strftime("%H:%M:%S")

        firstname = (request.POST.get('firstname', False))
        middlename = (request.POST.get('middlename', False))
        lastname = (request.POST.get('lastname', False))
        email = (request.POST.get('email', False))
        byuid = (request.POST.get('byuid', False))
        phone = (request.POST.get('phone', False))
        major = (request.POST.get('major', False))
        heard_about_id = (request.POST.get('heard_about', False))
        heard_about = HeardAbout.objects.get(pk=heard_about_id)
        heard_about = str(heard_about)
        semester_of_entry_id = (request.POST.get('semester_of_entry', False))
        semester_of_entry = SemesterOfEntry.objects.get(pk=semester_of_entry_id)
        semester_of_entry = str(semester_of_entry)
        academic_status_id = (request.POST.get('academic_status', False)) 
        academic_status = AcademicStatus.objects.get(pk=academic_status_id)
        academic_status = str(academic_status)
        gpa = (request.POST.get('gpa', False))
        opi_score_id = (request.POST.get('opi_score', False))
        if opi_score_id != '':
            opi_score = Scores.objects.get(pk=opi_score_id)
            opi_score = str(opi_score)
        else:
            opi_score = "None"
        raw_opi_date = (request.POST.get('opi_date', False))
        if raw_opi_date != '':
            format_opi_date = datetime.strptime(raw_opi_date, '%Y-%m-%d').date()
            opi_date = datetime.strftime(format_opi_date, '%m-%d-%Y')
        else:
            opi_date = "None"
        wpt_score_id = (request.POST.get('wpt_score', False))
        if wpt_score_id != '':
            wpt_score = Scores.objects.get(pk=wpt_score_id)
            wpt_score = str(wpt_score)
        else:
            wpt_score = "None"
        raw_wpt_date = (request.POST.get('wpt_date', False))
        if raw_wpt_date != '':
            format_wpt_date = datetime.strptime(raw_wpt_date, '%Y-%m-%d').date()
            wpt_date = datetime.strftime(format_wpt_date, '%m-%d-%Y')
        else:
            wpt_date = "None"
        alt_score_id = (request.POST.get('alt_score', False))
        if alt_score_id != '':
            alt_score = Scores.objects.get(pk=alt_score_id)
            alt_score = str(alt_score)
        else:
            alt_score = "None"
        raw_alt_date = (request.POST.get('alt_date', False))
        if raw_alt_date != '':
            format_alt_date = datetime.strptime(raw_alt_date, '%Y-%m-%d').date()
            alt_date = datetime.strftime(format_alt_date, '%m-%d-%Y')
        else:
            alt_date = "None"
        art_score_id = (request.POST.get('art_score', False))
        if art_score_id != '':
            art_score = Scores.objects.get(pk=art_score_id)
            art_score = str(art_score)
        else:
            art_score = "None"
        raw_art_date = (request.POST.get('art_date', False))
        if raw_art_date != '':
            format_art_date = datetime.strptime(raw_art_date, '%Y-%m-%d').date()
            art_date = datetime.strftime(format_art_date, '%m-%d-%Y')
        else:
            art_date = "None"
        other_test_name = (request.POST.get('other_test_name', 'None'))
        other_test_score = (request.POST.get('other_test_score', 'None'))
        raw_other_test_date = (request.POST.get('other_test_date', 'None'))
        if raw_other_test_date != '':
            format_other_test_date = datetime.strptime(raw_other_test_date, '%Y-%m-%d').date()
            other_test_date = datetime.strftime(format_other_test_date, '%m-%d-%Y')
        else:
            other_test_date = "None"
        institution_name = (request.POST.get('institution_name', 'None'))
        if institution_name == '':
            institution_name = "None"
        institution_location = (request.POST.get('institution_location', 'None'))
        if institution_location == '':
            institution_location = "None"
        raw_institution_from_date = (request.POST.get('institution_from_date', 'None'))
        if raw_institution_from_date != '':
            format_institution_from_date = datetime.strptime(raw_institution_from_date, '%Y-%m-%d').date()
            institution_from_date = datetime.strftime(format_institution_from_date, '%m-%d-%Y')
        else:
            institution_from_date = "None"
        raw_institution_to_date = (request.POST.get('institution_to_date', 'None'))
        if raw_institution_to_date != '':
            format_institution_to_date = datetime.strptime(raw_institution_to_date, '%Y-%m-%d').date()
            institution_to_date = datetime.strftime(format_institution_to_date, '%m-%d-%Y')
        else:
            institution_to_date = "None"
        degree_id = (request.POST.get('degree', False))
        if degree_id != '':
            degree = Degrees.objects.get(pk=degree_id)
            degree = str(degree)
        else:
            degree = "None"
        raw_graduation_date = (request.POST.get('graduation_date', False))
        if raw_graduation_date != '':
            format_graduation_date = datetime.strptime(raw_graduation_date, '%Y-%m-%d').date()
            graduation_date = datetime.strftime(format_graduation_date, '%m-%d-%Y')
        else:
            graduation_date = "None"
        recommender_name_1 = (request.POST.get('recommender_name_1', False))
        recommender_title_1 = (request.POST.get('recommender_title_1', False))
        recommender_institution_1 = (request.POST.get('recommender_institution_1', False))
        recommender_email_1 = (request.POST.get('recommender_email_1', False))
        recommender_phone_1 = (request.POST.get('recommender_phone_1', False))

        recommender_name_2 = (request.POST.get('recommender_name_2', False))
        recommender_title_2 = (request.POST.get('recommender_title_2', False))
        recommender_institution_2 = (request.POST.get('recommender_institution_2', False))
        recommender_email_2 = (request.POST.get('recommender_email_2', False))
        recommender_phone_2 = (request.POST.get('recommender_phone_2', False))
        student_signature = (request.POST.get('student_signature', False))
        raw_signature_date = (request.POST.get('student_date', False))
        format_signature_date = datetime.strptime(raw_signature_date, '%Y-%m-%d').date()
        signature_date = datetime.strftime(format_signature_date, '%m-%d-%Y')
        location_of_experience = (request.POST.get('location_of_experience', False))

        statement_of_purpose = request.FILES['statement_of_purpose']

        client = box_api.create_client()
        box_api.create_mapl_application(firstname=firstname, middlename=middlename, lastname=lastname, byuid=byuid, email=email, phone=phone, major=major, heard_about=heard_about, semester_of_entry=semester_of_entry, academic_status=academic_status, gpa=gpa, opi_score=opi_score, opi_date=opi_date, wpt_score=wpt_score, wpt_date=wpt_date, alt_score=alt_score, alt_date=alt_date, art_score=art_score, art_date=art_date, other_test_name=other_test_name, other_test_score=other_test_score, other_test_date=other_test_date, institution_name=institution_name, institution_location=institution_location, institution_from_date=institution_from_date, institution_to_date=institution_to_date, degree=degree, graduation_date=graduation_date, recommender_name_1=recommender_name_1, recommender_title_1=recommender_title_1, recommender_institution_1=recommender_institution_1, recommender_email_1=recommender_email_1, recommender_phone_1=recommender_phone_1, recommender_name_2=recommender_name_2, recommender_title_2=recommender_title_2, recommender_institution_2=recommender_institution_2, recommender_email_2=recommender_email_2, recommender_phone_2=recommender_phone_2, student_signature=student_signature, signature_date=signature_date, location_of_experience=location_of_experience)
        mapl_folder = '219592459094'
        student_name = firstname + ' ' + lastname

        FileSystemStorage(location="/tmp").save(statement_of_purpose.name, statement_of_purpose)
        files = []
        files.append("/tmp/" + statement_of_purpose.name)
        files.append("/tmp/" + f"{firstname} {lastname} MAPL Application.pdf")
        box_api.upload_files(client=client, student_name=student_name, files=files, slat_folder=mapl_folder)        
        #region
        # finished_date = datetime.strptime(request.POST['testdate1'], '%Y-%m-%d')

        # sqldb_testdate1 = (request.POST.get('testdate1'))
        # format_testdate1 = datetime.strptime(sqldb_testdate1, '%Y-%m-%d').date()
        # testdate1 = datetime.strftime(format_testdate1, '%m-%d-%Y')
        
        # finished_date_2 = datetime.strptime(request.POST['testdate2'], '%Y-%m-%d')

        # sqldb_testdate2 = (request.POST.get('testdate2'))
        # format_testdate2 = datetime.strptime(sqldb_testdate2, '%Y-%m-%d').date()
        # testdate2 = datetime.strftime(format_testdate2, '%m-%d-%Y')
        # endregion
        
        success = "Thank you for your submission!"
        return HttpResponse(success)

        
    else:
        form = MAPLForm_Forms()
        heard_about = HeardAbout.objects.all()
        semester_of_entry = SemesterOfEntry.objects.all()
        scores = Scores.objects.all()
        academic_status = AcademicStatus.objects.all()

        context = {'form': form, 
                heard_about: 'heard_about',
                semester_of_entry: 'semester_of_entry',
                scores: 'scores',
                academic_status: 'academic_status'
                }
    
        return render(request, 'mapl_form.html', context)