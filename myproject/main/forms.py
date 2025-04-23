from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from .models import Reservation, Table, Review

User = get_user_model()

# main/forms.py
from django import forms
from .models import Reservation, Table
from django.utils import timezone
from datetime import time as dt_time

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['guests', 'date', 'time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, restaurant_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.restaurant_id = restaurant_id

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model  = User
        fields = ['username','email','password1','password2']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating','comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min':1,'max':5}),
            'comment': forms.Textarea(attrs={'rows':3}),
        }
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']

class UserEmailForm(forms.Form):
    email = forms.EmailField(label="Email", required=True)

class CustomPasswordChangeForm(PasswordChangeForm):
    # можно тут перекрасить лейблы, поменять виджеты и т.д.
    pass
