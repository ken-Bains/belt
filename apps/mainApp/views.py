from django.shortcuts import render, redirect
from . import models
from django.contrib import messages

# Create your views here.


def index(request):
	
	return render(request, 'mainApp/index.html')

def newUser(request):
	first = request.POST['first_name']
	alias  = request.POST['alias']
	email = request.POST['email']
	password = request.POST['password']
	passwordCheck = request.POST['passwordCheck']
	form = "registration"

	res = models.User.objects.register(email, password, first, alias, passwordCheck, form)

	if len(res[0]) == 0:
		messages.success(request, "You have successfully logged in!!!!")
		request.session['id'] = res[1]
		return redirect('/books')

	for error in res[0]:
		messages.warning(request, error)

	return redirect('/')

def signOn(request):
	email = request.POST['email']
	password = request.POST['password']

	res = models.User.objects.register(email, password)

	if len(res[0]) == 0:
		messages.success(request, "You have successfully logged in!!!!")
		request.session['id'] = res[1]
		return redirect('/books')

	for error in res[0]:
		messages.warning(request, error)

	return redirect('/')

def all_books(request):
	if request.session.get('id'): #'id' not in request.session:
		userInfo = models.User.objects.filter(id = request.session['id'])
		all_reviews = models.Review.objects.all().order_by('-created_at')
		reviews = [all_reviews[0], all_reviews[1], all_reviews[2]]
		data = {"user":userInfo[0], "reviews":reviews, "all_reviews": all_reviews}
		return render(request, "mainApp/all_books.html", data)
	return redirect('/')

def logout(request):
	request.session.clear()
	return redirect('/')

def book_add_page(request):
	if request.session.get('id'):
		return render(request, 'mainApp/book_add.html')
	return redirect('/')

def one_book(request, id):
	if request.session.get('id'):
		book = models.Book.objects.filter(id=id)
		reviews = models.Review.objects.filter(book__id = id)
		data = {"book":book[0], "reviews": reviews}
		return render(request, 'mainApp/one_book.html', data)
	return redirect('/')

def add_new_book(request):
	res = models.Book.objects.add_book(request.POST, request.session['id'])
	if res['status'] == False:
		messages.warning(request, res['error'])
		return redirect ('/book/add')
	return redirect('/book/{}'.format(res['book_id']))

def user_info_page(request, id):
	if request.session.get('id'):
		all_reviews = models.Review.objects.filter(user__id = request.session['id'])
		reviews = [all_reviews[0], all_reviews[1], all_reviews[2]]
		user = all_reviews[0]
		data = { "reviews":reviews, "all_reviews": all_reviews, "user":user}
		return render(request, 'mainApp/user_info.html', data)
	return redirect('/')

def add_review(request):
	res = models.Book.objects.add_review(request.POST, request.session['id'])
	return redirect('/book/{}'.format(res.id))

