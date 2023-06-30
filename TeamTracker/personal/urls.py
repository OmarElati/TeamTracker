from django.urls import path
from personal.views import home_screen_view

app_name = 'personal'

urlpatterns = [
    path('profile/<str:username>/', home_screen_view, name='profile'),
]
