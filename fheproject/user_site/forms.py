from django import forms
from django.forms import ModelForm
from .models import InsuranceData
from django.core import validators


class InsuranceForm(ModelForm):
    
    secret_key_file = forms.FileField(label='Upload Secret Key')

    class Meta:
        model = InsuranceData

        fields = "__all__"

        exclude = ['user', 'approved', 'name_convention']  # Excluding certain field from the form


    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # Pop the request from kwargs
        super(InsuranceForm, self).__init__(*args, **kwargs)
        self.fields['email'].validators.append(
        validators.RegexValidator(
            regex=r'^[a-zA-Z0-9_.+-]+@(?:[a-zA-Z0-9-]+\.)*(?:gmail|outlook|hotmail|yahoo)\.(?:com|org|net)$',
            message='Please enter a valid email address from Gmail, Outlook, Hotmail, or Yahoo.',
            )
        )   


    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.request.user  # Set the user to the logged-in user
        instance.name_convention = str(self.request.user) + str(instance.name_convention) # Setting name convention
        if commit:
            instance.save()
        return instance
    

class DecryptForm(forms.Form):
    secret_key_file = forms.FileField(label='Upload Secret Key')