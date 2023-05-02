from email import charset
from pyexpat import model
from tokenize import String
from xml.dom.minidom import CharacterData
from django.db import models
from django.contrib.auth.models import *
from datetime import datetime as dt
import datetime
import random
from django.utils import timezone

from django.forms import ValidationError

class User(AbstractUser):
    pass

# The `Customer` model represents a user account for a student in a system. It inherits from the `models.Model` 
# class and has three fields: `user` which is a `OneToOneField` that relates the customer to a user 
# account, `dob` which represents the date of birth of the customer, and `credit` which is a 
# `FloatField` that represents the amount of credit the customer has. The `dob` field has a 
# custom label of "Date of birth". The `credit` field has a default value of 0.00.
class Customer(models.Model):  # Student accounts
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField('Date of birth')
    credit = models.FloatField(default=0.00)

# The class Transaction models a database for storing transactions that are to be analyzed by an Account 
# Manager. It has fields for the customer responsible for the transaction, the date of the transaction, 
# the cost of the transaction, whether the transaction has been paid, and whether the transaction is 
# requested to be canceled.
    # newTransaction(cust, cost, is_paid): This method creates a new transaction object with the provided 
    # customer, cost, and paid status, and returns the newly created transaction object. If the creation 
    # fails, it prints an error message.

    # getTransaction(id): This method retrieves the transaction object with the provided transaction ID, 
    # and returns the transaction object. If the transaction does not exist, it prints an error message.

    # updateTransaction(id, *transaction_data): This method updates the transaction object with the provided 
    # transaction ID with the provided transaction data. The transaction data can be a Customer object, 
    # a datetime.date object, a float, or a bool, and is determined by the data type of the input. 
    # It returns the updated transaction object. If the update fails or if the data item does not 
    # conform to any of the required input types, it prints an error message.

    # deleteTransaction(id): This method deletes the transaction object with the provided transaction ID. 
    # If the transaction does not exist or has an issue being deleted, it prints an error message.
class Transaction(models.Model):  # Database for storing all of the 'accounts' to be analysed by Account Manager
    customer = models.ForeignKey(Customer, blank=True, null=True, default=None, on_delete=models.SET_DEFAULT)  # User responsible for the transaction
    date = models.DateField()  # Date of transaction
    cost = models.FloatField()  # Cost of transaction
    is_settled = models.BooleanField()  # Whether the transaction has been paid
    request_to_cancel = models.BooleanField(default=False)
    def newTransaction(cust, cost, is_paid): #CREATE
        try:
            transaction = Transaction.objects.create(customer=cust, date=dt.today(), cost=cost, is_settled=is_paid)
            return transaction
        except:
            print("Transaction object could not be created.")

    def getTransaction(id): #READ
        try:
            transaction = Transaction.objects.get(id=id)
            return transaction
        except:
            print("No transaction exists with that transaction ID.")

    def updateTransaction(id, *transaction_data): #UPDATE
        try:
            for data_item in transaction_data:
                if isinstance(data_item, Customer):
                    Transaction.objects.filter(pk=id).update(customer=data_item)
                elif isinstance(data_item, datetime.date):
                    Transaction.objects.filter(pk=id).update(date=data_item)
                elif isinstance(data_item, float):
                    Transaction.objects.filter(pk=id).update(cost=data_item)
                elif isinstance(data_item, bool):
                    Transaction.objects.filter(pk=id).update(is_settled=data_item)
                else:
                    print(f"Data item {data_item} does not conform to any of the required input types." +
                    "\nThis value could not be updated.")
            return Transaction.objects.get(id=id)
        except:
            print("An error occurred when updating this object.")

    def deleteTransaction(id): #DELETE
        try:
            transaction = Transaction.objects.get(id=id)
            transaction.delete()
        except:
            print("This transaction does not exist, or had an issue being deleted.")

# The `Film` class is a model for storing information about films in a cinema. It has fields for the film's 
# `title`, `age_rating`, `duration`, `trailer_desc`, and `image`. It also has methods for creating, reading,
# updating and deleting films.

    # - `newFilm(title, age_rating, duration, trailer_desc)`: creates a new film with the given attributes and 
    # returns it, or prints an error message if the creation fails.

    # - `getFilm(id)`: retrieves and returns the film with the given ID, or prints an error message if the 
    # film could not be found.

    # - `removeFilm(id)`: deletes the film with the given ID if it exists and has no associated showings, 
    # or prints an error message if the film could not be deleted or has showings.

    # - `updateFilm(id, fieldToEdit)`: updates the fields of the film with the given ID based on the values 
    # in the `fieldToEdit` dictionary. If the update is successful, returns the updated film, 
    # or prints an error message if it fails.

    # - `__str__(self)`: returns the title of the film as a string.
