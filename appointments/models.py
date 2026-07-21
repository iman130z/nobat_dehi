# -*- coding: cp1256 -*-


from django.db import models
from django.contrib.auth.models import User

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # کاربر ثبت‌کننده
    patient_name = models.CharField(max_length=100)
    patient_phone = models.CharField(max_length=11)
    date = models.DateField()
    time = models.TimeField()
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.patient_name} - {self.date} {self.time}"
