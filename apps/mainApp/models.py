from __future__ import unicode_literals
from django.db import models
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]')

# Create your models here.
class userManager(models.Manager):
	def register(self, email, password, first=None, alias=None, passwordCheck=None, form=None):
		errors = []
		userId = 0
		if len(email) < 1:
			errors.append('email cannot be blank!')
		elif not EMAIL_REGEX.match(email):
			errors.append('email cannot be blank!')
		
		if len(password) < 8:
			errors.append('password needs to be grater than 8 characters')

		#if login form has no errors then check password and set session id. 
		if len(errors) == 0 and form != 'registration':
			user = User.objects.filter(email = email)
			hashed = user[0].password

			if bcrypt.hashpw(password.encode(), hashed.encode()) == hashed:
				# request.session['id'] = user[0].id
				userId = user[0].id


		# check to see if coming from registration page
		if form == "registration":
			if len(first) < 2:
				errors.append('first name must be longer than 2 characters')

			if len(alias) < 2:
				errors.append('alias name must be longer than 2 characters')

			if password != passwordCheck:
				errors.append('password does not match')
			
			checkIfEmailExist = User.objects.filter(email=email)

			if len(checkIfEmailExist) > 0:
				errors.append('invalid')

			if len(errors) == 0:
				hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
				user = User.objects.create(email=email, first_name= first, alias=alias, password=hashed)
				userId = user.id

		return [errors, userId]

class User(models.Model):
	first_name = models.CharField(max_length=50)
	alias = models.CharField(max_length=50)
	email = models.CharField(max_length=100)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = userManager()

#
#
#      ---------end of user-------
#

class bookManager(models.Manager):

	def add_book(self, post, user_id):
		title = post['book_title']
		author = post['author']
	
		check_if_book_exist = Book.objects.filter(title = title)
		
		if not check_if_book_exist:
			book_object = Book.objects.create(title = title, author=author)
		else:
			res = {"status": False, "error": "book already exist"}
			return res
		
		Book.objects.add_review(post, user_id, book_object)
		res = {"status": True, "book_id":book_object.id}
		return res 
	
	def add_review(self, post, user_id, book=None):
		review = post['review']
		rating = post['rating']
		if book == None:
			book_object = Book.objects.filter(id = post['book_id'])
			book = book_object[0]
		user_object = User.objects.filter(id = user_id)
		user = user_object[0]
		
		Review.objects.create(rating=rating, review=review, user=user, book=book)

		return book

class Book(models.Model):
	title = models.CharField(max_length=50)
	author = models.CharField(max_length=50)
	created_at = models.DateTimeField(auto_now_add = True)
	objects = bookManager()



class Review(models.Model):
	rating = models.SmallIntegerField()
	review = models.TextField(max_length=1000)
	created_at = models.DateTimeField(auto_now_add = True)
	user = models.ForeignKey('User')
	book = models.ForeignKey('Book')
	objects = bookManager()





