from django.contrib.auth import logout as auth_logout
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import *
import calendar
from .models import *
from datetime import datetime as dt
from .forms import *
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from django.contrib import messages
from django.http import Http404
from django.utils import timezone

import re
import random

from django.contrib import messages
from rest_framework.decorators import api_view
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.utils import timezone
from django.http import JsonResponse




#At first, it initializes the DateIntervalForm() to get the start and end date from the user. It then sets up the context dictionary with the form and a title to display on the page.
#Next, the function checks if the HTTP method is "POST". If it is, it validates the form data and gets the start and end dates from the form. It then filters the Transaction model by the selected date range to get all the transactions made within that period.
#If there are no transactions within that date range, it sets the titleText variable with a message informing the user that there were no transactions made in that date range. It then updates the context dictionary to include this message and returns the updated context to the template.
#If there are transactions within that date range, the function updates the context with the start and end dates, the transaction list, and the form. It then returns the updated context to the template.

def order_history_account_manager(request):
    return render(request, 'uweflix/order_history_account_manager.html')


def view_order_history_account_manager(request):
    form = DateIntervalForm()
    titleText = "Please select a date range to view transactions for:"
    context = {
        'form': form,
        'title_text': titleText
    }
    if request.method == "POST":
        form = DateIntervalForm(request.POST)
        if form.is_valid():
            startDate = form.cleaned_data['startDate']
            endDate = form.cleaned_data['endDate']
            transaction_list = Transaction.objects.filter(
                date__range=(startDate, endDate))
            if not transaction_list:
                titleText = f"There were no transactions made in the selected date range"
                context = {
                    'form': form,
                    'title_text': titleText
                }
            else:
                context = {
                    'start_date': startDate,
                    'end_date': endDate,
                    'transaction_list': transaction_list,
                    'form': form
                }
            form = DateIntervalForm()
        return render(request, "UweFlix/order_history_account_manager.html", context)
    else:
        return render(request, "UweFlix/order_history_account_manager.html", context)







# This code defines a function named account_modify that renders a HTML template named 
# 'uweflix/account_modify.html' along with a SelectUserForm instance. The template will
#  use the form to allow users to select an account to modify. The context dictionary 
# is used to pass the form instance to the template. Overall, this function provides 
# a basic starting point for modifying user accounts within a larger web application.
def account_modify(request):
    form = SelectUserForm()
    context = {
        'form':form
    }
    return render(request, 'uweflix/account_modify.html', context)

# This code defines a function named manage_accounts that retrieves a list 
# of all user objects using the User.objects.all() method and passes it 
# to a context dictionary. It then renders a HTML template named 
# 'uweflix/manage_accounts.html' using the context. Overall, this function 
# provides a way to manage user accounts by displaying a list of all user 
# accounts within a larger web application.
def manage_accounts(request):  # Manage Accounts
    user_list = User.objects.all()
    context = {
        'user_list': user_list
    }

    return render(request, 'uweflix/manage_accounts.html', context)

# This code defines a function named add_user that handles adding a new user to the system. 
# If the request method is POST, it attempts to extract the user data from the request object 
# and performs some basic validation on it. If any validation errors occur, an error message 
# is displayed to the user and they are redirected back to the account management page. 
# If the data is valid, a new User object is created with the extracted data and saved 
# to the database. A success message is then displayed to the user. If the request method 
# is not POST, it skips the validation and simply retrieves a list of all user objects 
# from the database and passes it to a context dictionary. It then renders a HTML 
# template named 'uweflix/manage_accounts.html' using the context. Overall, 
# this function provides a way to add new user accounts to the system and display a 
# list of all user accounts within a larger web application.
def add_user(request):
    if request.method == "POST":
        try:
            first_name = request.POST['first_name']
            if not first_name or any(char.isdigit() for char in first_name):
                raise ValueError("Invalid first name")
            last_name = request.POST['last_name']
            if not last_name or any(char.isdigit() for char in last_name):
                raise ValueError("Invalid last name")
            username = request.POST['username']
            if not username:
                raise ValueError("Please enter a valid username")
            email = request.POST['email']
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                raise ValueError("Invalid email")

            user = User(first_name=first_name, last_name=last_name,
                        username=username, email=email)
            user.save()
            messages.success(request, "User added successfully")
        except ValueError as e:
            messages.error(request, str(e))
            return redirect('manage_accounts')
    else:
        pass

    user_list = User.objects.all()
    context = {
        'user_list': user_list
    }
    return render(request, 'uweflix/manage_accounts.html', context)

# This code defines a function named `delete_user` that deletes a user with the given 
# ID (`myid`) from the database using the `User.objects.get()` and `delete()` 
# methods. It then displays a success message to the user and redirects 
# them to the `manage_accounts` view using the `redirect()` function. 
# Overall, this function provides a way to delete a user account from 
# the system within a larger web application.
def delete_user(request, myid):  # Manage Accounts
    user = User.objects.get(id=myid)
    user.delete()
    messages.info(request, 'USER DELETED SUCCESSFULLY')
    return redirect(manage_accounts)

# This code defines a function named `edit_user` that retrieves a user with the 
# given ID (`myid`) from the database using the `User.objects.get()` method and 
# passes it to a context dictionary along with a list of all user objects. 
# It then renders a HTML template named `'uweflix/manage_accounts.html'` using 
# the context. Overall, this function provides a way to display the details 
# of a user account for editing within a larger web application.
def edit_user(request, myid):  # Manage Accounts
    sel_user = User.objects.get(id=myid)
    user_list = User.objects.all()
    context = {
        'sel_user': sel_user,
        'user_list': user_list
    }
    return render(request, 'uweflix/manage_accounts.html', context)

# This code defines a function named `update_user` that updates the details of a user 
# account with the given ID (`myid`) using the data submitted in the request object. 
# It retrieves the user object from the database using the `User.objects.get()` 
# method and updates its fields with the submitted data using attribute assignment. 
# It then saves the updated user object to the database using the `save()` method. 
# A success message is then displayed to the user and they are redirected back to 
# the account management page using the `redirect()` function. Overall, this function 
# provides a way to update the details of a user account within a larger web application.
def update_user(request, myid):  # Manage Accounts
    user = User.objects.get(id=myid)
    user.first_name = request.POST['first_name']
    user.Last_name = request.POST['last_name']
    user.username = request.POST['username']
    user.email = request.POST['email']
    user.save()
    messages.info(request, "THE USER HAS BEEN UPDATED SUCCESSFULLY")
    return redirect('manage_accounts')

# This code defines a function named `manage_club_account` that retrieves a list of 
# all club objects from the database using the `Club.objects.all()` method and passes 
# it to a context dictionary. It then renders a HTML template named `'uweflix/manage_club_account.html'` 
# using the context. Overall, this function provides a way to display and manage a list of 
# all club accounts within a larger web application.
def manage_club_account(request):  # Manage Clubs
    club_list = Club.objects.all()
    context = {
        'club_list': club_list
    }

    return render(request, 'uweflix/manage_club_account.html', context)

# This code defines a function named `manage_club_account` that retrieves a list of all club objects 
# from the database using the `Club.objects.all()` method and passes it to a context dictionary. 
# It then renders a HTML template named `'uweflix/manage_club_account.html'` using the context. 
# Overall, this function provides a way to display and manage a list of all club accounts within 
# a larger web application.
def manage_club_account(request):  # Manage Clubs
    club_list = Club.objects.all()
    context = {
        'club_list': club_list
    }

    return render(request, 'uweflix/manage_club_account.html', context)

