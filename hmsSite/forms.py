from django import forms
from hmsSite.models import Project
from datetime import date
from django.core.validators import RegexValidator


class DateInput(forms.DateInput):
    input_type = 'date'
    attrs = {'min' : date.today().strftime("%Y-%M-%D")}

class ProjectSubmissionForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        exclude = [ 'approved' , 'image_thumbnail' , 'user' , 'last_reminder' , 'email_sent']
        widgets = {
            'start_date' : DateInput(),
            'end_date' : DateInput()
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['contact1_url'].label = "<a href=\"https://research-repository.uwa.edu.au/\" target=\"_blank\">Research Repositry URL<a/>"
        self.fields['contact2_url'].label = "<div class= \"url2\"> <a href=\"https://research-repository.uwa.edu.au/\" target=\"_blank\">Research Repositry URL<a/></div>"


class PhemeLoginForm(forms.Form):
    number_regex = RegexValidator(regex=r'^\d{8}$', message="Invalid UWA staff or student ID number")
    pheme_number = forms.CharField(label="Your UWA staff or student ID number")
    password = forms.CharField(widget=forms.PasswordInput(), label="Your Pheme password")

class StillRelevantForm(forms.Form):
    still_relevant = forms.BooleanField(required=False, label="Continue project")
    not_relevant = forms.BooleanField(required=False, label="Archive project")
    edit = forms.BooleanField(required=False, label="Edit project now")