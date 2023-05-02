# Import necessary packages and modules
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Club, ClubRep, Customer, Film, Prices, Screen, Showing, Ticket, Transaction
from datetime import datetime, timedelta
from django.utils import timezone

# Define test cases for models
class ModelTests(TestCase):
    
    def setUp(self):
        self.club = Club.objects.create(name='Test Club', street_number='123', street='Main Street', city='Test City', 
                                         post_code='12345', landline_number='1234567890', mobile_number='0987654321', 
                                         email='test@test.com', card_number='1234567890123456', card_expiry_date='12/34', 
                                         discount_rate=10)
        self.club_rep = ClubRep.objects.create(first_name='Test', last_name='Club Rep', club=self.club, 
                                               email='test_club_rep@test.com', phone_number='1234567890')
        self.customer = Customer.objects.create(first_name='Test', last_name='Customer', email='test_customer@test.com',
                                                 phone_number='0987654321', club=self.club, birthday=datetime.now()-timedelta(days=365*30),
                                                 discount_eligible=True)
        self.film = Film.objects.create(title='Test Film', age_rating='12A', duration=120, trailer_desc='Test Trailer',
                                         image='https://test.com/test.png')
        self.screen = Screen.objects.create(number='1', capacity=100, apply_covid_restrictions=False)
        self.showing = Showing.objects.create(film=self.film, screen=self.screen, start_time=datetime.now(),
                                               end_time=datetime.now()+timedelta(minutes=120))
        self.prices = Prices.objects.create(club=self.club, adult_price=10, child_price=5, senior_price=8)
        self.ticket = Ticket.objects.create(showing=self.showing, customer=self.customer, price=10, seat='A1', 
                                             ticket_type='Adult', discount_applied=True)
        self.transaction = Transaction.objects.create(customer=self.customer, total=10, payment_method='Credit Card',
                                                       date=datetime.now(), club=self.club)

    def test_club_fields(self):
        self.assertEqual(self.club.name, 'Test Club')
        self.assertEqual(self.club.street_number, '123')
        self.assertEqual(self.club.street, 'Main Street')
        self.assertEqual(self.club.city, 'Test City')
        self.assertEqual(self.club.post_code, '12345')
        self.assertEqual(self.club.landline_number, '1234567890')
        self.assertEqual(self.club.mobile_number, '0987654321')
        self.assertEqual(self.club.email, 'test@test.com')
        self.assertEqual(self.club.card_number, '1234567890123456')
        self.assertEqual(self.club.card_expiry_date, '12/34')
        self.assertEqual(self.club.discount_rate, 10)

    def test_club_rep_fields(self):
        self.assertEqual(self.club_rep.first_name, 'Test')
        self.assertEqual(self.club_rep.last_name, 'Club Rep')
        self.assertEqual(self.club_rep.club, self.club)
        self.assertEqual(self.club_rep.email, 'test_club_rep@test.com')
        self.assertEqual(self.club_rep.phone_number, '1234567890')

    def test_customer_fields(self):
        self.assertEqual(self.customer.first_name, 'Test')
        self.assertEqual(self.customer.last_name, 'Customer')
        self.assertEqual(self.customer.email, 'test_customer@test.com')
        self.assertEqual(self.customer.phone, '0987654321')

class ClubModelTestCase(TestCase):
    def setUp(self):
        Club.objects.create(name="Test Club", street_number="123", street="Test St",
                             city="Test City", post_code="12345", landline_number="0123456789",
                             mobile_number="9876543210", email="testclub@test.com",
                             card_number="1234-5678-9012-3456", card_expiry_date="2025-12-31",
                             discount_rate=10)

    def test_club_str(self):
        club = Club.objects.get(name="Test Club")
        self.assertEqual(str(club), "Test Club")
        
    def test_club_discount(self):
        club = Club.objects.get(name="Test Club")
        self.assertEqual(club.get_discount(), 10)

class CustomerModelTestCase(TestCase):
    def setUp(self):
        Customer.objects.create(name="Test Customer", email="testcustomer@test.com")

    def test_customer_str(self):
        customer = Customer.objects.get(name="Test Customer")
        self.assertEqual(str(customer), "Test Customer")

class FilmModelTestCase(TestCase):
    def setUp(self):
        Film.objects.create(title="Test Film", age_rating=12, duration=120,
                             trailer_desc="Test trailer", image="test.png")

    def test_film_str(self):
        film = Film.objects.get(title="Test Film")
        self.assertEqual(str(film), "Test Film")

