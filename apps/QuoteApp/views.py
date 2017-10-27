from django.shortcuts import render, redirect, HttpResponse
from models import *
from django.contrib import messages
import bcrypt


def index(request):
	return render(request, 'QuoteApp/index.html')

def process(request):
	if request.method == 'POST':
		errors = User.objects.validator(request.POST)
		if errors:
			for error in errors:
				print errors
				messages.error(request, errors[error])
			return redirect('/')
		else:
			hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
			user = User.objects.create(name = request.POST['name'], alias = request.POST['alias'], email = request.POST['email'], password = hashed_pw)
			request.session['id'] =  user.id
			request.session['alias'] = user.alias
			messages.success(request, 'You have successfully registered')
			return redirect('/success')

	if request.session.get('count')== None:
		request.session['count'] = 0

	request.session['count'] += 1

	return redirect('/')
def login(request):
	if request.method == 'POST':
		model_return = User.objects.login(request.POST)
		if 'user' in model_return:
			request.session['id'] = model_return['user'].id
			request.session['alias'] = model_return['user'].alias
			return redirect('/success')
		else:
			for error in model_return:
				messages.error(request, model_return[error])
			print messages
			return redirect('/')
	return redirect('/')
def success(request):
	if not 'id' in request.session:
		return redirect('/')
	context = {
		'all_users': User.objects.all(),
		'all_quotes' : Quote.objects.all()
	}
	return render(request, 'QuoteApp/success.html', context)

def quote(request):
	quotes = "query message"
	context = {
		'all_quotes': Quote.objects.all()
	}
	print quotes
	return render(request, 'QuoteApp/success.html', context)

def user(request):
	context = {
		'all_quotes': Quote.objects.all()
	}
	return render(request, 'QuoteApp/user.html', context)





def logout(request):
	del request.session['id']
	del request.session['alias']
	return redirect('/')















