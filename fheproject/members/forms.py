from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from django.core import validators

ALLOWED_DOMAINS = ['gmail.com', 'outlook.com', 'hotmail.com', 'yahoo.com']


            # regex=r'^[a-zA-Z0-9._%+-]+@(?:[a-zA-Z0-9-]+\.)+(?:' + '|'.join(ALLOWED_DOMAINS) + r')\.com$',
            # regex=r'^[a-zA-Z0-9._%+-]+@(?:[a-zA-Z0-9-]+\.)+(?:' + '|'.join(ALLOWED_DOMAINS) + r')\.[a-zA-Z]{2,}$',

class RegisterUserForm(UserCreationForm):

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class':'form-control'}),
        validators=[validators.RegexValidator(
            regex=r'^[a-zA-Z0-9_.+-]+@(?:[a-zA-Z0-9-]+\.)*(?:gmail|outlook|hotmail|yahoo)\.(?:com|org|net)$',
            message='Please enter a valid email address from Gmail, Outlook, Hotmail, or Yahoo.',
        )]
    )

    # email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = User

        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'