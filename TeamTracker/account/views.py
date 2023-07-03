from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.conf import settings

from account.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
from account.models import Account
from django.contrib.auth.decorators import login_required


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            if password1 != password2:
                form.add_error('password2', "Passwords do not match")
            else:
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                email = form.cleaned_data.get('email').lower()

                user = Account.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password1=password2)

                login(request, user)
                return redirect('home')
    else:
        form = RegistrationForm()

    return render(request, 'account/login-light-register.html', {'form': form})


def logout_view(request):
	logout(request)
	return redirect("login")


def login_view(request, *args, **kwargs):
	context = {}

	user = request.user
	if user.is_authenticated: 
		return redirect("home")

	destination = get_redirect_if_exists(request)
	print("destination: " + str(destination))

	if request.POST:
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)

			if user:
				login(request, user)
				if destination:
					return redirect(destination)
				return redirect("home")

	else:
		form = AccountAuthenticationForm()

	context['login_form'] = form
	return render(request, "account/login-light-login.html", context)


def get_redirect_if_exists(request):
	redirect = None
	if request.GET:
		if request.GET.get("next"):
			redirect = str(request.GET.get("next"))
	return redirect


def account_view(request, *args, **kwargs):
	"""
	- Logic here is kind of tricky
		is_self (boolean)
			is_friend (boolean)
				-1: NO_REQUEST_SENT
				0: THEM_SENT_TO_YOU
				1: YOU_SENT_TO_THEM
	"""
	context = {}
	user_id = kwargs.get("user_id")
	try:
		account = Account.objects.get(pk=user_id)
	except:
		return HttpResponse("Something went wrong.")
	if account:
		context['id'] = account.id
		context['username'] = account.username
		context['email'] = account.email
		context['profile_image'] = account.profile_image.url
		context['hide_email'] = account.hide_email
		context['first_name'] = account.first_name
		context['last_name'] = account.last_name
		context['address'] = account.address
		context['phone_number'] = account.phone_number
		context['bank'] = account.bank
		context['id_type'] = account.id_type
		context['id_type'] = account.bank_account

		# Define template variables
		is_self = True
		is_friend = False
		user = request.user
		if user.is_authenticated and user != account:
			is_self = False
		elif not user.is_authenticated:
			is_self = False
			
		# Set the template variables to the values
		context['is_self'] = is_self
		context['is_friend'] = is_friend
		context['BASE_URL'] = settings.BASE_URL
		return render(request, "account/account.html", context)


def account_search_view(request, *args, **kwargs):
	context = {}
	if request.method == "GET":
		search_query = request.GET.get("q")
		if len(search_query) > 0:
			search_results = Account.objects.filter(email__icontains=search_query).filter(username__icontains=search_query).distinct()
			user = request.user
			accounts = [] # [(account1, True), (account2, False), ...]
			for account in search_results:
				accounts.append((account, False)) # you have no friends yet
			context['accounts'] = accounts
				
	return render(request, "account/search_results.html", context)


def edit_account_view(request, *args, **kwargs):
	if not request.user.is_authenticated:
		return redirect("login")
	user_id = kwargs.get("user_id")
	account = Account.objects.get(pk=user_id)
	if account.pk != request.user.pk:
		return HttpResponse("You cannot edit someone elses profile.")
	context = {}
	if request.POST:
		form = AccountUpdateForm(request.POST, request.FILES, instance=request.user)
		if form.is_valid():
			account.profile_image.delete()
			account.email = form.cleaned_data['email']
			account.username = form.cleaned_data['username']
			account.first_name = form.cleaned_data['first_name']
			account.last_name = form.cleaned_data['last_name']
			account.hide_email = form.cleaned_data['hide_email']
			account.phone_number = form.cleaned_data['phone_number']
			account.address = form.cleaned_data['address']
			account.bank = form.cleaned_data['bank']
			account.id_type = form.cleaned_data['id_type']
			account.bank_account = form.cleaned_data['bank_account']
			form.save()
			return redirect("account:view", user_id=account.pk)
		else:
			form = AccountUpdateForm(request.POST, instance=request.user,
				initial={
					"id": account.pk,
					"email": account.email,
					"username": account.username,
					"first_name": account.first_name,
					"last_name": account.last_name,
					"profile_image": account.profile_image,
					"hide_email": account.hide_email,
					"id_type": account.id_type,
					"phone_number": account.phone_number,
					"address": account.address,
					"bank": account.bank,
					"bank_account": account.bank_account,
				}
			)
			context['form'] = form
	else:
		form = AccountUpdateForm(
			initial={
					"id": account.pk,
					"email": account.email,
					"username": account.username,
					"first_name": account.first_name,
					"last_name": account.last_name,
					"profile_image": account.profile_image,
					"hide_email": account.hide_email,
					"id_type": account.id_type,
					"phone_number": account.phone_number,
					"address": account.address,
					"bank": account.bank,
					"bank_account": account.bank_account,
				}
			)
		context['form'] = form
	context['DATA_UPLOAD_MAX_MEMORY_SIZE'] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
	return render(request, "account/side-menu-light-update-profile.html", {'user_id': user_id})

