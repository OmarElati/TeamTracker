from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.conf import settings
from account.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
from account.models import Account
from django.contrib.auth.decorators import login_required


def register_view(request): # function for handling user registration
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            if password1 != password2:
                form.add_error('password2', "Passwords do not match")
            else:
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                email = form.cleaned_data.get('email').lower()
                print(first_name,last_name,email,password1,password2)
                user = Account.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password1)

                login(request, user)
                return redirect('home')
        else:
            for field_name, errors in form.errors.items():
                for error in errors:
                    print(f"Error in {field_name}: {error}")
    else:
        form = RegistrationForm()
    
    return render(request, 'account/register.html', {'form': form})


def logout_view(request): # function for handling user logout
	logout(request)
	return redirect("login")


def login_view(request, *args, **kwargs): # function for handling user login
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
	return render(request, "account/login.html", context)


def get_redirect_if_exists(request): # Retrieves the redirect URL if it exists in the request's GET parameters
	redirect = None
	if request.GET:
		if request.GET.get("next"):
			redirect = str(request.GET.get("next"))
	return redirect


def account_view(request, *args, **kwargs): # Retrieves and displays the account details for a specific user

	context = {}
	user_id = kwargs.get("user_id")
	try:
		account = Account.objects.get(pk=user_id)
	except:
		return HttpResponse("Something went wrong.")
	if account: # Populate the context with account details
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




def edit_account_view(request, *args, **kwargs): # Handles the editing of the user's account
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
	return render(request, "account/update-profile.html", {'user_id': user_id})

