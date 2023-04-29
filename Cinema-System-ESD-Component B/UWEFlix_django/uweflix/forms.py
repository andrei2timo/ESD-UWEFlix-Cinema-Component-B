from django import forms
from uweflix.models import *
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator
from django.utils.safestring import mark_safe
from django.db.models import Count
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from datetime import datetime
from datetime import date
import time
import calendar

"""class EnterClubRepForm(forms.ModelForm):
    class Meta:
        model = ClubRep"""

# The DiscountForm class defines a Django form that allows a user to select a ClubRep object and 
# enter a discount value. The form has two fields: club_rep is a dropdown list of all ClubRep 
# objects in the database, and discountValue is a field for entering an integer discount value.
# This form can be used to collect input from users to create or update a discount record 
# for a particular ClubRep. The club_rep field is used to determine which ClubRep the 
# discount should apply to, and the discountValue field is used to set the value of the discount.
class DiscountForm(forms.Form):
    club_rep = forms.ModelChoiceField(queryset=ClubRep.objects.all(), label="Select Club Rep")
    discountValue = forms.IntegerField(label="Discount Value")

# The SearchClubRepForm class defines a Django form for searching for a specific ClubRep object 
# and choosing a time range statement. The form has two fields: clubrep_choice is a dropdown list
# of all ClubRep objects in the database, and timerange_choice is a dropdown list of statement 
# options, which include Monthly or Annual.
# The clubrep_choices variable is created by iterating over all ClubRep objects in the database 
# and creating a tuple for each object with its club_rep_num and the ClubRep object itself. 
# These tuples are then added to the clubrep_choices tuple of tuples.
# This form can be used to collect input from users to search for a specific ClubRep 
# object and select a statement time range. The clubrep_choice field is used to determine 
# which ClubRep object the user wants to view statements for, and the timerange_choice 
# field is used to determine whether the user wants to view Monthly or Annual statements.
class SearchClubRepForm(forms.Form):
    clubrep_choices = ()
    timerange_choices = ((None, "Select a statement:"),
                         ("Month", "Monthly Statement"),
                         ("Year", "Annual Statement"))
    for i in ClubRep.objects.all():
        tmp = ((i.club_rep_num, i),)
        clubrep_choices += tmp
    clubrep_choice = forms.ChoiceField(choices=clubrep_choices)
    timerange_choice = forms.ChoiceField(choices=timerange_choices)

# This class defines a custom user creation form that inherits from the built-in UserCreationForm provided by 
# Django. The form includes fields for the username, email, first name, and last name of a user. 
# The Meta class specifies that the form should use the built-in User model provided by Django.
# The __init__ method of the form initializes the form object and sets the help_text property of the password1
# and password2 fields to None, effectively hiding the default help text that Django provides for password 
# fields.
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['password1', 'password2']:
            self.fields[fieldname].help_text = None

# This code defines a custom user change form that inherits from the built-in UserChangeForm provided by 
# Django. The form includes fields for the username, email, first name, and last name of a user. 
# The Meta class specifies that the form should use the built-in User model provided by Django.
# This form is used to edit existing user information, and the fields available for editing match the 
# fields defined in the fields tuple of the Meta class. The CustomUserChangeForm form is used to 
# customize the default behavior of the built-in Django forms and tailor them to the specific needs of the app.
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username','email', 'first_name', 'last_name')

# This code defines a model form for registering a club representative in a web application. The form inherits
# from forms.ModelForm provided by Django.
# The Meta class specifies that the form should use the ClubRep model, which likely has fields for the club, 
# club representative number, and date of birth. The fields tuple specifies which fields of the model should 
# be included in the form.
# The dob field is further customized using forms.DateField and a widget parameter that specifies a DateInput 
# widget. This widget provides a visual interface for selecting a date.
# Overall, this form is used to collect information about a club representative and register them in the 
# web application.
class RegisterClubRepForm(forms.ModelForm):
    class Meta:
        model = ClubRep
        fields = ('club', 'club_rep_num', 'dob')
        dob = forms.DateField(widget=forms.DateInput())

