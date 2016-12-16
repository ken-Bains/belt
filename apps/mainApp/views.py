from django.shortcuts import render, redirect
from . import models
from django.contrib import messages

# Create your views here.


def index(request):
	return render(request, 'mainApp/index.html')

def newUser(request):
	res = models.User.objects.register(request.POST)
	message = "registered"
	return processSignon(request, res, message)

def signOn(request):
	res = models.User.objects.login(request.POST)
	message = "logged on"
	return processSignon(request, res, message)

def processSignon(request, res, message):	
	if not res[0]:
		messages.success(request, "You have successfully {}!!!!".format(message))
		request.session['id'] = res[1]
		return redirect('/success')

	for error in res[0]:
		messages.warning(request, error)
	return redirect('/')

def success(request):
	if request.session.get('id'):
		userInfo = models.User.objects.filter(id = request.session['id'])
		data = {"user":userInfo[0]}
		return render(request, "mainApp/success.html", data)
	return redirect('/')







