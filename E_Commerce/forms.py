from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'password']

        # Meta widgets won't work, don't know
        # widgets = {'username': forms.EmailInput(attrs={'class': 'form-control'}),
        #            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        #            }


class SignUpForm(UserCreationForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'class': "form-control"}))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        widgets = {'username': forms.TextInput(attrs={'class': 'form-control'}),
                   }

    def save(self, commit=True):
        user = super(SignUpForm,self).save(commit=False)
        name = user.username.split('@')
        user.first_name = name[0]
        user.email = user.username
        user.save()
        return user
