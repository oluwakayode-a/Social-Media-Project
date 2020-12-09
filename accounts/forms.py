from django import forms
from allauth.account.forms import SignupForm
from .models import Profile, User

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user',]


# class InterestForm(forms.ModelForm):
#     class Meta:
#         model = Interest
#         fields = ('interests',)

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=100, label='First Name', required=True)
    last_name = forms.CharField(max_length=100, label='Last Name', required=True)

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user


class EditUser(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')