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
    club_choices = ((None, "Select a club:"),)
    month_choices = ()
    year_choices = ()
    current_year = today.year
    for i in range(Club.objects.all().count()):
        tmp = ((Club.objects.get(id=i+1).id, Club.objects.get(id=i+1).name),)
        club_choices += tmp
    for i in range(12):
        choice_string = ""
        if i < 9:
            choice_string += "0"
        tmp = ((i+1, choice_string+str(i+1)),)
        month_choices += tmp
    for i in range(15):
        tmp = ((current_year+i,current_year+i),)
        year_choices += tmp
    club = forms.ChoiceField(choices=club_choices)
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