# This code defines a model form for registering a student in a web application.
# The Meta class specifies that the form should use the Customer model, which likely has fields for the 
# student's information such as their name, address, and date of birth. However, in this case, the 
# fields tuple only includes the dob field, indicating that only the student's date of birth is 
# needed for registration.
# Overall, this form is used to collect information about a student's date of birth in order to register 
# them in the web application. It is possible that additional forms or fields are used to collect other 
# information about the student at a later stage in the registration process.
class RegisterStudentForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('dob',)

# The code defines a Django form called "DatePickerForm" that has a single field "date", which is a DateField that is not required.
class DatePickerForm(forms.Form):
    date = forms.DateField(required=False)

# This is a Django form class called DateIntervalForm that contains two fields for capturing start and end 
# dates, respectively. The startDate field is required while the endDate field is optional.
class DateIntervalForm(forms.Form):
    startDate = forms.DateField(required=True)
    endDate = forms.DateField(required=False)

# This code defines a form with a single field that allows the user to select a user from a list of choices. 
# The list of choices is generated dynamically from all the User objects in the database.
class SelectUserForm(forms.Form):
    user_choices = ()
    for i in User.objects.all():
        tmp = ((i, i),)
        user_choices += tmp
    user = forms.ChoiceField(choices=user_choices)
    
# The AccessClubForm class is a form for users to access a club by providing their card details. It 
# contains fields for the club name, card number, expiry month, and expiry year. The form also has a 
# validation method that ensures the provided card number is valid and has 16 digits, the expiry date 
# is not in the past, and a club has been selected. The selected club and payment details are printed, 
# and the cleaned data is returned.
class AccessClubForm(forms.Form):
    today = date.today()
    club_choices = ((None, "Select a club:"),) + \
        tuple((club.id, club.name) for club in Club.objects.all())
    month_choices = ((i, f"{i:02d}") for i in range(1, 13))
    year_choices = ((i, str(i)) for i in range(today.year, today.year+15))
    club = forms.ChoiceField(choices=club_choices)
    card_number = forms.DecimalField(max_digits=16, decimal_places=0)
    expiry_month = forms.ChoiceField(choices=month_choices)
    expiry_year = forms.ChoiceField(choices=year_choices)

    def clean(self):
        club = self.cleaned_data.get('club')
        if not club:
            raise forms.ValidationError("Club is required.")

        card_number = self.cleaned_data.get('card_number')
        expiry_month = self.cleaned_data.get('expiry_month')
        expiry_year = self.cleaned_data.get('expiry_year')

        try:
            if len(str(int(card_number))) < 16:
                raise forms.ValidationError(
                    "Card number is less than 16 digits.")
        except:
            raise forms.ValidationError(
                "Card number is invalid. It must be 16 digits.")

        expiry_date = date(int(expiry_year), int(expiry_month), calendar.monthrange(
            int(expiry_year), int(expiry_month))[1])
        if expiry_date < date.today():
            raise forms.ValidationError(
                "The expiry date entered has already passed.")

        # Print out the selected club and payment details
        print(f"Selected club: {club}")
        print(
            f"Payment details - Card number: {card_number}, Expiry: {expiry_month}/{expiry_year}")

        return self.cleaned_data

# The `PaymentForm` is a form that allows users to select the number of adult, student, and child tickets 
# they want to purchase. It also displays the total cost of the selected tickets and allows the user 
# to choose from payment options. The form includes validation to ensure that at least one type 
# of ticket is purchased. The payment options are 'Customer: Pay with Card', 'Student: Pay with Credit', 
# and 'Select an option' which is the default. The `__setchoices__` method can be used to set new payment 
# options.
class PaymentForm(forms.Form):
    adult_tickets = forms.IntegerField(validators=[
        MaxValueValidator(100),
        MinValueValidator(0)
    ],required=False, initial=0)
    student_tickets = forms.IntegerField(validators=[
        MaxValueValidator(100),
        MinValueValidator(0)
    ],required=False, initial=0)
    child_tickets = forms.IntegerField(validators=[
        MaxValueValidator(100),
        MinValueValidator(0)
    ],required=False, initial=0)
    total_cost=forms.FloatField(label="Total Cost: ", disabled=True, required=False)
    payment_choices = [(None, 'Select an option:'),
                    ('nopay', 'Customer: Pay with Card'),
                    ('credit', 'Student: Pay with Credit'), ]
    payment_options = forms.ChoiceField(choices=payment_choices, widget=forms.Select(attrs={}))
    def clean(self):
        adult_tickets = self.cleaned_data.get('adult_tickets')
        student_tickets = self.cleaned_data.get('student_tickets')
        child_tickets = self.cleaned_data.get('child_tickets')
        if adult_tickets == 0 and student_tickets == 0 and child_tickets == 0:
            raise forms.ValidationError("You must purchase at least one ticket type.")
        return self.cleaned_data

    def __setchoices__(self, newvalue):
        self.payment_choices = newvalue

