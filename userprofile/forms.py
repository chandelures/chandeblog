from django import forms

from userprofile.models import User


class ProfileForm(forms.Form):
    class Meta:
        model = User
        fields = ['link', 'resume']