# This code defines a view function named `add_clubs()` that handles a POST request to add a new club 
# to the database. It first gets the data submitted in the request and performs some validation on the 
# fields. If any field is invalid, it raises a ValueError with a corresponding error message and 
# redirects the user back to the `manage_club_account` page with the error message displayed. 
# If all fields are valid, it creates a new Club object with the data and saves it to the database, 
# then redirects the user back to the `manage_club_account` page with a success message displayed.
# Finally, it renders the `manage_club_account` page with a context containing a list of all clubs 
# in the database.
def add_clubs(request):  # Manage Clubs
    if request.method == "POST":
        name = request.POST.get('name', '').strip()
        street_number = request.POST.get('street_number', '').strip()
        street = request.POST.get('street', '').strip()
        city = request.POST.get('city', '').strip()
        post_code = request.POST.get('post_code', '').strip()
        landline_number = request.POST.get('landline_number', '').strip()
        mobile_number = request.POST.get('mobile_number', '').strip()
        email = request.POST.get('email', '').strip()

        try:
            # Check if name is empty
            if not name:
                raise ValueError("Please enter a valid name.")

            # Check if street number is empty or contains non-digits
            if not street_number or not street_number.isdigit():
                raise ValueError("Please enter a valid street number.")

            # Check if street is empty
            if not street:
                raise ValueError("Please enter a valid street name.")

            # Check if city is empty
            if not city:
                raise ValueError("Please enter a valid city name.")

            # Check if post code is empty or contains non-alphanumeric characters
            if not post_code or not post_code.isalnum():
                raise ValueError("Please enter a valid post code.")

            # Check if landline number is empty or contains non-digits
            if landline_number and not landline_number.isdigit():
                raise ValueError("Please enter a valid landline number.")

            # Check if mobile number is empty or contains non-digits
            if mobile_number and not mobile_number.isdigit():
                raise ValueError("Please enter a valid mobile number.")

            # Check if email is valid
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                raise ValueError("Please enter a valid email.")

            club = Club(name=name, street_number=street_number, street=street, city=city,
                        post_code=post_code, landline_number=landline_number, mobile_number=mobile_number, email=email)
            club.save()
            messages.success(request, "Club added successfully")
        except ValueError as e:
            messages.error(request, str(e))
            return redirect('manage_club_account')

    club_list = Club.objects.all()
    context = {
        'club_list': club_list
    }
    return render(request, 'uweflix/manage_club_account.html', context)

# This function deletes a club record from the database based on the given club ID and then 
# redirects the user to the 'manage_club_account' page. A success message is displayed to 
# the user to indicate that the club has been successfully deleted.
def delete_clubs(request, myid):  # Manage Accounts
    clubs = Club.objects.get(id=myid)
    clubs.delete()
    messages.info(request, 'CLUB DELETED SUCCESSFULLY')
    return redirect(manage_club_account)

# This function handles the editing of a club in the system. It retrieves the club's information 
# from the database using the provided ID, and then renders a template to display the information 
# and allow the user to edit it. The context dictionary includes the selected club's 
# information and a list of all clubs in the system.
def edit_clubs(request, myid):  # Manage Accounts
    sel_clubs = Club.objects.get(id=myid)
    club_list = Club.objects.all()
    context = {
        'sel_clubs': sel_clubs,
        'club_list': club_list
    }
    return render(request, 'uweflix/manage_club_account.html', context)

# This function updates the details of a club in the database based on the form submitted in the
# corresponding HTML page. It takes a request object and an integer myid, which represents the 
# id of the club that needs to be updated. It fetches the club object from the database using 
# the myid parameter, and updates the fields of the club object based on the form data. 
# Finally, it saves the updated club object and returns a redirect response to the manage_club_account 
# view. A success message is also displayed to the user via the messages framework.
def update_clubs(request, myid):  # Manage Accounts
    clubs = Club.objects.get(id=myid)
    clubs.name = request.POST['name']
    clubs.street_number = request.POST['street_number']
    clubs.street = request.POST['street']
    clubs.city = request.POST['city']
    clubs.post_code = request.POST['post_code']
    clubs.landline_number = request.POST['landline_number']
    clubs.mobile_number = request.POST['mobile_number']
    clubs.email = request.POST['email']
    clubs.save()
    messages.info(request, "THE USER HAS BEEN UPDATED SUCCESSFULLY")
    return redirect('manage_club_account')

# This function renders the 'create_account.html' template which allows a user to create a new account. 
# It fetches a list of all clubs from the database and passes it as context to the template.
def create_account(request):  # Manage Clubs
    club_list = Club.objects.all()
    context = {
        'club_list': club_list
    }

    return render(request, 'uweflix/create_account.html', context)

# This function renders the `modify_delete_accounts.html` template and passes `account_list` and 
# `club_list` as context variables to display all the accounts and clubs in the system. It is used 
# to manage accounts related to clubs in the system.
def modify_delete_accounts(request):  # Manage Clubs
    account_list = Account.objects.all()
    club_list = Club.objects.all()
    context = {
        'account_list': account_list,
        'club_list': club_list

    }

    return render(request, 'uweflix/modify_delete_accounts.html', context)

# This function creates a new account based on the user's input, and performs input validation to ensure 
# the data entered is valid. If the request method is POST, it retrieves the user's input from the request
# and creates a new Account object with the data. If the input is invalid, it raises a ValueError and 
# redirects the user back to the create_account page. If the input is valid and the account is successfully 
# created, it displays a success message with the unique account number. If the request method is not POST, 
# it generates a random account number and displays the create_account page with the random number and a 
# list of existing accounts and clubs.
def create_account(request):
    if request.method == "POST":
        try:
            random_num_generator = request.POST.get(
                'random_num_generator', None)
            if random_num_generator:
                random_num_generator = int(random_num_generator)
            else:
                random_num_generator = random.randint(1000, 9999)
            first_initial = request.POST.get('first_initial', None)
            if not first_initial or any(char.isdigit() for char in first_initial) or len(first_initial) != 1:
                raise ValueError("Invalid first Initial")
            last_name = request.POST.get('last_name', None)
            if not last_name or any(char.isdigit() for char in last_name):
                raise ValueError("Invalid last name")
            club_id = request.POST.get('club', None)
            club = Club.objects.get(id=club_id)
            card_number = request.POST.get('card_number', None)
            expiry_month = request.POST.get('expiry_month', None)
            expiry_year = request.POST.get('expiry_year', None)

            # Additional input validation
            current_year = datetime.now().year
            if not expiry_month.isdigit() or int(expiry_month) > 12:
                raise ValueError("Invalid expiry month")
            if not expiry_year.isdigit() or int(expiry_year) < current_year:
                raise ValueError("Invalid expiry year")

            account = Account(random_num_generator=random_num_generator, first_initial=first_initial, last_name=last_name, club=club,
                              card_number=card_number, expiry_month=expiry_month, expiry_year=expiry_year)
            account.save()
            messages.success(
                request, f"Account added successfully, the unique account number is: {random_num_generator}")
        except ValueError as e:
            messages.error(request, str(e))
            return redirect('create_account')
    else:
        random_num_generator = random.randint(1000, 9999)

    account_list = Account.objects.all()
    club_list = Club.objects.all()
    context = {
        'account_list': account_list,
        'club_list': club_list,
        'random_num_generator': random_num_generator
    }
    return render(request, 'uweflix/create_account.html', context)

# This function deletes an Account object from the database using the account ID passed as a parameter, 
# and then redirects the user to the "modify_delete_accounts" page while displaying a success message.
def delete_account(request, myid):
    account = Account.objects.get(id=myid)
    account.delete()
    messages.info(request, 'ACCOUNT DELETED SUCCESSFULLY')
    return redirect(modify_delete_accounts)

# This function retrieves the selected account object with the given ID from the database and renders 
# the 'modify_delete_accounts' template with the selected account object, all accounts, and all 
# clubs as context variables.
def edit_account(request, myid):  # Manage Accounts
    sel_account = Account.objects.get(id=myid)
    account_list = Account.objects.all()
    club_list = Club.objects.all()
    context = {
        'sel_account': sel_account,
        'account_list': account_list,
        'club_list': club_list
    }
    return render(request, 'uweflix/modify_delete_accounts.html', context)

# This function updates an existing account with new information provided by the user. It retrieves 
# the account information using its ID, updates its fields using the request.POST data, 
# and then saves the changes to the database. Finally, it redirects the user to the 
# 'modify_delete_accounts' page and displays a success message.
def update_account(request, myid):  # Manage Accounts
    account = Account.objects.get(id=myid)
    account.first_initial = request.POST['first_initial']
    account.last_name = request.POST['last_name']
    club_id = request.POST['club']
    account.club = Club.objects.get(id=club_id)
    account.card_number = request.POST['card_number']
    account.expiry_month = request.POST['expiry_month']
    account.expiry_year = request.POST['expiry_year']
    account.save()
    messages.info(request, "THE ACCOUNT HAS BEEN UPDATED SUCCESSFULLY")
    return redirect('modify_delete_accounts')

# The `view_account` function renders the `modify_delete_accounts.html` template, 
# which displays the list of accounts and clubs for managing accounts.
def view_account(request):
    return render(request, 'uweflix/modify_delete_accounts.html')
    
    
    
    # This function googleAuthRegister handles the registration process for a new user
#  using Google authentication. If the user is already authenticated, it checks if
# the user is registered as a customer in the Customer model. If the user is not registered,
#  it creates a new Customer instance with a default date of birth of '2000-01-01', adds the
#  user to the Student group, and logs the user in as a customer with a session ID, user group,
#  and credit information. If the user is already registered, it logs the user in as a customer
# with the existing session ID, user group, and credit information. In both cases, it redirects
#  the user to the home page. If the user is not authenticated, it renders the register.html
#  template for the user to register.

