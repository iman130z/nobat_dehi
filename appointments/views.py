# -*- coding: utf-8 -*-

import jdatetime
import datetime
from django.shortcuts import render, redirect
from .models import Appointment
from .forms import AppointmentForm
from django.contrib.auth.decorators import login_required



def home(request):
    all_appointments = Appointment.objects.all()
    for app in all_appointments:
        # تبدیل میلادی به شمسی برای نمایش
        shamsi = jdatetime.date.fromgregorian(date=app.date)
        app.shamsi_date = f"{shamsi.year}/{shamsi.month:02d}/{shamsi.day:02d}"
    return render(request, 'home.html', {'appointments': all_appointments})

# ساعت‌های کاری
WORKING_HOURS = ['09:00', '09:30', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30']

@login_required
def book_appointment(request):
    today = datetime.date.today()
    now = datetime.datetime.now().time()

    available_dates = []
    for i in range(7):
        day = today + datetime.timedelta(days=i)
        if day.weekday() != 5:
            available_dates.append(day)

    selected_date = None
    available_times = []

    if request.method == 'POST':
        # گرفتن داده‌ها از POST
        patient_name = request.POST.get('patient_name')
        patient_phone = request.POST.get('patient_phone')
        date_str = request.POST.get('date')
        time_str = request.POST.get('time')

        if patient_name and patient_phone and date_str and time_str:
            try:
                # تبدیل تاریخ شمسی به میلادی
                parts = date_str.split('/')
                if len(parts) == 3:
                    year, month, day = map(int, parts)
                    selected_date = jdatetime.date(year, month, day).togregorian()
                   
                    # ساخت نوبت جدید
                    appointment = Appointment(
                        user=request.user,
                        patient_name=patient_name,
                        patient_phone=patient_phone,
                        date=selected_date,
                        time=datetime.datetime.strptime(time_str, '%H:%M').time(),
                        is_done=False
                    )
                    appointment.save()
                    return redirect('home')
            except Exception as e:
                print(f"Error in POST: {e}")
                # اگر خطا بود، دوباره فرم رو نشون بده
                pass
        else:
            # اگر داده‌ها کامل نبود
            print("Data missing")
    else:
        date_str = request.GET.get('date')
        if date_str:
            try:
                parts = date_str.split('/')
                if len(parts) == 3:
                    year, month, day = map(int, parts)
                    selected_date = jdatetime.date(year, month, day).togregorian()
                   
                    booked_times = Appointment.objects.filter(date=selected_date).values_list('time', flat=True)
                    booked_times_str = [t.strftime('%H:%M') for t in booked_times]

                    for time in WORKING_HOURS:
                        if time not in booked_times_str:
                            hour = int(time.split(':')[0])
                            minute = int(time.split(':')[1])
                            time_obj = datetime.time(hour, minute)

                            if selected_date == today:
                                if time_obj > now:
                                    available_times.append(time)
                            else:
                                available_times.append(time)
            except Exception as e:
                print(f"Error in GET: {e}")

    available_dates_shamsi = []
    for d in available_dates:
        shamsi = jdatetime.date.fromgregorian(date=d)
        available_dates_shamsi.append({
            'date': d,
            'display': f"{shamsi.year}/{shamsi.month:02d}/{shamsi.day:02d}"
        })

    return render(request, 'book.html', {
        'available_dates': available_dates_shamsi,
        'selected_date': selected_date,
        'available_times': available_times,
        'WORKING_HOURS': WORKING_HOURS,
        'today': today,
    })

    # مقداردهی اولیه فرم با تاریخ شمسی
    initial_data = {}
    if selected_date:
        shamsi_selected = jdatetime.date.fromgregorian(date=selected_date)
        initial_data['shamsi_date'] = f"{shamsi_selected.year}/{shamsi_selected.month:02d}/{shamsi_selected.day:02d}"
   
    form = AppointmentForm(initial=initial_data)
    return render(request, 'book.html', {
        'form': form,
        'available_dates': available_dates_shamsi,
        'selected_date': selected_date,
        'available_times': available_times,
        'WORKING_HOURS': WORKING_HOURS,
        'today': today,
    })

    form = AppointmentForm(initial={'shamsi_date': selected_date.strftime('%Y/%m/%d')} if selected_date else {})
    return render(request, 'book.html', {
        'form': form,
        'available_dates': available_dates_shamsi,
        'selected_date': selected_date,
        'available_times': available_times,
        'WORKING_HOURS': WORKING_HOURS,
        'today': today,  # برای استفاده در template
    })