class Film(models.Model):
    title = models.CharField(max_length=100)
    age_rating = models.CharField(max_length=3)
    """Age Ratings:
        - U
        - PG
        - 12
        - 12A
        - 15
        - 18"""
    duration = models.CharField(max_length=3)
    # Store duration in minutes only (e.g. 120)
    trailer_desc = models.CharField(max_length=500)
    image = models.ImageField(default="placeholder.png")

    def newFilm (title, age_rating, duration, trailer_desc): #create
        try:
            film = Film.objects.create(title=title,age_rating=age_rating, duration=duration, trailer_desc=trailer_desc)
            return film
        except:
            print("Film could not be added")

    def getFilm(id): #read
        try:
            film = film.objects.get(id=id)
            return film
        except:
            print("Film could not be found")


    def removeFilm(id): #Delete
        try:
            film = Film.objects.get(id=id)
            if not Showing.objects.exists(film=film):
                film.delete()
            else:
                print ("Selected film has showings, couldn't be deleted")      
        except:
            print("Film could not be deleted, and may not exist")

    def updateFilm(id, fieldToEdit): #update
        try:
            for field in fieldToEdit:
                if isinstance(field, int):
                    Film.objects.filter(id=id).update(title=field)
                elif isinstance(field, bool):
                    Film.objects.filter(id=id).update(age_rating=field)
            return Film.objects.get(id=id)
        except:
            print("film could not be updated")

    def __str__(self):
        return self.title

# The `Screen` class represents a movie theater screen and has two attributes: `capacity` which is an integer 
# that represents the number of seats in the screen and `apply_covid_restrictions` which is a boolean that 
# indicates if there are any COVID-19 related restrictions applied to the screen. 

# The class provides four methods:

    # - `newScreen(seats, covidRestrictions)` is a create method that creates a new `Screen` object with the 
    # given parameters `seats` and `covidRestrictions`.

    # - `getScreen(id)` is a read method that retrieves a `Screen` object based on the given `id`.

    # - `updateScreen(id, fieldToEdit)` is an update method that updates the `Screen` object with the 
    # given `id` based on the value in `fieldToEdit`.

    # - `removeScreen(id)` is a delete method that removes a `Screen` object based on the given `id`.
class Screen(models.Model):
    capacity = models.IntegerField()
    apply_covid_restrictions =  models.BooleanField(null=True)

    def __str__(self):
        return "Screen " + str(self.id)

    def __str__(self):
        return "Screen " + str(self.id)

    def newScreen(seats, covidRestrictions): #Create
        try:
            screen = Screen.objects.create(capacity=seats, apply_covid_restrictions=covidRestrictions)
            return screen
        except:
            print("Screen cannot be created, perhaps you are missing some parameters?")

    def getScreen(id): #Read
        try:
            screen = Screen.objects.get(id=id)
            return screen
        except:
            print("Screen cannot be found, perhaps you have entered an incorrect id?")

    def updateScreen(id, fieldToEdit): #Update
        try:
            if isinstance(fieldToEdit, bool):
                Screen.objects.filter(id=id).update(apply_covid_restrictions=fieldToEdit)
            elif isinstance(fieldToEdit, (int, float)):
                Screen.objects.filter(id=id).update(capacity=fieldToEdit)
            return Screen.objects.get(id=id)
        except Exception as e:
            print("Screen cannot be found, perhaps you have entered an invalid field type?")
            print(e)

    def removeScreen(id): #Delete
        try:
            screen = Screen.objects.get(id=id)
            screen.delete()
        except:
            print("Screen cannot be found, perhaps you have entered an incorrect id?")

# The `Showing` class represents a movie showing, with information on the screen, the movie being shown, 
# the time of the showing, and the number of remaining tickets. 

    # - The `newShowing` method creates a new showing object with the given parameters and assigns the 
    # capacity of the screen to the `remaining_tickets` field. 
    # If the screen has Covid restrictions applied, the `remaining_tickets` field is divided by 2. 
    
    # - The `getShowing` method retrieves a showing object by its ID. 
    
    # - The `filmShowing` method updates a showing object's `screen`, `film`, `time`, `remaining_tickets` 
    # and `apply_covid_restrictions` fields with the given parameters. 
    
    # Finally, the `deleteShowing` method deletes a showing object from the database by its ID.
