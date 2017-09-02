from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import connection
from FieldManagement import validations
from FieldManagement import views as FMviews
from FieldManagement.validations import exists,validateEmail
# Create your views here.


		

def admin_login(request):
    # context = RequestContext(request)

    if request.method == 'POST':	
        AdminId = request.POST.get('AdminId')
        Password = request.POST.get('Password')
        user = authenticate(username=AdminId, password=Password)
        if (user is not None) and exists(AdminId,"AdminId","Admin"):
            if user.is_active:
                login(request, user)
                return render(request,"home.html",{ 'LoginSuccess' : True,'LogoutSuccess' : False })
            else:
                return HttpResponse("You're account is disabled.")
        else:
          # print  "invalid login details " + AdminId + " " + Password
            return render(request,"admin_login.html",{'UserType':'Admin','Invalid' : "Invalid login Details. Retry logging in !"})
    else:
        return render(request,"admin_login.html",{'UserType':'Admin'})

def student_login(request):
    # context = RequestContext(request)
    print "Student logging in"
    if request.method == 'POST':	
        StudId = request.POST.get('StudentId')
        Password = request.POST.get('Password')
        user = authenticate(username=StudId, password=Password)
        if (user is not None) and exists(StudId,"StudId","Student"):
            if user.is_active:
                login(request, user)
                return render(request,"home.html",{ 'LoginSuccess' : True,'LogoutSuccess' : False })
            else:
                return HttpResponse("You're account is disabled.")
        else:
          # print  "invalid login details " + AdminId + " " + Password
            return render(request,"admin_login.html",{'UserType':'Student','Invalid' : "Invalid login Details. Retry logging in !"})
    else:
        return render(request,"admin_login.html",{'UserType':'Student'})

def professsor_login(request):
    # context = RequestContext(request)
    if request.method == 'POST':	
        ProfId = request.POST.get('ProfessorId')
        Password = request.POST.get('Password')
        user = authenticate(username=ProfId, password=Password)
        if (user is not None) and exists(ProfId,"ProfId","Professor"):
            if user.is_active:
                login(request, user)
                return render(request,"home.html",{ 'LoginSuccess' : True,'LogoutSuccess' : False })
            else:
                return HttpResponse("You're account is disabled.")
        else:
          # print  "invalid login details " + AdminId + " " + Password
            return render(request,"admin_login.html",{'UserType':'Professor','Invalid' : "Invalid login Details. Retry logging in !"})
    else:
        return render(request,"admin_login.html",{'UserType':'Professor'})  

def plotManager_login(request):
    # context = RequestContext(request)
    if request.method == 'POST':	
       	MangID = request.POST.get('Plot-ManagerId')
        Password = request.POST.get('Password')
        user = authenticate(username=MangID, password=Password)
        if (user is not None) and exists(MangID,"MangID","PlotManager"):
            if user.is_active:
                login(request, user)
                return render(request,"home.html",{ 'LoginSuccess' : True,'LogoutSuccess' : False })
            else:
                return HttpResponse("You're account is disabled.")
        else:
          # print  "invalid login details " + AdminId + " " + Password
            return render(request,"admin_login.html",{'UserType':'Plot-Manager','Invalid' : "Invalid login Details. Retry logging in !"})
    else:
        return render(request,"admin_login.html",{'UserType':'Plot-Manager'})                        

@login_required
def Loginlogout(request):
    logout(request)
    return render(request,"home.html",{ 'LoginSuccess' : False,'LogoutSuccess' : True })





