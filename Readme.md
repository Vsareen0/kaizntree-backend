# Instructions

Add these email values to send password verification email:

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''


Add these values for postgresql configurations

'ENGINE': 'django.db.backends.postgresql_psycopg2',
'NAME': '', # username
'USER' : '', # user
'PASSWORD' : '', # password
'HOST' : '', # host
'PORT' : '', #port


- Run python manage.py makemgrations users
- Run python manage.py migrate users
- Run python manage.py makemgrations inventory
- Run python manage.py migrate inventory
- Run python manage.py migrate

- Run python manage.py runserver