class Showing(models.Model):
    screen = models.ForeignKey(Screen, default=1, on_delete=models.CASCADE)
    film = models.ForeignKey(Film,on_delete=models.CASCADE)
    time = models.DateTimeField()
    remaining_tickets = models.IntegerField(default=150)  # NEEDS TO BE ASSIGNED TO THE SCREEN CAPACITY SOMEHOW!

    def newShowing(screen, film, time):#CREATE
        try:
            showing = Showing.objects.create(screen=screen, film=film, time=time, remaining_tickets=screen.capacity)
            if screen.apply_covid_restrictions == True:
                showing.remaining_tickets = showing.remaining_tickets / 2
                showing.save()
            return showing
        except:
            print("Showing object could not be created")

    def getShowing(id):#READ
        try:
            showing = Showing.objects.get(id=id)
            return showing
        except:
            print("No showinf exists with that showing ID.")

    def filmShowing(id, *showing_data): #UPDATE
        try:
            for data_item in showing_data:
                if isinstance(data_item, Screen):
                    Showing.objects.filter(pk=id).update(screen=data_item)
                elif isinstance(data_item, Film):
                    Showing.objects.filter(pk=id).update(film=data_item)
                elif isinstance(data_item, float):
                    Showing.objects.filter(pk=id).update(time=data_item)
                elif isinstance(data_item, int):
                    Showing.objects.filter(pk=id).update(remaining_tickets=data_item)
                elif isinstance(data_item, bool):
                    Showing.objects.filter(pk=id).update(apply_covid_restrictions=False)
                else:
                    print(f"Data item {data_item} does not confrom to any of the  required input types." +
                          "\nThis value could not be updated.")
            return Showing.objects.get(id=id)
        except:
            print("An error occurred when updating this object.")

    def deleteShowing(id): #DELETE
        try:
            showing = Showing.objects.get(id=id)
            showing.delete()
        except:
            print("This film Showing has Successfully been deleted.")
            
    def __str__(self):
        formatted_time = self.time.strftime("%Y-%m-%d %H:%M:%S")
        return f"{self.film.title} - {formatted_time}"

# The `Ticket` class is a model class that represents an individual ticket booking. It has fields for a 
# `transaction` foreign key, a `showing` foreign key, and a `ticket_type`. 

    # - The `newTicket` method creates a new ticket object with the given transaction, showing, and ticket 
    # type parameters. The `getTicket` method retrieves the ticket object with the given ID. 

    # - The `updateTicket` method updates the fields of the ticket object with the given ID based on the 
    # fieldToEdit parameter. 
    
    # - Finally, the `removeTicket` method deletes the ticket object with the given ID.
class Ticket(models.Model):  # Individual ticket booking database
    transaction = models.ForeignKey(Transaction, default=1, on_delete=models.SET_DEFAULT)
    showing = models.ForeignKey(Showing, default=1, on_delete=models.SET_DEFAULT)  # Screen the booking is being viewed at
    ticket_type = models.CharField(max_length=7)

    def newTicket(trans, show, type): #Create
        try:
            ticket = Ticket.objects.create(transaction=trans, showing=show, ticket_type=type)
            return ticket
        except:
            print("Ticket cannot be created, perhaps you are missing a parameter?")

    def getTicket(id): #Read
        try:
            ticket = Ticket.objects.get(id=id)
            return ticket
        except:
            print("Ticket cannot be found, perhaps you have entered an incorrect id?")

    def updateTicket(id, fieldToEdit): #Update
        try:
            for field in fieldToEdit:
                if isinstance(field, Transaction):
                    Ticket.objects.filter(id=id).update(transaction=field)
                elif isinstance(field, Showing):
                    Ticket.objects.filter(id=id).update(showing=field)
                elif isinstance(field, String):
                    Ticket.objects.filter(id=id).update(ticket_type=field)
            return Ticket.objects.get(id=id)
        except:
            print("Ticket cannot be updated, perhaps you have entered an invalid field type?")

    def removeTicket(id): #Delete
        try:
            ticket = Ticket.objects.get(id=id)
            ticket.delete()
        except:
            print("Ticket cannot be found, perhaps you have entered an invalid id?")

