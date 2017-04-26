# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from models import *
from django.db.models import Count
import bcrypt

def current_user(request):
	return User.objects.get(id=request.session['user_id'])

def logout(request):
	request.session.clear()
	return redirect('/')

def index(request):
	return render(request,"belt/index.html")

def createUser(request):
	if request.method != 'POST':
		return redirect('/')

	attempt = User.objects.validateUser(request.POST)
	if attempt['status'] == True:
		user=User.objects.createUser(request.POST)
		request.session['user_id']=user.id
		return redirect('/pokes')

	else:
		for error in attempt['errors']:
			messages.add_message(request, messages.ERROR, error, extra_tags="registration")
		return redirect('/')

def loginUser(request):
	if request.method != 'POST':
		return redirect('/')

	attempt = User.objects.loginUser(request.POST)
	print attempt['status']

	if attempt['status'] == True:
		request.session['user_id']=attempt['user'].id
		return redirect('/pokes')

	else:
		messages.add_message(request, messages.ERROR, attempt['message'], extra_tags="login")
		return redirect('/')

def pokes(request):
	print request.session['user_id']

	### Top poked users id excluding the current user.	

	user = User.objects.filter(id=request.session['user_id']).first()
	print user.name

	### get the number of different pokers and their pokes for the current user.
	pokers=Poke.objects.filter(user=user)
	list_of_pokers = []
	for poker in pokers:
		if poker.poke_user.id not in list_of_pokers:
			list_of_pokers.append(poker.poke_user.id)
	number_of_pokers=len(list_of_pokers)

	pokers_filtered = User.objects.filter(id__in= list_of_pokers)

	search=Poke.objects.filter(user=user).values('user').order_by('poke_user').annotate(the_count=Count('user'))


	### List of users and pokes excluding current user
	poke=User.objects.all().exclude(id=request.session['user_id']).annotate(num_pokes=Count('user_poked')).order_by('-num_pokes')
	context = {
		'user': user,
		'poke': poke,
		'number_of_pokers':number_of_pokers,
		'pokers_filtered':pokers_filtered,
	}

	return render(request,"belt/pokes.html",context)

def pokesAdd(request,id):
	print id
	request.session['user_id']
	user=User.objects.filter(id=id).first()
	poke_user=User.objects.filter(id=request.session['user_id']).first()
	poke=Poke.objects.create(user=user,poke_user=poke_user)
	return redirect('/pokes')