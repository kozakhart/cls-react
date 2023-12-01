from django import forms
from django.contrib.auth.models import User
from django.shortcuts import render
from .models import OPIForm, SLATForm, MAPLForm
from datetime import datetime, date, time, timedelta
from calendar import TUESDAY

class SLATForm_Forms(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        today = date.today()
        model = SLATForm

        fields = ('firstname', 'lastname', 'byuid', 'language', 'thesis',
                'transcript', 'opi')
        labels = {
            'firstname':'', 'lastname':'', 'byuid':'', 'language':'', 'thesis':'',
                'transcript':'', 'opi':''
        }
        widgets = {
            'firstname': forms.TextInput(attrs={'class':'formbox, input-class', 'placeholder': 'First Name', 'name':'firstname'}),
            'lastname': forms.TextInput(attrs={'class':'formbox, input-class', 'placeholder': 'Last Name', 'name':'lastname'}),
            'byuid': forms.TextInput(attrs={'class':'formbox, input-class', 'placeholder': 'BYU ID','minlength': '9', 'name':'byuid' }),
            'language': forms.Select(attrs={'class':'formbox, input-class','placeholder': '', 'name':'language'}),
            'thesis' : forms.DateInput(attrs={'type': 'date', 'class': 'formbox, input-class', 'min': today, 'name':'thesis'}),
            'transcript' : forms.ClearableFileInput(attrs={'type':'file', 'class':'formbox, input-class, file-input','id':'transcript', 'name':'transcript'}),
            'opi' : forms.ClearableFileInput(attrs={'type':'file', 'class':'formbox, input-class, file-input', 'id':'opi', 'name':'opi'}),
        }
        
class MAPLForm_Forms(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['middlename'].required = False
        self.fields['opi_score'].required = False
        self.fields['opi_date'].required = False
        self.fields['wpt_score'].required = False
        self.fields['wpt_date'].required = False
        self.fields['alt_score'].required = False
        self.fields['alt_date'].required = False
        self.fields['art_score'].required = False
        self.fields['art_date'].required = False
        self.fields['other_test_name'].required = False
        self.fields['other_test_score'].required = False
        self.fields['other_test_date'].required = False
        self.fields['institution_name'].required = False
        self.fields['institution_location'].required = False
        self.fields['institution_from_date'].required = False
        self.fields['institution_to_date'].required = False
        self.fields['degree'].required = False
        self.fields['graduation_date'].required = False

    class Meta:
        model = MAPLForm
        fields = ('firstname', 'middlename', 'lastname', 'email', 'byuid', 'phone', 'major', 'heard_about', 'semester_of_entry', 'gpa', 'location_of_experience', 'opi_score', 'opi_date', 'wpt_score', 'wpt_date', 'alt_score', 'alt_date', 'art_score', 'art_date', 'other_test_name', 'other_test_score', 'other_test_date', 'institution_name', 'institution_location', 'institution_from_date', 'institution_to_date', 'degree', 'graduation_date', 'recommender_name_1', 'recommender_title_1', 'recommender_institution_1', 'recommender_email_1', 'recommender_phone_1', 'recommender_name_2', 'recommender_title_2', 'recommender_institution_2', 'recommender_email_2', 'recommender_phone_2', 'statement_of_purpose', 'student_signature', 'student_date', 'academic_status')
        labels = {'firstname':'', 'middlename':'', 'lastname':'', 'email':'', 'byuid':'', 'phone':'', 'major':'', 'heard_about':'', 'semester_of_entry':'', 'gpa':'', 'location_of_experience':'', 'opi_score':'', 'opi_date':'', 'wpt_score':'', 'wpt_date':'', 'alt_score':'', 'alt_date':'', 'art_score':'', 'art_date':'', 'other_test_name':'', 'other_test_score':'', 'other_test_date':'', 'institution_name':'', 'institution_location':'', 'institution_from_date':'', 'institution_to_date':'', 'degree':'', 'graduation_date':'', 'recommender_name_1':'', 'recommender_title_1':'', 'recommender_institution_1':'', 'recommender_email_1':'', 'recommender_phone_1':'', 'recommender_name_2':'', 'recommender_title_2':'', 'recommender_institution_2':'', 'recommender_email_2':'', 'recommender_phone_2':'', 'statement_of_purpose':'', 'student_signature':'', 'student_date':'', 'academic_status':''}
        widgets = {
            'firstname': forms.TextInput(attrs={'class':'formbox, input-class', 'placeholder': 'First Name', 'name':'firstname'}),
            'middlename': forms.TextInput(attrs={'class':'formbox, input-class', 'placeholder': 'Middle Name', 'name':'middlename'}),
            'lastname': forms.TextInput(attrs={'class':'formbox, input-class', 'placeholder': 'Last Name', 'name':'lastname'}),
            'email': forms.TextInput(attrs={'class':'formbox, input-class', 'placeholder': 'Email', 'name':'email'}),
            'byuid': forms.TextInput(attrs={'class':'formbox, input-class', 'placeholder': 'BYU ID', 'name':'byuid'}),
            'phone': forms.TextInput(attrs={'class':'formbox, input-class', 'placeholder': 'Phone', 'name':'phone'}),
            'major': forms.TextInput(attrs={'class':'formbox, input-class', 'placeholder': 'Major', 'name':'major'}),
            'heard_about': forms.Select(attrs={'class':'formbox, input-class', 'placeholder': 'How did you hear about MAPL?', 'name':'heard_about'}),
            'semester_of_entry': forms.Select(attrs={'class':'formbox, input-class', 'placeholder': 'Semester of Entry', 'name':'semester_of_entry'}),
            'gpa': forms.TextInput(attrs={'class':'formbox, input-class', 'placeholder': 'GPA', 'name':'gpa'}),
            'location_of_experience': forms.Textarea(attrs={'class':'formbox, input-class', 'placeholder': 'Please Describe', 'name':'location_of_experience'}),
            'opi_score': forms.Select(attrs={'class':'formbox, input-class', 'placeholder': 'OPI Score', 'name':'opi_score'}),
            'opi_date': forms.DateInput(attrs={'type':'date', 'class':'formbox, input-class', 'placeholder': 'Date', 'name':'opi_date'}),
            'wpt_score': forms.Select(attrs={'class':'formbox, input-class', 'placeholder': 'WPT Score', 'name':'wpt_score'}),
            'wpt_date': forms.DateInput(attrs={'type':'date', 'class':'formbox, input-class', 'placeholder': 'Date', 'name':'wpt_date'}),
            'alt_score': forms.Select(attrs={'class':'formbox, input-class', 'placeholder': 'ALT Score', 'name':'alt_score'}),
            'alt_date': forms.DateInput(attrs={'type':'date', 'class':'formbox, input-class', 'placeholder': 'Date', 'name':'alt_date'}),
            'art_score': forms.Select(attrs={'class':'formbox, input-class', 'placeholder': 'ART Score', 'name':'art_score'}),
            'art_date': forms.DateInput(attrs={'type':'date', 'class':'formbox, input-class', 'placeholder': 'Date', 'name':'art_date'}),
            'other_test_name': forms.TextInput(attrs={'class':'formbox, input-class', 'placeholder': 'Other Test Name', 'name':'other_test_name'}),
            'other_test_score': forms.TextInput(attrs={'class':'formbox, input-class', 'placeholder': 'Other Test Score', 'name':'other_test_score'}),
            'other_test_date': forms.DateInput(attrs={'type':'date', 'class':'formbox, input-class', 'placeholder': 'Date', 'name':'other_test_date'}),
            'institution_name': forms.TextInput(attrs={'class':'formbox, input-class', 'placeholder': 'Institution Name', 'name':'institution_name'}),
            'institution_location': forms.TextInput(attrs={'class':'formbox, input-class', 'placeholder': 'Institution Location', 'name':'institution_location'}),
            'institution_from_date': forms.DateInput(attrs={'type':'date', 'class':'formbox, input-class', 'placeholder': 'From', 'name':'institution_from_date'}),
            'institution_to_date': forms.DateInput(attrs={'type':'date', 'class':'formbox, input-class', 'placeholder': 'To', 'name':'institution_to_date'}),
            'degree': forms.Select(attrs={'class':'formbox, input-class', 'placeholder': 'Degree', 'name':'degree'}),
            'graduation_date': forms.DateInput(attrs={'type':'date', 'class':'formbox, input-class', 'placeholder': 'Graduation Date', 'name':'graduation_date'}),
            'recommender_name_1': forms.TextInput(attrs={'class':'formbox, input-class', 'placeholder': 'Recommender Name', 'name':'recommender_name_1'}),
            'recommender_title_1': forms.TextInput(attrs={'class':'formbox, input-class', 'placeholder': 'Title', 'name':'recommender_title_1'}),
            'recommender_institution_1': forms.TextInput(attrs={'class':'formbox, input-class', 'placeholder': 'Institution', 'name':'recommender_institution_1'}),
            'recommender_email_1': forms.TextInput(attrs={'class':'formbox, input-class', 'placeholder': 'Email', 'name':'recommender_email_1'}),
            'recommender_phone_1': forms.TextInput(attrs={'class':'formbox, input-class', 'placeholder': 'Phone', 'name':'recommender_phone_1'}),
            'recommender_name_2': forms.TextInput(attrs={'class':'formbox, input-class', 'placeholder': 'Recommender Name', 'name':'recommender_name_2'}),
            'recommender_title_2': forms.TextInput(attrs={'class':'formbox, input-class', 'placeholder': 'Title', 'name':'recommender_title_2'}),
            'recommender_institution_2': forms.TextInput(attrs={'class':'formbox, input-class', 'placeholder': 'Institution', 'name':'recommender_institution_2'}),
            'recommender_email_2': forms.TextInput(attrs={'class':'formbox, input-class', 'placeholder': 'Email', 'name':'recommender_email_2'}),
            'recommender_phone_2': forms.TextInput(attrs={'class':'formbox, input-class', 'placeholder': 'Phone', 'name':'recommender_phone_2'}),
            'statement_of_purpose': forms.ClearableFileInput(attrs={'type':'file', 'class':'formbox, input-class, file-input', 'id':'statement_of_purpose', 'name':'statement_of_purpose'}),
            'student_signature': forms.TextInput(attrs={'class':'formbox, input-class', 'placeholder': 'Student Signature', 'name':'student_signature'}),
            'student_date': forms.DateInput(attrs={'type':'date', 'class':'formbox, input-class', 'placeholder': 'Date', 'name':'student_date'}),
            'academic_status': forms.Select(attrs={'class':'formbox, input-class', 'placeholder': 'Academic Status', 'name':'academic_status'}),
        }
class OPIForm_Forms(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['agree'].required = True
        self.fields['language_other'].required = False
        self.fields['cannot_come'].required = False
        self.fields['reason_other'].required = False

    class Meta:

        today = date.today()
        one_week = today + timedelta(days=7)
        two_weeks = today + timedelta(days=14)
        model = OPIForm

        fields = ('agree', 'firstname', 'lastname', 'byuid', 'netid',
        'email', 'reason', 'reason_other', 'language',
        'language_other', 'experience', 'major', 'second_major',
        'minor', 'scores', 'come_to_campus',
        'cannot_come', 'testdate1', 'time1', 'time2',
        'testdate2', 'time3', 'time4', 'CertificateStatus', 'phone')
        labels = {
        'agree':'*I agree to the OPI Assessment Agreement as defined above.', 'firstname':'', 'lastname': "", 'byuid': "", 'netid': "",
        'email': "", 'reason': "", 'reason_other':"", 'language':"",
        'language_other': "", 'experience': "", 'major': "", 'second_major': "",
        'minor': "", 'scores':"", 'come_to_campus':"",
        'cannot_come': "", 'testdate1': "", 'time1': '', 'time2': "",
        'testdate2': "", 'time3':"", 'time4':"", 'CertificateStatus': "", 'phone':""
        }
        
        widgets = {
            'agree': forms.CheckboxInput(attrs={'class':'formbox, agree', 'name':'agree'}),
            'firstname': forms.TextInput(attrs={'class':'formbox, input-class', 'placeholder': 'First Name', 'name':'firstname'}),
            'lastname': forms.TextInput(attrs={'class':'formbox, input-class', 'placeholder': 'Last Name', 'name':'lastname'}),
            'byuid': forms.TextInput(attrs={'class':'formbox, input-class', 'placeholder': 'BYU ID','minlength': '9', 'name':'byuid' }),
            'netid': forms.TextInput(attrs={'class':'formbox, input-class', 'placeholder': "BYU Net ID", 'name':'netid'}),
            'email': forms.TextInput(attrs={'class':'formbox, input-class', 'placeholder': 'Email', 'name':'email'}),
            'reason': forms.Select(attrs={'class':'fopythormbox, input-class', 'placeholder': '', 'name':'reason'}),
            'reason_other': forms.TextInput(attrs={'class':'formbox, input-class', 'placeholder': 'Category', 'name':'reason_other'}),
            'language': forms.Select(attrs={'class':'formbox, input-class','placeholder': '', 'name':'language'}),
            'language_other' : forms.TextInput(attrs={'class':'formbox, input-class', 'placeholder': '', 'name':'language_other', 'required':'False'}),
            'experience': forms.Select(attrs={'class':'formbox, input-class', 'placeholder': '', 'name':'experience'}),
            'major' : forms.TextInput(attrs={'class':'formbox, input-class', 'placeholder': 'Major', 'name':'major'}),
            'second_major' : forms.TextInput(attrs={'class':'formbox, input-class', 'placeholder': 'Second Major', 'name':'second_major'}),
            'minor' : forms.TextInput(attrs={'class':'formbox, input-class', 'placeholder': 'Minor', 'name':'minor'}),
            'scores': forms.Select(attrs={'class':'formbox, input-class', 'placeholder': '', 'name':'scores'}),
            'come_to_campus': forms.Select(attrs={'class':'formbox, input-class', 'placeholder': '', 'name':'come_to_campus'}),
            'cannot_come': forms.Select(attrs={'class':'formbox, input-class', 'placeholder': '', 'name':'cannot_come', 'required':'False'}),
            'testdate1' : forms.DateInput(attrs={'type': 'date', 'class': 'formbox, input-class', 'min': one_week, 'name':'testdate1'}),
            'time1': forms.TimeInput(attrs={'class':'formbox, input-class', 'type': 'time', 'min' : '08:00', 'max' : '17:00', 'step' : '900', 'autocomplete': 'on', 'value': '12:00', 'name':'time1'}),
            'time2': forms.TimeInput(attrs={'class':'formbox, input-class', 'type': 'time', 'min' : '08:00', 'max' : '17:00', 'step' : '900', 'autocomplete': 'on', 'value': '15:00', 'name':'time2'}),
            'testdate2': forms.DateInput(attrs={'type': 'date','class':'formbox, input-class', 'min': two_weeks, 'name':'testdate2'}),
            'time3': forms.TimeInput(attrs={'class':'formbox, input-class', 'type': 'time', 'min' : '08:00', 'max' : '17:00', 'step' : '900', 'autocomplete': 'on', 'value': '12:00', 'name':'time3'}),
            'time4': forms.TimeInput(attrs={'class':'formbox, input-class', 'type': 'time', 'min' : '08:00', 'max' : '17:00', 'step' : '900', 'autocomplete': 'on', 'value': '15:00', 'name':'time4'}),
            'CertificateStatus': forms.TextInput(attrs={'class':'formbox, input-class', 'placeholder': 'Email', 'name':'CertificateStatus'}),
            'phone': forms.TextInput(attrs={'class':'formbox, input-class', 'placeholder': 'Phone Number', 'name':'phone'}),
      
        }