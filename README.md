# simple_cloud_file_manager

This app seeks to create a simple cloud file manager using python,django, and a REST framework. It only provides the server-side REST service, the user interface is being developed in its own repository.


![](http://i.imgur.com/W0vRSh7.png)

## Django REST Boilerplate

Boilerplate for Django projects using Django REST Framework.

## Project Setup

Install required packages:
```
pip3 install -r requirements/local.txt
```

Initialize database:
```
python3 manage.py makemigrations
python3 manage.py migrate
```

## Fixtures

To load in sample data for all tables at once:
```
bash scripts/load_sample_data.sh
```

This will create an initial superuser account with the following credentials:
```
admin@email.com
pass1234
```
