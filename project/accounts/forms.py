from django import forms
from .models import User, Profile
from django.contrib.auth.forms import UserCreationForm
CHOICES = (
    ("m", "Male"),
    ("f", "Female"),
)


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={ 'class' : 'form-control signin-up', 'placeholder' : 'Email Address' }))
    firstName = forms.CharField(label="", widget=forms.TextInput(attrs={ 'class' : 'form-control signin-up ', 'placeholder' : 'Name' }), required=False)
    lastName = forms.CharField(label="", widget=forms.TextInput(attrs={ 'class' : 'form-control signin-up', 'placeholder' : 'Last Name' }), required=False)
    gender = forms.ChoiceField(label='', widget=forms.RadioSelect(), choices=CHOICES)
    location = forms.CharField(label="", widget=forms.TextInput(attrs={ 'class' : 'form-control signin-up', 'placeholder' : 'Location' }), required=False)
    birthday = forms.DateField(label="", widget=forms.DateInput(attrs={ 'class' : 'form-control',
                                                                        'type' : "date",
                                                                        'placeholder' : 'Birthday'
                                                     }, format=('%Y-%m-%d')), required=False)
    class Meta:
        model = User
        exclude =('createdDate', 'last_login', 'is_superuser', 'groups',
                  'user_permissions', 'is_staff',
                  'is_active', 'date_joined', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({'class' : 'form-control', 'placeholder' : 'Enter username'})
        self.fields['username'].label = ''

        self.fields['password1'].widget.attrs = {'class' : 'form-control', 'placeholder' : 'Enter password'}
        self.fields['password1'].label = ''

        self.fields['password2'].widget.attrs = {'class' : 'form-control', 'placeholder' : 'Enter password'}
        self.fields['password2'].label = ''

    def clean_username(self):
        username = self.cleaned_data['username']
        if ' ' in username:
            raise forms.ValidationError("Usename can't contain spaces")
        return username

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        if commit:
            user.save()
        return user



class ProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(label="Enter you profile picture", required=False)
    bio = forms.CharField(label="", widget=forms.Textarea(attrs={'class': 'form-control signin-up', 'placeholder': 'Your Bio'}), required=False)
    website_link = forms.URLField(label="", widget=forms.URLInput(attrs={'class': 'form-control signin-up', 'placeholder': 'Website URL'}), required=False)
    facebook_link = forms.URLField(label="", widget=forms.URLInput(attrs={'class': 'form-control signin-up', 'placeholder': 'Facebook URL'}), required=False)
    linkedin_link = forms.URLField(label="", widget=forms.URLInput(attrs={'class': 'form-control signin-up', 'placeholder': 'Linkedin URL'}), required= False)

    class Meta:
        model = Profile
        fields = ('profile_picture', 'bio', 'website_link', 'facebook_link', 'linkedin_link')


class UserLoginForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput
    )

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.user = None
        self.fields['username'].widget.attrs.update({''})
        self.fields['password'].widget.attrs.update({''})


