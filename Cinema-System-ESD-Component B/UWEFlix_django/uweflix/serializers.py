from rest_framework import serializers
from .models import Club, ClubRep, Customer, Film, Prices, Screen, Showing, Ticket, Transaction

# This code snippet is importing serializers from Django's REST framework and some models from the project's 
# own models module. Then, it defines three serializer classes: FilmSerializer, ScreenSerializer, and 
# ClubSerializer, all of them inherit from ModelSerializer. These serializers specify which fields of 
# each model should be serialized and sent over the API. FilmSerializer includes fields for a Film model, 
# ScreenSerializer includes fields for a Screen model, and ClubSerializer includes fields for a Club model.

class FilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = ('id', 'title', 'age_rating', 'duration', 'trailer_desc', 'image')

class ScreenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Screen
        fields = ('id', 'capacity', 'apply_covid_restrictions')

class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ('name', 'street_number', 'street', 'city', 'post_code', 'landline_number',
                  'mobile_number', 'email', 'card_number', 'card_expiry_date', 'discount_rate')
