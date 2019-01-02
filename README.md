# SMS Registration using DRF

A working example of user registration using django rest framework

## Features

- Django 2.0+
- Uses [Pipenv](https://github.com/kennethreitz/pipenv) - the officially recommended Python packaging tool from Python.org.
- Development, Staging and Production settings with [django-configurations](https://django-configurations.readthedocs.org).
- Get value insight and debug information while on Development with [django-debug-toolbar](https://django-debug-toolbar.readthedocs.org).
- Collection of custom extensions with [django-extensions](http://django-extensions.readthedocs.org).
- HTTPS and other security related settings on Staging and Production.
- PostgreSQL database support with psycopg2.


## How to install
### Install PipEnv
Please visit [Pragmatic Installation of Pipenv](https://pipenv.readthedocs.io/en/latest/install/#pragmatic-installation-of-pipenv) for detailed instructions of PipEnv installation.

**note:** Use the pip version which matches the python version of your Pipfile:  


```bash
pip3 install pipenv
```

### Running the project for local development
Copy and paste the following bash commands in your terminal to run the project for local development:
 
```bash
git clone git@github.com:mohsen-mahmoodi/django-rest-framework-sms-registration.git
cd django-rest-framework-sms-registration.git
cp example.env .env
echo "Install requirements from Pipfile"
pipenv install --dev
echo "Run Django specific configuration and setup commands"
pipenv run python manage.py migrate
pipenv run python manage.py createsuperuser
echo "Start the project using the development server"
pipenv run python manage.py runserver
```
 
## How to test
A sample API call is included using POSTMAN collection in order to test the APIs 