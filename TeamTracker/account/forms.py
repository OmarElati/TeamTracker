from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from account.models import Account


class RegistrationForm(UserCreationForm): # RegistrationForm
	email = forms.EmailField(max_length=254, help_text='Required. Add a valid email address.')

	class Meta:
		model = Account
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

	def clean_email(self):
		# Clean and validate the email field
		email = self.cleaned_data['email'].lower()
		try:
			# Check if the email is already in use
			account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
			raise forms.ValidationError('Email "%s" is already in use.' % email)
		except Account.DoesNotExist:
			return email

	def clean_username(self):
		# Clean and validate the username field
		username = self.cleaned_data['username']
		try:
			# Check if the username is already in use
			account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
		except Account.DoesNotExist:
			return username
		raise forms.ValidationError('Username "%s" is already in use.' % username)


class AccountAuthenticationForm(forms.ModelForm): # A form for authenticating user login

	password = forms.CharField(label='Password', widget=forms.PasswordInput)

	class Meta:
		model = Account
		fields = ('email', 'password')

	def clean(self):
		# Clean and validate the form data
		if self.is_valid():
			email = self.cleaned_data['email']
			password = self.cleaned_data['password']
			if not authenticate(email=email, password=password):
				raise forms.ValidationError("Invalid login")


class AccountUpdateForm(forms.ModelForm): # A form for updating user account information

    class Meta:
        model = Account
        fields = ('username', 'email', 'profile_image', 'hide_email', 'bank', 'phone_number', 'bank_account')

    def clean_email(self):
		# Validates the email field to ensure it is unique
        email = self.cleaned_data['email'].lower()
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
        except Account.DoesNotExist:
            return email
        raise forms.ValidationError('Email "%s" is already in use.' % account)

    def clean_username(self):
		# Validates the username field to ensure it is unique
        username = self.cleaned_data['username']
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
        except Account.DoesNotExist:
            return username
        raise forms.ValidationError('Username "%s" is already in use.' % username)


    def save(self, commit=True):
		# Saves the updated account information
        account = super(AccountUpdateForm, self).save(commit=False)
        account.username = self.cleaned_data['username']
        account.email = self.cleaned_data['email'].lower()
        account.profile_image = self.cleaned_data['profile_image']
        account.hide_email = self.cleaned_data['hide_email']
        if commit:
            account.save()
        return account
