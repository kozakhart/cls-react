from django import forms
from .models import MAPLForm

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
        self.fields['coursework_explanation'].required = False
        self.fields['graduation_date'].required = False

    class Meta:
        model = MAPLForm
        fields = ('firstname', 'middlename', 'lastname', 'language', 'email', 'byuid', 'phone', 'major', 'heard_about', 
                  'semester_of_entry', 'gpa', 'location_of_experience', 'opi_score', 'opi_date', 'wpt_score', 'wpt_date', 
                  'alt_score', 'alt_date', 'art_score', 'art_date', 'other_test_name', 'other_test_score', 'other_test_date', 
                  'institution_name', 'institution_location', 'institution_from_date', 'institution_to_date', 'degree', 
                  'bachelors_completion', 'coursework_explanation',
                  'graduation_date', 'recommender_name_1', 'recommender_title_1', 'recommender_institution_1', 
                  'recommender_email_1', 'recommender_phone_1', 'recommender_name_2', 'recommender_title_2', 
                  'recommender_institution_2', 'recommender_email_2', 'recommender_phone_2', 'statement_of_purpose', 
                  'student_signature', 'student_date', 'academic_status')
        labels = {'firstname':'', 'middlename':'', 'lastname':'', 'language':'', 'email':'', 'byuid':'', 'phone':'', 
                  'major':'', 'heard_about':'', 'semester_of_entry':'', 'gpa':'', 'location_of_experience':'', 'opi_score':'', 
                  'opi_date':'', 'wpt_score':'', 'wpt_date':'', 'alt_score':'', 'alt_date':'', 'art_score':'', 'art_date':'', 
                  'other_test_name':'', 'other_test_score':'', 'other_test_date':'', 'institution_name':'', 'institution_location':'', 
                  'institution_from_date':'', 'institution_to_date':'', 'degree':'', 'bachelors_completion':'', 'coursework_explanation':'',
                  'graduation_date':'', 'recommender_name_1':'', 'recommender_title_1':'', 'recommender_institution_1':'', 
                  'recommender_email_1':'', 'recommender_phone_1':'', 'recommender_name_2':'', 'recommender_title_2':'', 
                  'recommender_institution_2':'', 'recommender_email_2':'', 'recommender_phone_2':'', 'statement_of_purpose':'', 
                  'student_signature':'', 'student_date':'', 'academic_status':''}
        widgets = {
            'firstname': forms.TextInput(attrs={'class':'formbox, input-class', 'placeholder': 'First Name', 'name':'firstname'}),
            'middlename': forms.TextInput(attrs={'class':'formbox, input-class', 'placeholder': 'Middle Name', 'name':'middlename'}),
            'lastname': forms.TextInput(attrs={'class':'formbox, input-class', 'placeholder': 'Last Name', 'name':'lastname'}),
            'language': forms.Select(attrs={'class':'formbox, input-class', 'placeholder': 'What language are you taking?', 'name':'language'}),
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
            'bachelors_completion': forms.Select(attrs={'class':'formbox, input-class', 'placeholder': "Will you have all of your coursework for your Bachelor's degree completed before beginning the MAPL program?", 'name':'bachelors_completion'}),
            'coursework_explanation': forms.TextInput(attrs={'class':'formbox, input-class', 'default':'NA', 'placeholder': "Coursework to finish", 'name':'coursework_explanation'}),
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