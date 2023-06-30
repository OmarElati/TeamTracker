from django.shortcuts import render
from django.shortcuts import render
from account.models import Account
from django.contrib.auth.decorators import login_required


@login_required
def home_screen_view(request):
    account = Account.objects.get(email=request.user.email)
    first_name = account.first_name
    last_name = account.last_name
    context = {
        'first_name': first_name,
        'last_name': last_name
    }
    
    return render(request, "personal/side-menu-light-profile-overview-1.html", context)