# The Club class represents a database table that stores information about a club. It has fields for the club 
# name, address details, contact details, and payment details. The class has methods for creating a 
# new club record in the database, retrieving an existing club record from the database, updating 
# a club record in the database, and deleting a club record from the database.

    # - The newClub method creates a new club record in the database;
    
    # - The getClub method retrieves an existing club record from the database based on an ID;
    
    # - The updateClub method updates an existing club record in the database based on an ID and the club data 
    #   to be updated, and the removeClub method deletes an existing club record from the database based on an ID.
class Club(models.Model):
    name = models.CharField(max_length=100)
    #Address details
    street_number = models.IntegerField()
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    post_code = models.CharField(max_length=8)
    #Contact details
    landline_number = models.CharField(max_length=11)
    mobile_number = models.CharField(max_length=11)
    email = models.EmailField()
    #Payment details
    card_number = models.IntegerField(blank=True, null=True)
    card_expiry_date = models.DateField(blank=True, null=True)
    discount_rate = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

    def newClub(club_name, address_street_num, address_street, address_city, address_postcode, contact_landline, contact_mobile, contact_email): #Create
        try:
            club = Club.objects.create(name=club_name, street_number=address_street_num, street=address_street, city=address_city, post_code=address_postcode, landline_number=contact_landline, mobile_number=contact_mobile, email=contact_email)
            return club
        except:
            print("Club can't be created")

    def getClub(id): #Read
        try:
            club = Club.objects.get(id=id)
            return club
        except:
            print("Club can't be found")

    def updateClub(id, *club_data): #Update
        try:
            for data_item in club_data:
                if data_item == 'name':
                    Club.objects.filter(id=id).update(name=data_item)
                elif data_item == 'card_number':
                    Club.objects.filter(id=id).update(card_number=data_item)
                elif data_item == 'card_expiry_date':
                    Club.objects.filter(id=id).update(card_expiry_date=data_item)
                elif data_item == 'discount_rate':
                    Club.objects.filter(id=id).update(discount_rate=data_item)
            return Club.objects.filter(id=id)
        except:
           print(f"Data item {data_item} does not conform to any of the required input types." +
                    "\nThis value could not be updated.")

    def removeClub(id): #Delete
        try:
            club = Club.objects.get(id=id)
            club.delete()
        except:
            print("Club can't be found, therefore can't be deleted")


class ClubRep(Customer):
    club = models.ForeignKey(Club, null=True, on_delete=models.CASCADE)
    club_rep_num = models.CharField(max_length=8)

    def __str__(self):
        return f"{self.club_rep_num} - {self.user.first_name} {self.user.last_name}"
    #first_name = models.CharField(max_length=30)
    #last_name = models.CharField(max_length=30)
    #"A unique Club Representative number and unique password is allocated to the
    #Club Representative."
    #Therefore:
    #- Unique CR number = username (inherited from User model), ensure that username is numbers only
    #- Unique CR password = password (inherited from User model)

# The `Prices` class represents the pricing information for different types of customers 
# (adult, student, and child). It has three attributes `adult`, `student`, and `child`, each 
# representing the price for that customer type. It also has two methods: 

    # - `changePrices` and `getCurrentPrices`. 
    # `changePrices` takes in new prices for each customer type and creates a new `Prices` object with those 
    # prices. `getCurrentPrices` retrieves the most recent `Prices` object and returns the prices for each 
    # customer type.
class Prices(models.Model):
    adult = models.FloatField(default=5.0)
    student = models.FloatField(default=4.0)
    child = models.FloatField(default=3.0)

    def changePrices(adult, student, child):
        Prices.objects.create(adult=adult, student=student, child=child)

    def getCurrentPrices():
        currentPrices = Prices.objects.last()
        return currentPrices.adult, currentPrices.student, currentPrices.child

# The `Account` class is a model for user accounts in a system, with fields for a random number generator, 
# first initial, last name, associated club, card number, and expiration date. It has a `__str__` 
# method to return the full name of the account holder. The `save` method is overridden to set a random 
# number generator for the account if one is not already assigned before saving the account object.
class Account(models.Model):
    random_num_generator = models.IntegerField(blank=True, null=True)
    first_initial = models.CharField(max_length=1, default='')
    last_name = models.CharField(max_length=50)
    club = models.ForeignKey('Club', on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16)
    expiry_year = models.IntegerField(default=timezone.now().year)
    expiry_month = models.CharField(max_length=2, default='')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if not self.random_num_generator:
            self.random_num_generator = random.randint(0000, 9999)
        super().save(*args, **kwargs)