def googleAuthRegister(request):
    user = request.user
    if request.user.is_authenticated:
        if not Customer.objects.filter(user=request.user).exists():
            student = Customer.objects.create(
                user=request.user, dob='2000-01-01')
            group = Group.objects.get(name='Student')
            group.user_set.add(request.user)
            messages.success(
                request, 'You have been registered as a customer.')
            # Log in the user as a customer
            request.session['user_id'] = request.user.id
            request.session['user_group'] = "Student"
            request.session['credit'] = Customer.objects.get(
                user=request.user.id).credit
            request.user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request)
        else:
            messages.warning(
                request, 'You are already registered as a customer.')
            # Log in the user as a customer
            request.session['user_id'] = request.user.id
            request.session['user_group'] = "Student"
            request.session['credit'] = Customer.objects.get(
                user=request.user.id).credit
            request.user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request)
        return redirect('home')

    return render(request, 'uweflix/register.html')
    
'''
def registerPage(request):
    form = CustomUserCreationForm()
    customer_form = RegisterStudentForm()
    context = {
        'form': form,
        'customer_form': customer_form
    }
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        customer_form = RegisterStudentForm(request.POST)
        if form.is_valid():
            if customer_form.is_valid():
                dob = customer_form.cleaned_data['dob']
                user=form.save()
                user.is_active = False
                user.save()
                student = Customer.objects.create(user=user, dob=dob)
                group=Group.objects.get(name='Student')
                group.user_set.add(user)
                context['confirm'] = "Your request has been recieved. Please wait for a Cinema Manager to approve your account."
                return render(request, 'uweflix/register.html', context)
    return render(request, 'uweflix/register.html', context)
'''    

# This function renders the index.html template, which represents the home page of the UWEFlix web application.
def home(request):
    return render(request, 'uweflix/index.html')
    
# This function handles the club discounts feature of the web application. It displays a form to set 
# a discount for a selected Club Representative, and updates the corresponding Club object in the 
# database with the new discount rate. The function also retrieves a list of all Club Representatives 
# to display on the page, and returns the rendered discount.html template with the context data. 
# The function validates the form input and displays a success message if the discount is 
# applied successfully.
def clubdiscount(request):
    context = {}
    form = DiscountForm()
    club_reps = ClubRep.objects.all()

    if request.method == "POST":
        form = DiscountForm(request.POST)
        if form.is_valid():
            club_rep = form.cleaned_data['club_rep']
            discount_value = form.cleaned_data['discountValue']

            # Apply the discount to the selected club_rep
            club = club_rep.club
            club.discount_rate = discount_value
            club.save()

            messages.success(request, f'Discount of {discount_value}% applied to {club_rep.user.first_name} {club_rep.user.last_name} of {club.name}.')

    context['form'] = form
    context['club_reps'] = club_reps
    return render(request, "uweflix/discount.html", context)

# This function renders the "am_home.html" template and passes a context dictionary containing 
# the number of transactions made today to the template. The template is used to display 
# information about the daily transactions.
def am_home(request):
    transactions = Transaction.objects.filter(date = dt.today())
    transactions = transactions.count()
    context = {
        'transactions': transactions
    }
    return render(request, 'uweflix/am_home.html', context)

# This function renders the 'club_rep_home.html' template, which is the home page for club 
# representatives after they log in.
def club_rep_home(request):
    return render(request, 'uweflix/club_rep_home.html')

# This is a view function for the cinema manager's home page. It first checks if the user is 
# a cinema manager by checking their user_group attribute in the session. If they are, it 
# sets the context variable to include a boolean value indicating whether or not COVID-19 
# restrictions are currently being applied. If the request method is POST, it loops through 
# all screens and toggles the value of the apply_covid_restrictions attribute. Finally, it 
# returns the cinema_manager_home.html template with the context variable. If the user is 
# not a cinema manager, it redirects them to the index page.
def cinema_manager_home(request):
    if request.session['user_group'] == "Cinema Manager":
        context = {}
        restrictions = Screen.objects.first().apply_covid_restrictions
        context = {
            'restrictions_bool' : restrictions
        }
        if request.method == "POST":
            for screen in Screen.objects.all():
                Screen.updateScreen(screen.id, not screen.apply_covid_restrictions)
                context = {
                    'restrictions_bool' : not screen.apply_covid_restrictions
                }
            redirect('cinema_manager_home')
        return render(request, 'uweflix/cinema_manager_home.html', context)
    else:
        return redirect('/')

# This function renders the `student_home.html` template for the logged-in user who is a student.
def student_home(request):
    return render(request, 'uweflix/student_home.html')

# This function retrieves all the films from the database and renders them in the viewings.html template.
def viewings(request):
    films = Film.objects.all()
    context = {'films':films}
    return render(request, 'uweflix/viewings.html', context)

# This function retrieves all showings for a given film, orders them by time and renders the `showings.html` 
# template with a context containing the retrieved showings and the film object.
def showings(request, film):
    showings = Showing.objects.filter(film=film).order_by('time')
    film = Film.objects.get(pk=film)
    context = {'showings':showings, 'film':film}
    return render(request, 'uweflix/showings.html', context)

