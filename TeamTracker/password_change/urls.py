from django.urls import path

from password_change.views import change_password

app_name = 'password_change'

urlpatterns = [
    path('<user_id>/changepwd/', change_password, name="change_password"),
]
