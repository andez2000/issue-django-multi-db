# Getting Started

We begin with an empty folder that is opened up in VSCode.

## Create and activate venv

Open the terminal window and execute the following command:

```console
py -m venv venv
venv\scripts\activate
```

Activating the venv set up your shell to use the environment's Python executable and its site-packages by default.

## Install Django

From the venv prompt:

```console
pip install django
```

## Create new project

From the venv prompt:

```console
django-admin startproject core .
```

This creates a new core folder with the following files:

1. \__init\__.py
2. asgi.py
3. settings.py
4. urls.py
5. wsgi.pi

## Create new application

From the venv prompt:

```console
py manage.py startapp acmeapp
```

This creates an `acmeapp` folder in the root of the project with the following files:

1. \__init.py\__
2. admin.py
3. apps.py
4. models.py
5. tests.py
6. views.py

## Update settings

Add `acmeapp` to `settings.INSTALLED_APPS`.

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'acmeapp'
]
```

## Links

[Django Testing - Introduction to testing in Django - Django Testing Series Part 1](https://www.youtube.com/watch?v=swEjbCW9XDY).  

