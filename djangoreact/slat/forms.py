from django import forms
from .models import SLATForm
from datetime import date

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
        