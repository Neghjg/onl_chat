from django import forms
from .models import *


class CreateGroupForm(forms.Form):
    group_photo = forms.ImageField(required=False)
    group_name = forms.CharField()