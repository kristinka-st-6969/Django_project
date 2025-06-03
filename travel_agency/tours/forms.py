from django import forms
from .models import Booking
from datetime import date

class BookingForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        }),
        label='Дата начала тура',
        initial=date.today,
    )

    persons = forms.ChoiceField(
        choices=[
            (1, '1 человек'),
            (2, '2 человека'),
            (3, '3 человека'),
            (4, '4 человека'),
            (5, '5 человек'),
            (6, '6 человек')
        ],
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Количество человек'
    )

    class Meta:
        model = Booking
        fields = ['date', 'persons']
