from django.urls import path
from .views import Home, LoginUser, LogoutUser, RegisterUser, SearchView
from .roulette import StartView, TwistView


app_name = 'roulette'
urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutUser.as_view(), name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('start/', StartView.as_view(), name="start"),
    path('twist/', TwistView.as_view(), name="twist"),
    path('search/', SearchView.as_view(), name="search")
]
