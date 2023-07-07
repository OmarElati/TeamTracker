from django.shortcuts import render
from django.shortcuts import render
from account.models import Account
from django.contrib.auth.decorators import login_required


@login_required # Only accessible for authenticated users
def home_screen_view(request): # rendering the home screen view
    account = Account.objects.get(email=request.user.email)
    first_name = account.first_name
    last_name = account.last_name
    context = {
        'first_name': first_name,
        'last_name': last_name,
    }

    return render(request, "personal/profile.html", context)
