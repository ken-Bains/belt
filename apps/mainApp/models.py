from __future__ import unicode_literals
from django.db import models
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]')

# Create your models here.
class userManager(models.Manager):
	def register(self, post):
		first = post['first_name']
		last  = post['last_name']
		email = post['email']
		password = post['password']
		passwordCheck = post['passwordCheck']
		errors = []
		userId = 0

		if len(first) < 2:
			errors.append('first name must be longer than 2 characters')

		if len(last) < 2:
			errors.append('last name must be longer than 2 characters')

		if len(email) < 1:
			errors.append('email cannot be blank')
		elif not EMAIL_REGEX.match(email):
			errors.append('email not in right format')
		
		if len(password) < 8:
			errors.append('password needs to be grater than 8 characters')

		if password != passwordCheck:
			errors.append('password does not match')


		if not errors:
			emailExist = User.objects.filter(email=email)
			if not emailExist:
				hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
				user = User.objects.create(email=email, first_name= first, last_name=last, password=hashed)
				userId = user.id
			else:
				errors.append('Invalid login')
		
		return [errors, userId]

	def login(self, post):
		email = post['email']
		password = post['password']
		errors = []
		userId = 0
		
		if len(email) < 1:
			errors.append('email cannot be blank!')
		elif not EMAIL_REGEX.match(email):
			errors.append('email not in right format')
		
		if len(password) < 8:
			errors.append('password needs to be grater than 8 characters')
		
		if not errors:
			emailExist = User.objects.filter(email=email)

			if emailExist:
				hashed = emailExist[0].password

				if bcrypt.hashpw(password.encode(), hashed.encode()) == hashed:
					userId = emailExist[0].id
			else:
				errors.append('Invalid login')


		return [errors, userId]

class User(models.Model):
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	email = models.CharField(max_length=100)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = userManager()




