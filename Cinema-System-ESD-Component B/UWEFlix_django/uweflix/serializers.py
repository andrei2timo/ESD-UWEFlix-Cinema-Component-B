from rest_framework import serializers
from .models import Club, Customer, Film, Prices, Screen, Showing, Ticket, Transaction


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('user', 'dob', 'credit')


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('customer', 'date', 'cost',
                  'is_settled', 'request_to_cancel')


class FilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = ('title', 'age_rating', 'duration', 'trailer_desc', 'image')


class ScreenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Screen
        fields = ('capacity', 'apply_covid_restrictions')


class ShowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Showing
        fields = ('screen', 'film', 'time', 'remaining_tickets')


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('transaction', 'showing', 'ticket_type')


class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ('name', 'street_number', 'street', 'city', 'post_code', 'landline_number',
                  'mobile_number', 'email', 'card_number', 'card_expiry_date', 'discount_rate')


class PricesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prices
        fields = ('adult', 'student', 'child')
