from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os


class MyAccountManager(BaseUserManager):
	def create_user(self, email, first_name, last_name, password=None, username=None):
		if not email:
			raise ValueError('Users must have an email address')
		if not first_name:
			raise ValueError('Users must have a first name')
		if not last_name:
			raise ValueError('Users must have a last name')

		username = f"{first_name.lower()}.{last_name.lower()}"

		user = self.model(
			email=self.normalize_email(email),
			username=username,
            first_name=first_name,
            last_name=last_name,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, first_name, last_name, password, username=None):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			first_name=first_name,
            last_name=last_name,
            username=username,
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


def get_profile_image_filepath(self, filename):
	return 'profile_images/' + str(self.pk) + '/profile_image.png'

def get_default_profile_image():
	return "images/logo.svg"


class Account(AbstractBaseUser):
	email 					= models.EmailField(verbose_name="email", max_length=60, unique=True)
	username 				= models.CharField(max_length=30, unique=True)
	first_name 				= models.CharField(max_length=30)
	last_name 				= models.CharField(max_length=30)
	date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin				= models.BooleanField(default=False)
	is_active				= models.BooleanField(default=True)
	is_staff				= models.BooleanField(default=False)
	is_superuser			= models.BooleanField(default=False)
	profile_image			= models.ImageField(max_length=255, upload_to=get_profile_image_filepath, null=True, blank=True, default=get_default_profile_image)
	hide_email				= models.BooleanField(default=True)
	bank 					= models.CharField(max_length=100)
	id_type 				= models.CharField(max_length=100, blank=True, null=True)
	phone_number 			= models.CharField(max_length=20, blank=True, null=True)
	bank_account 			= models.CharField(max_length=100, blank=True, null=True)
	address 				= models.CharField(max_length=200)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

	objects = MyAccountManager()

	def save(self, *args, **kwargs):
        # Set the username as a combination of the first name and last name
		self.username = self.first_name + self.last_name
		super(Account, self).save(*args, **kwargs)

	def __str__(self):
		return self.username

	def get_profile_image_filename(self):
		return str(self.profile_image)[str(self.profile_image).index('profile_images/' + str(self.pk) + "/"):]

	# For checking permissions. to keep it simple all admin have ALL permissons
	def has_perm(self, perm, obj=None):
		return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
	def has_module_perms(self, app_label):
		return True