# This is a view function decorated with the `@api_view` decorator which accepts GET and POST requests to 
# the films endpoint. If the request method is GET, all films are retrieved from the database and 
# serialized using the `FilmSerializer` and returned as a Response object with status 200 OK. If 
# the request method is POST, the request data is deserialized using the `FilmSerializer`. 
# If the data is valid, a new film object is created and saved to the database, and the serialized data 
# is returned as a Response object with status 201 CREATED. If the data is invalid, the errors 
# are returned as a Response object with status 400 BAD REQUEST.
@api_view(['GET','POST'])
def films_endpoint(request):
    if request.method == 'GET':
        films = Film.objects.all()
        serializer = FilmSerializer(films, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = FilmSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# This is a Django Rest Framework API view that handles GET, PUT, and DELETE requests for a specific Film 
# object identified by its primary key (pk). 
# In case the requested Film object does not exist, it returns a 404 NOT FOUND response. If the request 
# method is GET, it returns a serialized representation of the Film object. If the request method is 
# PUT, it updates the Film object with the request data, validates it, and returns a serialized 
# representation of the updated Film object. If the request method is DELETE, it deletes the Film object 
# and returns a 204 NO CONTENT response.
@api_view(['GET', 'PUT', 'DELETE']) 
def specific_film_endpoint(request, pk): 
    try: 
        film = Film.objects.get(pk=pk) 
    except film.DoesNotExist: 
        return Response(status=status.HTTP_404_NOT_FOUND) 
    if request.method == 'GET': 
        serializer = FilmSerializer(film) 
        return Response(serializer.data) 
    elif request.method == 'PUT': 
        serializer = FilmSerializer(film, data=request.data) 
        if serializer.is_valid(): 
            serializer.save() 
            return Response(serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    elif request.method == 'DELETE': 
        film.delete() 
        return Response(status=status.HTTP_204_NO_CONTENT)

# This function is responsible for adding a film to the database, deleting a film from the database, 
# and updating a film in the database. It uses the deleteFilmForm to handle the deletion of a film 
# and displays the add_film.html template to the user to input details for a new film or edit 
# an existing film. If the form data is valid and meets the required conditions, it saves the new 
# film, updates the existing film, or deletes the film from the database and redirects the user 
# to the same page with success or error messages displayed.
def add_film(request):
    form = deleteFilmForm()
    context = {"form":form}
    if request.method == "POST":
        ages = {"U", "PG", "12", "12A", "15", "18"}
        title = request.POST.get('title')
        age_rating = request.POST.get('age_rating')
        duration = request.POST.get('duration')
        trailer_desc = request.POST.get('trailer_desc')
        if duration is not None and duration.isdigit():
            if(age_rating in ages):
                film = Film()
                film.title = title
                film.age_rating = age_rating
                film.duration = duration
                film.trailer_desc = trailer_desc
                try:
                    image = request.FILES.get('image')
                    film.image = image
                except:
                    pass
                film.save()
                messages.success(request, 'Film added successfully!')
            else:
                messages.error(request, 'Invalid Age Rating')
        else:
            messages.error(request, 'Duration is not a valid number')
        if 'delete_film' in request.POST: 
            form = deleteFilmForm(request.POST)
            if form.is_valid():
                film_id = form.cleaned_data.get('film')
                if film_id is not None:
                    try:
                        film = Film.objects.get(id=film_id)
                        film.delete()
                        messages.success(request, 'Film deleted successfully!')
                    except Film.DoesNotExist:
                        messages.error(request, 'Film does not exist')
                else:
                    messages.error(request, 'Invalid Film ID')
        if 'edit_film' in request.POST:
            ages = {"U", "PG", "12", "12A", "15", "18"}
            title = request.POST.get("edit_title")
            age_rating = request.POST.get("edit_age_rating")
            duration = request.POST.get("edit_duration")
            trailer_desc = request.POST.get("edit_trailer_desc")
            film_id = request.POST.get("film")
            try:
                film = Film.objects.get(id=film_id)
                if duration is not None and duration.isdigit():
                    if age_rating in ages:
                        film.title = title
                        film.age_rating = age_rating
                        film.duration = duration
                        film.trailer_desc = trailer_desc
                        try:
                            image = request.FILES.get('edit_image')
                            film.image = image
                        except:
                            pass
                        film.save()
                        messages.success(request, 'Film updated successfully!')
                    else:
                        messages.error(request, 'Invalid Age Rating')
                else:
                    messages.error(request, 'Duration is not a valid number')
            except Film.DoesNotExist:
                messages.error(request, 'Film does not exist')
    return render(request, 'uweflix/add_film.html', context)

# The `edit_film` function is responsible for editing a film object in the database based on the form 
# data submitted via a POST request. The function creates an `EditFilmForm` object to display the form, 
# and if a POST request is received, the function validates the data and updates the film object in 
# the database. If the film object exists in the database, the data is updated and the form is 
# populated with the updated film data, otherwise an error message is printed. Finally, the function 
# renders the `add_film.html` template with the context containing the form data.
def edit_film(request):
    form = EditFilmForm()
    context = {"form": form}
    if request.method == "POST":
        ages = {"U", "PG", "12", "12A", "15", "18"}
        title = request.POST.get("title")
        age_rating = request.POST.get("age_rating")
        duration = request.POST.get("duration")
        trailer_desc = request.POST.get("trailer_desc")
        film = None
        if duration is not None and duration.isdigit():
            if age_rating in ages:
                try:
                    film = Film.objects.get(title=title)
                    film.age_rating = age_rating
                    film.duration = duration
                    film.trailer_desc = trailer_desc
                    try:
                        image = request.FILES.get("image")
                        film.image = image
                    except:
                        pass
                    film.save()
                except Film.DoesNotExist:
                    print("Film does not exist")
            else:
                print("Invalid Age Rating")
        else:
            print("Duration is not a valid number")
        if film:
            form = EditFilmForm(instance=film)
    context["form"] = form
    return render(request, "uweflix/add_film.html", context)

# This is a Django REST Framework API view function that handles HTTP GET and POST requests for 
# screens. If the request method is GET, it retrieves all screens from the database, serializes 
# the data using the ScreenSerializer and returns a Response object containing the serialized data with 
# a 200 OK status code. If the request method is POST, it creates a new screen object using the data 
# in the request, validates the data using the ScreenSerializer, saves the new object to the database 
# and returns a Response object containing the serialized data with a 201 CREATED status code if the data
# is valid. If the data is invalid, it returns a Response object containing the validation errors with a
# 400 BAD REQUEST status code.
@api_view(['GET','POST'])
def screens_endpoint(request):
    if request.method == 'GET':
        screens = Screen.objects.all()
        serializer = ScreenSerializer(screens, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = ScreenSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# The given code defines an API endpoint for a specific screen identified by its primary key. 
# It supports GET, PUT, and DELETE requests. 
# The GET request returns the details of the screen in JSON format. 
# The PUT request updates the existing screen details with the provided data and returns the updated data. 
# The DELETE request deletes the screen and returns a success message. 
# If the screen is not found, it returns a 404 NOT FOUND response. If there are any validation 
# errors in the data provided for PUT request, it returns a 400 BAD REQUEST response.
@api_view(['GET', 'PUT', 'DELETE']) 
def specific_screen_endpoint(request, pk): 
    try: 
        screen = Screen.objects.get(pk=pk) 
    except screen.DoesNotExist: 
        return Response(status=status.HTTP_404_NOT_FOUND) 
    if request.method == 'GET': 
        serializer = ScreenSerializer(screen) 
        return Response(serializer.data) 
    elif request.method == 'PUT': 
        serializer = ScreenSerializer(screen, data=request.data) 
        if serializer.is_valid(): 
            serializer.save() 
            return Response(serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    elif request.method == 'DELETE': 
        screen.delete() 
        return Response(status=status.HTTP_204_NO_CONTENT)

# This is a view function for adding a new screen and editing existing screens. It renders a form to 
# add a new screen and lists all the existing screens with options to edit them. If the user 
# submits the add screen form, it validates the data, creates a new screen object, and saves 
# it to the database. If the user submits the edit screen form, it validates the data, retrieves 
# the selected screen object from the database, updates its data, and saves it. Overall, the function 
# handles GET and POST requests and renders the 'add_screen.html' template with the relevant context data.
def add_screen(request):
    context = {}
    form = addScreenForm()
    selected_screen = None
    form1 = editScreenForm()
    screens = Screen.objects.all()
    options = [screen.id for screen in screens]
    if screens:
        context['screens'] = screens
        context['options'] = options
    if request.method == "POST":
        form = addScreenForm(request.POST)
        if form.is_valid():
            capacity = form.cleaned_data['capacity']
            covid_restrictions = form.cleaned_data['apply_covid_restrictions']
            screen = Screen(capacity=capacity, apply_covid_restrictions=covid_restrictions)
            screen.save()
            return redirect('add_screen')
            
        if 'edit_screen' in request.POST:
            capacity = request.POST.get('capacity')
            covid_restrictions = request.POST.get('apply_covid_restrictions')
            try:
                selected_screen = Screen.objects.get(id=screen_id)
                if capacity is not None and capacity.isdigit():
                    screen_id = Screen.objects.get(id=id)
                    screen_id.capacity = capacity
                    screen_id.apply_covid_restrictions = covid_restrictions
                selected_screen = Screen.objects.get(id=screen_id)
                form1 = editScreenForm(request.POST, instance=selected_screen)
            except Screen.DoesNotExist:
                    print("Screen does not exist")
            if screen_id:
                form = EditFilmForm(instance=screen_id)

    context['form'] = form
    context['form1'] = form1
    context['selected_screen'] = selected_screen
    return render(request, 'uweflix/add_screen.html', context)

# This is a Django REST Framework API view function that handles GET and POST requests for the 'showings' 
# endpoint. If a GET request is received, all 'Showing' objects are retrieved from the database and 
# serialized using the 'ShowingSerializer', then returned with a 200 status code. If a POST request
# is received, the data from the request is deserialized using the 'ShowingSerializer' and if the data 
# is valid, a new 'Showing' object is created and saved to the database, and the serialized data for 
# the new object is returned with a 201 status code. If the data is invalid, a 400 status code is 
# returned along with the validation errors.
@api_view(['GET','POST']) # @here see if this works with relations
def showings_endpoint(request):
    if request.method == 'GET':
        showings = Showing.objects.all()
        serializer = ShowingSerializer(showings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = ShowingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# This is a view function named `add_showing` that adds a new showing to the database. The function takes
# a request object as its parameter, initializes an empty context dictionary and an `addShowingForm` 
# instance, and gets all existing showings from the database along with their IDs. If there are any 
# showings, their IDs are added to the context dictionary.

# If the request method is POST, the function populates the form with the data submitted via the 
# form and, if the form is valid, it creates a new showing object and saves it to the database 
# using the `newShowing` method of the `Showing` model. The `newShowing` method takes the screen, 
# film, and time parameters as its arguments and creates a new showing with these parameters.

# Finally, the function populates the context dictionary with the `addShowingForm` instance and renders 
# the `add_showing.html` template with the context.
def add_showing(request):
    context = {}
    form = addShowingForm
    showings = Showing.objects.all().order_by('film__title', 'time')
    context = {
        'showings': showings,
    }
    if request.method == "POST":
        form = addShowingForm(request.POST)
        if form.is_valid():
            screen = form.cleaned_data['screen']
            film = form.cleaned_data['film']
            time = form.cleaned_data['time']
            existing_showing = Showing.objects.filter(screen=screen, time__date=time.date(), time__time=time.time())

            if existing_showing.exists():
                return JsonResponse({'success': False, 'message': 'Error: Showing already live at this time on this screen'})
            else:
                Showing.newShowing(screen, film, time)
                return JsonResponse({'success': True, 'message': 'Showing added successfully'})
    else:
        messages.error(request, 'Error adding the showing. Please check the form for any mistakes.')
        form = addShowingForm()
    context['form'] = form
    context['showings'] = showings

    return render(request, 'uweflix/add_showing.html', context)

# This is a view function for editing an existing showing. It receives a request and a showing_id as 
# input parameters. It creates an instance of the editShowingForm and sets up the context dictionary 
# with this form. The function then tries to retrieve the showing instance based on the provided 
# showing_id, and if it does not exist, returns a 404 error. If the 'edit_showing' button is clicked, 
# the function attempts to update the showing with the information provided in the form. If the form is 
# valid, it saves the changes and displays a success message. If the form is not valid, it displays an 
# error message. Finally, it returns the render of the edit_showing.html template with the updated context.
def edit_showing(request, showing_id):
    form = editShowingForm()
    context = {"form":form}
    showing = get_object_or_404(Showing, id=showing_id)
    form = editShowingForm(instance=showing)
    context = {"form": form}

    if request.method == "POST":
        form = editShowingForm(request.POST, instance=showing)
        if form.is_valid():
            form.save()
            messages.success(request, 'Showing updated successfully!')
            
            return redirect('add_showing')
        else:
            messages.error(request, 'Error updating the showing. Please check the form for any mistakes.')

    return render(request, 'uweflix/edit_showing.html', context)

# This is a view function for deleting an existing showing. It receives a request and a showing_id as 
# input parameters. The function checks if the request method is 'POST', and if so, it tries to retrieve 
# the showing instance based on the provided showing_id. If the showing does not exist, it returns a 404 
# error. The function then deletes the showing instance and displays a success message. Afterward, it 
# returns the render of the add_showing.html template. If the request method is not 'POST', it redirects 
# the user to the homepage.

def delete_showing(request, showing_id):
    if request.method == 'POST':
        showing = get_object_or_404(Showing, id=showing_id)
        showing.delete()
        messages.success(request, 'Showing deleted successfully!')
        return render(request, 'uweflix/add_showing.html', {})
    else:
        return redirect('/')
    
# This function handles the registration process for a new user. It first creates instances of the 
# `CustomUserCreationForm` and `RegisterStudentForm` forms, and then renders the `register.html` 
# template with these forms as context. If the request method is `POST`, it checks if both forms are 
# valid. If they are, it creates a new user with the information entered in the `CustomUserCreationForm`, 
# sets the user's `is_active` attribute to `False`, and saves the user. It then creates a new `Customer` 
# instance with the user and the date of birth entered in the `RegisterStudentForm`, adds the user to the
# `Student` group, and renders the `register.html` template with a confirmation message.
def registerPage(request):
    form = CustomUserCreationForm()
    customer_form = RegisterStudentForm()
    context = {
        'form': form,
        'customer_form': customer_form
    }
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        customer_form = RegisterStudentForm(request.POST)
        if form.is_valid():
            if customer_form.is_valid():
                dob = customer_form.cleaned_data['dob']
                user=form.save()
                user.is_active = False
                user.save()
                student = Customer.objects.create(user=user, dob=dob)
                group=Group.objects.get(name='Student')
                group.user_set.add(user)
                context['confirm'] = "Your request has been recieved. Please wait for a Cinema Manager to approve your account."
                return render(request, 'uweflix/register.html', context)
    return render(request, 'uweflix/register.html', context)

#@unauthenticated_user
def login(request):
    if request.method == 'POST':
        un = request.POST['username'] #Gets Username
        pw = request.POST['password'] #Gets Password
        user = authenticate(username=un, password=pw)
        if user is not None:
            request.session['user_id'] = user.id
            if user.groups.filter(name='Student').exists():
                request.session['user_group'] = "Student"
                request.session['credit'] = Customer.objects.get(user=user.id).credit
                return redirect ('student_home')
            elif user.groups.filter(name='Club Rep').exists():
                request.session['user_group'] = "Club Rep"
                request.session['credit'] = ClubRep.objects.get(user=user).credit
                return redirect ('club_rep_home')
            elif user.groups.filter(name='Account Manager').exists():
                request.session['user_group'] = "Account Manager"
                return redirect ('am_home')
            elif user.groups.filter(name='Cinema Manager').exists():
                request.session['user_group'] = "Cinema Manager"
                return redirect ('cinema_manager_home')
        else:
            messages.error(request, "Bad Credentials")
    return render(request, "uweflix/login.html")

def logout(request):
    auth_logout(request)
    try:
        del request.session['user_id']
        del request.session['user_group']
        del request.session['credit']
    except KeyError:
        pass
    finally:
        return redirect("/login/")


def userpage(request):
    context = {}
    return render(request, 'uweflix/user.html', context)

# The `payment` function handles the payment process for movie tickets. It retrieves the showing, adult, 
# student, and child prices and creates a payment form. If the form is submitted and valid, the function 
# checks the remaining tickets and the payment option. If the user is signed in as a student, the function 
# checks whether the payment can be made using credit. If the user is not signed in, the function redirects
# to the payment page to pay with a credit card. If the payment is successful, it creates a new transaction
# and generates a new ticket for each ticket purchased, then updates the remaining tickets and redirects 
# to the thank you page.
def payment(request, showing):

    if 'user_id' in request.session:
        if request.session['user_group'] == "Club Rep":
            return redirect('rep_payment', showing=showing)

    adult,student,child=Prices.getCurrentPrices()

    showing = Showing.getShowing(id=showing)
    form = PaymentForm()
    context = {
        "showing": showing,
        "form": form,
        "adult_price": adult,
        "student_price": student,
        "child_price": child
    }

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            total_cost = float(form["total_cost"].data)
            adult_tickets = int(form["adult_tickets"].data)
            student_tickets = int(form["student_tickets"].data)
            child_tickets = int(form["child_tickets"].data)
            total_tickets = adult_tickets + student_tickets + child_tickets
            payment_option = form.cleaned_data.get("payment_options")
            if showing.remaining_tickets < total_tickets: #If there is NOT enough tickets
                print("Not enough tickets remaining to make this booking.")
                return render(request, "uweflix/error.html")
            else:
                if 'user_id' in request.session:  # If signed in
                    user_type = request.session['user_group']
                    if (user_type == "Student"):
                        #Club reps and students
                        user = Customer.objects.get(user=request.session['user_id'])
                        if payment_option == 'credit' and user.credit >= total_cost: # If paying with credit
                            user.credit -= total_cost
                            request.session['credit'] = user.credit
                            user.save()
                            paying = True
                        elif payment_option == "nopay":
                            return redirect(f'/pay_with_card/?user={user.id}&cost={total_cost}&adult={adult_tickets}&student={student_tickets}&child={child_tickets}&showing={showing.id}')
                        else:
                            context = {'error': "Credit error: You do not have sufficient credit to make this order, please add funds and try again."}
                            return render(request, "uweflix/error.html", context)
                    else:
                        context = {'error': "Account based error: Your account type is not permitted to purchase tickets. Please change accounts and try again."}
                        return render(request, "uweflix/error.html", context)
                elif payment_option == "nopay":  # Regular customer pays with card
                    return redirect(f'/pay_with_card/?user={0}&cost={total_cost}&adult={adult_tickets}&student={student_tickets}&child={child_tickets}&showing={showing.id}')
                else:
                    context = {'error': "As a regular customer, you may only make purchases via credit card. Please go back and select this option."}
                    return render(request, "uweflix/error.html", context)
                new_transaction = Transaction.newTransaction(user, total_cost, paying)
                for i in range(adult_tickets):
                    Ticket.newTicket(new_transaction, showing, "adult")
                for i in range(student_tickets):
                    Ticket.newTicket(new_transaction, showing, "student")
                for i in range(child_tickets):
                    Ticket.newTicket(new_transaction, showing, "child")
                showing.remaining_tickets -= (adult_tickets + student_tickets + child_tickets)
                showing.save()
                request.session['screen'] = showing.screen.id
                request.session['transaction'] = new_transaction.id
                request.session['film'] = showing.film.title
                request.session['age_rating'] = showing.film.age_rating
                request.session['date'] = showing.time.strftime("%d/%m/%y")
                request.session['time'] = showing.time.strftime("%H:%M")
                request.session['successful_purchase'] = True
                request.session['covid_restrictions'] = showing.screen.apply_covid_restrictions
                if showing.screen.apply_covid_restrictions:
                    request.session['allocated_seat'] = showing.screen.capacity - showing.remaining_tickets
                return redirect('/thanks')
        else:
            return render(request, 'uweflix/payment.html', context={'form':form, "showing": showing})
    return render(request, 'uweflix/payment.html', context)

# The pay_with_card function is a view function in the UWEFlix web application. It handles the process 
# of a user making a payment for cinema tickets using a card. It receives the user's input from a 
# CardPaymentForm, validates it and creates Ticket and Transaction objects to complete the purchase. 
# It then stores relevant information about the purchase in the user's session and redirects them to a 
# thank-you page. If the form is not valid, it will render the payment page again with the invalid form.
def pay_with_card(request):
    form = CardPaymentForm()
    context = {
        'user': request.GET.get('user'),
        'cost': request.GET.get('cost'),
        'adult': request.GET.get('adult'),
        'student': request.GET.get('student'),
        'child': request.GET.get('child'),
        'showing': request.GET.get('showing'),
        'form':form
    }
    if request.method=="POST":
        form = CardPaymentForm(request.POST)
        if form.is_valid():
            id = int(context['user'])
            user=None
            if id == 0:
                pass
            else:
                user= Customer.objects.get(id= context['user'])
            total_cost = float(context['cost'])
            adult_tickets = int(context['adult'])
            child_tickets = int(context['child'])
            student_tickets = int(context['student'])
            showing = Showing.getShowing(int(context['showing']))
            new_transaction = Transaction.newTransaction(user, total_cost, True)
            for i in range(adult_tickets):
                Ticket.newTicket(new_transaction, showing, "adult")
            for i in range(student_tickets):
                Ticket.newTicket(new_transaction, showing, "student")
            for i in range(child_tickets):
                Ticket.newTicket(new_transaction, showing, "child")
            showing.remaining_tickets -= (adult_tickets + student_tickets + child_tickets)
            showing.save()
            request.session['screen'] = showing.screen.id
            request.session['transaction'] = new_transaction.id
            request.session['film'] = showing.film.title
            request.session['age_rating'] = showing.film.age_rating
            request.session['date'] = showing.time.strftime("%d/%m/%y")
            request.session['time'] = showing.time.strftime("%H:%M")
            request.session['successful_purchase'] = True
            request.session['covid_restrictions'] = showing.screen.apply_covid_restrictions
            if showing.screen.apply_covid_restrictions:
                    request.session['allocated_seat'] = showing.screen.capacity - showing.remaining_tickets
            return redirect('/thanks')
        else: return render(request,"uweflix/pay_with_card.html",{'form':form})

    return render(request,"uweflix/pay_with_card.html",context)

# The `rep_payment` function processes a payment for a club representative who is purchasing tickets on
# behalf of their club. The function retrieves the showing being booked and the representative's discount 
# rate, and displays the payment form. When the user submits the payment form, the function validates 
# the form and creates a new transaction for the purchase of student tickets. If the payment is successful, 
# the function updates the remaining tickets for the showing and redirects to a confirmation page. 
# If there are not enough tickets remaining to make the booking, or if there is an issue with the 
# payment, the function returns an error page.
def rep_payment(request, showing):
    showing = Showing.getShowing(id=showing)
    form = RepPaymentForm()
    rep = ClubRep.objects.get(user_id=request.session["user_id"])
    discountRate = rep.club.discount_rate
    adult,student,child=Prices.getCurrentPrices()
    context = {
        "showing": showing,
        "form": form,
        "discount_rate": discountRate,
        "student_price" : student
    }
    if request.method == 'POST':
        form = RepPaymentForm(request.POST)
        if form.is_valid():
            print("Valid")
            total_cost = float(form["total_cost"].data)
            student_tickets = int(form["rep_student_tickets"].data)
            total_tickets = student_tickets
            payment_option = form.cleaned_data.get("payment_options")
            if showing.remaining_tickets < total_tickets:  # If there is NOT enough tickets
                error_message = "Not enough tickets remaining to make this booking."
                print(error_message)
                context['error_message'] = error_message
            else:
                user_type = request.session['user_group']
                user = Customer.objects.get(user=request.session['user_id'])
                if payment_option == 'credit' and user.credit >= total_cost: # If paying with credit
                    user.credit -= total_cost
                    request.session['credit'] = user.credit
                    user.save()
                    paying = True
                elif user_type == "Club Rep" and payment_option == "tab":
                    paying = False
                else:
                    context = {'error': "Credit error: You do not have sufficient credit to make this order, please add funds and try again."}
                    return render(request, "uweflix/error.html", context)
                new_transaction = Transaction.newTransaction(user, total_cost, paying)
                for i in range(student_tickets):
                    Ticket.newTicket(new_transaction, showing, "student")
                showing.remaining_tickets -= student_tickets
                showing.save()
                request.session['screen'] = showing.screen.id
                request.session['transaction'] = new_transaction.id
                request.session['film'] = showing.film.title
                request.session['age_rating'] = showing.film.age_rating
                request.session['date'] = showing.time.strftime("%d/%m/%y")
                request.session['time'] = showing.time.strftime("%H:%M")
                request.session['successful_purchase'] = True
                request.session['covid_restrictions'] = showing.screen.apply_covid_restrictions
                if showing.screen.apply_covid_restrictions:
                    request.session['allocated_seat'] = showing.screen.capacity - showing.remaining_tickets
                return redirect('/thanks')
        else:
            print("invalid")
            return render(request, 'uweflix/rep_payment.html', context={'form':form, "showing": showing})
    return render(request, 'uweflix/rep_payment.html', context)

# The `thanks` function is a Django view that renders a "thank you" page after a successful purchase. 
# The function first checks if the 'successful_purchase' key is in the request session; if it's not 
# found, the function raises an Http404 exception. If the key is found, it is removed from the session, 
# and the function returns an HTML page rendered by the Django template engine.
def thanks(request):
    if 'successful_purchase' not in request.session:
        raise Http404("Forbidden access to this page.")
    del request.session['successful_purchase']
    return render(request, "uweflix/thanks.html")

# The `error` function is a view in the `uweflix` Django web application that simply renders the 
# `uweflix/error.html` template. This template is used to display an error message to the user 
# in case an error occurs during a transaction or a user tries to access a page that they do 
# not have permission to access.
def error(request):
    return render(request, "uweflix/error.html")

# The `topup` function is a Django view that handles the top-up functionality for users' accounts. 
# The function first checks if the user is logged in and has the appropriate user group ("Club Rep" or 
# "Student"). If the user is authorized, the function handles the POST request containing the top-up 
# amount, adds the amount to the user's account credit, and updates the user's session with the new 
# credit amount. Finally, the function renders the "topup.html" template. If the user is not authorized, 
# the function redirects the user to the home page.
def topup(request):
    if 'user_group' in request.session:
        if request.session['user_group'] == "Club Rep":
            userObject = ClubRep
        elif request.session['user_group'] == "Student":
            userObject = Customer
        else:
            return redirect('home') 
        if request.method == 'POST':
            topUpValue = request.POST.get("topUpValue")
            loggedInRep = userObject.objects.get(user = request.session['user_id'])
            loggedInRep.credit = loggedInRep.credit + round(float(topUpValue), 2)
            request.session['credit'] = loggedInRep.credit
            loggedInRep.save()
        return render(request, "uweflix/topup.html")
    else:
        return redirect('home')

# The `view_accounts` function renders the `view_accounts.html` template, which displays a list of 
# user accounts. This function does not perform any action on the user accounts; it is only 
# responsible for displaying them.
def view_accounts(request):
    return render(request, "uweflix/view_accounts.html")

# The `daily_transactions` function takes a `request` object and returns a rendered HTML page that 
# displays a list of transactions made on a given day. It displays a form that allows the user 
# to select a date to view transactions for, and upon submitting the form, retrieves and displays
# the transactions for the selected date. If no transactions were made on the selected date, 
# it displays a message indicating so.
def daily_transactions(request):
    form = DatePickerForm()
    titleText = "Please select a day to view transactions for:"
    context = {
        'form': form,
        'title_text': titleText}
    if request.method == "POST":
        form = DatePickerForm(request.POST)
        if form.is_valid():
            selectedDate = dt.today()
            if "search" in request.POST:
                selectedDate = form.cleaned_data['date']
            elif "today" in request.POST:
                selectedDate = dt.today()
            transaction_list = Transaction.objects.filter(date = selectedDate)
            if not transaction_list:
                titleText = f"There were no transactions made on {str(selectedDate)}"
                context = {
                    'form': form,
                    'title_text': titleText
                }
            else:
                context = {
                    'selected_date': selectedDate,
                    'transaction_list': transaction_list,
                    'form': form
                }
        return render(request, "uweflix/daily_transactions.html", context)
    else:
        return render(request, "uweflix/daily_transactions.html", context)

# The `customer_statements` function renders a page for generating customer statements based on a 
# selected club representative and time range. The function creates a form object, and if a valid 
# POST request is received, it validates the form data and uses it to retrieve a list of transactions 
# for the selected club representative and time range. The function then adds the club representative's 
# club name and transaction list to the context and renders the `customer_statements.html` template with 
# the context. If the request is not a POST request, the function simply renders the template with the form.
def customer_statements(request):
    form = SearchClubRepForm()
    context = {'form': form}
    if request.method == "POST":
        form = SearchClubRepForm(request.POST)
        if form.is_valid():
            clubrep = ClubRep.objects.get(
                club_rep_num=form.cleaned_data['clubrep_choice']
            )
            trange = form.cleaned_data['timerange_choice']
            if trange == 'Month':
                transaction_list = Transaction.objects.filter(
                    customer=clubrep,
                    date__year=dt.now().year,
                    date__month=dt.now().month,

                )
            elif trange == "Year":
                transaction_list = Transaction.objects.filter(
                    customer=clubrep,
                    date__year=dt.now().year,
                )
            context = {
                'club_rep_num': clubrep.club_rep_num,
                'club_name': clubrep.club.name,  # add club name to context
                'transaction_list': transaction_list,
                'form': form,

            }
        return render(request, 'uweflix/customer_statements.html', context)
    else:
        return render(request, 'uweflix/customer_statements.html', context)

# The `settle_payments` function appears to handle the process of settling payments for a specific Club Rep. 
# It first checks if the logged-in user belongs to the Club Rep user group, and then retrieves all 
# transactions made by the Club Rep that have not been settled for the current month. If the request 
# method is POST, it sets the `is_settled` field of all transactions to True and redirects back to 
# the `settle_payments` view. Finally, it renders the `settle_payments.html` template with the 
# transaction list and Club Rep number as context.
def settle_payments(request):
    context = {}
    if request.session["user_group"] == "Club Rep":
        club_rep = ClubRep.objects.get(user_id=request.session["user_id"])
        transaction_list = Transaction.objects.filter(
                customer=club_rep,
                date__year = dt.now().year,
                date__month = dt.now().month,
                is_settled = False
            )
        context = {
            'transactions': transaction_list,
            'club_rep': club_rep.club_rep_num
            }
        if request.method == "POST":
            for transaction in transaction_list:
                #Need to discuss the 'paying' aspect of this.
                transaction.is_settled = True
                transaction.save()
                return redirect('settle_payments')   
        return render(request, 'uweflix/settle_payments.html', context)
    else:
        return redirect('home')

# The `set_payment_details` function is used to set the payment details for a club. It takes a POST 
# request containing a form with information about the club's payment details such as card number 
# and expiration date. If the form is valid, it updates the club object with the new payment details 
# and displays a success message. If the form is invalid, it re-renders the form with error messages. 
# Finally, it renders the "set_payment.html" template with the form and any messages.
def set_payment_details(request):
    form = AccessClubForm()
    context = {'form': form}
    if request.method == "POST":
        form = AccessClubForm(request.POST)
        if form.is_valid():
            club_id = form.cleaned_data['club']
            club_obj = Club.objects.get(id=club_id)
            club_obj.card_number = form.cleaned_data['card_number']
            month = form.cleaned_data['expiry_month']
            year = form.cleaned_data['expiry_year']
            formatted_date = f"{year}-{month}-{calendar.monthrange(int(year), int(month))[1]}"
            club_obj.card_expiry_date = formatted_date
            club_obj.save()

            # Success message variables
            club_name = club_obj.name
            card_number = form.cleaned_data['card_number']
            expiry_month = form.cleaned_data['expiry_month']
            expiry_year = form.cleaned_data['expiry_year']
            success_message = True
            context.update({'success_message': success_message,
                            'club_name': club_name,
                            'card_number': card_number,
                            'expiry_month': expiry_month,
                            'expiry_year': expiry_year})
        else:
            context = {'form': form}
    return render(request, "uweflix/set_payment.html", context)

# This is a Django REST Framework view function that supports both GET and POST requests to the 
# "/clubs_endpoint" endpoint. When a GET request is received, it retrieves all club objects from 
# the database, serializes them using the ClubSerializer, and returns the serialized data in a 
# Response object with a status code of 200. When a POST request is received, it deserializes the 
# request data using the ClubSerializer, validates the data, saves it to the database, and returns 
# the serialized data in a Response object with a status code of 201 if successful. If there are 
# validation errors, it returns a Response object with the errors and a status code of 400.
@api_view(['GET','POST'])
def clubs_endpoint(request):
    if request.method == 'GET':
        clubs = Club.objects.all()
        serializer = ClubSerializer(clubs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = ClubSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# This is a Django Rest Framework view function decorated with `@api_view` that accepts GET, PUT, 
# and DELETE requests to interact with a specific Club instance identified by its primary key (pk). 
# If the Club with the given pk does not exist, it returns a 404 response. If the request method 
# is GET, it returns a serialized representation of the Club instance. If the request method is PUT,
# it updates the Club instance with the provided data and returns the updated serialized representation.
# If the request method is DELETE, it deletes the Club instance and returns a 204 response.
@api_view(['GET', 'PUT', 'DELETE']) 
def specific_club_endpoint(request, pk): 
    try: 
        club = Club.objects.get(pk=pk) 
    except club.DoesNotExist: 
        return Response(status=status.HTTP_404_NOT_FOUND) 
    if request.method == 'GET': 
        serializer = ClubSerializer(club) 
        return Response(serializer.data) 
    elif request.method == 'PUT': 
        serializer = ClubSerializer(club, data=request.data) 
        if serializer.is_valid(): 
            serializer.save() 
            return Response(serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    elif request.method == 'DELETE': 
        club.delete() 
        return Response(status=status.HTTP_204_NO_CONTENT)

# This function handles the addition of a new club. It initializes an empty context dictionary and 
# an instance of the addClubForm. If the request method is POST, it validates the submitted form, 
# creates a new Club instance with the submitted data, saves it, and displays a success message. 
# It then redirects the user to the cinema manager home page. The rendered template is 
# "Uweflix/add_club.html".
def add_club(request):
    context = {}
    form = addClubForm()
    if request.method == "POST":
        form = addClubForm(request.POST)
        if form.is_valid():
            club = form.save(commit=False)
            clubName = form.cleaned_data['name']
            clubStreetNumber = form.cleaned_data['street_number']
            clubStreet = form.cleaned_data['street']
            clubCity = form.cleaned_data['city']
            clubPostcode = form.cleaned_data['post_code']
            clubLandlineNumber = form.cleaned_data['landline_number']
            clubMobileNumber = form.cleaned_data['mobile_number']
            clubEmail = form.cleaned_data['email']
            Club.newClub(clubName, clubStreetNumber, clubStreet, clubCity, clubPostcode, clubLandlineNumber, clubMobileNumber, clubEmail)
            messages.success(request, "Club successfully registered.")
            return redirect('/cinema_manager_home')

    context['form'] = form
    return render(request, "Uweflix/add_club.html", context)

# This function adds a new club representative to the system. It takes in two forms, `ClubRepCreationForm` 
# and `addRepForm`, and validates them. If both forms are valid, it saves the user object and creates 
# a new `ClubRep` object. It assigns a unique username to the user and adds the user to the 
# "Club Rep" group. It then redirects the user to a success page.
def add_rep(request):
    context = {}
    userForm = ClubRepCreationForm()
    form = addRepForm()
    if request.method == "POST":
        userForm = ClubRepCreationForm(request.POST)
        form = addRepForm(request.POST)
        if userForm.is_valid():
            if form.is_valid():
                user = userForm.save(commit=False)
                dob = form.cleaned_data['dob']
                club = form.cleaned_data['club']
                clubRepNum = 1
                if ClubRep.objects.exists():
                    clubRepNum = int(ClubRep.objects.all().last().club_rep_num) + 1
                crUsername = ("%04d" % (clubRepNum,))
                user.username = crUsername
                user.save()
                newCr = ClubRep.objects.create(user=user, club=club, dob=dob, club_rep_num=clubRepNum)
                userGroup = Group.objects.get(name="Club Rep")
                user.groups.add(userGroup)
                request.session['new_cr'] = newCr.club_rep_num
                request.session['new_club'] = newCr.club.name
                request.session['successful_creation'] = True
                return redirect("/rep_success")
    context['form'] = form
    context['userform'] = userForm
    return render(request, "uweflix/add_rep.html", context)

# The function `rep_success` renders a success page after a Club Representative is successfully created. 
# It checks whether the `successful_creation` flag is set in the session data, and raises a 404 error 
# if it is not. If the flag is set, it deletes the flag from the session data and renders the success page.
def rep_success(request):
    if 'successful_creation' not in request.session:
        raise Http404("Forbidden access to this page.")
    del request.session['successful_creation']
    return render(request, "uweflix/rep_success.html")

# This is a Django view function called `review_students` that takes a `userID` parameter in the URL. 
# It displays a list of students who have registered on the website and are awaiting review. The function 
# sets a default student to be reviewed if none is specified in the URL. The user can change the student 
# to review by selecting a different one from the list. If the user clicks accept or deny, the function 
# updates the database accordingly and redirects back to the default student. If the form is being 
# submitted via POST, the function updates the database based on the button clicked and redirects 
# back to the default student. The function renders the template `UweFlix/review_students.html` with 
# the `context` dictionary containing the list of students, the chosen student, and the URL ID.
def review_students(request, userID):
    print(userID)
    students = User.objects.filter(is_active=False)
    studentChoice = students.first()
    if userID == 0 and studentChoice is not None:
        return redirect('review_students', userID=studentChoice.id)
    if userID != 0:
        studentChoice = User.objects.get(id = userID)
    context = {
        'students' : students,
        'chosenStudent' : studentChoice,
        'urlID' : userID
    }
    if (request.method == "POST"):
        name = request.POST.get('name')
        if name == "changeStudent":
            studentID = request.POST['ReviewStudentForm']
            studentChoice = User.objects.get(id = studentID)
            return redirect('review_students', userID=studentChoice.id)
        else:
            if name == "acceptStudent":
                User.objects.filter(id=userID).update(is_active=True)
            elif name == "denyStudent":
                studentChoice.delete()
            students = User.objects.filter(is_active=False)
            studentChoice = students.first()
            return redirect('review_students', userID=0)
    return render(request, "UweFlix/review_students.html", context)

# The `view_order_history` function allows a Club Rep or a Student to view their order history within a 
# selected date range. The function first renders a DateIntervalForm and prompts the user to select a 
# date range to view their transactions. Once submitted, the function retrieves the user's transaction
# history and returns it to the user. If there are no transactions made during the specified date 
# range, the function returns a message indicating that no transactions were made during that period. 
# If the user is not authenticated, they are redirected to the login page.
def view_order_history(request):
    form = DateIntervalForm()
    titleText = "Please select a date range to view transactions for:"
    context = {
        'form': form,
        'title_text': titleText}
    if request.method == "POST":
        user = None
        if request.session["user_group"] == "Club Rep":
            user = ClubRep.objects.get(user_id=request.session["user_id"])
        elif request.session["user_group"] == "Student":
            user = Customer.objects.get(user=request.session["user_id"])
        if user is not None:
            form = DateIntervalForm(request.POST)
            if form.is_valid():
                startDate = form.cleaned_data['startDate']
                endDate = form.cleaned_data['endDate']
                transaction_list = Transaction.objects.filter(customer=user, date__range = (startDate, endDate))
                if not transaction_list:
                    titleText = f"There were no transactions made in your date range"
                    context = {
                        'form': form,
                        'title_text': titleText
                    }
                else:
                    context = {
                        'start_date': startDate,
                        'end_date': endDate,
                        'transaction_list': transaction_list,
                        'form': form
                    }
                form = DateIntervalForm()
            return render(request, "UweFlix/view_order_history.html", context)
        else:
            form = DateIntervalForm()
            titleText = "Please select a date range to view transactions for:"
            context = {
                'form': form,
                'title_text': titleText}
            return render(request, "UweFlix/view_order_history.html", context)
    else:
        return render(request, "UweFlix/view_order_history.html", context)

# The `change_ticket_prices` function takes in a `request` object and returns an HTTP response with a rendered
# template. The function initializes a `ChangePriceForm` instance and a `context` dictionary containing the 
# form. If the HTTP request method is "POST," the function attempts to validate the form data. If the form 
# is valid, the function calls the `changePrices` function of the `Prices` class with the cleaned data values
# for adult, student, and child ticket prices. The function then updates the `context` dictionary with a 
# confirmation message containing the new ticket prices and renders the template with the updated `context` 
# dictionary.
def change_ticket_prices(request):
    form = ChangePriceForm()
    context = {
        'form':form
    }
    if request.method=="POST":
        form = ChangePriceForm (request.POST)
        if form.is_valid():
            Prices.changePrices(form.cleaned_data['adult'],form.cleaned_data['student'], form.cleaned_data['child'])
            adult,student,child=Prices.getCurrentPrices()
            context['confirm'] = f"Prices confirmed. New ticket prices: \nAdult = £{adult}\nStudent = £{student}\nChild = £{child}"
    return render(request, "uweflix/change_ticket_prices.html", context)

# The `request_cancellation` function is used to handle user requests for ticket cancellations. It retrieves 
# the user's transaction history from the database and filters out any transactions that have already been 
# requested for cancellation. It then groups the tickets by showing time, ticket type, and transaction 
# number, and passes them to the template for display. If the user submits a request for cancellation, 
# the function updates the transaction status in the database and redirects the user back to the 
# cancellation request page.
def request_cancellation(request):
    now = timezone.now()
    user = None
    showingsToCancel = []
    adultTickets = []
    childTickets = []
    studentTickets = []
    if request.session["user_group"] == "Club Rep":
        user = ClubRep.objects.get(user_id=request.session["user_id"])
    elif request.session["user_group"] == "Student":
        user = Customer.objects.get(user=request.session["user_id"])
    if user is not None:
        transaction_list = Transaction.objects.filter(customer=user, request_to_cancel=False)
        for purchase in transaction_list:
            allTickets = Ticket.objects.filter(transaction=purchase)
            ticket = allTickets.first()
            if ticket is not None:
                showingTime = ticket.showing.time
                if showingTime > now:
                    showingsToCancel.append(ticket)
                    adultTickets.append(len(allTickets.filter(ticket_type="adult")))
                    childTickets.append(len(allTickets.filter(ticket_type="child")))
                    studentTickets.append(len(allTickets.filter(ticket_type="student")))
    zippedList = zip(showingsToCancel, adultTickets, childTickets, studentTickets)
    context = {
        'zipped': zippedList
    }
    if request.method == "POST":
        requestedTransaction = Transaction.objects.filter(id=request.POST.get('transaction_number'))
        requestedTransaction.update(request_to_cancel=True)
        return redirect('request_cancellation') 
    return render(request, "uweflix/request_cancellation.html", context)

# The `approve_cancellation` function is a view in a Django web application that handles the approval of 
# ticket cancellations requested by customers. It first retrieves a list of transactions that have been 
# requested for cancellation, then checks if the tickets are still valid for cancellation (i.e., 
# the showing time has not passed). The view then renders a template with a list of tickets that can 
# be approved for cancellation. 

# If the user approves a cancellation request, the function retrieves the corresponding transaction and 
# calculates the total cost of the transaction. If the transaction has already been settled, the customer 
# is refunded the transaction cost, which is added to their credit. The function then updates the 
# remaining tickets for the corresponding showing and deletes the transaction from the database. 
# The view then redirects to the approve_cancellation page.
def approve_cancellation(request):
    now = timezone.now()
    user = None
    showingsToCancel = []
    adultTickets = []
    childTickets = []
    studentTickets = []
    transaction_list = Transaction.objects.filter(request_to_cancel=True)
    for purchase in transaction_list:
        allTickets = Ticket.objects.filter(transaction=purchase)
        ticket = allTickets.first()
        if ticket is not None:
            showingTime = ticket.showing.time
            if showingTime > now:
                showingsToCancel.append(ticket)
                adultTickets.append(len(allTickets.filter(ticket_type="adult")))
                childTickets.append(len(allTickets.filter(ticket_type="child")))
                studentTickets.append(len(allTickets.filter(ticket_type="student")))
    zippedList = zip(showingsToCancel, adultTickets, childTickets, studentTickets)
    context = {
        'zipped': zippedList
    }
    if request.method == "POST":
        requestedTransaction = Transaction.getTransaction(request.POST.get('transaction_number'))
        ticketList = Ticket.objects.filter(transaction=requestedTransaction.id)
        totalTickets = ticketList.count()
        transactionCost = requestedTransaction.cost
        if requestedTransaction.customer is not None:
            customer = Customer.objects.get(id=requestedTransaction.customer.id)
            if requestedTransaction.is_settled == True:
                customer.credit += transactionCost
                customer.save()
        showing = ticketList.first().showing
        showing.remaining_tickets += totalTickets
        showing.save()
        Transaction.deleteTransaction(requestedTransaction.id)
        return redirect('approve_cancellations') 
    return render(request, "uweflix/approve_cancellations.html", context)
