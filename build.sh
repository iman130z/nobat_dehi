#!/bin/bash
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
echo "from django.contrib.auth import get_user_model; user = get_user_model(); user.objects.create_superuser('sina', 'sinakhammar@gmail.com', 'sina1234')" | python manage.py shell