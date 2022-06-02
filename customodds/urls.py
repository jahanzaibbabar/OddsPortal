from django.urls import path
from . import views


urlpatterns = [
    path('login', views.login_user, name='login'),
    path('<str:url>', views.home_page, name='home_page'),
    path('user/logout', views.logout_user, name='logout'),
    path('', views.home_main, name='home_main'),
    path('urls/odds', views.get_odds, name='get_data'),
    path('urls/matches', views.get_matches_urls, name='matches')
]
