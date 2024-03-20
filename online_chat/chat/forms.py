from django import forms
from .models import *


class CreateGroupForm(forms.ModelForm):
    group_photo = forms.ImageField(required=False)
    group_name = forms.CharField()
    
    class Meta:
        model = ChatMessage3
        fields = (
            "group_photo",
            "group_name"
        )
        