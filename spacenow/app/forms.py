from django import forms
from django.forms import widgets
from django.contrib.auth.models import User

from app.models import Profile, News

class UserSignupForm(forms.ModelForm):
    class Meta:
        model = User       
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
        )


class UserSignupProfileform(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'about_me',
            'img_file',
        )

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = (
            'title',
            'index_body',
            'body',
            'img_file',
            'news_file',
        )

