from django.db import models

# Create your models here.

class User(models.Model):
	username = models.TextField()
	password = models.TextField()
	photo = models.TextField()

class Friend(models.Model):
	username = models.TextField()
	friendname = models.TextField()
	status = models.FloatField()

class Gift(models.Model):
	username = models.TextField()
	giftname = models.TextField()
	photo = models.TextField()
	price = models.FloatField()
	content = models.TextField()
	url = models.TextField()

class Fund(models.Model):
	username = models.TextField()
	giftname = models.TextField()
	giftid = models.FloatField()
	amount = models.FloatField()

class History(models.Model):
	username = models.TextField()
	detail = models.TextField()
	time = models.DateTimeField()