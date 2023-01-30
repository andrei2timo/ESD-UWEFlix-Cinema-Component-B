# ESD-UWEFlix-Cinema-Component-B

By:
[![Developers Tag]( https://img.shields.io/badge/Developer-andrei2timo-blue.svg )]( https://github.com/andrei2timo )
[![Developers Tag]( https://img.shields.io/badge/Developer-alamerton-blue.svg )]( https://github.com/alamerton )<br>
[![Developers Tag]( https://img.shields.io/badge/Developer-snayak-blue.svg )]( https://github.com/Hyperoid29 )<br>
The UWEFlix website is developed using a Django virtual environment, and is intended to replace the existing paper system.

## Installation instructions - Linux
```
$ git clone git@github.com:andrei2timo/ESD-UWEFlix-Cinema-Component-A.git
$ cd Cinema-System-ESD-Component A/UWEFlix_django
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
cd Cinema-System-ESD-Component A/UWEFlix_django
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
After completing the previous steps, open a web browser and type **http://localhost:8000**
