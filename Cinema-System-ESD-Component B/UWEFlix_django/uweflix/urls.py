from django.urls import path
from uweflix import views
from uweflix.models import *
from .views import *


urlpatterns = [
    path("club_discount/", views.clubdiscount, name="club_discount"),
    path("account_modify/", views.account_modify, name="account_modify"),
    path("manage_accounts/", views.manage_accounts, name="manage_accounts"),
    path('add_user', add_user, name='add_user'),
    path('delete_user/<int:myid>/', delete_user, name='delete_user'),
    path('edit_user/<int:myid>/', edit_user, name='edit_user'),
    path('update_user/<int:myid>/', update_user, name='update_user'),
    path('manage_club_account/', views.manage_club_account, name='manage_club_account'),
    path('add_clubs', add_clubs, name='add_clubs'),
    path('delete_clubs/<int:myid>/', delete_clubs, name='delete_clubs'),
    path('edit_clubs/<int:myid>/', edit_clubs, name='edit_clubs'),
    path('update_clubs/<int:myid>/', update_clubs, name='update_clubs'),
    
    
    path('modify_delete_accounts/', views.modify_delete_accounts,
         name='modify_delete_accounts'),
    path('create_account/', create_account, name='create_account'),
    path('delete_account/<int:myid>/', delete_account, name='delete_account'),
    path('edit_account/<int:myid>/', edit_account, name='edit_account'),
    path('update_account/<int:myid>/', update_account, name='update_account'),
    path('view_account/', view_account, name='view_account'),

    
    
    
    path("", views.viewings, name="home"),
    path("viewings/", views.viewings, name="viewings"),
    path("showings/<int:film>/", views.showings, name="showings_by_film"),
    path("add_film/", views.add_film, name="add_film"),
    path("films_endpoint/", views.films_endpoint, name="films_endpoint"),
    path("specific_film_endpoint/<int:pk>/", views.specific_film_endpoint, name="specific_film_endpoint"),
    path("login/", views.login, name="login"),
    path("topup/", views.topup, name="topup"),
    path("logout/", views.logout, name="logout"),
    path("register/", views.registerPage, name="registerPage"),
    path("payment/<int:showing>/", views.payment, name="payment"),
    path("rep_payment/<int:showing>/", views.rep_payment, name="rep_payment"),
    path("pay_with_card/", views.pay_with_card, name="pay_with_card"),
    path("view_accounts/", views.view_accounts, name="view_accounts"),
    path("daily_transactions/", views.daily_transactions, name="daily_transactions"),
    path("customer_statements/", views.customer_statements, name="customer_statements"),
    path("thanks/", views.thanks, name="thanks"),
    path("user/", views.userpage, name="user-page"),
    path("add_club/", views.add_club, name="add_club"),
    path("clubs_endpoint/", views.clubs_endpoint, name="clubs_endpoint"),
    path("specific_club_endpoint/<int:pk>/", views.specific_club_endpoint, name="specific_club_endpoint"),
    path("add_rep/", views.add_rep, name="add_rep"),
    path("club_rep_home/", views.club_rep_home, name="club_rep_home"),
    path("cinema_manager_home/", views.cinema_manager_home, name="cinema_manager_home"),
    path("student_home/", views.student_home, name="student_home"),
    path("set_payment/", views.set_payment_details, name="set_payment"),
    path("am_home/", views.am_home, name="am_home"),
    path("settle_payments/", views.settle_payments, name="settle_payments"),
    path("review_students/<int:userID>", views.review_students, name="review_students"),
    path("rep_success/", views.rep_success, name="rep_success"),
    path("change_ticket_prices/", views.change_ticket_prices, name="change_ticket_prices"),
    path("view_order_history/", views.view_order_history, name="view_order_history"),
    path("request_cancellation/", views.request_cancellation, name="request_cancellation"),
    path("approve_cancellations/", views.approve_cancellation, name="approve_cancellations"),
    path("screens_endpoint/", views.screens_endpoint, name="screens_endpoint"),
    path("specific_screen_endpoint/<int:pk>/", views.specific_screen_endpoint, name="specific_screen_endpoint"),
    path("add_screen/", views.add_screen, name="add_screen"),
    path("add_showing/", views.add_showing, name="add_showing"),
    path('edit_showing/<int:showing_id>/', views.edit_showing, name='edit_showing'),
    path('delete_showing/<int:showing_id>', views.delete_showing, name='delete_showing'),
]
