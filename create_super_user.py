import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mytodolist.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()
super_user = User(username='admin', email='admin@example.com')
super_user.set_password('veryStrongPassword123')
super_user.is_superuser = True
super_user.is_staff = True
super_user.save()