# This code defines a form for club representatives to make a payment for student tickets. 
# The form includes fields for the number of student tickets and the total cost, as well as a choice 
# field for payment options such as credit or adding to a monthly bill. The clean method ensures that 
# at least one student ticket is purchased, and the __setchoices__ method allows for updating the 
# payment options available.
class RepPaymentForm(forms.Form):
    rep_student_tickets = forms.IntegerField(validators=[
        MaxValueValidator(100),
        MinValueValidator(10)
    ],required=False, initial=0)
    total_cost=forms.FloatField(label="Total Cost: ", disabled=True, required=False)
    payment_choices = [(None, 'Select an option:'),
                    ('credit', 'Club Reps: Pay with Credit'), 
                    ('tab', 'Club Reps: Add to monthly bill')]
    payment_options = forms.ChoiceField(choices=payment_choices, widget=forms.Select(attrs={}))
    def clean(self):
        student_tickets = self.cleaned_data.get('student_tickets')
        if student_tickets == 0:
            raise forms.ValidationError("You must purchase at least one ticket type.")
        return self.cleaned_data

    def __setchoices__(self, newvalue):
        self.payment_choices = newvalue

# This form class allows a user to select a user from a list of all User objects in the database. 
# It populates the user_choices tuple with a list of tuples where each tuple contains the User 
# object's ID and name as a string. The form field user is a ChoiceField that uses the user_choices 
# tuple as its list of options.
class SelectUserForm(forms.Form):
    user_choices = ()
    for i in User.objects.all():
        tmp = ((i, i),)
        user_choices += tmp
    user = forms.ChoiceField(choices=user_choices)

#The `addClubForm` is a Django ModelForm used for adding a new club to a database. The form includes 
# all fields of the `Club` model except for `card_number`, `card_expiry_date`, and `discount_rate`. 
# These excluded fields will not be shown in the form.
class addClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = "__all__"
        exclude = "card_number", "card_expiry_date", "discount_rate"

# The addRepForm is a Django form used to create or update a ClubRep model instance. It is a ModelForm 
# that inherits from forms.ModelForm and specifies the model to be used as ClubRep. The form includes 
# all the fields of the model (fields = "__all__") except for user, credit, and club_rep_num, which 
# are excluded using the exclude attribute. This form allows creating or updating ClubRep instances 
# with ease, by automatically generating the form fields based on the model definition.
class addRepForm(forms.ModelForm):
    class Meta:
        model = ClubRep
        fields = "__all__"
        exclude = "user", "credit", "club_rep_num"

