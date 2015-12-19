from django import forms
from bill.models import Booking,Service_order

class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking
        exclude = ['person','is_delete','price','company']

class ServiceOrderForm(forms.ModelForm):
    class Meta:
        model = Service_order
        exclude = ['person','is_delete','price']
