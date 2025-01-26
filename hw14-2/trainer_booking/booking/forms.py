from django import forms
from .models import *


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['service', 'datetime_start', 'datetime_end']