# The `ClubRepCreationForm` is a form that inherits from `CustomUserCreationForm` and is used to create a 
# new `User` object with the role of a `ClubRep`. It only includes the `first_name` and `last_name` 
# fields in the form, and has a `Meta` class that specifies the `User` model as the model to be used, 
# and the `first_name` and `last_name` fields as the only fields to be displayed in the form.
class ClubRepCreationForm(CustomUserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name',)

# The `CardPaymentForm` is a form used for collecting credit card information. It includes fields for 
# the card number, expiry month, and expiry year. The form also includes a `clean` method which validates 
# the entered card number and expiry date. If the card number is not exactly 16 digits, a validation error
# is raised. If the expiry date has already passed, another validation error is raised.
class CardPaymentForm(forms.Form):
    today = date.today()
    month_choices = ()
    year_choices = ()
    current_year = today.year
    for i in range(12):
        choice_string = ""
        if i < 9:
            choice_string += "0"
        tmp = ((i+1, choice_string+str(i+1)),)
        month_choices += tmp
    for i in range(15):
        tmp = ((current_year+i,current_year+i),)
        year_choices += tmp
    card_number = forms.DecimalField(max_digits=16, decimal_places=0)
    expiry_month = forms.ChoiceField(choices=month_choices)
    expiry_year = forms.ChoiceField(choices=year_choices)

    def clean(self):
        card_number = self.cleaned_data.get('card_number')
        expiry_month = self.cleaned_data.get('expiry_month')
        expiry_year = self.cleaned_data.get('expiry_year')
        try:
            if len(str(int(card_number))) < 16:
                raise forms.ValidationError("Card number is less than 16 digits.")
        except:
            raise forms.ValidationError("Card number is invalid. It must be 16 digits.")
        expiry_date = date(int(expiry_year), int(expiry_month), calendar.monthrange(int(expiry_year), int(expiry_month))[1])
        if expiry_date < self.today:
            raise forms.ValidationError("The expiry date entered has already passed.")
        return self.cleaned_data

# The ChangePriceForm is a ModelForm that is used to change the prices of different ticket types. 
# It is associated with the Prices model and includes all the fields of the model. The form allows 
# users to edit the price of different ticket types by updating the corresponding fields.
class ChangePriceForm(forms.ModelForm):
   class Meta:
        model = Prices
        fields = "__all__"

# The `addShowingForm` class is a Django ModelForm used for adding a new `Showing` object to the database. 
# It includes all the fields defined in the `Showing` model, except for the `remaining_tickets` field, 
# which is automatically calculated based on the number of tickets sold. This form is used to create 
# new showings for a movie theater, with fields for the movie, date, time, and theater number.
class addShowingForm(forms.ModelForm):
    class Meta:
        model = Showing
        fields = "__all__"
        exclude = ('remaining_tickets',)

# The `editShowingForm` is a Django ModelForm that allows users to edit an existing instance of the 
# `Showing` model. The form includes all fields of the `Showing` model, except for the `remaining_tickets` 
# field. Users can make changes to the values of these fields and submit the form to update the 
# corresponding `Showing` object in the database.    
class editShowingForm(forms.ModelForm):
    class Meta:
        model = Showing
        fields = "__all__"
        exclude = ('remaining_tickets',)

# The `deleteFilmForm` class is a form in Django that presents a dropdown list of films to choose from, 
# to delete a film. It is created using the `forms.Form` base class and has a single field called `film`, 
# which is a `forms.ChoiceField` object. The choices for this field are obtained by querying the `Film` 
# model and dynamically generating a tuple of (id, title) pairs, with a default choice of "Select a film:".
class deleteFilmForm(forms.Form):
    film_choices = ((None, "Select a film:"),)
    for i in Film.objects.all():
        tmp = ((i.id, i.title),)
        film_choices += tmp
    film = forms.ChoiceField(choices=film_choices)

# The `addScreenForm` is a Django ModelForm for creating new Screen instances. It is associated with 
# the `Screen` model and includes all of its fields. The form also defines `age_rating_choices`, 
# an empty tuple that is used to populate the choices for the `age_rating` field in the form.
class addScreenForm(forms.ModelForm):
    age_rating_choices = ()
    class Meta:
        model = Screen
        fields = "__all__"

# The `editScreenForm` class is a Django ModelForm used to edit a `Screen` instance. It specifies that the 
# form should include the `capacity` and `apply_covid_restrictions` fields of the `Screen` model. 
# It also defines the widgets to use for these fields, such as a NumberInput widget for the `capacity` 
# field with a placeholder, and a CheckboxInput widget for the `apply_covid_restrictions` field with a 
# CSS class.
class editScreenForm(forms.ModelForm):
    class Meta:
        model = Screen
        fields = ('capacity', 'apply_covid_restrictions')
        widgets = {
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Screen capacity'}),
            'apply_covid_restrictions': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

# The `EditFilmForm` is a form class used to edit the details of a film. It is a subclass of 
# `forms.ModelForm`, which is a form class that creates a form based on a Django model. The form includes 
# fields for the film's `title`, `genre`, `year`, `description`, and `poster`. Each field is given a 
# widget to specify the type of input that should be used (e.g., `TextInput` for `title` and `genre`, 
# `NumberInput` for `year`, `Textarea` for `description`, and `FileInput` for `poster`). The form is 
# bound to the `Film` model, and the `fields` attribute is set to a tuple of the fields to include 
# in the form.
class EditFilmForm(forms.ModelForm):
    class Meta:
        model = Film
        fields = ('title', 'genre', 'year', 'description', 'poster')

    title = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    genre = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    year = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    poster = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
