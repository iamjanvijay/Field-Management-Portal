from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
# Create your views here.

def home(request) :
		# print request.user
		return render(request,"home.html",{})	