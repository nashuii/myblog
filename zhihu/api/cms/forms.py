from django import forms
from utils.captcha.mycaptcha import Captcha
import json

class LoginForm(forms.Form):
    username = forms.CharField(max_length=10, min_length=4)
    password = forms.CharField(max_length=16, min_length=6)
    captcha = forms.CharField(max_length=4, min_length=4)
    remember = forms.BooleanField(required=False)

    def clean_captcha(self):
        captcha = self.cleaned_data.get('captcha', None)
        if not Captcha.check_captcha(captcha):
            raise forms.ValidationError('验证码错误')
        return captcha

class Register(forms.Form):
    username = forms.CharField(max_length = 10,min_length = 4)
    password = forms.CharField(max_length = 16,min_length = 6)
    email = forms.EmailField(required = True)

class AddarticleForm(forms.Form):
    title = forms.CharField(max_length = 200)
    category = forms.IntegerField(required = True)
    desc = forms.CharField(max_length = 200, required = False)
    thumbnail = forms.URLField(max_length = 100, required = False)
    content_html = forms.CharField()

class AddtagForm(forms.Form):
    tagname = forms.CharField(max_length=20)

class AddCategoryForm(forms.Form):
    categoryname = forms.CharField(max_length=20)

class UpdateProfileForm(forms.Form):
    username = forms.CharField(min_length=4, max_length=10,required=False)
    avatar = forms.URLField(max_length=200, required=False)

class UpdateEmailForm(forms.Form):
    email = forms.EmailField(required=True)