class ShowingModelTestCase(TestCase):
    def setUp(self):
        film = Film.objects.create(title="Test Film", age_rating=12, duration=120,
                                    trailer_desc="Test trailer", image="test.png")
        screen = Screen.objects.create(capacity=100, apply_covid_restrictions=False)
        Showing.objects.create(film=film, screen=screen, time=timezone.make_aware(datetime(2023, 5, 1, 14, 0, 0)))

    def test_showing_str(self):
        showing = Showing.objects.get(time=timezone.make_aware(datetime(2023, 5, 1, 14, 0, 0)))
        self.assertEqual(str(showing), "Test Film - 2023-05-01 14:00:00")

    def test_delete_showing(self):
        # Create a new showing for testing purposes
        film = Film.objects.create(title="Test Film 2", age_rating=12, duration=120,
                                trailer_desc="Test trailer 2", image="test2.png")
        screen = Screen.objects.create(capacity=100, apply_covid_restrictions=False)
        showing_to_delete = Showing.objects.create(film=film, screen=screen, time=timezone.make_aware(datetime(2023, 5, 2, 14, 0, 0)))

        # Delete the showing
        showing_to_delete.delete()

        # Test that the deleted showing no longer exists
        with self.assertRaises(Showing.DoesNotExist):
            Showing.objects.get(time=timezone.make_aware(datetime(2023, 5, 2, 14, 0, 0)))

        # Test that other showings still exist
        showing = Showing.objects.get(time=timezone.make_aware(datetime(2023, 5, 1, 14, 0, 0)))
        self.assertIsNotNone(showing)

class ScreenModelTestCase(TestCase):
    def setUp(self):
        Screen.objects.create(capacity=100, apply_covid_restrictions=False)

    def test_screen_str(self):
        screen = Screen.objects.get(capacity=100)
        self.assertEqual(str(screen), "Screen 1")

class TicketModelTestCase(TestCase):
    def setUp(self):
        customer = Customer.objects.create(name="Test Customer", email="testcustomer@test.com")
        showing = Showing.objects.create(film=Film.objects.create(title="Test Film", age_rating=12, duration=120,
                                                                    trailer_desc="Test trailer", image="test.png"),
                                          screen=Screen.objects.create(capacity=100, apply_covid_restrictions=False),
                                          date_time="2023-05-01 14:00:00")
        Ticket.objects.create(customer=customer, showing=showing, seat_number=1, price=10)

    def test_ticket_str(self):
        ticket = Ticket.objects.get(seat_number=1)
        self.assertEqual(str(ticket), "Test Film - 2023-05-01 14:00:00 - Seat 1")

class TransactionModelTestCase(TestCase):
    def setUp(self):
        customer = Customer.objects.create(name="Test Customer", email="testcustomer@test.com")
        transaction = Transaction.objects.create(customer=customer, total_amount=100)
        film = Film.objects.create(title="Test Film", age_rating=18, duration=120, trailer_desc="Test Trailer", image="test.png")
        screen = Screen.objects.create(name="Test Screen", capacity=100, apply_covid_restrictions=True)
        showing = Showing.objects.create(film=film, screen=screen, start_time="2023-04-26 18:00:00", end_time="2023-04-26 20:00:00")
        ticket = Ticket.objects.create(showing=showing, seat_number="A1", price=10, status="AVAILABLE")
        transaction.tickets.add(ticket)

    def test_transaction_str(self):
        transaction = Transaction.objects.first()
        self.assertEqual(str(transaction), f"Transaction #{transaction.id} ({transaction.customer.name}): {transaction.total_amount} USD")

    def test_transaction_tickets(self):
        transaction = Transaction.objects.first()
        self.assertEqual(transaction.tickets.count(), 1)
        self.assertEqual(transaction.tickets.first().showing.film.title, "Test Film")
        self.assertEqual(transaction.tickets.first().price, 10)

    def test_transaction_total_amount(self):
        transaction = Transaction.objects.first()
        self.assertEqual(transaction.total_amount, 10)

    def test_ticket_str(self):
        ticket = Ticket.objects.first()
        self.assertEqual(str(ticket), f"Ticket #{ticket.id} ({ticket.showing.film.title} - {ticket.showing.start_time.strftime('%Y-%m-%d %H:%M:%S')})")

    def test_ticket_book(self):
        ticket = Ticket.objects.first()
        ticket.book()
        self.assertEqual(ticket.status, "BOOKED")

    def test_ticket_cancel(self):
        ticket = Ticket.objects.first()
        ticket.cancel()
        self.assertEqual(ticket.status, "AVAILABLE")
