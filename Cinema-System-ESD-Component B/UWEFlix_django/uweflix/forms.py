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

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['password1', 'password2']:
            self.fields[fieldname].help_text = None

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username','email', 'first_name', 'last_name')

class RegisterClubRepForm(forms.ModelForm):
    class Meta:
        model = ClubRep
        fields = ('club', 'club_rep_num', 'dob')
        dob = forms.DateField(widget=forms.DateInput())

class RegisterStudentForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('dob',)

class DatePickerForm(forms.Form):
    date = forms.DateField(required=False)

class DateIntervalForm(forms.Form):
    startDate = forms.DateField(required=True)
    endDate = forms.DateField(required=False)

class SelectUserForm(forms.Form):
    user_choices = ()
    for i in User.objects.all():
        tmp = ((i, i),)
        user_choices += tmp
    user = forms.ChoiceField(choices=user_choices)
    

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

class SelectUserForm(forms.Form):
    user_choices = ()
    for i in User.objects.all():
        tmp = ((i, i),)
        user_choices += tmp
    user = forms.ChoiceField(choices=user_choices)


class addClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = "__all__"
        exclude = "card_number", "card_expiry_date", "discount_rate"

class addRepForm(forms.ModelForm):
    class Meta:
        model = ClubRep
        fields = "__all__"
        exclude = "user", "credit", "club_rep_num"

class ClubRepCreationForm(CustomUserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name',)

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

class ChangePriceForm(forms.ModelForm):
   class Meta:
        model = Prices
        fields = "__all__"

class addShowingForm(forms.ModelForm):
    class Meta:
        model = Showing
        fields = "__all__"
        exclude = ('remaining_tickets',)
    
class editShowingForm(forms.ModelForm):
    class Meta:
        model = Showing
        fields = "__all__"
        exclude = ('remaining_tickets',)

class deleteFilmForm(forms.Form):
    film_choices = ((None, "Select a film:"),)
    for i in Film.objects.all():
        tmp = ((i.id, i.title),)
        film_choices += tmp
    film = forms.ChoiceField(choices=film_choices)

class addScreenForm(forms.ModelForm):
    age_rating_choices = ()
    class Meta:
        model = Screen
        fields = "__all__"

class editScreenForm(forms.ModelForm):
    class Meta:
        model = Screen
        fields = ('capacity', 'apply_covid_restrictions')
        widgets = {
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Screen capacity'}),
            'apply_covid_restrictions': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class EditFilmForm(forms.ModelForm):
    class Meta:
        model = Film
        fields = ('title', 'genre', 'year', 'description', 'poster')

    title = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    genre = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    year = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    poster = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
