from rest_framework import serializers
from .models import Club, ClubRep, Customer, Film, Prices, Screen, Showing, Ticket, Transaction

class FilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = ('title', 'age_rating', 'duration', 'trailer_desc', 'image')

class ScreenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Screen
        fields = ('capacity', 'apply_covid_restrictions')

class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ('name', 'street_number', 'street', 'city', 'post_code', 'landline_number',
                  'mobile_number', 'email', 'card_number', 'card_expiry_date', 'discount_rate')
