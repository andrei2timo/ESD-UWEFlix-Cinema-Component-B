# ESD-UWEFlix-Cinema-Component-B

By: <br>
[![Developers Tag]( https://img.shields.io/badge/Developer-andrei2timo-blue.svg )]( https://github.com/andrei2timo ) <br>
[![Developers Tag]( https://img.shields.io/badge/Developer-alamerton-blue.svg )]( https://github.com/alamerton )<br>
[![Developers Tag]( https://img.shields.io/badge/Developer-snayak-blue.svg )]( https://github.com/Hyperoid29 )<br>
[![Developers Tag]( https://img.shields.io/badge/Developer-ChristianECDawson-blue.svg )]( https://github.com/ChristianECDawson )<br>
The UWEFlix website is developed using a Django virtual environment, and is intended to replace the existing paper system.

## Installation instructions - Linux
```
$ git clone git@github.com:andrei2timo/ESD-UWEFlix-Cinema-Component-B.git
$ cd Cinema-System-ESD-Component B/UWEFlix_django
$ pip install requirements.txt
$ python3 manage.py makemigrations
$ python3 manage.py migrate
$ python3 manage.py runserver
```
After completing the previous steps, open a web browser and type **http://localhost:8000**

## Installation instructions - Windows

Clone the repository from GitHub:
```
git clone git@github.com:andrei2timo/ESD-UWEFlix-Cinema-Component-B.git
```

Set up a Virtual Environment using: 
```
py -3 -m venv .venv
.venv\scripts\activate
```
... and Install the modules and components required:
```
cd Cinema-System-ESD-Component B/UWEFlix_django
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
After completing the previous steps, open a web browser and type **http://localhost:8000**

## Usernames and passwords for test cases:
```
Cinema Manager account:
  Username: cinema_manager
  Password: uweflix1234
  
Student account:
  Username: george.washington
  Password: uweflix123

Account manager:
  Username: account_manager
  Password: Uweflix_Project
  
Club Representative:
  Username: 0020
  Password: uweflix123

Test user:
  Username: 0001
  Password: uweflix1234
  
  Username: andrei_test
  Password: uweflix1234
