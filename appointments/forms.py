# -*- coding: utf-8 -*-


from django import forms
from .models import Appointment
import jdatetime

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient_name', 'patient_phone', 'date', 'time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'hidden'}),  # مخفی
            'time': forms.Select(attrs={'class': 'form-control'}),  # انتخاب‌گر
            'patient_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'مثال: علی رضایی'}),
            'patient_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'مثال: ۰۹۱۲۳۴۵۶۷۸۹'}),
        }
        labels = {
            'patient_name': 'نام بیمار',
            'patient_phone': 'شماره تلفن',
            'date': 'تاریخ',
            'time': 'ساعت',
        }
