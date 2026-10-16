from django import forms

from .models import car


class CarForm(forms.ModelForm):
    class Meta:
        model = car
        fields = ['car_name']
        labels = {'car_name': 'Car make'}
