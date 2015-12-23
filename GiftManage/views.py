from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from GiftManage.models import User
from GiftManage.models import Friend
from GiftManage.models import Gift
from GiftManage.models import Fund
from GiftManage.models import History
from django.shortcuts import render_to_response
from django.db.models import Sum
from datetime import *
import os
import json
import sys
import traceback

# Create your views here.


def login(request):
	final = { "status" : "error" }
	try:
		username = request.GET.get('username', None)
		password = request.GET.get('password', None)
		user = User.objects.get(username = username, password = password)
		final = {
			"status" : "success",
			"username" : username
		}
	except Exception as e:
		return HttpResponse(json.dumps(final))
	return HttpResponse(json.dumps(final))

def register(request):
	final = { "status" : "error" }
	try:
		username = request.GET.get('username', None)
		password = request.GET.get('password', None)
		if User.objects.filter(username = username).exists():
			print username, password
			return HttpResponse(json.dumps(final))
		else:
			newuser = User(username = username, password = password, photo = "")
			newuser.save()
			final = {
				"status" : "success",
				"username" : username
			}
	except Exception as e:
		print e
		return HttpResponse(json.dumps(final))
	return HttpResponse(json.dumps(final))

def gethistory(request):
	final = { "status" : "error" }
	try:
		username = request.GET.get('username', None)
		history = History.objects.filter(username = username).order_by("time")
		res = []
		count = 0
		for record in history:
			res.append({
				"detail" : record.detail,
				"time" : str(record.time)
				})
			if count > 10:
				break
			count += 1
		final = {
			"status" : "success",
			"result" : res
		}
	except Exception as e:
		print e
		return HttpResponse(json.dumps(final))
	return HttpResponse(json.dumps(final))

def getfriendrequest(request):
	final = { "status" : "error" }
	try:
		username = request.GET.get('username', None)
		frequest = Friend.objects.filter(friendname = username, status = 0)
		res = []
		for record in frequest:
			res.append(record.username)
		final = {
			"status" : "success",
			"result" : res
		}
	except Exception as e:
		return HttpResponse(json.dumps(final))
	return HttpResponse(json.dumps(final))

def getfriends(request):
	final = { "status" : "error" }
	try:
		username = request.GET.get('username', None)
		frequest = Friend.objects.filter(username = username, status = 1)
		res = []
		for record in frequest:
			res.append(record.friendname)
		final = {
			"status" : "success",
			"result" : res
		}
	except Exception as e:
		return HttpResponse(json.dumps(final))
	return HttpResponse(json.dumps(final))

def getgifts(request):
	final = { "status" : "error" }
	try:
		username = request.GET.get('username', None)
		gifts = Gift.objects.filter(username = username)
		res = []
		for record in gifts:
			res.append({
				"name" : record.giftname,
				"price" : record.price,
				"id" : record.id,
				"get" : Fund.objects.filter(giftid = record.id).aggregate(Sum('amount'))
				})
		final = {
			"status" : "success",
			"result" : res
		}
	except Exception as e:
		return HttpResponse(json.dumps(final))
	return HttpResponse(json.dumps(final))

def getgiftdetail(request):
	final = { "status" : "error" }
	try:
		giftid = request.GET.get('giftid', None)
		gift = Gift.objects.get(id = giftid)
		detail = {
			"giftname" : gift.giftname,
			"price" : gift.price, 
			"content" : gift.content, 
			"url" : gift.url,
			"get" : Fund.objects.filter(giftid = giftid).aggregate(Sum('amount')),
			"id" : giftid
		}
		res = []
		funds = Fund.objects.filter(giftid = giftid)
		for record in funds:
			res.append({
				"amount" : record.amount,
				"username" : record.username
				})
		final = {
			"status" : "success",
			"result" : {
				"detail" : detail,
				"funds" : res
			}
		}
	except Exception as e:
		return HttpResponse(json.dumps(final))
	return HttpResponse(json.dumps(final))

def getfunds(request):
	final = { "status" : "error" }
	try:
		username = request.GET.get('username', None)
		funds = Fund.objects.filter(username = username)
		res = []
		for record in funds:
			res.append({
				"name" : record.giftname,
				"id" : record.id,
				"amount" : record.amount
				})
		final = {
			"status" : "success",
			"result" : res
		}
	except Exception as e:
		return HttpResponse(json.dumps(final))
	return HttpResponse(json.dumps(final))

def searchfriend(request):
	final = { "status" : "error" }
	try:
		username = request.GET.get('username', None)
		keyword = request.GET.get('keyword', None)
		users = User.objects.filter(username__contains = keyword)
		res = []
		for record in users:
			if record.username == username:
				continue
			res.append({
				"name" : record.username,
				"isfriend" : Friend.objects.filter(username = username, friendname = record.username, status = 1).exists(),
				"isrequesting" : Friend.objects.filter(username = username, friendname = record.username, status = 0).exists()
				})
		final = {
			"status" : "success",
			"result" : res
		}
	except Exception as e:
		return HttpResponse(json.dumps(final))
	return HttpResponse(json.dumps(final))

def addfriend(request):
	final = { "status" : "error" }
	try:
		username = request.GET.get('username', None)
		friend = request.GET.get('friend', None)
		newrequest = Friend(username = username, friendname = friend, status = 0)
		newrequest.save()
		final = { "status" : "success" }
	except Exception as e:
		return HttpResponse(json.dumps(final))
	return HttpResponse(json.dumps(final))

def acceptfriend(request):
	final = { "status" : "error" }
	try:
		username = request.GET.get('username', None)
		friend = request.GET.get('friend', None)
		Friend.objects.filter(username = friend, friendname = username).update(status = 1)
		newrequest = Friend(username = username, friendname = friend, status = 1)
		newrequest.save()
		history = History(username = friend, detail = "add " + username + " as new friend", time = datetime.now())
		history.save()
		history = History(username = username, detail = "add " + friend + " as new friend", time = datetime.now())
		history.save()
		final = { "status" : "success" }
	except Exception as e:
		return HttpResponse(json.dumps(final))
	return HttpResponse(json.dumps(final))

def publishgift(request):
	final = { "status" : "error" }
	try:
		username = request.GET.get('username', None)
		giftname = request.GET.get('giftname', "")
		price = request.GET.get('price', 0)
		content = request.GET.get('content', "")
		url = request.GET.get('url', "")
		newgift = Gift(
			username = username, 
			giftname = giftname, 
			photo = "", 
			price = price, 
			content = content, 
			url = url
			)
		newgift.save()
		history = History(username = username, detail = "pulish a new wish " + giftname, time = datetime.now())
		history.save()
		final = { "status" : "success" }
	except Exception as e:
		return HttpResponse(json.dumps(final))
	return HttpResponse(json.dumps(final))

def publishfund(request):
	final = { "status" : "error" }
	try:
		username = request.GET.get('username', None)
		giftname = request.GET.get('giftname', "")
		giftid = request.GET.get('giftid', 0)
		amount = request.GET.get('amount', 0)
		newfund = Fund(
			username = username, 
			giftname = giftname, 
			giftid = giftid, 
			amount = amount
			)
		newfund.save()
		history = History(username = username, detail = "pay " + str(amount) + " for " + giftname, time = datetime.now())
		history.save()
		final = { "status" : "success" }
	except Exception as e:
		return HttpResponse(json.dumps(final))
	return HttpResponse(json.dumps(final))

def index(request):
	return render_to_response('resource/html/index.html')

def signup(request):
	return render_to_response('resource/html/register.html')

def home(request):
	return render_to_response('resource/html/homepage.html')


