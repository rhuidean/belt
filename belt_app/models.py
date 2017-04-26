# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import re, bcrypt


class UserManager(models.Manager):
	def validateUser(self,post):
		is_valid = True
		errors=[]

		### name check
		if len(post.get('name')) == 0:
			is_valid = False
			errors.append('Name field cannot be blank.')

	
		### email duplicate check
		user = User.objects.filter(email=post.get('email')).first()
		if user:
			errors.append('You must provide a valid email.')
			is_valid = False

		### alias check
		if len(post.get('alias')) == 0:
			is_valid = False
			errors.append('Alias field cannot be blank.')

		### alias duplicate check
		user = User.objects.filter(email=post.get('alias')).first()
		if user:
			errors.append('The alias has been taken.')
			is_valid = False

		### email check
		if not re.search(r'^\w+\@\w+\.\w+',post.get('email')):
			is_valid = False
			errors.append('You must provide a valid email address')

		### password check
		if  len(post.get('password')) == 0:
			is_valid = False
			errors.append('Password cannot be blank.')

		### password confirmation
		if post.get('password') != post.get('password_confirmation'):
			is_valid = False
			errors.append('Your passwords do not match.')

		return {"status": is_valid, "errors": errors}

	def createUser(self, post):
		return User.objects.create(
			name = post.get('name'),
			email= post.get('email'),
			password=bcrypt.hashpw(post.get('password').encode(), bcrypt.gensalt().encode()),
			)


	def loginUser(self,post):
		user = User.objects.filter(email=post.get('email')).first()
		if user and bcrypt.checkpw(post.get('password').encode(), user.password.encode()):
			return {'status': True, 'user':user}
		else:
			return {"status": False, "message": 'Invalid credentials'}



class User(models.Model):
	name = models.CharField(max_length=255)
	alias = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	date_of_birth = models.DateField(null=True)
	objects = UserManager()

class Poke(models.Model):
	user = models.ForeignKey(User, related_name='user_poked')
	poke_user = models.ForeignKey(User, related_name='pokes')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)



