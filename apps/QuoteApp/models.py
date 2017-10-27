from django.db import models
import re
import bcrypt
from datetime import datetime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')


class UserManager(models.Manager):
	def validator(self, postData):
		errors = {}
		if len(postData['name']) < 3 or len(postData['alias']) < 3:
			errors['name_error'] = "Name and Alias must be at least three characters long"
		if not EMAIL_REGEX.match(postData['email']):
			errors['email'] = "Not a valid email address"
		if len(postData['password']) < 8 or len(postData['confirm_password']) < 8:
			errors['password_length'] = "Password must be at least eight characters"
		if postData['password'] != postData['confirm_password']:
			errors['password_match'] = "Passwords must match"
		# print postData['email']
		if User.objects.filter(name = postData['name']):
			errors['exist'] = "You are already in the system. Please login or register with different name"
		return errors
		if User.objects.filter(alias = postData['alias']):
			errors['exist'] = "This alias is already taken. Please choose another alias"
		return errors

	def login(self, postData):
		errors = {}
		if User.objects.filter(email = postData['email']):
			user_check = User.objects.get(email = postData['email'])
			if bcrypt.checkpw(postData['password'].encode(), user_check.password.encode()):
				print 'Login Success!'
				return { 'user' : user_check }
			else:
				print 'invalid'
				errors ['invalid'] = 'Invalid Login'
				return errors
		else:
			errors['invalid'] = 'Invalid Login'
			return errors



class User(models.Model):
	name = models.CharField(max_length = 255)
	alias = models.CharField(max_length = 255)
	email = models.CharField(max_length = 255)
	password = models.CharField(max_length = 255)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = UserManager()


class Quote(models.Model):
	quote = models.CharField(max_length = 255)
	author = models.CharField(max_length = 255)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	user = models.ForeignKey(User, related_name = 'quotes')
